/*----------------------------------<Slider>----------------------------------*/
//Mapear botões
var btn_go_slide = document.getElementById('slideRight');
var btn_back_slide = document.getElementById('slideLeft')

//Chamar funções do botão
btn_back_slide.addEventListener('click', passaEsquerda)
btn_go_slide.addEventListener('click', passaDireita);

//Variaveis para o slider funcionar
var slide1 = document.getElementsByName('img01')[0]
var passaSlide = 1550
var count = 1;

//Mapear Radio Inputs
var image1 = document.getElementById('radio1')
var image2 = document.getElementById('radio2')
var image3 = document.getElementById('radio3')
var image4 = document.getElementById('radio4')
image1.checked=true

//pular para X slide
image1.addEventListener('click', slide01)
image2.addEventListener('click', slide02)
image3.addEventListener('click', slide03)
image4.addEventListener('click', slide04)


//Funcionamento do slider
function passaDireita(){
    count += 1;
    if (count > 4){
        count = 1
    }
    var theSlide = document.getElementsByName('img0'+count)[0]
    theSlide.className = "slideatual";
    for (var c=1; c<=4; c++){
        if (c != count){
        var nullSlide = document.getElementsByName('img0'+c)[0]
        nullSlide.className = 'slides'
        } else{
            continue
        }
    }

    if (count == 1){
        passaSlide = 1570
        image1.checked=true

    }

    if (count == 2){
        passaSlide = 530
        image2.checked=true

    }
    if (count == 3){
        image3.checked=true
        passaSlide = -509

    }
    if (count == 4){
        image4.checked=true
        passaSlide = -1550

    }

    slide1.style.marginLeft = `${passaSlide}px`

}

function passaEsquerda(){
    count -= 1
    if (count == 0){
        count = 4
    }
    var theSlide = document.getElementsByName('img0'+count)[0]
    theSlide.className = "slideatual";var theSlide = document.getElementsByName('img0'+count)[0]
    theSlide.className = "slideatual";
    for (var c=1; c<=4; c++){
        if (c != count){
        var nullSlide = document.getElementsByName('img0'+c)[0]
        nullSlide.className = 'slides'
        } else{
            continue
        }
    }

    if (count == 1){
        passaSlide = 1570
        image1.checked=true
    }

    if (count == 2){
        passaSlide = 530
        image2.checked=true
    }
    if (count == 3){
        image3.checked=true
        passaSlide = -509
    }
    if (count == 4){
        image4.checked=true
        passaSlide = -1550
    }

    slide1.style.marginLeft = `${passaSlide}px`
    if (count < 0){
        count = 1
    }

}

//Ir para o 1° slide
function slide01(){
    count = 0
    image1.style.backgroundColor = 'blue'
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
/*-------------------------------<AutoComplete>-------------------------------*/

// Autocomplete da barra de pesquisa
function autoComplete() {

// Importação de "bibliotecas para funcionamento do autoComplete"
  const head = document.head || document.getElementsByTagName('head')[0]
  const styles = ["http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.16/themes/ui-lightness/jquery-ui.css"];
  const scripts = [
      "https://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.js",
      "https://ajax.googleapis.com/ajax/libs/jqueryui/1.8.16/jquery-ui.js"];

    // Criando o estilo que será necessário para executar o autocomplete
    for(let i in styles){
      let style = document.createElement("link")
      style.rel = "stylesheet"
      style.type = "text/css"
      style.href = styles[i]
      head.appendChild(style)
    }

    // Criando os estilos que serão necessários para executar o autocomplete
    for(let i in scripts){
      let script = document.createElement("script")
      script.src = scripts[i]
      script.type = "text/javascript";
      head.appendChild(script)
    }

//Execução da função de autoComplete
$( function() {
  //sugests será o que aparecerá como recomendação de autocomplete
  var sugests = ['PS4', 'PS3', 'PlayStation4', 'PlayStation3', 'PlayStation',
  'Xbox One', 'Xbox360', 'Xbox', 'Switch', 'Nintendo Switch', 'Nintendo', '3DS',
  'Nintendo 3DS'];
  $( "#barra_pesquisa" ).autocomplete({
    source: sugests });
  });
}
