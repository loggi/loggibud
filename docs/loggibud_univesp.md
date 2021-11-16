Desafio LoggiBUD (Univesp)
==========================

*This page contains a undergraduate level introduction to optimization problems and LoggiBUD.
It was developed in colaboration with The Virtual University of the State of São Paulo.
All the content is in Portuguese, but we welcome contributions to translate it to other languages.*

# Pré-requisitos Do Curso
Entery Level Knowledage of python 
Familarty with colab 


# Conteúdo do curso

## Boas Vindas

Lançamento do desafio e boas vindas ao curso. Transmitido como 
[live no Youtube](https://www.youtube.com/watch?v=9FsW0dGlMq0).

## Aula 1: Introdução ao Colab e ao LoggiBUD

Nesta aula, apresentamos uma visão introdutória da ferramenta Google Colab, do repositório
LoggiBUD, e do nosso desafio principal. O mais importante desta aula é que o aluno
familiarize-se e sinta-se confortável com o Colab, e que tenha uma primeira impressão do
problema a ser tratado. Não é necessário um entendimento profundo do repositório ou de
estratégias de otimização. Nas aulas a seguir investigaremos gradativamente estes conceitos.

* [Videoaula](https://www.youtube.com/watch?v=Yqt9BjJX5Zg)
* [Tarefa (Colab)](https://colab.research.google.com/drive/1hAcU97GX5M8azYlvMfF4NivL0cnabERY)
* [Soluções (Colab)](https://colab.research.google.com/drive/1Y71edxRvBPjTmYeFISU-QyfQwDtYtRaP)

### Material Suplementar

O repositório LoggiBUD, bem como os programas a serem desenvolvidos neste curso são implementados
na linguagem Python (versão 3). Se você não está familiarizado com o Python, sugerimos que veja as
aulas da disciplina COM110 “Algoritmos e Programação de Computadores” da Univesp, disponível [no
Youtube](https://www.youtube.com/watch?v=sBZUFk243n4).

## Aula 2: Introdução ao TSP

Nesta aula, estudamos um problema bastante explorado na comunidade acadêmica: o Problema do
Caixeiro Viajante (Traveling Salesperson Problem - TSP). Este é um tópico simples de entender mas
em geral complicado de ser resolvido.

Aqui são apresentadas duas estratégias para tratar casos simples: um algoritmo baseado em Força
Bruta, e outro em um solver comercial, o OR-Tools.

O TSP é um assunto completo por si só, mas para nossos propósitos ele também é útil como uma introdução
ao problema principal do curso.

* [Videoaula](https://www.youtube.com/watch?v=_kZHaidxFpo)
* [Tarefa (Colab)](https://colab.research.google.com/drive/1wwJfmbIkrShzseUW5fWCK63CP35hN0Xo)
* [Soluções (Colab)](https://colab.research.google.com/drive/17xFnT5N9rlW7hixmuMPYwTuylliJm24g)

### Material Suplementar

Biggs, Norman. "The traveling salesman problem a guided tour of combinatorial optimization." (1986): 
514-515. - Este livro possui assuntos interessantes, tratando desde a história do TSP até diversas
estratégias para resolvê-lo.

[Definição do TSP na Wikipedia](https://en.wikipedia.org/wiki/Travelling_salesman_problem)

[Documentação do OR-Tools.](https://developers.google.com/optimization)

## Aula 3: Introdução ao VRP

Uma vez entendido o TSP, introduzimos o que pode ser entendido como a sua generalização: o Problema
de Roteamento de Veículos (Vehicle Routing Problem, VRP). Como primeira abordagem, tratamos da sua
versão estática, em que todas as entregas já são conhecidas a priori. 

Aqui nós adaptamos o algoritmo com o solver comercial da aula anterior para lidar com o VRP, e
apresentamos estratégias para verificar a factibilidade das soluções.

* [Videoaula](https://www.youtube.com/watch?v=vQBAI4LrAok)
* [Tarefa (Colab)](https://colab.research.google.com/drive/1E-JOjQ-WMMOqaCfIOV9U00ACFS8NmfHb)
* [Soluções (Colab)](https://colab.research.google.com/drive/1bRatZ6VfSqjYDqUoKPZKXOMvXrr5bqPj)

### Material Suplementar

[Definição na Wikipedia](https://en.wikipedia.org/wiki/Vehicle_routing_problem)

Toth, Paolo, and Daniele Vigo, eds. The vehicle routing problem. Society for Industrial and Applied
Mathematics, 2002. Para o aluno interessado na modelagem matemática do VRP e em outros algoritmos.


## Aula 4: VRP estático no LoggiBUD

Nas duas aulas anteriores tratamos de dois problemas clássicos da literatura (o TSP e o VRP). Estes
problemas possuem diversas aplicações práticas, porém nós focamos em instâncias pequenas e/ou artificiais,
com pouca representatividade na indústria.

Sendo assim, nesta aula nós apresentamos novamente o repositório do LoggiBUD e suas instâncias mais
realistas. Ao final, adaptamos nosso algoritmo de antes para ser capaz de resolvê-las, mas ainda tratando
de casos estáticos.

* [Videoaula](https://www.youtube.com/watch?v=o5MnFkblTPw)
* [Live](https://www.youtube.com/watch?v=b6qSBT7YA7o)
* [Tarefa (Colab)](https://colab.research.google.com/drive/1i_Ow384-wco_Y6MdRRmFr0THBZMD6RFI)
* [Soluções (Colab)](https://colab.research.google.com/drive/1RkEGIevdCbqa35bXIGuwBbQuJxbyfFyc)


## Aula 5: VRP dinâmico no LoggiBUD - Parte 1

Introduzir o LoggiBUD foi um passo importante na nossa jornada para resolver problemas mais reais.
Contudo, a assumpção de um problema estático significa que todas as entregas são conhecidas desde
o início, e isso deixa de ser uma realidade em empresas como a Loggi que opera com centenas de
milhares de pedidos por dia e precisam respeitar restrições operacionais, como espaço disponível
nos galpões de agências, pedidos com datas específicas etc.

Portanto, precisamos de uma abordagem que seja capaz de rotear um pedido tão logo ele se torne
disponível. Nesta aula iniciamos o tratamento do VRP dinâmico, que é o problema principal desse curso.
Este assunto também é muito estudado, mas encontra-se num estado menos maduro, dispondo de menos
solvers comerciais como no caso dinâmico.

Iniciamos a aula revisando o algoritmo ingênuo apresentado na primeira aula com um pouco mais de
detalhes, e em seguida propomos um aperfeiçoamento com o TSP. Concluímos com um exemplo de
algoritmo menos ingênuo e um pouco mais elaborado para obter melhores soluções.

* [Videoaula](https://www.youtube.com/watch?v=OaL0WEB-gog)
* [Tarefa (Colab)](https://colab.research.google.com/drive/1el7G9M4lWuz6IIhQ-m09GZIpCaQDrvfP)
* [Soluções (Colab)](https://colab.research.google.com/drive/1hAO17Vz9RE0qFgMJL3OEYNeXiCHFa_lO)


## Aula 6: VRP dinâmico no LoggiBUD - Parte 2

Nesta aula final continuamos o tema de antes, em que não possuímos informação completa das entregas
de um dia. A diferença é que a informação de dias anteriores está à nossa disposição. Assim,
apresentamos um algoritmo que faz uso desta informação histórica para construir um modelo capaz
de rotear um pedido assim que ele se torna disponível.

Com isso, temos todo o conhecimento necessário para resolver o desafio final. Agora é a vez dos
alunos elaborarem um algoritmo capaz de resolver este problema dinâmico.


* [Videoaula](https://www.youtube.com/watch?v=-hbAGOoIqLs)
* [Tarefa (Colab)](https://colab.research.google.com/drive/1pYi55RnagpT7KTTjCp_IPRVQuhjuu5iF)
* [Soluções (Colab)](https://colab.research.google.com/drive/1BeTZ1rk6kWhHbS71v90UJwmoQwVdqIcB)

## Encerramento e premiação

Encerramento do desafio e premiação dos melhores trabalhos. Transmitido como 
[live no Youtube](https://www.youtube.com/watch?v=k5JeRGmHn_Q).
