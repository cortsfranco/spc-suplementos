document.addEventListener('DOMContentLoaded', function() {
    // Inicializar DataTable
    $('#clientesTable').DataTable({
        language: {
            url: '//cdn.datatables.net/plug-ins/1.10.24/i18n/Spanish.json'
        },
        order: [[0, 'asc']],
        responsive: true
    });

    // Formulario de cliente
    const clienteForm = document.getElementById('clienteForm');
    if (clienteForm) {
        clienteForm.addEventListener('submit', function(e) {
            e.preventDefault();
            guardarCliente();
        });
    }
});

function guardarCliente() {
    const formData = new FormData(document.getElementById('clienteForm'));
    const clienteId = document.getElementById('cliente_id').value;
    
    const url = clienteId ? 
        `/clientes/${clienteId}/editar` : 
        '/clientes/nuevo';

    fetch(url, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            mostrarNotificacion('Cliente guardado exitosamente', 'success');
            $('#clienteModal').modal('hide');
            setTimeout(() => window.location.reload(), 1500);
        } else {
            mostrarNotificacion(data.message, 'danger');
        }
    })
    .catch(error => {
        mostrarNotificacion('Error al procesar la solicitud', 'danger');
    });
}

function editarCliente(id) {
    fetch(`/clientes/${id}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('cliente_id').value = data.id;
            document.getElementById('nombre').value = data.nombre;
            document.getElementById('telefono').value = data.telefono || '';
            document.getElementById('email').value = data.email || '';
            document.getElementById('direccion').value = data.direccion || '';
            
            document.getElementById('clienteModalLabel').textContent = 'Editar Cliente';
            $('#clienteModal').modal('show');
        })
        .catch(error => {
            mostrarNotificacion('Error al cargar el cliente', 'danger');
        });
}

function verHistorial(id) {
    fetch(`/clientes/${id}/historial`)
        .then(response => response.json())
        .then(data => {
            const tbody = document.querySelector('#historialTable tbody');
            tbody.innerHTML = '';
            
            data.ventas.forEach(venta => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${venta.fecha}</td>
                    <td>${venta.numero_venta}</td>
                    <td class="formato-moneda">${venta.total}</td>
                    <td>
                        <span class="badge bg-${venta.estado_pago === 'pagado' ? 'success' : 'warning'}">
                            ${venta.estado_pago}
                        </span>
                    </td>
                `;
                tbody.appendChild(tr);
            });
            
            document.getElementById('clienteHistorialNombre').textContent = data.cliente.nombre;
            $('#historialModal').modal('show');
        })
        .catch(error => {
            mostrarNotificacion('Error al cargar el historial', 'danger');
        });
}

function eliminarCliente(id) {
    if (confirm('¿Estás seguro de que deseas eliminar este cliente?')) {
        fetch(`/clientes/${id}/eliminar`, {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                mostrarNotificacion('Cliente eliminado exitosamente', 'success');
                setTimeout(() => window.location.reload(), 1500);
            } else {
                mostrarNotificacion(data.message, 'danger');
            }
        })
        .catch(error => {
            mostrarNotificacion('Error al eliminar el cliente', 'danger');
        });
    }
} 