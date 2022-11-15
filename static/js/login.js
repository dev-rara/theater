function log_out() {
    $.removeCookie('mytoken');
    alert('로그아웃 되었습니다.')
    window.location.href = '/login'
}

function log_in() {
    let id = $('#input-username').val()
    let password = $('#input-password').val()
    
    if (id == '') {
        $('#help-id-login').text('아이디를 입력하세요')
        $('#input-username').focus()
        retrun;
    } else {
        $('#help-id-login').text('')
    }
    
    if (password == '') {
        $('#help-password-login').text('비밀번호를 입력해주세요.')
        $('#input-password').focus()
        return;
    } else {
        $('#help-password-login').text('')
    }
    
    $.ajax({
        type: "POST",
        url: "/api/login",
        data: {id_give: id, password_give: password},
        success: function (response) {
            if (response['result'] == 'success') {
                $.cookie('mytoken', response['token']);
                window.location.href = '/index';
            } else {
                alert(response['msg'])
            }
        }
    });
}