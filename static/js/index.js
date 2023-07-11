const searchForm = document.querySelector('.search-bar');
const searchInput = document.querySelector('.search-input');
const searchButton = document.querySelector('.search-btn');
const loginForm=document.querySelector('#login-form')
const loginTitle=document.querySelector('#login-title')
const signupForm=document.querySelector('#signup-form')
var header = document.querySelector("header");

console.log(header)
window.addEventListener("scroll",function(){
    var header = document.querySelector("header");
    header.classList.toggle("sticky",window.scrollY>1)
    console.log('Inside window scroll')
})
gsap.fromTo(searchForm, {opacity: 0, y: -20}, {opacity: 1, y: 0, duration: 1, delay: 0.2});
gsap.fromTo(searchInput, {opacity: 0, x: -20}, {opacity: 1, x: 0, duration: 1, delay: 0.2});
gsap.fromTo(searchButton, {opacity: 0, x: 20}, {opacity: 1, x: 0, duration: 1, delay: 0.2});

gsap.fromTo(loginForm,{opacity:0,y:5},{opacity: 1, y: 0, duration: 1, delay: 0.2})
gsap.fromTo(signupForm,{opacity:0,y:5},{opacity: 1, y: 0, duration: 1, delay: 0.2})
gsap.fromTo(loginTitle, {opacity: 0}, {opacity: 1, duration: 1,delay:0.2});

const formBtn = document.querySelector('.form-btn');

let direction = 1;
let backgroundX = 0;
if(formBtn){
function moveBackgroundImage() {
  backgroundX += direction * 2;
  if (backgroundX > 100) {
    direction = -1;
  } else if (backgroundX < -100) {
    direction = 1;
  }
  gsap.to(formBtn, {
    backgroundPosition: `${backgroundX}px 0px`,
    duration: 0.1,
    onComplete: moveBackgroundImage
  });
}

moveBackgroundImage();
}


console.log('Its working')

console.log('working javascript')


