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

            for (let i=0; i<r_list.length; i++) {
                let review = r_list[i]['review']
                let userid = r_list[i]['userid']

                let temp_html = `
                        <div class="review_card">
                            <div class="info_img">
                                <img src=#>
                            </div>
                            <div class="info_text">
                                <div class="info_review">${review}</div>
                            </div>
                            <button class="review_delete"> X</button>
                        </div>`
                $('#review_card_box').append(temp_html)
            }
        }
    })
}

                // theater_id에 따른 공연DB를 가져오고 싶은데. 음
                // // 현재 id의 review데이터
                // let r_list = JSON.parse(response['review_list'])
                // // review의 theater_id를 얻기위함
                // let r = r_list.map(item=> {
                //     return item.theater_id
                // })
                //
                // // 전체 theater 리스트
                // let t_list = response['theater_list']
                // let current_list = t_list.filter(item =>{
                //     // console.log(item.theater_id)
                //     // console.log(...r, '리뷰번호') : 배열형태여서 스프레드로 풀어줌
                //     // console.log(Number(item.theater_id) === Number(...r))
                //     return Number(item.theater_id) === Number(...r)
                // })
                // console.log(current_list)



                //
                // // review의 theater_id를 얻기위함
                // let r = r_list.map(item=> {
                //     return item.theater_id
                // })
                //
                // // 전체 theater 리스트
                // let t_list = response['theater_list']
                // // console.log(t_list)
                // for(let i=0; i<t_list.length; i++) {
                //     if (Number(r)==Number(t_list[i]['theater_id'])){
                //         console.log(t_list[i])
                //     }
                // }
                //
