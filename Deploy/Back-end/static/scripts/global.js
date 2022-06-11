const menuButton = document.querySelector('ul .menu-icon')
let c = 2

menuButton.addEventListener('touchstart', changeBtns)
menuButton.addEventListener('click', changeBtns)


if (window.innerWidth > 768){
    let btnsContainer = document.querySelector('.btns')
    btnsContainer.style.display = 'flex'
}

function changeBtns(){
    let btnsContainer = document.querySelector('.btns')
    if(c%2 == 0){
        btnsContainer.style.display = 'flex'
        setTimeout(()=>{
            btnsContainer.style.opacity = '1'
        }, 200)
        c++
    } else{
        btnsContainer.style.opacity = '0'
        setTimeout(()=>{
            btnsContainer.style.display = ''
        },200)
        c++
    }
}
