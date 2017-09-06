function showForm(element_id) {
    var obj = document.getElementById(element_id);
        if (obj.style.display != "block") {
            obj.style.display = "block";
            $(".header__login-panel_button").text("Отмена");
        } else {
            obj.style.display = "none";
            $(".header__login-panel_button").text("Войти");
        }
}