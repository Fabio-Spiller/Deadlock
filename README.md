# TDE 3: Programação Concorrente (Filósofos, Semáforos e Deadlock)

Fabio Spiller


Linguagem escolhida: Python 3.10

Vídeo no YouTube: https://www.youtube.com/watch?v=qvHlPGtESf4

## Como executar

Não precisa instalar nada, só ter o Python 3.10 ou mais novo. Dentro da pasta do projeto, rode:

```bash
# Parte 1: Jantar dos Filósofos
python filosofos/ingenuo.py
python filosofos/corrigido.py

# Parte 2: Contador com e sem semáforo
python semaforo/semsemaforo.py
python semaforo/comsemaforo.py

# Parte 3: Deadlock
python deadlock/deadlock.py
python deadlock/deadcorrigido.py
```

## Parte 1: Jantar dos Filósofos

### Como funciona o problema

São cinco filósofos sentados numa mesa redonda. Cada um passa o tempo pensando, depois fica com fome e tenta comer. Entre cada dois filósofos existe um garfo, então são cinco garfos no total. Pra comer, o filósofo precisa pegar os dois garfos que estão do lado dele, o da esquerda e o da direita. Como cada garfo é dividido com o vizinho, dois filósofos vizinhos nunca conseguem comer ao mesmo tempo.

No código, cada filósofo é uma thread e cada garfo é um Lock.

### Por que a versão ingênua trava (filosofos/ingenuo.py)

Se todos os filosofos querem comer ao mesmo tempo, e precisa de dois garfos pra comer, não tem garfo o suficiente pra todo mundo comer.

Como todo mundo segura um garfo na esquerda ao mesmo tempo, e só vai soltar depois de pegar o garfo na mão direita e comer, todo mundo fica esperando o vizinho soltar um grafo o que nunca acontece.

aqui tem quatro condições de Coffman estão presentes ao mesmo tempo:

- Exclusão mútua: um garfo só pode estar na mão de um filósofo por vez.
- Manter e esperar: o filósofo segura o garfo da esquerda enquanto espera o da direita.
- Não preempção: ninguém pode tirar o garfo da mão de outro filósofo, só quem está com ele pode soltar.
- Espera circular: o filósofo 0 espera o 1, que espera o 2, e assim por diante até o 4, que espera o 0.

### A solução: ordem dos garfos (filosofos/corrigido.py)

A ideia é numerar os garfos e combinar uma regra: todo filósofo pega sempre primeiro o garfo de número menor e depois o de número maior.

```python
left  = min(p, (p + 1) % 5)
right = max(p, (p + 1) % 5)
```

Pros filósofos 0, 1, 2 e 3 continuam na mesma, eles já pegavam o menor primeiro. A diferença está no filósofo 4. Os garfos dele são o 4 e o 0, então agora ele tenta pegar o garfo 0 antes do 4.

Com isso, o filósofo 4 e o filósofo 0 passam a disputar o mesmo garfo primeiro e ai quem perde, fica sem nenhum garfo, enquanto o outro fica com 2 come e libera os garfos.

A condição de Coffman que eu quebro aqui é a espera circular.

### Pseudocódigo

```
N = 5 filósofos
Garfos numerados de 0 a 4 (o garfo i fica entre o filósofo i e o filósofo i+1)

Para cada filósofo p:
  primeiro = o menor entre p e (p+1) mod 5
  segundo  = o maior entre p e (p+1) mod 5

  Repetir para sempre:
    pensar
    ficar com fome
    pegar o garfo "primeiro"  (espera se estiver ocupado)
    pegar o garfo "segundo"   (espera se estiver ocupado)
    comer
    soltar o garfo "segundo"
    soltar o garfo "primeiro"
```

### Passo a passo do filósofo

1. Pensa.
2. Logo fica com fome.
3. Tenta pegar o garfo de número menor. Se estiver ocupado, espera.
4. Tenta pegar o garfo de número maior. Se estiver ocupado, espera.
5. Come.
6. Solta o garfo maior e depois o menor.
7. Volta a pensar e repete tudo.

### Todo mundo come? (progresso e justiça)

Se tiver tempo suficiente sim.

Sobre justiça: depois de comer, o filósofo solta os dois garfos e ai mesmo que ele pense e fique com fome de novo os garfos vão estar ocupados e ele vai ter que esperar


