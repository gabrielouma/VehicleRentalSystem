//Password show
var input = document.querySelector(".pswrd");
var show = document.querySelector(".show");

show.addEventListener("click", active);
function active(){
    if(input.type === "password"){
        input.type = "text";
        show.style.color = "#1da1f2";
        show.textContent = "HIDE";
        input.removeAttribute("readonly");
    }else{
        input.type = "password";
        show.style.color = "#111";
        show.textContent = "SHOW";
        input.setAttribute("readonly", "true");
    }
};

//Answer show
var input2 = document.querySelector(".pswrd2");
var show2 = document.querySelector(".show2");

show2.addEventListener("click", active2);
function active2(){
    if(input2.type === "password"){
        input2.type = "text";
        show2.style.color = "#1da1f2";
        show2.textContent = "HIDE";
        input2.removeAttribute("readonly");
    }else{
        input2.type = "password";
        show2.style.color = "#111";
        show2.textContent = "SHOW";
        input2.setAttribute("readonly", "true");
    }
};

//  Profile picture
const imgDiv = document.querySelector('.user-img');
const img = document.querySelector('#photo');
const file = document.querySelector('#file');
const uploadbtn = document.querySelector('#uploadbtn');

file.addEventListener('change', function(){
    const chosedfile = this.files[0];
    if(chosedfile){
        const reader = new FileReader();

        reader.addEventListener('load', function(){
            img.setAttribute('src', reader.result);
        });
        reader.readAsDataURL (chosedfile);
    }
});