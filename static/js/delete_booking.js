document.addEventListener("DOMContentLoaded", function () {
    const deleteModal = new bootstrap.Modal(document.getElementById("deleteModal"));
    const deleteButtons = document.getElementsByClassName("btn-delete");
    const deleteConfirm = document.getElementById("deleteConfirm");
    
    for (let button of deleteButtons) {
        button.addEventListener("click", (e) => {
            let bookingId = e.target.getAttribute("data-booking_id");
            deleteConfirm.href = `delete_booking/${bookingId}`;
            let workshop = e.target.getAttribute("data-booking_workshop");
            let tickets = e.target.getAttribute("data-booking-tickets");
            document.getElementById("wk-del").innerText = `${tickets} places on a ${workshop}`;
            deleteModal.show();
        });
}

})