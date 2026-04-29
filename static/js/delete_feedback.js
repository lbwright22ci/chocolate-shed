document.addEventListener("DOMContentLoaded", function () {
    const deleteModal = new bootstrap.Modal(document.getElementById("deleteModal"));
    const deleteButtons = document.getElementsByClassName("btn-delete");
    const deleteConfirm = document.getElementById("deleteConfirm");
    
    for (let button of deleteButtons) {
        button.addEventListener("click", (e) => {
            let feedbackId = e.target.getAttribute("data-feedback_id");
            deleteConfirm.href = `delete/${feedbackId}`;
            deleteModal.show();
        });
}

})