// URLs
const Host = 'http://127.0.0.1:8008';
const URLs = {
    login: Host + '/login',
};

function login() {
    post_data = {
        'account': $('#account-input').val(),
        'passwd': $('#passwd-input').val()
    };
    $.ajax({
        url: URLs.login,
        type: 'POST',
        data: post_data,
        complete: function(jqXHR, textStatus) {
            if (200 == jqXHR.state())
        }
    });
}