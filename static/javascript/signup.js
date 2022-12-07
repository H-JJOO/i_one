{
    //정규 표현식 (Regular expression)
    const signupFrmElem = document.querySelector('#signup_frm')

    const idRegex = /^([a-zA-Z0-9]{4,15})$/;//대소문자 + 숫자 조합 4~15글자
    const pwRegex = /^([a-zA-Z0-9!@_]{4,20}$)/;//대소문자 + 숫자 조합 4~15글자
    const nmRegex = /^([가 -힣]{2,10})$/; //`한글 2~10자 조합 (영어, 특수기호X)
    const emailRegex = /^(?=.{8,50}$)([0-9a-z_]{4,})@([0-9a-z][0-9a-z\-]*[0-9a-z]\.)?([0-9a-z][0-9a-z\-]*[0-9a-z])\.([a-z]{2,15})(\.[a-z]{2})?$/; // 이메일

    if (signupFrmElem) {

        signupFrmElem.addEventListener('submit', (e) => {
            const inputId = signupFrmElem.userId.value;
            const inputPw = signupFrmElem.password.value;
            const inputCheckPw = signupFrmElem.checked_password.value;
            const inputNm = signupFrmElem.name.value;
            const inputEmail = signupFrmElem.email.value;


            if (!idRegex.test(inputId)) {
                console.log(idRegex)
                console.log(inputId)
                alert('아이디는 대소문자, 숫자조합으로 4~20자 되어야 합니다.');
                e.preventDefault();
                document.querySelector('#userId').scrollIntoView();
            } else if (!pwRegex.test(inputPw)) {
                alert('비밀번호는 대소문자, 숫자, !, @, _ 조합으로 4~100자 되어야합니다.');
                e.preventDefault();
                document.querySelector('#password').scrollIntoView();
            } else if (inputPw !== inputCheckPw) {
                alert('비밀번호 확인을 확인해주세요.');
                e.preventDefault();
                document.querySelector('#checked_password').scrollIntoView();
            } else if (!nmRegex.test(inputNm)) {
                alert('이름은 한글 조합으로 2~10자 여야합니다.');
                e.preventDefault();
                document.querySelector('#name').scrollIntoView();
            } else if (!emailRegex.test(inputEmail)) {
                alert('이메일 형식을 확인해주세요. Ex) abc123@examle.com');
                e.preventDefault();
                document.querySelector('#email').scrollIntoView();
            } else {

            }

        });
    }


}