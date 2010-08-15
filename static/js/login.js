function show_login_form() {
	$("#login-form").show("blind", {}, 500);
	return false;
}

function hide_login_form() {
	$("#login-form:visible").hide("blind");
}

function cancel_login() {
	$("#login-form:visible").hide("blind");
    return false;
}

function login_setup() {
	$("#login-link").click(show_login_form);
	$("#login-form input[type=submit]").click(hide_login_form);
	$("#login-cancel").click(cancel_login);
}

$(login_setup);

