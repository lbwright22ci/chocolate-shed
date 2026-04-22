document.addEventListener("DOMContentLoaded", function () {

    document.getElementById("ReservationForm2").addEventListener("submit", validateConditions);

    function validateConditions(e){
        e.preventDefault();
        let consent = e.target.consent_given;
        let allergies = e.target.has_dietary_requirements;
        let info = e.target.additional_information;

        let feedbackMsg = document.getElementById("feedback_consent");
        console.log(info.value.length);
        console.log(consent.checked);

        if(!consent.checked){
            feedbackMsg.innerText = " You must agree to terms and conditions in order to confirm your booking";
            if(allergies.checked && info.value.length==0){
                feedbackMsg.innerText +=" You must provide further information about the allergies or dietary requirements members of your booking have." ;
            }
        }else if(allergies.checked && info.value.length==0){
            feedbackMsg.innerText +=" You must provide further information about the allergies or dietary requirements members of your booking have." ;
        }else{
            e.target.submit();
        }
    }


})