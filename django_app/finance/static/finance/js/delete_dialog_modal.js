var deleteDialogModal = document.getElementById('deleteDialogModal')
deleteDialogModal.addEventListener('show.bs.modal', function (event) {
    var button = event.relatedTarget
    var delete_url = button.getAttribute('data-bs-del-url')
    var modalDeleteUrl = deleteDialogModal.querySelector('.modal-content form')
    modalDeleteUrl.action = delete_url
})