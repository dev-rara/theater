$(document).ready(function () {
    theater_show('클래식');
    // theater_show()
});

function log_out() {
    $.removeCookie('mytoken');
    alert('로그아웃 했습니다.')
    window.location.href = '/login'
}


// 공연 리스트 보여주기
function theater_show(type) {
    let select_type = type;
    // console.log(type)
    $('#perform_box').empty()

    $.ajax({
        type: 'GET',
        url: `/theater?type_give=${select_type}`,
        data: {},
        success: function (response) {
            //DB조건 추가시, 파일 타입 에러로 인해 JSON.parse()추가
            let list = JSON.parse(response['theater_list'])
            // console.log(list)
            for (let i=0; i< 5; i++){
                let title = list[i]['TITLE']
                let date = list[i]['DATE']
                let img = list[i]['MAIN_IMG']
                let url = list[i]['ORG_LINK']
                let place = list[i]['PLACE']
                let id = list[i]['theater_id']
                // console.log(title,id)
                let temp_html = `
                    <div class="perform_card" id="${id}">
                        <a href="${url}" target="_blank"><img src="${img}"></a>
                        <div class="card_info">
                            <p>${title}</p>
                            <p>${date}</p>
                            <p>${place}</p>
                        </div>
                        <button class="card_btn" onclick="make_review(${id})">리뷰쓰기</button>
                    </div>`

                $('#perform_box').append(temp_html)
            }
        }
    })
}

// 공연 검색
function theater_search() {
    let codename = $('#performance option:selected').val();
    let query = $('#searchBar_input').val()

    $('#searchBar_input').empty()
    $('#search_box').empty()
    // console.log(codename, query)

    $.ajax({
        type: 'GET',
        url: `/search?input_query=${query}`,
        data: {},
        success: function(response) {
            //DB조건 추가시, 파일 타입 에러로 인해 JSON.parse()추가
            let list = JSON.parse(response['search_result'])
            for (let i=0; i<5; i++){
                console.log(list[i]['TITLE'])
                let title = list[i]['TITLE']
                let date = list[i]['DATE']
                let img = list[i]['MAIN_IMG']
                let url = list[i]['ORG_LINK']
                let place = list[i]['PLACE']
                let id = list[i]['theater_id']

                let temp_html = `
                    <div class="perform_card">
                        <a href="${url}" target="_blank"><img src="${img}"></a>
                        <div class="card_info">
                            <p>${title}</p>
                            <p>${date}</p>
                            <p>${place}</p>
                        </div>
                        <button class="card_btn" onclick="make_review(${id})">리뷰쓰기</button>
                    </div>`
                $('#search_box').append(temp_html)
            }
        }
    })
}

// 메인에서 리뷰작성 버튼 클릭 -> 데이터포함 페이지 이동
function make_review(id) {
    console.log(id)
    $.ajax({
        type: 'GET',
        url: `/detail?id_give=${id}`,
        data: {},
        success: function (response) {
            console.log(response)
            let url = response['url']
            window.location.href = `/detail/${id}`;
        }
    })
}

