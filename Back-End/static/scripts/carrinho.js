let produtosCarrinho = []

window.onload = function() {
    localStorage.setItem('idProduto', produtosJson[0].id)

    if (localStorage.idProduto){
        var prod = localStorage.idProduto;
        console.log(localStorage.idProduto);console.log(produtosJson[prod-1])
    }
}