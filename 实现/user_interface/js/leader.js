// URLs
const Host = 'http://127.0.0.1:5000';
const URLs = {
    hello_world: Host + '/',
    login: Host + '/login',
    who_am_i: Host + '/who_am_i',
    change_passwd: Host + '/change_passwd',
    logout: Host + '/logout',

    stu_mine_class: Host + '/student/mine_class',
    stu_mine_grade: Host + '/student/mine_grade',
    stu_exam_info: Host + '/student/exam_info',
    stu_classes_list: Host + '/student/class_list',  // classes_list
    stu_change_selected: Host + '/student/choice_class',

    tea_mine_class: Host + '/teacher/mine_class',
    tea_class_info: Host + '/teacher/class_info',
    tea_class_people: Host + '/teacher/class_people',
    tea_update_grade: Host + '/teacher/insert_grade',
    tea_exam_info: Host + '/teacher/exam_info',

    admin_account_list: Host + '/admin/account_list',
    admin_change_account: Host + '/admin/change_account',
    admin_exam_info: Host + '/admin/exam_info/',
    admin_change_exam: Host + '/admin/change_exam',
    admin_class_list: Host + '/admin/class_list/',
    admin_course_list: Host + '/admin/course_list',
    admin_change_course: Host + '/admin/change_course',
    admin_schedule_list: Host + '/admin/schedule_list',
    admin_change_schedule: Host + '/admin/change_schedule',

    root_show_tables: Host + '/root/show_tables',
    root_get_table: Host + '/root/get_table',
};
const Actions = {
    hello_world: function() {
        $.ajax({
            xhrFields: {
                withCredentials: true
            },
            url: URLs.hello_world,
            type: 'GET',
            complete: function(jqXHR) {
                if (200 !== jqXHR.status)
                    alert('无法与服务器建立联系，请刷新页面或一段时间后再试！');
            }
        });
    },
    login: function() {
        const post_data = {
            'account': $('#account-input').val(),
            'password': $('#passwd-input').val()
        };
        $.ajax({
            xhrFields: {
                withCredentials: true
            },
            url: URLs.login,
            type: 'POST',
            data: post_data,
            complete: function(jqXHR) {
                if (200 === jqXHR.status) {
                    const data = JSON.parse(jqXHR.responseText);
                    if ('student' === data.type.toString())
                        window.location.href = './student.html';
                    else if ('instructor' === data.type.toString())
                        window.location.href = './instructor.html';
                    else if ('superior' === data.type.toString())
                        window.location.href = './superior.html';
                    else if ('admin' === data.type.toString())
                        window.location.href = './admin.html';
                    else if ('root' === data.type.toString())
                        window.location.href = './root.html';
                }
                else if (400 === jqXHR.status)
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
    who_am_i: function() {
        $.ajax({
            xhrFields: {
                withCredentials: true
            },
            url: URLs.who_am_i,
            type: 'GET',
            complete: function(jqXHR) {
                if (200 === jqXHR.status) {
                    let data = JSON.parse(jqXHR.responseText);
                    $('#mine-name').text(data['name']);
                }
                else {
                    alert('获取个人信息失败，请尝试重新登录！');
                    window.location.href = './login.html';
                }

            }
        });
    },
    change_passwd: function() {
        const post_data = {
            'old_password': $('#old-passwd-input').val(),
            'new_password': $('#new-passwd-input').val()
        };
        $.ajax({
            xhrFields: {
                withCredentials: true
            },
            url: URLs.change_passwd,
            type: 'POST',
            data: post_data,
            complete: function(jqXHR) {
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
    logout: function() {
        $.ajax({
            xhrFields: {
                withCredentials: true
            },
            url: URLs.logout,
            type: 'GET',
            complete: function(jqXHR) {
                if (200 === jqXHR.status) {
                    window.location.href = './login.html';
                    setCookie('frame_url', './content/default.html');
                }

                else
                    alert('注销失败，请稍后重试！');
            }
        });
    },

    stu_mine_class: function() {
        let data = [];
        $.ajax({
            xhrFields: {
                withCredentials: true
            },
            url: URLs.stu_mine_class,
            type: 'GET',
            async: false,
            complete: function(jqXHR) {
                if (200 === jqXHR.status) {
                    data = JSON.parse(jqXHR.responseText);
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
            xhrFields: {
                withCredentials: true
            },
            url: URLs.stu_mine_grade,
            type: 'GET',
            async: false,
            complete: function(jqXHR) {
                if (200 === jqXHR.status) {
                    data = JSON.parse(jqXHR.responseText);
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
    stu_exam_info: function() {
        let data = [];
        $.ajax({
            xhrFields: {
                withCredentials: true
            },
            url: URLs.stu_exam_info,
            type: 'GET',
            async: false,
            complete: function(jqXHR) {
                if (200 === jqXHR.status) {
                    data = JSON.parse(jqXHR.responseText);
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
    stu_classes_list: function() {
        let data = [];
        $.ajax({
            xhrFields: {
                withCredentials: true
            },
            url: URLs.stu_classes_list,
            type: 'GET',
            async: false,
            complete: function(jqXHR) {
                if (200 === jqXHR.status) {
                    data = JSON.parse(jqXHR.responseText);
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
    stu_change_selected: function(class_id) {
        $.ajax({
            xhrFields: {
                withCredentials: true
            },
            data: {
                'class_id': class_id
            },
            url: URLs.stu_change_selected + '/' + class_id,
            type: 'GET',
            complete: function(jqXHR) {
                if (200 === jqXHR.status) {
                    window.location.reload();
                }
                else if (401 === jqXHR.status) {
                    alert('您未登录，请登录后重试！');
                    top.location.href = '../login.html'
                }
                else if(404 === jqXHR.status)
                    alert('该课程不存在！');
                else
                    alert('未知错误，请稍后重试！');
            }
        });
    },

    tea_mine_class: function() {
        let data = [];
        $.ajax({
            xhrFields: {
                withCredentials: true
            },
            url: URLs.tea_mine_class,
            type: 'GET',
            async: false,
            complete: function(jqXHR) {
                if (200 === jqXHR.status) {
                    data = JSON.parse(jqXHR.responseText);
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
    tea_class_info: function() {
        let data = [];
        $.ajax({
            xhrFields: {
                withCredentials: true
            },
            url: URLs.tea_class_info,
            type: 'GET',
            async: false,
            complete: function(jqXHR) {
                if (200 === jqXHR.status) {
                    data = JSON.parse(jqXHR.responseText);
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
    tea_class_people: function(class_id) {
        let data = [];
        $.ajax({
            xhrFields: {
                withCredentials: true
            },
            url: URLs.tea_class_people + '/' + class_id,
            type: 'GET',
            data: {
                'class_id': class_id
            },
            async: false,
            complete: function(jqXHR) {
                if (200 === jqXHR.status) {
                    data = JSON.parse(jqXHR.responseText);
                }
                else if (401 === jqXHR.status) {
                    alert('您未登录，请登录后重试！');
                    top.location.href = '../login.html'
                }
                else if (403 === jqXHR.status)
                    alert('该课程任课老师不是你，请重新登录后重试！');
                else if(404 === jqXHR.status)
                    data = [];
                else
                    alert('未知错误，请稍后重试！');
            }
        });
        return data;
    },
    tea_update_grade: function(class_id) {
        let post_data = {
            'class_id': class_id,
            'grade': []
        };
        $('td.grade-td input').each(function() {
            let student_id = $(this).attr('title');
            let grade = $(this).val();
            post_data['grade'].push({'student_id': student_id, 'grade': grade});
        });

        $.ajax({
            xhrFields: {
                withCredentials: true
            },
            url: URLs.tea_update_grade,
            type: 'POST',
            data: JSON.stringify(post_data),
            contentType: "application/json",
            complete: function(jqXHR) {
                if (200 === jqXHR.status) {
                    alert('提交成功');
                    window.location.reload();
                }
                else if (401 === jqXHR.status) {
                    alert('您未登录，请登录后重试！');
                    top.location.href = '../login.html'
                }
                else if (403 === jqXHR.status)
                    alert('该课程任课老师不是你，请重新登录后重试！');
                else if(404 === jqXHR.status)
                    alert('该课程不存在，请尝试刷新页面后重试');
                else
                    alert('未知错误，请稍后重试！');
            }
        });
    },
    tea_exam_info: function() {
        let data = [];
        $.ajax({
            xhrFields: {
                withCredentials: true
            },
            url: URLs.tea_exam_info,
            type: 'GET',
            async: false,
            complete: function(jqXHR) {
                if (200 === jqXHR.status) {
                    data = JSON.parse(jqXHR.responseText);
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

    admin_account_list: function() {
        let data = [];
        $.ajax({
            xhrFields: {
                withCredentials: true
            },
            url: URLs.admin_account_list,
            type: 'GET',
            async: false,
            complete: function(jqXHR) {
                if (200 === jqXHR.status) {
                    data = JSON.parse(jqXHR.responseText);
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
    admin_change_account: function(post_data) {
        $.ajax({
            xhrFields: {
                withCredentials: true
            },
            url: URLs.admin_change_account,
            type: 'POST',
            data: JSON.stringify(post_data),
            contentType: "application/json",
            complete: function(jqXHR) {
                if (200 === jqXHR.status) {
                    window.location.reload();
                }
                else if (401 === jqXHR.status) {
                    alert('您未登录，请登录后重试！');
                    top.location.href = '../login.html'
                }
                else if (403 === jqXHR.status)
                    alert('操作不允许，请重新登录后重试！');
                else
                    alert('未知错误，请稍后重试！');
            }
        });
    },
    admin_exam_info: function() {
        let data = [];
        $.ajax({
            xhrFields: {
                withCredentials: true
            },
            url: URLs.admin_exam_info,
            type: 'GET',
            async: false,
            complete: function(jqXHR) {
                if (200 === jqXHR.status) {
                    data = JSON.parse(jqXHR.responseText);
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
    admin_exam_info_detail: function(exam_id) {
        let data = [];
        $.ajax({
            xhrFields: {
                withCredentials: true
            },
            url: URLs.admin_exam_info,
            type: 'GET',
            data: {
                'exam_id': exam_id
            },
            async: false,
            complete: function(jqXHR) {
                if (200 === jqXHR.status) {
                    data = JSON.parse(jqXHR.responseText);
                }
                else if (401 === jqXHR.status) {
                    alert('您未登录，请登录后重试！');
                    top.location.href = '../login.html'
                }
                else if (403 === jqXHR.status)
                    alert('操作不允许，请重新登录后重试！');
                else if(404 === jqXHR.status)
                    data = [];
                else
                    alert('未知错误，请稍后重试！');
            }
        });
        return data;
    },
    admin_class_list: function() {
        let data = [];
        $.ajax({
            xhrFields: {
                withCredentials: true
            },
            url: URLs.admin_class_list,
            type: 'GET',
            async: false,
            complete: function(jqXHR) {
                if (200 === jqXHR.status) {
                    data = JSON.parse(jqXHR.responseText);
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
    admin_class_detail: function(class_id) {
        let data = [];
        $.ajax({
            xhrFields: {
                withCredentials: true
            },
            url: URLs.admin_class_list,
            type: 'GET',
            data: {
                'class_id': class_id
            },
            async: false,
            complete: function(jqXHR) {
                if (200 === jqXHR.status) {
                    data = JSON.parse(jqXHR.responseText);
                }
                else if (401 === jqXHR.status) {
                    alert('您未登录，请登录后重试！');
                    top.location.href = '../login.html'
                }
                else if (403 === jqXHR.status)
                    alert('操作不允许，请重新登录后重试！');
                else if(404 === jqXHR.status)
                    data = [];
                else
                    alert('未知错误，请稍后重试！');
            }
        });
        return data;
    },
    admin_course_list: function() {
        let data = [];
        $.ajax({
            xhrFields: {
                withCredentials: true
            },
            url: URLs.admin_course_list,
            type: 'GET',
            async: false,
            complete: function(jqXHR) {
                if (200 === jqXHR.status) {
                    data = JSON.parse(jqXHR.responseText);
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
    admin_change_course: function(post_data) {
        $.ajax({
            xhrFields: {
                withCredentials: true
            },
            url: URLs.admin_change_course,
            type: 'POST',
            data: JSON.stringify(post_data),
            contentType: "application/json",
            complete: function(jqXHR) {
                if (200 === jqXHR.status) {
                    window.location.reload();
                }
                else if (401 === jqXHR.status) {
                    alert('您未登录，请登录后重试！');
                    top.location.href = '../login.html'
                }
                else if (403 === jqXHR.status)
                    alert('操作不允许，请重新登录后重试！');
                else
                    alert('未知错误，请稍后重试！');
            }
        });
    },
    admin_schedule_list: function() {
        let data = [];
        $.ajax({
            xhrFields: {
                withCredentials: true
            },
            url: URLs.admin_schedule_list,
            type: 'GET',
            async: false,
            complete: function(jqXHR) {
                if (200 === jqXHR.status) {
                    data = JSON.parse(jqXHR.responseText);
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
    admin_change_schedule: function(post_data) {
        $.ajax({
            xhrFields: {
                withCredentials: true
            },
            url: URLs.admin_change_schedule,
            type: 'POST',
            data: JSON.stringify(post_data),
            contentType: "application/json",
            complete: function(jqXHR) {
                if (200 === jqXHR.status) {
                    window.location.reload();
                }
                else if (401 === jqXHR.status) {
                    alert('您未登录，请登录后重试！');
                    top.location.href = '../login.html'
                }
                else if (403 === jqXHR.status)
                    alert('操作不允许，请重新登录后重试！');
                else
                    alert('未知错误，请稍后重试！');
            }
        });
    },

    root_show_tables: function() {
        let data = [];
        $.ajax({
            xhrFields: {
                withCredentials: true
            },
            url: URLs.root_show_tables,
            type: 'GET',
            async: false,
            complete: function(jqXHR) {
                if (200 === jqXHR.status) {
                    data = JSON.parse(jqXHR.responseText);
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
    root_get_table: function(table_name) {
        let data = [];
        $.ajax({
            xhrFields: {
                withCredentials: true
            },
            data: {
                'table_name': table_name
            },
            url: URLs.root_get_table + '/' + table_name,
            type: 'GET',
            async: false,
            complete: function(jqXHR) {
                if (200 === jqXHR.status) {
                    data = JSON.parse(jqXHR.responseText);
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
const Tools = {
    get_grade_class: function(grade) {
        grade = parseFloat(grade);

        if (-1 === grade) {
            return '';
        }
        else if (grade >= 90)  // 优
            return 'success';
        else if (grade >= 75)  // 良
            return 'info';
        else if (grade >= 60)  // 及格
            return 'warning';
        else
            return 'danger';
    },
    get_course_type: function(class_type) {
        if (-1 === ['必修', '校任选课', '人文类选修课', '学院任选课'].indexOf(class_type))
            class_type = parseInt(class_type);

        switch (class_type) {
            case 1:
                return '必修';
            case 2:
                return '校任选课';
            case 3:
                return '人文类选修课';
            case 4:
                return '学院任选课';
            case '必修':
                return '1';
            case '校任选课':
                return '2';
            case '人文类选修课':
                return '3';
            case '学院任选课':
                return '4';
        }
    },
    get_weekday: function(day) {
        day = parseInt(day);

        switch (day) {
            case 0:
                return '周日';
            case 1:
                return '周一';
            case 2:
                return '周二';
            case 3:
                return '周三';
            case 4:
                return '周四';
            case 5:
                return '周五';
            case 6:
                return '周六';
        }
    },
    get_section: function(section) {
        section = parseInt(section);

        switch (section) {
            case 1:
                return '1-2节';
            case 2:
                return '3-4节';
            case 3:
                return '5-6节';
            case 4:
                return '7-8节';
            case 5:
                return '9-10节';
        }
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
function who_am_i() {
    Actions.who_am_i();
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
function logout() {
    Actions.logout();
}

function stu_mine_class() {
    let mine_classes = Actions.stu_mine_class();
    for (let i in mine_classes) {
        mine_classes[i].day = Tools.get_weekday(mine_classes[i].day);
        mine_classes[i].section = Tools.get_section(mine_classes[i].section);
    }
    new Vue({
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
        mine_grade[i].grade_class = Tools.get_grade_class(mine_grade[i].grade);
        mine_grade[i].type = Tools.get_course_type(mine_grade[i].type);
        if (-1 === mine_grade[i].grade)
            mine_grade[i].grade = '未录入';
    }
    new Vue({
        el: '#mine_grade-table',
        data: {
            mine_grades: mine_grade
        }
    });
    $('#mine_grade-table tbody').show();
}
function stu_classes_list() {
    let data = Actions.stu_classes_list();
    for (let i in data) {
        data[i].course_info.type = Tools.get_course_type(data[i].course_info.type);
        for (let j in data[i].time) {
            data[i].time[j].day = Tools.get_weekday(data[i].time[j].day);
            data[i].time[j].section = Tools.get_section(data[i].time[j].section);
        }
    }
    let classes_list = new Vue({
        el: '#classes_list',
        data: {
            all_classes: data
        }
    });
    $('#classes_list tbody').show();
}
function stu_exam_info() {
    let exam_info = Actions.stu_exam_info();
    new Vue({
        el: '#exam_info-table',
        data: {
            exams: exam_info
        }
    });
    $('#exam_info-table tbody').show();
}
function stu_change_selected(class_id) {
    Actions.stu_change_selected(class_id);
}

function tea_mine_class() {
    let data = Actions.tea_mine_class();
    for (let i in data) {
        data[i].day = Tools.get_weekday(data[i].day);
        data[i].section = Tools.get_section(data[i].section);
    }
    new Vue({
        el: '#mine_class-table',
        data: {
            mine_classes: data
        }
    });
    $('#mine_class-table tbody').show();
}
function tea_load_classes_list() {
    let data = Actions.tea_class_info();
    let course_count = {};
    for (let i in data) {
        if (!course_count[data[i]['course_name']]) {
            course_count[data[i]['course_name']] = 1;
            data[i]['course_name'] += '_1';
        }
        else {
            course_count[data[i]['course_name']] += 1;
            data[i]['course_name'] += '_' + course_count[data[i]['course_name']].toString();
        }
        $('#class_list-student').append('<dd><a href="./content/tea_students_list.html?class_id=' + data[i]['class_id'] + '" target="content">' + data[i]['course_name'] + '</a></dd>');
    }
}
function tea_students_list() {
    const class_id = get_url_param('class_id');

    // Class info.
    let data = Actions.tea_class_info();
    let class_info = new Vue({
        el: '#class_info-table',
        data: {
            class_id: '',
            course_id: '',
            course_name: '',
            type: '',
            classroom_id: '',
            time: '',
            students_count: '--'
        }
    });
    for (let i in data) {
        if (class_id === data[i]['class_id']) {
            class_info.$data.class_id = data[i]['class_id'];
            class_info.$data.course_id = data[i]['course_id'];
            class_info.$data.course_name = data[i]['course_name'];
            class_info.$data.type = Tools.get_course_type(data[i]['type']);
            class_info.$data.classroom_id = data[i]['classroom_id'];
            let time_info = '';
            for (let j in data[i]['time'])
                time_info += Tools.get_weekday(data[i]['time'][j]['day']) + ' ' + Tools.get_section(data[i]['time'][j]['section']) + '，';
            class_info.$data.time = time_info;
            break;
        }
    }
    $('#class_info-table tbody').show();

    // Students List.
    data = Actions.tea_class_people(class_id);
    class_info.$data.students_count = data.length;
    for (let i in data) {
        data[i].grade_class = Tools.get_grade_class(data[i].grade);
        if (-1 === data[i].grade)
            data[i].grade = '未录入';
    }
    new Vue({
        el: '#students_list-table',
        data: {
            students: data
        }
    });
    $('#students_list-table tbody').show()
}
function tea_change_grade(mod) {
    if (1 === mod) {  // Start
        $('td.grade-td').each(function() {
            let grade = $(this).text();
            let student_id = $(this).siblings().first().text();
            if ('未录入' === grade)
                grade = '';
            $(this).html('<input type="text" value="' + grade + '" title="' + student_id + '" placeholder="未录入">');
            $(this).attr('class', 'grade-td');
        });
        $('#update_grade-start').hide();
        $('#update_grade-started').show();
    }
    else if (-1 === mod)  // Cancel
        window.location.reload();
    else  // Submit
        Actions.tea_update_grade(get_url_param('class_id'));
}
function tea_exam_info() {
    let exam_info = Actions.tea_exam_info();
    new Vue({
        el: '#exam_info-table',
        data: {
            exams: exam_info
        }
    });
    $('#exam_info-table tbody').show();
}

function admin_account_list() {
    let data = Actions.admin_account_list();
    for (let i in data) {
        while (-1 !== data[i]['account'].indexOf(' '))
            data[i]['account'] = data[i]['account'].replace(' ', '_');
    }
    new Vue({
        el: '#account_list',
        data: {
            all_accounts: data
        }
    });
    $('#account_list tbody').show();
}
function admin_change_account(mod, data) {
    if (1 === mod) {
        if (!data.account || !data.acco_type || !data.name || !data.passwd) {
            alert('信息不全，无法添加！');
            return;
        }
        let post_data = {
            'change_type': 'INSERT',
            'detail': {
                'account': data.account,
                'name': data.name,
                'type': data.acco_type,
                'passwd': data.passwd
            }
        };
        if ('student' === data.acco_type)
            post_data['detail']['year'] = '20' + data.account.substring(0, 2);
        Actions.admin_change_account(post_data);
    }
    else if (2 === mod) {
        if (!data.type || !data.account) {
            alert('信息不全，无法删除！');
            return;
        }
        let post_data = {
            'change_type': 'DELETE',
            'detail': {
                'account': data.account,
                'type': data.type
            }
        };
        Actions.admin_change_account(post_data);
    }
    else if (4 === mod) {
        if (!data) {
            alert('信息不全，无法修改！');
            return;
        }
        let name = $('#' + data + '-name').val();
        let passwd = $('#' + data + '-pass').val();
        if (!name && !passwd) {
            alert('你未作任何修改！');
            return;
        }
        let post_data = {
            'change_type': 'UPDATE',
            'detail': {
                'account': data,
                'name': name? name: null,
                'password': passwd? passwd: null
            }
        };
        Actions.admin_change_account(post_data);
    }
    else if (41 ===mod) {  // 切换到修改模式
        if (!data) {
            alert('信息不全，无法启动修改！');
            return;
        }
        let name = $('#' + data + '-name').text();
        let acco_type = $('#' + data + '-type').text();
        $('#' + data).html(
            '<td>' + data + '</td>' +
            '<td><input id="' + data + '-name" value="' + name + '" placeholder="姓名"></td>' +
            '<td><input id="' + data + '-pass" placeholder="密码，如留空则维持原密码不变。"><span id="' + data + '-type" hidden>' + acco_type + '</span></td>' +
            '<td>' +
            '<a href="#" onclick="window.location.reload()">取消</a> ' +
            '<a href="#" onclick="admin_change_account(4, \'' + data + '\')">确认</a>' +
            '</td>'
        );
    }
}
function admin_exam_info() {
    let data = Actions.admin_exam_info();
    new Vue({
        el: '#exam_info',
        data: {
            all_exams: data
        }
    });
    $('#exam_info tbody').show();
}
function admin_exam_info_detail() {
    let exam_id = get_url_param('exam_id');
    let data = Actions.admin_exam_info_detail(exam_id);
    data['students_count'] = data.student.length;
    new Vue({
        el: '#exam_info-table',
        data: data
    });
    $('#exam_info-table tbody').show();
    $('#class_info-table tbody').show();
    new Vue({
        el: '#students_list-table',
        data: {
            students: data.student
        }
    });
    $('#students_list-table tbody').show();
}
function admin_class_list() {
    let data = Actions.admin_class_list();
    new Vue({
        el: '#class_list',
        data: {
            all_classes: data
        }
    });
    $('#class_list tbody').show();
}
function admin_class_detail() {
    let class_id = get_url_param('class_id');
    let data = Actions.admin_class_detail(class_id);
    new Vue({
        el: '#class_info-table',
        data: {
            class_id: class_id,
            course_id: data.course_info.course_id,
            course_name: data.course_info.course_name,
            students_count: data.student.length
        }
    });
    $('#class_info-table tbody').show();
    new Vue({
        el: '#students_list-table',
        data: {
            students: data.student
        }
    });
    $('#students_list-table tbody').show();
}
function admin_course_list() {
    let data = Actions.admin_course_list();
    for (let i in data) {
        data[i]['type'] = Tools.get_course_type(data[i]['type']);
        while (-1 != data[i]['course_id'].indexOf(' '))
            data[i]['course_id'] = data[i]['course_id'].replace(' ', '_');
    }
    new Vue({
        el: '#course_list',
        data: {
            all_courses: data
        }
    });
    $('#course_list tbody').show();
}
function admin_change_course(mod, data) {
    if (1 === mod) {
        if (!data.course_id || !data.course_name || !data.type || !data.credit || !data.period) {
            alert('信息不全，无法添加！');
            return;
        }
        let post_data = {
            'change_type': 'INSERT',
            'detail': data
        };
        Actions.admin_change_course(post_data);
    }
    else if (2 === mod) {
        if (!data) {
            alert('信息不全，无法删除！');
            return;
        }
        let post_data = {
            'change_type': 'DELETE',
            'detail': {
                'course_id': data,
            }
        };
        Actions.admin_change_course(post_data);
    }
    else if (4 === mod) {
        if (!data) {
            alert('信息不全，无法修改！');
            return;
        }
        let course_name = $('#' + data + '-name').val();
        let course_type = $('#' + data + '-type').val();
        let credit = $('#' + data + '-credit').val();
        let period = $('#' + data + '-period').val();
        if (!course_name && !course_type && !credit && !period) {
            alert('你未作任何修改！');
            return;
        }
        while (-1 !== data.indexOf('_'))
            data = data.replace('_', ' ');
        let post_data = {
            'change_type': 'UPDATE',
            'detail': {
                'course_id': data,
                'course_name': course_name? course_name: null,
                'type': course_type? course_type: null,
                'credit': credit? credit: null,
                'period': period? period: null,
            }
        };
        Actions.admin_change_course(post_data);
    }
    else if (41 === mod) {  // 切换到修改模式
        if (!data) {
            alert('信息不全，无法启动修改！');
            return;
        }
        let course_name = $('#' + data + '-name').text();
        let course_type = $('#' + data + '-type').text();
        let credit = $('#' + data + '-credit').text();
        let period = $('#' + data + '-period').text();
        $('#' + data).html(
            '<td>' + data + '</td>' +
            '<td><input id="' + data + '-name" value="' + course_name + '" placeholder="课程名"></td>' +
            '<td><select class="form-control" id="' + data + '-type">' +
            '<option value="1">必修</option>' +
            '<option value="2">校任选课</option>' +
            '<option value="3">人文选修课</option>' +
            '<option value="4">学院选修课</option>' +
            '</select></td>' +
            '<td><input id="' + data + '-credit" value="' + credit + '" placeholder="学分"></td>' +
            '<td><input id="' + data + '-period" value="' + period + '" placeholder="学时"></td>' +
            '<td>' +
            '<a href="#" onclick="window.location.reload()">取消</a> ' +
            '<a href="#" onclick="admin_change_course(4, \'' + data + '\')">确认</a>' +
            '</td>'
        );
        $('#' + data + '-type').val(Tools.get_course_type(course_type));
    }
}
function admin_schedule_list() {
    let data = Actions.admin_schedule_list();
    new Vue({
        el: '#schedule_list',
        data: {
            all_schedules: data
        }
    });
    $('#schedule_list tbody').show();
}
function admin_change_schedule(mod, data) {
    if (1 === mod) {
        if (!data.class_id || !data.classroom_id || !data.week || !data.day || !data.section) {
            alert('信息不全，无法添加！');
            return;
        }
        let post_data = {
            'change_type': 'INSERT',
            'detail': data
        };
        Actions.admin_change_schedule(post_data);
    }
    else if (2 === mod) {
        if (!data) {
            alert('信息不全，无法删除！');
            return;
        }
        let post_data = {
            'change_type': 'DELETE',
            'detail': {
                'schedule_id': data,
            }
        };
        Actions.admin_change_schedule(post_data);
    }
    else if (4 === mod) {
        if (!data) {
            alert('信息不全，无法修改！');
            return;
        }
        let class_id = $('#' + data + '-class').val();
        let classroom_id = $('#' + data + '-room').val();
        let week = $('#' + data + '-week').val();
        let day = $('#' + data + '-day').val();
        let sect = $('#' + data + '-sect').val();
        if (!class_id && !classroom_id && !week && !day || !sect) {
            alert('你未作任何修改！');
            return;
        }
        let post_data = {
            'change_type': 'UPDATE',
            'detail': {
                'schedule_id': data,
                'class_id': class_id? class_id: null,
                'classroom_id': classroom_id? classroom_id: null,
                'week': week? week: null,
                'day': day? day: null,
                'section': sect? sect: null
            }
        };
        Actions.admin_change_schedule(post_data);
    }
    else if (41 === mod) {  // 切换到修改模式
        if (!data) {
            alert('信息不全，无法启动修改！');
            return;
        }
        let class_id = $('#' + data + '-class').text();
        let course_name = $('#' + data + '-cour').text();
        let classroom_id = $('#' + data + '-room').text();
        let week = $('#' + data + '-week').text();
        let day = $('#' + data + '-day').text();
        let sect = $('#' + data + '-sect').text();
        $('#' + data).html(
            '<td>' + data + '</td>' +
            '<td><input id="' + data + '-class" value="' + class_id + '" placeholder="教学班ID"></td>' +
            '<td>' + course_name + '</td>' +
            '<td><input id="' + data + '-room" value="' + classroom_id + '" placeholder="周"></td>' +
            '<td><input id="' + data + '-week" value="' + week + '" placeholder="周"></td>' +
            '<td><input id="' + data + '-day" value="' + day + '" placeholder="星期"></td>' +
            '<td><input id="' + data + '-sect" value="' + sect + '" placeholder="节"></td>' +
            '<td>' +
            '<a href="#" onclick="window.location.reload()">取消</a> ' +
            '<a href="#" onclick="admin_change_schedule(4, \'' + data + '\')">确认</a>' +
            '</td>'
        );
    }
}

function root_show_tables() {
    let data = Actions.root_show_tables();
    for (let i in data)
        $('#tables-list').append('<dd><a href="./content/root_get_table.html?table_name=' + data[i] + '" target="content">' + data[i] + '</a></dd>');
}
function root_get_table() {
    const table_name = get_url_param('table_name');
    let data = Actions.root_get_table(table_name);
    let table = new Vue({
        el: '#table',
        data: {
            table: data
        }
    });
    $('#table').show();
}

// Tools
function change_url() {
    let frame_url = window.frames[0].window.location.href;
    setCookie('frame_url', frame_url, 0.001);
}
function setCookie(c_name, value, expire_days) {
    let ex_date = new Date();
    ex_date.setDate(ex_date.getDate() + expire_days);
    document.cookie = c_name + "=" + encodeURI(value) + ((expire_days==null) ? "" : ";expires=" + ex_date.toUTCString());
}
function getCookie(c_name) {
    if (document.cookie.length > 0) {
        let c_start = document.cookie.indexOf(c_name + "=");
        if (c_start !== -1) {
            c_start = c_start + c_name.length + 1;
            let c_end = document.cookie.indexOf(";", c_start);
            if (c_end === -1)
                c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start, c_end));
        }
    }
    return "";
}
function get_url_param(key) {
    let reg = new RegExp("(^|&)" + key + "=([^&]*)(&|$)"); //构造一个含有目标参数的正则表达式对象
    let r = window.location.search.substr(1).match(reg);  //匹配目标参数
    if (r != null)
        return unescape(r[2]);
    return null; //返回参数值
}

Actions.hello_world();
