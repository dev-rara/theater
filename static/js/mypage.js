// nav에서 마이페이지 버튼 클릭
function go_mypage(user) {
    console.log(user)
    $.ajax({
        type: 'GET',
        url: `/myreview?id_give=${user}`,
        data: {},
        success: function (response) {
            window.location.href = `/mypage/${user}`;
        }
    })
}

// 마이페이지 댓글보여주기
function myReviewShow(id) {
    // 매개변수 id = 현재 로그인 user
    $.ajax({
        type: 'GET',
        url: `/mycard?id_give=${id}`,
        data: {},
        success: function (response) {
            let r_list = JSON.parse(response['review_list'])
            for (let i=0; i<r_list.length; i++){
                console.log(r_list[i])
                let review = r_list[i]['review']
                let theater_id = r_list[i]['theater_id']
                let temp_html = `
                        <div class="review_card">
                            <div class="review_view">
                                <div class="info_review">${review}</div>
<!--                                <button onclick="review_del(${theater_id})">삭제</button>-->
                            </div>
                            <a href="/detail/${theater_id}" class="info_theater">공연정보로<br>이동</a>
                        </div>
                        `
                $('#review_card_box').append(temp_html)
            }
        }
    })
}
