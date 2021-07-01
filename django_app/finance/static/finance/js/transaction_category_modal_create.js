var addDialogModal = document.getElementById('addDialogModal');
var form = document.getElementById('modalForm');
addDialogModal.addEventListener('show.bs.modal', function (event) {
    $.ajax({
        type: 'GET',
        url: form.action,
        success: function (data) {
            $('.modal-body').html(data);
        }
    });
})

var chained_select = document.getElementById('id_category');
form.addEventListener('submit', function (event) {
    event.preventDefault();
    $.ajax({
        type: 'POST',
        url: form.action,
        data: $(form).serialize(),
        success: function (response) {
            $(chained_select).append($('<option>', { value: response['pk'], text: response['name'] }));
            $(chained_select).val(response['pk']).trigger('change');
            $(document.getElementById('addDialogModal')).modal('hide');
        },
        // TODO: Написать обработку ошибок
        error: function () {
            alert('error');
        }
    });
})
