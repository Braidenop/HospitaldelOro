$(function () {
    $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'searchdata'
            },
            dataSrc: ""
        },
        columns: [
            {"data": "id"},
            {"data": "usuario.full_name"},
            {"data": "usuario.username"},
            {"data": "fecha_nacimiento"},
            {"data": "edad"},
            {"data": "telefono"},
            {"data": "cedula"},
            {"data": "direccion"},
            {"data": "ciudad_resid"},
            {"data": "genero.name"},
            {"data": "id"},
        ],
        columnDefs: [

            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="/admi/editar_pacie/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/admi/eliminar_pacie/' + row.id + '/" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });
});