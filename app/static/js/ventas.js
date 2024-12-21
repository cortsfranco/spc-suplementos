let productosEnVenta = [];

document.addEventListener('DOMContentLoaded', function() {
    const ventaForm = document.getElementById('ventaForm');
    const agregarProductoBtn = document.getElementById('agregarProductoBtn');
    const productosContainer = document.getElementById('productosContainer');
    const totalVentaSpan = document.getElementById('totalVenta');

    if (agregarProductoBtn) {
        agregarProductoBtn.addEventListener('click', agregarLineaProducto);
    }

    if (ventaForm) {
        ventaForm.addEventListener('submit', function(e) {
            e.preventDefault();
            if (validarFormulario()) {
                guardarVenta();
            }
        });
    }

    // Inicializar select2 para clientes
    $('.select-cliente').select2({
        theme: 'bootstrap-5',
        placeholder: 'Seleccionar cliente...'
    });
});

function agregarLineaProducto() {
    const template = document.getElementById('lineaProductoTemplate');
    const clon = template.content.cloneNode(true);
    
    // Inicializar select2 para el nuevo producto
    const nuevoSelect = clon.querySelector('.select-producto');
    $(nuevoSelect).select2({
        theme: 'bootstrap-5',
        placeholder: 'Seleccionar producto...'
    });

    // Agregar eventos
    const cantidad = clon.querySelector('.cantidad-producto');
    cantidad.addEventListener('input', actualizarSubtotal);
    
    const btnEliminar = clon.querySelector('.eliminar-producto');
    btnEliminar.addEventListener('click', function(e) {
        e.preventDefault();
        this.closest('.linea-producto').remove();
        actualizarTotal();
    });

    productosContainer.appendChild(clon);
}

function actualizarSubtotal(e) {
    const lineaProducto = e.target.closest('.linea-producto');
    const selectProducto = lineaProducto.querySelector('.select-producto');
    const cantidad = parseFloat(e.target.value) || 0;
    const precio = parseFloat(selectProducto.options[selectProducto.selectedIndex].dataset.precio) || 0;
    
    const subtotal = cantidad * precio;
    lineaProducto.querySelector('.subtotal').textContent = subtotal.toFixed(2);
    
    actualizarTotal();
}

function actualizarTotal() {
    const subtotales = document.querySelectorAll('.subtotal');
    let total = 0;
    
    subtotales.forEach(sub => {
        total += parseFloat(sub.textContent) || 0;
    });
    
    totalVentaSpan.textContent = total.toFixed(2);
}

function validarFormulario() {
    const cliente = document.querySelector('.select-cliente').value;
    if (!cliente) {
        mostrarNotificacion('Debe seleccionar un cliente', 'danger');
        return false;
    }

    const productos = document.querySelectorAll('.linea-producto');
    if (productos.length === 0) {
        mostrarNotificacion('Debe agregar al menos un producto', 'danger');
        return false;
    }

    let valido = true;
    productos.forEach(linea => {
        const producto = linea.querySelector('.select-producto').value;
        const cantidad = linea.querySelector('.cantidad-producto').value;
        
        if (!producto || !cantidad || cantidad <= 0) {
            mostrarNotificacion('Verifique los productos y cantidades', 'danger');
            valido = false;
        }
    });

    return valido;
}

function guardarVenta() {
    const formData = new FormData(document.getElementById('ventaForm'));
    
    fetch('/ventas/nueva', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            mostrarNotificacion('Venta registrada exitosamente', 'success');
            setTimeout(() => {
                window.location.href = '/ventas';
            }, 1500);
        } else {
            mostrarNotificacion(data.message, 'danger');
        }
    })
    .catch(error => {
        mostrarNotificacion('Error al procesar la venta', 'danger');
    });
}

function verDetalleVenta(ventaId) {
    fetch(`/ventas/${ventaId}/detalle`)
        .then(response => response.json())
        .then(data => {
            llenarModalDetalle(data);
            $('#detalleVentaModal').modal('show');
        });
}

function llenarModalDetalle(data) {
    document.getElementById('detalleVentaNumero').textContent = data.numero_venta;
    document.getElementById('detalleVentaFecha').textContent = data.fecha;
    document.getElementById('detalleVentaCliente').textContent = data.cliente;
    document.getElementById('detalleVentaTotal').textContent = `$${data.total.toFixed(2)}`;
    
    const tbody = document.getElementById('detalleVentaProductos');
    tbody.innerHTML = '';
    
    data.items.forEach(item => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${item.producto}</td>
            <td>${item.cantidad}</td>
            <td>$${item.precio_unitario.toFixed(2)}</td>
            <td>$${item.subtotal.toFixed(2)}</td>
        `;
        tbody.appendChild(tr);
    });
} 