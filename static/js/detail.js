

// 디테일 페이지 - 리뷰 작성
function reviewSave(id) {
    let review = $('#review_text').val()
    console.log(id, review)
    $.ajax({
        type: 'POST',
        url: `/review`,
        data: {'review_give':review, 'id_give':id},
        success: function (response) {
            let msg = response['result']
            // 페이지 새로고침 (포스트에)
            window.location.reload()
        }
    })
}


// 디테일 페이지 - 리뷰 보여줌
function reviewShow(id) {
    console.log(id)
    $.ajax({
        type: 'GET',
        url: `/review`,
        data: {},
        success: function (response) {
            let list = response['review_list']
            console.log(list)
            // 전체 review에서 현재공연(id)의 댓글만 보여줄 수 있게함
            let current_list = list.filter((item,idx,arr)=>{
                return Number(item.theater_id) === Number(id)
                // console.log(Number(item.theater_id) === Number(id))
            })
            // 해당 페이지의 id가 있는 DB만 보여줘.
            if(current_list){
                for (let i = 0; i < current_list.length; i++) {
                // console.log(list[i])
                let user = current_list[i]['userid']
                let review = current_list[i]['review']
                let theater_id = current_list[i]['theater_id']
                let temp_html = `
                    <div class="review_card">
                        <div class="review_view">
                            <p class="review_view_id">${user}</p>
                            <p class="review_view_text">${review}</p>
                        </div>
                    </div>`
                $('#culture_review_show').append(temp_html)
                }
            }
        }
    })
}


// 리뷰 삭제
function reviewDel(id){
    console.log(id)
    // 리뷰 고유 id찾아서 삭제해야함.
    // 출력되는 id는 공연id임
}