### Logs de execução

Versão ingênua (travou):

```
Filosofo 0 pensando
Filosofo 1 pensando
Filosofo 2 pensando
Filosofo 3 pensando
Filosofo 4 pensando
Filosofo 2 com fome
Filosofo 2 pegou o garfo 2
Filosofo 4 com fome
Filosofo 4 pegou o garfo 4
Filosofo 3 com fome
Filosofo 1 com fome
Filosofo 0 com fome
Filosofo 1 pegou o garfo 1
Filosofo 0 pegou o garfo 0
Filosofo 3 pegou o garfo 3
FIM
Vezes que cada um comeu: [0, 0, 0, 0, 0]
```

Versão corrigida:

```
Filosofo 1 pensando
Filosofo 2 pensando
Filosofo 3 pensando
Filosofo 4 pensando
Filosofo 4 com fome
Filosofo 3 com fome
Filosofo 1 com fome
Filosofo 4 pegou o garfo 0
Filosofo 3 pegou o garfo 3
Filosofo 1 pegou o garfo 1
Filosofo 0 com fome
Filosofo 2 com fome
Filosofo 2 pegou o garfo 2
Filosofo 3 pegou o garfo 4
Filosofo 3 comendo
Filosofo 3 pensando
Filosofo 4 pegou o garfo 4
Filosofo 2 pegou o garfo 3
Filosofo 4 comendo
Filosofo 2 comendo
Filosofo 3 com fome
Filosofo 4 pensando
Filosofo 0 pegou o garfo 0
Filosofo 1 pegou o garfo 2
Filosofo 2 pensando
Filosofo 3 pegou o garfo 3
Filosofo 1 comendo
Filosofo 3 pegou o garfo 4
Filosofo 4 com fome
Filosofo 2 com fome
Filosofo 3 comendo
Filosofo 1 pensando
Filosofo 2 pegou o garfo 2
Filosofo 0 pegou o garfo 1
Filosofo 3 pensando
Filosofo 0 comendo
Filosofo 2 pegou o garfo 3
Filosofo 1 com fome
Filosofo 2 comendo
Filosofo 3 com fome
Filosofo 0 pensando
Filosofo 4 pegou o garfo 0
Filosofo 1 pegou o garfo 1
Filosofo 2 pensando
Filosofo 1 pegou o garfo 2
Filosofo 4 pegou o garfo 4
Filosofo 3 pegou o garfo 3
Filosofo 4 comendo
Filosofo 0 com fome
Filosofo 1 comendo
Filosofo 2 com fome
Filosofo 1 pensando
Filosofo 4 pensando
Filosofo 0 pegou o garfo 0
Filosofo 3 pegou o garfo 4
Filosofo 2 pegou o garfo 2
FIM
Vezes que cada um comeu: [1, 2, 2, 2, 2]
```


## Parte 2: Threads e semáforos (contador)

### O experimento

Criei 8 threads e cada uma soma 1 num contador compartilhado 200.000 vezes. No final o contador deveria valer 8 x 200.000 = 1.600.000.

duas versões:

- semsemaforo.py: as threads mexem no contador sem nenhum controle.
- comsemaforo.py: antes de mexer no contador, cada thread precisa pegar a permissão de um semáforo que só tem uma permissão. 


### Pseudocódigo

```
count = 0
sem = Semaforo com 1 permissão

tarefa():
  repetir M vezes:
    Versão 1 (sem semáforo):
      valor = count
      pequeno trabalho
      count = valor + 1

    Versão 2 (com semáforo):
      pegar a permissão do semáforo
      valor = count
      pequeno trabalho
      count = valor + 1
      devolver a permissão (sempre, mesmo se der erro)

programa principal:
  iniciar T threads executando tarefa()
  esperar todas terminarem
  mostrar o valor esperado, o valor obtido e o tempo
```

### Resultados

Valor esperado em todas as execuções: 1.600.000

Sem semáforo:
```
esperado = 1600000 obtido = 1218970 tempo = 0.38 segundos
```

Com semáforo:
```
esperado = 1600000 obtido = 1600000 tempo = 2.75 segundos
```

### Por que a versão sem semáforo perde incrementos

Porque precisa ler, somar o valor e depois escrever o novo valor, e no meio do caminho os processos podem se atropelar, por exemplo: 

