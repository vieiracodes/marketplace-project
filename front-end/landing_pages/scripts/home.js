const c = (el)=>document.querySelector(el);
const cs = (el)=>document.querySelectorAll(el);

produtosJson.map((item, index)=>{
    let produtosItem = c('#exclusivosVoid .produto').cloneNode(true);
    produtosItem.querySelector('.nome-produto').innerHTML = item.name;
    produtosItem.querySelector('.preco').innerHTML = item.price.toFixed(2);
    produtosItem.querySelector('.resumo').innerHTML = item.description;
    produtosItem.querySelector('.img_produto').src = item.img
    produtosItem.querySelector('.link').href = item.link
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
btn_back_slide.addEventListener('touchstart', passaEsquerda)
btn_go_slide.addEventListener('click', passaDireita);
btn_go_slide.addEventListener('touchstart', passaDireita);

//Variaveis para o slider funcionar
var slide1 = document.getElementsByClassName('passaSlide')[0]
var passaSlide = 0
var count = 1;
var margin = document.getElementsByClassName('destaques')[0]

console.log(margin.offsetLeft)

//Mapear Radio Inputs
var image1 = document.getElementById('radio1')
var image2 = document.getElementById('radio2')
var image3 = document.getElementById('radio3')
var image4 = document.getElementById('radio4')

//pular para X slide
image1.addEventListener('click', slide01)
image1.addEventListener('touchstart', slide01)

image2.addEventListener('click', slide02)
image2.addEventListener('touchstart', slide02)

image3.addEventListener('click', slide03)
image3.addEventListener('touchstart', slide03)

image4.addEventListener('click', slide04)
image4.addEventListener('touchstart', slide04)

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
        for(var c = 1; c <= 4; c++){
            var theSlidesB = document.getElementsByClassName('slides')[c]
            theSlidesB.style.marginLeft = '0%'
            console.log(theSlidesB)
        }
        
    }

    if (count == 2){
        for(var c = 1; c <= 4; c++){
            var theSlidesB = document.getElementsByClassName('slides')[c]
            theSlidesB.style.marginLeft = '-100%'
            console.log(theSlidesB)
        }
        
    }
    if (count == 3){
        for(var c = 2; c <= 4; c++){
            var theSlidesB = document.getElementsByClassName('slides')[c]
            theSlidesB.style.marginLeft = '-200%'
            console.log(theSlidesB)
        }
    }
    if (count == 4){
        for(var c = 3; c <= 4; c++){
            var theSlidesB = document.getElementsByClassName('slides')[c]
            theSlidesB.style.marginLeft = '-300%'
            console.log(theSlidesB)
        }
        
    }

    
}

function passaEsquerda(){
    count -= 1
    if (count == 0){
        count = 4
    }

    btn_go_slide.style.opacity = "0"
    btn_back_slide.style.opacity = '0'
    setTimeout(()=>{
        btn_back_slide.style.opacity = '1'
        btn_go_slide.style.opacity = '1'
    }, 390)

    var slide_checker = document.getElementById('radio'+count)
    slide_checker.className = "slide_selector_checked"
    for (var c=1; c<=4; c++){
        if (c != count){
            var slide_nullCheck = document.getElementById('radio'+c)
            slide_nullCheck.className = "slide_selector"
        } else{
            continue
        }
    }
    if (count == 1){
            var theSlides = document.getElementsByClassName('slides')[count]
            theSlides.style.marginLeft = '000%'
            image1.checked=true
            console.log(theSlides)
        
    }

    if (count == 2){
        var slide02 = document.getElementsByClassName('slides')[2]
        slide02.style.marginLeft = '-100%'
        
        
    }
    if (count == 3){
        var theSlides = document.getElementsByClassName('slides')[1]
        theSlides.style.marginLeft = '-100%'
        for(var c = 3; c > 1; c--){
            var theSlides = document.getElementsByClassName('slides')[c]
            theSlides.style.marginLeft = `-200% `

        }
    }
    if (count == 4){
        for(var c = 3; c >= 1; c--){
            var theSlides = document.getElementsByClassName('slides')[c]
            theSlides.style.marginLeft = `-${c}00%`

        }
        
        
    }
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