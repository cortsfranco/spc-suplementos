document.addEventListener('DOMContentLoaded', function() {
    // Sidebar toggle
    const sidebarToggle = document.getElementById('sidebarCollapse');
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', function() {
            document.getElementById('sidebar').classList.toggle('active');
            document.getElementById('content').classList.toggle('active');
        });
    }

    // Inicializar tooltips de Bootstrap
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });

    // Lógica para el formulario de ventas
    const ventaForm = document.getElementById('ventaForm');
    if (ventaForm) {
        // Establecer fecha actual por defecto
        document.getElementById('fecha').valueAsDate = new Date();

        // Agregar nuevo producto a la venta
        document.getElementById('agregarProducto').addEventListener('click', function() {
            const productoTemplate = document.querySelector('.producto-item').cloneNode(true);
            productoTemplate.querySelector('.producto-select').value = '';
            productoTemplate.querySelector('.cantidad').value = '';
            productoTemplate.querySelector('.precio').value = '';
            
            // Agregar evento para eliminar producto
            productoTemplate.querySelector('.btn-remove-producto').addEventListener('click', function() {
                this.closest('.producto-item').remove();
                calcularTotal();
            });

            // Agregar eventos a los nuevos campos
            agregarEventosProducto(productoTemplate);
            
            document.querySelector('.productos-lista').appendChild(productoTemplate);
        });

        // Agregar eventos a los productos existentes
        document.querySelectorAll('.producto-item').forEach(item => {
            agregarEventosProducto(item);
        });
    }
});

function agregarEventosProducto(productoItem) {
    const selectProducto = productoItem.querySelector('.producto-select');
    const inputCantidad = productoItem.querySelector('.cantidad');
    const inputPrecio = productoItem.querySelector('.precio');

    selectProducto.addEventListener('change', function() {
        const option = this.options[this.selectedIndex];
        const precio = option.dataset.precio;
        inputPrecio.value = precio;
        calcularSubtotal(productoItem);
    });

    inputCantidad.addEventListener('input', function() {
        calcularSubtotal(productoItem);
    });
}

function calcularSubtotal(productoItem) {
    const cantidad = productoItem.querySelector('.cantidad').value;
    const precio = productoItem.querySelector('.precio').value;
    const subtotal = cantidad * precio;
    calcularTotal();
}

function calcularTotal() {
    let total = 0;
    document.querySelectorAll('.producto-item').forEach(item => {
        const cantidad = item.querySelector('.cantidad').value;
        const precio = item.querySelector('.precio').value;
        if (cantidad && precio) {
            total += cantidad * precio;
        }
    });
    document.getElementById('total').textContent = total.toFixed(2);
}

// Confirmaciones para eliminar
document.querySelectorAll('.btn-danger').forEach(btn => {
    btn.addEventListener('click', function(e) {
        if (!confirm('¿Estás seguro de que deseas eliminar este elemento?')) {
            e.preventDefault();
        }
    });
}); 