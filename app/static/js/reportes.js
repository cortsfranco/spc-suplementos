document.addEventListener('DOMContentLoaded', function() {
    // Inicializar los gráficos
    inicializarGraficos();

    // Evento para actualizar reportes
    document.getElementById('filtrosReporte').addEventListener('submit', function(e) {
        e.preventDefault();
        actualizarReportes();
    });

    // Establecer fechas por defecto (último mes)
    const hoy = new Date();
    const haceMes = new Date();
    haceMes.setMonth(haceMes.getMonth() - 1);
    
    document.getElementById('fecha_hasta').valueAsDate = hoy;
    document.getElementById('fecha_desde').valueAsDate = haceMes;
});

function inicializarGraficos() {
    // Gráfico de ventas por día
    const ctxVentas = document.getElementById('ventasPorDia').getContext('2d');
    window.graficoVentas = new Chart(ctxVentas, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Ventas Diarias',
                data: [],
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    // Gráfico de productos más vendidos
    const ctxProductos = document.getElementById('productosMasVendidos').getContext('2d');
    window.graficoProductos = new Chart(ctxProductos, {
        type: 'bar',
        data: {
            labels: [],
            datasets: [{
                label: 'Cantidad Vendida',
                data: [],
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                borderColor: 'rgb(54, 162, 235)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

function actualizarReportes() {
    const formData = new FormData(document.getElementById('filtrosReporte'));
    
    fetch('/reportes/datos', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        actualizarTarjetas(data.totales);
        actualizarGraficos(data.graficos);
        actualizarTabla(data.productos);
    })
    .catch(error => {
        mostrarNotificacion('Error al actualizar los reportes', 'danger');
    });
}

function actualizarTarjetas(totales) {
    document.getElementById('totalVentas').textContent = formatearMoneda(totales.ventas);
    document.getElementById('totalGanancias').textContent = formatearMoneda(totales.ganancias);
    document.getElementById('cantidadVentas').textContent = totales.cantidad_ventas;
    document.getElementById('ticketPromedio').textContent = formatearMoneda(totales.ticket_promedio);
}

function actualizarGraficos(datos) {
    // Actualizar gráfico de ventas
    window.graficoVentas.data.labels = datos.ventas.fechas;
    window.graficoVentas.data.datasets[0].data = datos.ventas.valores;
    window.graficoVentas.update();

    // Actualizar gráfico de productos
    window.graficoProductos.data.labels = datos.productos.nombres;
    window.graficoProductos.data.datasets[0].data = datos.productos.cantidades;
    window.graficoProductos.update();
}

function formatearMoneda(valor) {
    return new Intl.NumberFormat('es-AR', {
        style: 'currency',
        currency: 'ARS'
    }).format(valor);
} 