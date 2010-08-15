function show_login_form() {
	$("#login-form").show("blind", {}, 500);
	return false;
}

function hide_login_form() {
	$("#login-form:visible").hide("blind");
}

function login_setup() {
	$("#login-link").click(show_login_form);
	$("#login-form input").click(hide_login_form);
}

$(login_setup);