```
Thread 1 lê o contador: 100
Thread 2 lê o contador: 100
Thread 2 grava 101
Thread 1 grava 101
```

Um dos incrementos se perdeu. Isso acontece muitas vezes durante a execução, por isso o resultado final fica abaixo de 1.600.000.

### Por que a versão com semáforo dá certo

O semáforo com uma permissão funciona como uma chave única. Só quem está com a chave pode mexer no contador, e as outras threads são obrigadas a esperar pra não atropelar a escrita da atual.

### Desempenho

Uma é mais lenta, porque sempre precisa esperar a thread que chegou primeiro e isso forma fila, porém o numero chega correto.
Enquanto a outra só escreve de qualquer jeito mesmo se tiver atropelando, mas é muito mais rapida.


### Justiça

Não tem uma justiça de fato, quem pegar primeiro quando a thread libera.

### Visibilidade

Quando uma thread grava um valor, as outras precisam enxergar esse valor atualizado. No Java existe  happens-before: tudo que uma thread fez antes de devolver a permissão do semáforo fica visível pra próxima thread que pegar a permissão. No Python não existe uma regra formal desse jeito, mas o Lock e o Semaphore funcionam na prática como uma barreira: o que foi gravado antes de liberar fica visível pra quem pegar depois.


## Parte 3: Deadlock

### O cenário (deadlock/deadlock.py)

São duas threads e dois locks, A e B:

- A thread 1 pega o lock A, espera e tenta pegar o lock B.
- A thread 2 pega o lock B, espera e tenta pegar o lock A.

basicamente as threads tentam pegar o lock uma da outra, mas a thread só libera quando tem os dois, então fica infinitamente um esperando o outro.

Depois de 3 segundos o programa mostra quais threads ainda estão vivas. As duas continuam lá.

### Condições de Coffman que apareceram

- Exclusão mútua: cada lock só pode estar com uma thread por vez.
- Manter e esperar: a thread 1 segura o A enquanto espera o B, e a thread 2 segura o B enquanto espera o A.
- Não preempção: nenhuma thread consegue tirar o lock da outra, e elas esperam pra sempre.
- Espera circular: a thread 1 espera a 2, e a thread 2 espera a 1.

### Prova do travamento

```
T1 esperando LOCK_A
T1 pegou LOCK_A
T2 esperando LOCK_B
T2 pegou LOCK_B
T1 esperando LOCK_B
T2 esperando LOCK_A
depois de 3 seg, ainda vivas:
 - MainThread
 - T1
 - T2
```

### A correção (deadlock/deadcorrigido.py)

É simples: todas as threads pegam sempre o lock A primeiro e depois o B. Na hora de soltar, soltam o B e depois o A.

```
Thread 1 e Thread 2:
  pegar o lock A
  pegar o lock B
  fazer o trabalho
  soltar o lock B
  soltar o lock A
```

Agora, se a thread 2 não conseguir o lock A, ela fica esperando sem segurar nada e permite a 1 terminar o seu serviço e liberar.

A condição de Coffman quebrada aqui também é a espera circular. Como todo mundo segue a mesma ordem, não tem como uma thread esperar a outra e a outra esperar de volta.

### Saída da versão corrigida

```
T1 esperando LOCK_A
T1 pegou LOCK_A
T2 esperando LOCK_A
T1 esperando LOCK_B
T1 pegou LOCK_B
T1 concluiu
T2 pegou LOCK_A
T2 esperando LOCK_B
T2 pegou LOCK_B
T2 concluiu
3 seg, ta vivo ainda:
 - MainThread
```

### Outras formas de lidar com deadlock

Existem quatro jeitos clássicos de lidar com deadlock:

- Ignorar: assumir que é raro e tentar resetar o processo
- Detectar e recuperar: deixar acontecer e ver quem trava quem e parar um dos processos
- Prevenir: quebrar uma das condições de Coffman antes de acontecer, que foi o que eu fiz colocando uma ordem fixa pros locks
- Evitar: antes de entregar um recurso, ver se isso pode travar alguém e só entregar se for seguro, tipo o algoritmo do Banqueiro


## Conclusão

O controle mal organizado de algum recurso pode levar ao travamento, pelo simples fato de um processo precisar usar algo que ta travado em outro processo, ou um processo simplesmente atropela outros porque não tem mecanismos que garantam a confiabilidade.
