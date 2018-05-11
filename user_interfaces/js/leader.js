// URLs
const Host = 'http://127.0.0.1:8008';
const URLs = {
    login: Host + '/login',
    logout: Host + '/logout',
    change_passwd: Host + '/change_passwd',
};
const Actions = {
    login: function() {
        post_data = {
            'account': $('#account-input').val(),
            'password': $('#passwd-input').val()
        };
        $.ajax({
            url: URLs.login,
            type: 'POST',
            data: post_data,
            complete: function(jqXHR, textStatus) {
                if (200 == jqXHR.state()) {

                }
                else if (400 == jqXHR.state())
                    alert('请求错误！');
                else if (403 == jqXHR.state())
                    alert('账户或密码错误，请确认后重试！');
                else if (404 == jqXHR.state())
                    alert('账号不存在，请确认后重试！');
                else
                    alert('未知错误，请稍后重试！');
            }
        });
    },
    logout: function() {
        $.ajax({
            url: URLs.logout,
            type: 'GET',
            complete: function(jqXHR, textStatus) {
                if (200 == jqXHR.state())
                    window.location.href = './login.html';
                else
                    alert('注销失败，请稍后重试！');
            }
        });
    },
    change_passwd: function() {

    },
};

function login() {
    const account_input = $('#account-input');
    const passwd_input = $('#passwd-input');
    // 参数检查
    if (!account_input.val() || !passwd_input.val()) {
        alert('登录信息不全，请将账号和密码填写完整后重试！');
        return;
    }
    // 登录
    Actions.login();
    // 善后，清空输入框
    account_input.val('');
    passwd_input.val('')
}

function logout() {
    Actions.logout();
}

function change_passwd() {
    // 前置条件
    Actions.change_passwd();
    // 后置条件
}