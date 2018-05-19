// URLs
const Host = 'http://127.0.0.1:8008';
const URLs = {
    login: Host + '/login',
    logout: Host + '/logout',
    change_passwd: Host + '/change_passwd',
};
const Actions = {
    login: function() {
        const post_data = {
            'account': $('#account-input').val(),
            'password': $('#passwd-input').val()
        };
        $.ajax({
            url: URLs.login,
            type: 'POST',
            data: post_data,
            complete: function(jqXHR, textStatus) {
                if (200 === jqXHR.state()) {
                    const data = eval('(' + jqXHR.responseText + ')');
                    if ('student' === data.type)
                        window.location.href = './student.html';
                    else if ('instructor' === data.type)
                        window.location.href = './instructor.html';
                    else if ('superior' === data.type)
                        window.location.href = './superior.html';
                    else if ('admin' === data.type)
                        window.location.href = './admin.html';
                    else if ('root' === data.type)
                        window.location.href = './root.html';
                }
                else if (400 ===jqXHR.state())
                    alert('请求错误！');
                else if (403 === jqXHR.state())
                    alert('账户或密码错误，请确认后重试！');
                else if (404 === jqXHR.state())
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
                if (200 === jqXHR.state())
                    window.location.href = './login.html';
                else
                    alert('注销失败，请稍后重试！');
            }
        });
    },
    change_passwd: function() {
        const post_data = {
            'old_password': $('#old-passwd-input').val(),
            'new_password': $('#new-passwd-input').val()
        };
        $.ajax({
            url: URLs.change_passwd,
            type: 'POST',
            data: post_data,
            complete: function(jqXHR, textStatus) {
                if (200 === jqXHR.state()) {
                    // hhh...
                }
                else if (401 ===jqXHR.state()) {
                    alert('未登录，请登录后重试！');
                    window.location.href = './login.html';
                }
                else if (403 === jqXHR.state())
                    alert('旧密码错误，请确认后重试！');
                else if (404 === jqXHR.state())
                    alert('账号不存在，请确认后重试！');
                else
                    alert('未知错误，请稍后重试！');
            }
        });
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
    const o_passwd_input = $('#old-passwd-input');
    const n_passwd_input = $('#new-passwd-input');
    const rn_passwd_input = $('#re-new-passwd-input');
    // 参数检查
    if (!o_passwd_input.val() || !n_passwd_input.val() || !rn_passwd_input.val()) {
        alert('提交信息不全，请将旧密码、新密码和确认新密码填写完整后重试！');
        return;
    }
    // 修改密码
    Actions.change_passwd();
    // 善后，清空输入框
    o_passwd_input.val('');
    n_passwd_input.val('');
    rn_passwd_input.val('');
}