document.addEventListener("DOMContentLoaded", function () {

    document.getElementById("ReservationForm2").addEventListener("submit", (e) => validateConditions(e));

    function validateConditions(e){
        e.preventDefault();
        let consent = e.target.consent_given;
        let feedbackMsg = document.getElementById("feedback_consent");

        if(consent == false){
            feedbackMsg.innerText = " You must agree to terms and conditions in order to confirm your booking";
        }
        else{
            e.target.submit();
        }
    }


})