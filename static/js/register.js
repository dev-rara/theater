$(document).ready(function () {
    $("#input-username").on("propertychange change paste input", function () {
        $('#help-id').text('아이디 중복확인을 해주세요.').removeClass('is-safe').removeClass('is-success').addClass('is-danger')
        $('#input-username').focus()
        return;
    })
});

function sign_up() {
    let id = $('#input-username').val()
    let password = $('#input-password').val()
    let password2 = $('#input-password2').val()

    if (password2 == '') {
        $('#help-password2').text('비밀번호를 입력해주세요.').removeClass('is-safe').addClass('is-danger')
        $('#input-password2').focus()
        return;
    } else if (password2 != password) {
        $('#help-password2').text('비밀번호가 일치하지 않습니다.').removeClass('is-safe').addClass('is-danger')
        $('#input-password2').focus()
        return;
    } else {
        $('#help-password2').text('비밀번호가 일치합니다.').removeClass('is-danger').addClass('is-success')
    }

    $.ajax({
        type: "POST",
        url: "/api/signup",
        data: {id_give: id, password_give: password2},
        success: function (response) {
            alert('회원가입이 완료되었습니다.')
            window.location.replace('/login')
        }
    });
}

function id_invalid_check() {
    let id = $('#input-username').val()

    if (id == '') {
        $('#help-id').text('아이디를 입력해주세요.').removeClass('is-safe').addClass('is-danger')
        $('#input-username').focus()
        return;
    } else if (!$('#help-id').hasClass('is-success')) {
        $('#help-id').text('아이디 중복확인을 해주세요.').removeClass('is-safe').addClass('is-danger')
        $('#input-username').focus()
        return;
    }
}

function password_invalid_check() {
    let password = $('#input-password').val()
    let password2 = $('#input-password2').val()
    
    if (password == '') {
        $('#help-password').text('비밀번호를 입력해주세요.').removeClass('is-safe').addClass('is-danger')
        $('#input-password').focus()
        return;
    } else if (!check_password(password)) {
        $('#help-password').text('비밀번호를 확인해주세요. 영문과 숫자 필수, 특수문자(!@#$%^&*) 사용가능 8-20자').removeClass('is-safe').addClass('is-danger')
        $('#input-password').focus()
        return
    } else {
        $('#help-password').text('사용할 수 있는 비밀번호입니다.').removeClass('is-danger').addClass('is-success')
    }
}

function check_id(asValue) {
    var regExp = /^(?=.*[a-zA-Z])[-a-zA-Z0-9_.]{5,10}$/;
    return regExp.test(asValue);
}

function check_password(asValue) {
    var regExp = /^(?=.*\d)(?=.*[a-zA-Z])[0-9a-zA-Z!@#$%^&*]{8,20}$/;
    return regExp.test(asValue);
}

function id_overlap_check() {
    let id = $('#input-username').val()
    
    if (id == '') {
        $('#help-id').text('아이디를 입력해주세요.').removeClass('is-safe').addClass('is-danger')
        $('#input-username').focus()
        return;
    }
    
    if (!check_id(id)) {
        $('#help-id').text('아이디 형식을 확인해주세요. 영문과 숫자,일부 특수문자(._-) 조합의 5-10자 입력가능').removeClass('is-safe').addClass('is-danger')
        $('#input-username').focus()
        return;
    }
    $('#help-id').addClass('is-loading')
    $.ajax({
        type: "POST",
        url: "/api/signup/check-id",
        data: {id_give: id},
        success: function (response) {
            if (response['exists']) {
                $('#help-id').text('이미 존재하는 아이디입니다.').removeClass('is-safe').addClass('is-danger')
                $('#input-username').focus()
            } else {
                $('#help-id').text('사용할 수 있는 아이디입니다.').removeClass('is-danger').addClass('is-success')
            }
        }
    });
    $('#help-id').removeClass('is-loading')
}