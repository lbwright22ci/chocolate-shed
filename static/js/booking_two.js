document.addEventListener("DOMContentLoaded", function () {

    document.getElementById("ReservationForm2").addEventListener("submit", validateConditions);

    function validateConditions(e){
        e.preventDefault();
        let consent = e.target.consent_given;
        let allergies = e.target.has_dietary_requirements;
        let info = e.target.additional_information;

        let feedbackMsg = document.getElementById("feedback-consent");

        feedbackMsg.innerText= '';

        if(!consent.checked){
            feedbackMsg.innerText = " You must agree to terms and conditions in order to confirm your booking";
            if(allergies.checked && info.value.length==0){
                feedbackMsg.innerText +=" You must provide further information about the allergies or dietary requirements members of your booking have." ;
            }
        }else if(allergies.checked && info.value.length==0){
            feedbackMsg.innerText +=" You must provide further information about the allergies or dietary requirements members of your booking have." ;
        }else if(info.value.length !=0 && allergies.checked == false){
            feedbackMsg.innerText +="You must tick the 'Members of my group have specific dietary needs or allergies' if you are submitting further information.";
        }
        else {
            e.target.submit();
        }
    }


})