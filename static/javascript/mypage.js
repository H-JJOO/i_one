$(document).ready(function () {
    const id = 1;
    $.ajax({
        type: "GET", url: `/users/${id}`, data: {}, success: function (response) {
            const rows = response["users"];
            let name = rows['name']
            let email = rows["email"]
            let gender = rows["gender"] === 1 ? '남자' : '여자'
            let location = rows["location"]
            let intro = rows["intro"]
            let img = rows["profile_image"]
            let imgsrc = "../static/img/" + img
            let temp_html = `
    <div class="mypage_mid">
        <div class="mypage_midbox">
            <div class="mypage_img">
            <img src="${imgsrc}" id="user_image">
            </div>
            <div class="mypage_name">
                이름 : ${name}
                <hr>
            </div>
            <div class="mypage_email">
                이메일 : ${email}
                <hr>
            </div>
            <div class="mypage_gender">
                성별 : ${gender}
                <hr>
            </div>
            <div class="mypage_location">
                지역 : ${location}
                <hr>
            </div>
            <div class="mypage_intro">
                자기소개 : <p>${intro}</p>
                <hr> 
            </div>
            <div class="editbtn">
                <button class="mybtn" type="button"><a href="/mypage/edit">프로필 수정</a></button>
                <button class="homebtn" type="button"><a href="/">홈으로</a></button>
            </div>
       </div>
    </div>
    `
            $('.mypage_main').append(temp_html)
        }
    })
})