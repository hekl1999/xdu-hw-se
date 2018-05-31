// URLs
const Host = 'http://127.0.0.1:8080';
const URLs = {
    login: Host + '/login',
    logout: Host + '/logout',
    change_passwd: Host + '/change_passwd',
    stu_mine_class: Host + '/student/stu_mine_class',
    stu_mine_grade: Host + '/stu_mine_grade',
    stu_class_list: Host + '/student/stu_class_list'
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
                if (200 === jqXHR.status) {
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
                else if (400 ===jqXHR.status)
                    alert('请求错误！');
                else if (403 === jqXHR.status)
                    alert('账户或密码错误，请确认后重试！');
                else if (404 === jqXHR.status)
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
                if (200 === jqXHR.status)
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
                if (200 === jqXHR.status) {
                    alert('密码修改成功，请使用新秘密重新登录！');
                    window.location.href = './login.html';
                }
                else if (401 ===jqXHR.status) {
                    alert('未登录，请登录后重试！');
                    window.location.href = './login.html';
                }
                else if (403 === jqXHR.status)
                    alert('旧密码错误，请确认后重试！');
                else if (404 === jqXHR.status)
                    alert('账号不存在，请确认后重试！');
                else
                    alert('未知错误，请稍后重试！');
            }
        });
    },
    stu_mine_class: function() {
        let data = [];
        $.ajax({
            url: URLs.stu_mine_class,
            type: 'GET',
            async: false,
            complete: function(jqXHR, textStatus) {
                if (200 === jqXHR.status) {
                    data = eval('(' + jqXHR.responseText + ')');
                }
                else if (401 === jqXHR.status) {
                    alert('您未登录，请登录后重试！');
                    top.location.href = '../login.html'
                }
                else if(404 === jqXHR.status)
                    data = [];
                else
                    alert('未知错误，请稍后重试！');
            }
        });
        return data;
    },
    stu_mine_grade: function() {
        let data = [];
        $.ajax({
            url: URLs.stu_mine_grade,
            type: 'GET',
            async: false,
            complete: function(jqXHR, textStatus) {
                if (200 === jqXHR.status) {
                    data = eval('(' + jqXHR.responseText + ')');
                }
                else if (401 === jqXHR.status) {
                    alert('您未登录，请登录后重试！');
                    top.location.href = '../login.html'
                }
                else if(404 === jqXHR.status)
                    data = [];
                else
                    alert('未知错误，请稍后重试！');
            }
        });
        return data;
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
    if (n_passwd_input.val() !== rn_passwd_input.val()) {
        alert('两次输入的密码不相同，请确认后重试！');
        return;
    }
    // 修改密码
    Actions.change_passwd();
    // 善后，清空输入框
    o_passwd_input.val('');
    n_passwd_input.val('');
    rn_passwd_input.val('');
}

function stu_mine_class() {
    let mine_classes = Actions.stu_mine_class();
    for (let i in mine_classes) {
        switch (mine_classes[i].day) {
            case 0:
                mine_classes[i].day = '周日';
                break;
            case 1:
                mine_classes[i].day = '周一';
                break;
            case 2:
                mine_classes[i].day = '周二';
                break;
            case 3:
                mine_classes[i].day = '周三';
                break;
            case 4:
                mine_classes[i].day = '周四';
                break;
            case 5:
                mine_classes[i].day = '周五';
                break;
            case 6:
                mine_classes[i].day = '周六';
                break;
        }
        switch (mine_classes[i].section) {
            case 1:
                mine_classes[i].section = '1-2节';
                break;
            case 2:
                mine_classes[i].section = '3-4节';
                break;
            case 3:
                mine_classes[i].section = '5-6节';
                break;
            case 4:
                mine_classes[i].section = '7-8节';
                break;
            case 5:
                mine_classes[i].section = '9-10节';
                break;
        }
    }
    let mine_class_table = new Vue({
        el: '#mine_class-table',
        data: {
            mine_classes: mine_classes
        }
    });
    $('#mine_class-table tbody').show();
}

function stu_mine_grade() {
    let mine_grade = Actions.stu_mine_grade();
    for (let i in mine_grade) {
        if (-1 === mine_grade[i].grade) {
            mine_grade[i].grade = '未录入';
            mine_grade[i].grade_class = '';
        }
        else if (mine_grade[i].grade >= 90)  // 优
            mine_grade[i].grade_class = 'success';
        else if (mine_grade[i].grade >= 75)  // 良
            mine_grade[i].grade_class = 'info';
        else if (mine_grade[i].grade >= 60)  // 及格
            mine_grade[i].grade_class = 'warning';
        else
            mine_grade[i].grade_class = 'danger';

        switch (mine_grade[i].type) {
            case 1:
                mine_grade[i].type = '必修';
                break;
            case 2:
                mine_grade[i].type = '校任选课';
                break;
            case 3:
                mine_grade[i].type = '人文类选修课';
                break;
            case 4:
                mine_grade[i].type = '学院任选课';
                break;
        }
    }
    let mine_grade_table = new Vue({
        el: '#mine_grade-table',
        data: {
            mine_grades: mine_grade
        }
    });
    $('#mine_grade-table tbody').show();
}
