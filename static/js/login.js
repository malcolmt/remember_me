function show_login_form() {
	$("#login-form").slideDown(300);
	return false;
}

function hide_login_form() {
	$("#login-form:visible").removeClass("active").slideUp(300);
}

function cancel_login() {
	$("#login-form:visible").removeClass("active").slideUp(300);
	return false;
}

function login_setup() {
	$("#login-link").click(show_login_form);
	$("#login-form input[type=submit]").click(hide_login_form);
	$("#login-cancel").click(cancel_login);
}

$(login_setup);

