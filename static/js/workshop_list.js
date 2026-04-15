document.addEventListener("DOMContentLoaded", function () {

    document.getElementById("filter-dropdown-ages").addEventListener("click", (e) => ToggleAgeList(e));

    function ToggleAgeList(e){
        document.getElementById("filter-dropdown-reveal-ages").classList.toggle("hide");
    }


})