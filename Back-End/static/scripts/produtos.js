let produtosJson = [
    {id:1, name:'Naruto Ultimate Ninja Storm 4', img:'static/sources/images/home/jog009.webp',destaque:'static/sources/images/home/des004.jpg', price:250.00, description:'A última criação da aclamada série STORM leva você para uma aventura intensa e impressionante. Aproveite o sistema de batalha totalmente reformulado e prepare-se para mergulhar nas lutas mais épicas que você já viu na série NARUTO SHIPPUDEN: Ultimate Ninja STORM! Prepare-se para o jogo da série STORM mais esperado até o momento!', exclusive:null, link:'pag_produtos/naruto_ultimate_ninja_storm_4.html'},

    {id:2, name:'Forza Horizon 4', img:'static/sources/images/home/jog001.jpg', destaque:'static/sources/images/products/forza-horizon-4.jpg', price:250.00, description:'Um dos melhores games de corrida de carros já feito. O mundo aberto de Forza Horizon 4 é sincronizado e compartilhado, são até 72 jogadores dividindo o mesmo servidor. Mas também é possível jogar no modo offline.', exclusive:'exclusivos_Xbox', link:'pag_produtos/forza-horizon-4.html'}, 

    {id:3, name:'Naruto Ultimate Ninja Storm 3', img:'static/sources/images/home/jog010.jpg', destaque:'static/sources/images/home/des003.jpg', price:230.00, description:'Lorem ipsum', exclusive:null, link:'pag_produtos/naruto-ultimate-ninja-storm-3.html'},

    {id:4, name:'Killer Instinct', img:`static/sources/images/home/jog002.webp`, destaque:'static/sources/images/products/killer-instinct.jpg', price:150.90, description:'Iniciam-se os combos, é dada sequência na pancadaria e, por fim, executam-se os movimentos finalizadores. Os Ultra Combos, que são movimentos especiais usados apenas para finalizar uma partida com vitória. Tudo que é encontrado nos jogos atuais de luta, não dá pra perder.',exclusive:'exclusivos_Xbox', link:'pag_produtos/killer-instinct.html'},

    {id:5, name:'Halo 5 Guardians', img:'static/sources/images/home/jog003.webp', destaque:'static/sources/images/products/halo-5-guardians.webp', price:219.00, description:'O velho e conhecido Masterchief. Para os fãs do Xbox, esse personagem é o mais significativo de todo o universo Microsoft. Apesar de não ser tão acionado como em títulos anteriores, o game é impecável.', exclusive:'exclusivos_Xbox', link:'pag_produtos/halo-5-guardians.html'},

    {id:6, name:'Gears 5', img:'static/sources/images/home/jog004.jpg',destaque:'static/sources/images/products/gears-5.jpg', price:299.99, description:'Mais do que um shooter contra alienígenas, hoje o game possui um mundo cujo enredo pode ser expansivo, inclusive, para outras mídias. Lidar com fatos do passado na história que teve inícios em Gears 4 é o ponto alto do game. Para os fãs de jogos táticos a série oferece o Gears Tactics, bem próximo do XCOM 2.', exclusive:'exclusivos_Xbox', link:'pag_produtos/gears-5.html'},

    {id:7, name:'PlayStation 5', img:'static/sources/images/home/con001.png', destaque:'static/sources/images/products/playstation5.jpg', price:4499.99, description:'Maravilhe-se com os gráficos incríveis e experimente os recursos do novo PS5.', exclusive:'console', link:'pag_produtos/playstation-5.html'},

    {id:8, name:'Nintendo Switch', img:'static/sources/images/home/con002.webp', destaque:'static/sources/images/products/nintendo-switch.jpg', price:2989.99, description:'O Nintendo Switch foi desenvolvido para fazer parte da sua vida, transformando-se de um console doméstico em um console portátil num piscar de olhos.', exclusive:'console', link:'pag_produtos/nintendo-switch.html'},

    {id:9, name:'Xbox Series X', img:'static/sources/images/home/con003.jpg', destaque:'static/sources/images/products/xbox-series-x.jpg', price:4100.99, description:'Os 12 teraflops de poder de processamento alojados no sistema em um chip (SOC) funcionam com as arquiteturas Zen 2 e RDNA 2 da AMD para resultar em mundos que exigem um olhar mais atento.', exclusive:'console', link:'pag_produtos/xbox-serie-x.html'},

    {id:10, name:'PlayStation 4', img:'static/sources/images/home/con004.webp', destaque:'static/sources/images/products/playstation-4.webp', price:2290.00, description:'Faça do seu jeito no Victory Royale, ganhe a Série Mundial e lidere seu esquadrão dentro da batalha. Com alguns dos maiores e melhores jogos disponíveis, para PS4 e milhões de jogadores ao redor do mundo, todos aqui estão esperando por você.', exclusive:'console', link:'pag_produtos/playstation-4.html'},

    {id:11, name:'Gran Turismo 7', img:'static/sources/images/home/jog005.jpg', destaque:'static/sources/images/products/grand-turismo-7.jpg', price:349.99, description:'A clássica franquia de corrida da Sony ganhou mais um jogo em 2022. Gran Turismo 7 vai além de, simplesmente, disputar corridas: é um título que busca celebrar a cultura automobilística. Exemplos disso são a presença do circuito de Interlagos, em São Paulo (SP) e do piloto Lewis Hamilton, carinhosamente apelidado como "maestro" do game.', exclusive:'exclusivos_Ps', link:'pag_produtos/gran-turismo-7.html'},

    {id:12, name:'Ghost of Tsushima', img:'static/sources/images/home/jog006.jpg', destaque:'static/sources/images/products/ghost-of-tsushima.jpeg', price:319.90, description:'Como um bom samurai, Ghost of Tsushima chega para anunciar sua posição nesta lista. O game é o exclusivo que vai fechar a geração e, como tal, tende a explorar o máximo do que o console consegue entregar. De fato, a narrativa de Jin Sakai pelo vasto mundo de Tsushima impressiona pela beleza e por aproveitar de mecânicas de exploração de mundo aberto apresentadas em The Legend of Zelda: Breath of The Wild.', exclusive:'exclusivos_Ps', link:'pag_produtos/ghost-of-tsushima.html'},

    {id:13, name:'Uncharted 4', img:'static/sources/images/home/jog007.webp', destaque:'static/sources/images/products/uncharted-4.jpg', price:219.99, description:'A saga de Nathan Drake é, certamente, uma das mais icônicas dos games. O quarto título da série coloca o protagonista em conflito com sua esposa, para ajudar o irmão fugitivo e seguir novamente atrás de relíquias escondidas no melhor estilo Indiana Jones. Contudo, por não trazer tanta inovação assim e manter o sistema linear de fases, o game não foi tão bem recebido como os anteriores. Ainda assim, é uma excelente pedida para os jogadores de PlayStation 4.', exclusive:'exclusivos_Ps', link:'pag_produtos/uncharted-4.html'},

    {id:14, name:'Final Fantasy 7 Remake', img:'static/sources/images/home/jog008.jpg', destaque:'static/sources/images/products/final-fantasy-vii-remake.jpg', price:299.90, description:'Um leitor mais desavisado pode questionar: “valem remakes?”. Pois bem, no caso de Final Fantasy 7 Remake, esta regra pode ser quebrada, pois, simplesmente, o jogo não é só uma recriação do clássico. Quem jogou até o fim, sabe que estamos falando de algo completamente diferente.', exclusive:'exclusivos_Ps', link:'pag_produtos/final-fantasy-7-remake.html'}
]

/*{id:, name:, img:, price:, description:, exclusive:},*/