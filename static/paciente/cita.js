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
            {"data": "paciente.full_name"},
            {"data": "esp_medic.id_medico.usuario.full_name"},
            {"data": "esp_medic.id_especialidad.nombre_esp"},
            {"data": "esp_medic.dia_laboral"},
            {"data": "esp_medic.horario.name"},
            {"data": "esp_medic.consul.name"},
            {"data": "motivo.name"},
            {"data": "id"},
        ],
        columnDefs: [

            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="/admi/editar_cita/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/admi/eliminar_cita/' + row.id + '/" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });
});