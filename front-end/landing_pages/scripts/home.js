const c = (el)=>document.querySelector(el);
const cs = (el)=>document.querySelectorAll(el);

produtosJson.map((item, index)=>{
    let produtosItem = c('#exclusivosVoid .produto').cloneNode(true);
    produtosItem.querySelector('.nome-produto').innerHTML = item.name;
    produtosItem.querySelector('.preco').innerHTML = item.price[0].toFixed(2);
    produtosItem.querySelector('.resumo').innerHTML = item.description;
    produtosItem.querySelector('.img_produto').src = item.img
    if (item.exclusive != null){
        produtosItem.classList.add(item.exclusive)
        c(`#${item.exclusive} .container_produtos`).append(produtosItem);
    } else {
        c('#outros .container_produtos').append(produtosItem);
    }
});

//Mapear botões
var btn_go_slide = document.getElementById('slideRight');
var btn_back_slide = document.getElementById('slideLeft');

//Chamar funções do botão
btn_back_slide.addEventListener('click', passaEsquerda);
btn_go_slide.addEventListener('click', passaDireita);

//Variaveis para o slider funcionar
var slide1 = document.getElementById('passaSlide')
var passaSlide = 1550
var count = 1;

//Mapear Radio Inputs
var image1 = document.getElementById('radio1')
var image2 = document.getElementById('radio2')
var image3 = document.getElementById('radio3')
var image4 = document.getElementById('radio4')

//pular para X slide
image1.addEventListener('click', slide01)
image2.addEventListener('click', slide02)
image3.addEventListener('click', slide03)
image4.addEventListener('click', slide04)

//Funcionamento do slider
function passaDireita(){
    count += 1;

    btn_go_slide.style.opacity = "0"
    btn_back_slide.style.opacity = '0'
    setTimeout(()=>{
        btn_back_slide.style.opacity = '1'
        btn_go_slide.style.opacity = '1'
    }, 390)

    if (count > 4){
        count = 1
    }
    var theSlide = document.getElementsByName('img0'+count)[0]
    theSlide.className = "slideatual";
    var slide_checker = document.getElementById('radio'+count)
    slide_checker.className = "slide_selector_checked"
    for (var c=1; c<=4; c++){
        if (c != count){
            var slide_nullCheck = document.getElementById('radio'+c)
            slide_nullCheck.className = "slide_selector"
            var nullSlide = document.getElementsByName('img0'+c)[0]
            nullSlide.className = 'slides'
        } else{
            continue
        }
    }
   
    if (count == 1){
        passaSlide = 1560
        
    }

    if (count == 2){
        passaSlide = 520
        
    }
    if (count == 3){
        passaSlide = -520
        
    }
    if (count == 4){
        passaSlide = -1560

    }

    slide1.style.marginLeft = `${passaSlide}px`
    
}

function passaEsquerda(){
    count -= 1

    btn_go_slide.style.opacity = "0"
    btn_back_slide.style.opacity = '0'
    setTimeout(()=>{
        btn_back_slide.style.opacity = '1'
        btn_go_slide.style.opacity = '1'
    }, 390)

    if (count == 0){
        count = 4
    }
    var theSlide = document.getElementsByName('img0'+count)[0]
    theSlide.className = "slideatual";var theSlide = document.getElementsByName('img0'+count)[0]
    theSlide.className = "slideatual";
    var slide_checker = document.getElementById('radio'+count)
    slide_checker.className = "slide_selector_checked"
    for (var c=1; c<=4; c++){
        if (c != count){
            var slide_nullCheck = document.getElementById('radio'+c)
            slide_nullCheck.className = "slide_selector"
            var nullSlide = document.getElementsByName('img0'+c)[0]
            nullSlide.className = 'slides'
        } else{
            continue
        }
    }
   
    if (count == 1){
        passaSlide = 1560
        image1.checked=true
    }

    if (count == 2){
        passaSlide = 520
        image2.checked=true
    }
    if (count == 3){
        image3.checked=true
        passaSlide = -520
    }
    if (count == 4){
        image4.checked=true
        passaSlide = -1560
    }

    slide1.style.marginLeft = `${passaSlide}px`
    if (count < 0){
        count = 1
    }

}

//Ir para o 1° slide
function slide01(){
    count = 0
    passaDireita()
}

//Ir para o 2° slide
function slide02(){
    count = 1
    passaDireita()
}
//Ir para o 3° slide
function slide03(){
    count = 2
    passaDireita()
}

//Ir para o 4° slide
function slide04(){
    count = 3
    passaDireita()
}