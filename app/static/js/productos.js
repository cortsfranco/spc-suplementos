document.addEventListener('DOMContentLoaded', function() {
    // Inicializar DataTable
    const productosTable = $('#productosTable').DataTable({
        language: {
            url: '//cdn.datatables.net/plug-ins/1.10.24/i18n/Spanish.json'
        },
        order: [[1, 'asc']],
        responsive: true
    });

    // Evento para nuevo producto
    document.getElementById('productoForm').addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(this);
        const productoId = document.getElementById('producto_id').value;
        
        const url = productoId ? 
            `/productos/${productoId}/editar` : 
            '/productos/nuevo';

        fetch(url, {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                mostrarNotificacion('Producto guardado exitosamente', 'success');
                $('#productoModal').modal('hide');
                setTimeout(() => window.location.reload(), 1500);
            } else {
                mostrarNotificacion(data.message, 'danger');
            }
        })
        .catch(error => {
            mostrarNotificacion('Error al procesar la solicitud', 'danger');
        });
    });

    // Calcular ganancia automáticamente
    ['precio_costo', 'precio_venta'].forEach(id => {
        document.getElementById(id).addEventListener('input', calcularGanancia);
    });
});

function editarProducto(id) {
    fetch(`/productos/${id}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('producto_id').value = data.id;
            document.getElementById('codigo').value = data.codigo;
            document.getElementById('nombre').value = data.nombre;
            document.getElementById('descripcion').value = data.descripcion;
            document.getElementById('precio_costo').value = data.precio_costo;
            document.getElementById('precio_venta').value = data.precio_venta;
            document.getElementById('stock').value = data.stock;
            document.getElementById('stock_minimo').value = data.stock_minimo;
            
            document.getElementById('productoModalLabel').textContent = 'Editar Producto';
            $('#productoModal').modal('show');
        })
        .catch(error => {
            mostrarNotificacion('Error al cargar el producto', 'danger');
        });
}

function eliminarProducto(id) {
    if (confirm('¿Estás seguro de que deseas eliminar este producto?')) {
        fetch(`/productos/${id}/eliminar`, {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                mostrarNotificacion('Producto eliminado exitosamente', 'success');
                setTimeout(() => window.location.reload(), 1500);
            } else {
                mostrarNotificacion(data.message, 'danger');
            }
        })
        .catch(error => {
            mostrarNotificacion('Error al eliminar el producto', 'danger');
        });
    }
}

function ajustarStock(id) {
    const cantidad = prompt('Ingrese la cantidad a ajustar (use números negativos para restar):');
    if (cantidad !== null) {
        fetch(`/productos/${id}/ajustar-stock`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ cantidad: parseInt(cantidad) })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                mostrarNotificacion('Stock ajustado exitosamente', 'success');
                setTimeout(() => window.location.reload(), 1500);
            } else {
                mostrarNotificacion(data.message, 'danger');
            }
        })
        .catch(error => {
            mostrarNotificacion('Error al ajustar el stock', 'danger');
        });
    }
}

function calcularGanancia() {
    const precioCosto = parseFloat(document.getElementById('precio_costo').value) || 0;
    const precioVenta = parseFloat(document.getElementById('precio_venta').value) || 0;
    const ganancia = precioVenta - precioCosto;
    
    const porcentajeGanancia = precioCosto > 0 ? (ganancia / precioCosto * 100) : 0;
    
    document.getElementById('ganancia').textContent = 
        `$${ganancia.toFixed(2)} (${porcentajeGanancia.toFixed(2)}%)`;
}

// Función para actualizar precios masivamente
function actualizarPrecios() {
    const porcentaje = prompt('Ingrese el porcentaje de aumento (ejemplo: 10 para 10%):');
    if (porcentaje !== null) {
        fetch('/productos/actualizar-precios', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ porcentaje: parseFloat(porcentaje) })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                mostrarNotificacion('Precios actualizados exitosamente', 'success');
                setTimeout(() => window.location.reload(), 1500);
            } else {
                mostrarNotificacion(data.message, 'danger');
            }
        })
        .catch(error => {
            mostrarNotificacion('Error al actualizar los precios', 'danger');
        });
    }
} 