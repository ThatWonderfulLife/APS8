# APS8

![LogoUnip](https://unip.br/assets/img/logo/logo-unip.svg)
### APS Ultimo semestre Ciências da Computação UNIP 2023

#### Descrição

Utilizando um dos datasets do [site fornecido](https://www.kaggle.com/datasets) foi feita uma API para consulta de jogos, contendo os dados variados e de importancia para a analise dos mesmos, aplicando um retorno em arquivo .json.
[Link do dataset](https://www.kaggle.com/datasets/rush4ratio/video-game-sales-with-ratings)

##### Integrantes do Grupo
|**Nome**|**RA**|**Turma**|
|---|---|---|
|Pedro Marques Arena|N618AE4|CC8Q18|
|Mauricio Vitaliano Dolacio|N604AH8|CC8P18|
|João Vitor Fernandes de Lima|F314618|CC8P18|
|João Vitor Mine Nascimento|N5816B9|CC8Q18|
|Bruna Sabbato da Silva|F208850|CC8P18|
|Débora Inacio Santos|F250083|CCP18|

#### Documentação / Use Cases

**ATENÇÃO: OS MÉTODOS REQUEREM AUTENTICAÇÃO PARA ACESSO E O MÉTODO POST REQUER ESPECIFICAÇÃO DO TIPO DE CONTEUDO PARA "type/json"**

1. GET
- "/getAllGames"
- "/getAllGamesByConsole/< console >"
- "/getAllByYear/< year >"
- "/getAllByGenre/< genre >"
- "/getAllByPublisher/< publisher > "
- "/getFromUserScore"
- "/getFromCriticScore"
- "/getFromGlobalSales"
- "/getFromDeveloper/< developer >"
- "/getBestFromDeveloper/< developer >"
1. POST
- "/postNewEntry" -> .json file

3. DELETE
- 

