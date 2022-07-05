var date_range = null;
var date_now = new moment().format('YYYY-MM-DD');



function generate_report() {
    var parameters = {
        'action': 'search_report',
        'start_date': date_now,
        'end_date': date_now,
    };

    if (date_range !== null) {
        parameters['start_date'] = date_range.startDate.format('YYYY-MM-DD');
        parameters['end_date'] = date_range.endDate.format('YYYY-MM-DD');
    }

    $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: parameters,
            dataSrc: ""
        },
        order: false,
        paging: false,
        ordering: false,
        info: false,
        searching: true,
        dom: 'Bfrtip',
        buttons: [

        ],
        columns: [
            {"data": "id"},
            {"data": "esp_medic.id_medico.usuario.full_name"},
            {"data": "esp_medic.id_especialidad.nombre_esp"},
            {"data": "esp_medic.dia_laboral.name"},
            {"data": "esp_medic.horario.name"},
            {"data": "esp_medic.consul.name"},
            {"data": "fecha_cita"},
            {"data": "motivo.name"},
            {"data": "id"},
        ],
        columnDefs: [

            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type) {
                    var buttons = '<a href="/medico/crearHis/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });
}

$(function () {
    $('input[name="date_range"]').daterangepicker({
        locale: {
            format: 'YYYY-MM-DD',
            applyLabel: '<i class="fas fa-chart-pie"></i> Aplicar',
            cancelLabel: '<i class="fas fa-times"></i> Cancelar',
        }
    }).on('apply.daterangepicker', function (ev, picker) {
        date_range = picker;
        generate_report();
    }).on('cancel.daterangepicker', function (ev, picker) {
        $(this).data('daterangepicker').setStartDate(date_now);
        $(this).data('daterangepicker').setEndDate(date_now);
        date_range = picker;
        generate_report();
    });

    generate_report();
});