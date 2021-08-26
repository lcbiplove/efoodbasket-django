window.addEventListener("load", function(){
    var editBtn = this.document.getElementById("edit-btn");
    var updatableInputs = this.document.querySelectorAll(".input-can-update");
    var profileForm = this.document.getElementById("profile-form");
    
    var isEditEnabled = function(){
        return editBtn.classList.contains("enabled");
    }

    editBtn.onclick = function(){
        if(!isEditEnabled()){
            updatableInputs.forEach(element => {
                element.removeAttribute("readonly");
            });
            updatableInputs[0].focus();
            this.innerHTML = "Save";
            this.classList.add("enabled");
        }
        else {
            this.classList.remove("enabled");
            profileForm.submit();
        }
    }
});