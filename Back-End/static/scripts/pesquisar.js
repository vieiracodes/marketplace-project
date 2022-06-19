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
