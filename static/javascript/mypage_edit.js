$(document).ready(function () {
    const id = 1;
    $.ajax({
        type: "GET",
        url: `/users/${id}`,
        data: {},
        success: function (response) {
            const rows = response["users"];
            let name = rows['name']
            let email = rows["email"]
            let intro = rows["intro"]
            let img = rows["profile_image"]
            let imgsrc = "../static/img/" + img
            let temp_html = `
    <div class="myedit_mid">
        <div class="myedit_midbox">
            <div class="myedit_img">
                <img src="${imgsrc}" id="user_image">
            </div>
            <div class="img_button">
                <label class="editlabel" for="img_edit">
                <div class="btn-upload">사진 업로드</div>
                </label>
                <input class="myedit_imgupload" type="file" id="img_edit"/>
                <!--                사진삭제 변경 필요-->
                <button class="myedit_imgdel">
                    사진 삭제
                </button>
            </div>
        </div>
        <div>
            <label><p>이름</p></label>
            <input class="myedit_name"  value="${name}" id="name_edit">
        </div>
        <div>
            <label><p>이메일 변경</p></label>
            <input class="myedit_email" value="${email}" id="email_edit">
        </div>
        자기 소개 변경
        <div>
            <textarea class="myedit_intro">${intro}</textarea>
        </div>
        <div class="myedit_bottom">
            <button class="okbtn" id="profile_edit">
                확인
            </button>
            <a href="/mypage">
                <button type="button" class="cancelbtn">취소</button>
            </a>
        </div>
    </div>`
            $('.myedit_main').append(temp_html)

            // $("input[type=file]").change(function (event) {
            //     let tmpPath = URL.createObjectURL(event.target.files[0]);
            //
            //     $("#user_image").attr("src", tmpPath);
            // });
            //
            // $(".myedit_imgdel").click(function () {
            //     $("#user_image").attr("src", "../static/img/default-user-image.png");
            // })
            $(".okbtn").click(function () {
                const name = $(".myedit_name").val();
                const email = $(".myedit_email").val();
                const intro = $(".myedit_intro").val();
                // const imageInput = $("#img_edit")[0];

                // if (imageInput.files.length === 0) {
                //     alert("파일은 선택해주세요");
                //     return;
                // }

                const formData = new FormData();
                formData.append("name", name);
                formData.append("email", email);
                formData.append("intro", intro);
                // formData.append("file", imageInput.files[0]);

                $.ajax({
                    type: "PUT",
                    url: `/users/${id}`,
                    processData: false,
                    contentType: false,
                    data: formData,
                    success: function (response) {
                        alert(response["msg"])
                        window.location.href = "/mypage"
                    }
                })
            })
        }
    })
})

