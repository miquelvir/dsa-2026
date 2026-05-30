# Report

Estructura de Dades 
Report DSA Maps


# 1. Anàlisi de la complexitat temporal d’inicialitzar el mapa d’interseccions en notació Big-O. Incloeu els casos mitjà, millor i pitjor si són diferents:

La complexitat per l'iteració sobre carrers és de O(E), on E és el nombre de segments (arestes). Per cada inserció (graph_add_street), es calcula el hash en O(1) i es recorre el bucket per trobar si ja existeix el node. En el cas mitjà, el bucket és curt (HashMap amb factor de càrrega baix), O(1). En el cas pitjor (totes les claus col·lisionen al mateix bucket), resulta en O(E) per inserció.

Millor cas: O(E) “E és nombre de arestes”

Cas mitjà: O(E)

Pitjor cas: O(E^2)


# 2. Anàlisi de la complexitat temporal de trobar les coordenades d’un carrer o lloc donat el nom en notació Big-O. Incloeu els casos mitjà, millor i pitjor si són diferents:

Les llistes de llocs i cases s'implementen com a llistes simplement enllaçades dinàmicament. La cerca es realitza seqüencialment, recorrent element per element fins a trobar el nom coincident.

Millor cas: O(1) (per a llocs) i (cases/carrers)

Cas mitjà: O(A/2) que és O(A) simplificat (per a llocs) “Aquí, A indica el nombre de llocs encadenats en la llista”

Pitjor cas: O(A) (per a llocs) i O(C) (per a cases/carrers) “Aquí, H indica igualment el nombre de cases encadenades en la llista”
La cerca de Levenshtein (find_closest_place, find_closest_street) recorre tota la llista sempre per trobar el mínim, sempre O(A·L) o O(C·L), on L és la longitud màxima dels noms, és a dir, meno o igual a 256, per tant O(A) o O(H). 

# 3. Anàlisi de la complexitat temporal del vostre algorisme de cerca de camins en notació Big-O. Incloeu els casos mitjà, millor i pitjor si són diferents:


Hi ha un coll d'ampolla a visited_contains: per cada segment processat, es recorre la llista de visitats linealment. De fet, amb la implementació actual de VisitedList com a llista encadenada, el BFS és O(E · V). 

Millor cas: O(1)

Cas mitjà: O(E*V) “E indica arestes, V vèrtexs”

Pitjor cas: O(V*E+V^2)

# 4. Un gràfic que compari la latència per trobar carrers connectats buscant seqüencialment a la llista (lab 4) en comparació amb l’ús del mapa d’interseccions (lab 5), en funció de la mida del mapa:


## 4.1 (a) Determineu experimentalment els resultats mesurant diverses vegades el comportament del vostre programa amb diferents escenaris rellevants a la mateixa màquina. Incloeu les dades en brut a l’informe, a més del gràfic:

La cerca lineal recorre tota la llista de carrers amb complexitat O(E). La cerca per HashMap va directa al bucket, amb complexitat O(1) de mitjana.

TAULA DE DADES EN BRUT: 

 ![Screenshot de Taula en Brut1](https://github.com/user-attachments/assets/0db694b2-74e8-4798-9bc9-29d5ba2c0618)

 GRAFIC DE LES DADES:
 
 ![Screenshot de Gráfico1](https://github.com/user-attachments/assets/061695e6-220f-445c-8f83-dd77c9de69de)

## 4.2 (b) Expliqueu els resultats:

La cerca lineal (street_list_find_connected_linear) recorre la llista sencera de E segments fins trobar els que surten de la intersecció cercada, per tant la latència creix proporcionalment amb el valor de E, és una relació lineal clara. El HashMap (graph_find_connected) calcula el bucket directament amb la funció de hash i accedeix en un temps constant, independentment del nombre de carrers que s'hagin carregat. El HashMap és fins a 167.304 vegades més ràpid per als mapes grans.

El ràtio de millora creix amb n perquè la cerca lineal escala O(n) mentre el HashMap es manté O(1): la diferència entre classes de complexitat s'amplifica a mesura que el mapa creix. Les mesures s'han fet amb 10.000 repeticions per al lineal i 10.000.000 per al HashMap, necessari perquè cada crida al HashMap dura aprox 2 a 3 ns i el que hem utilitzat per a calular el temps no té resolució suficient per a menys repeticions.

# 5. Un gràfic que compari la latència per trobar un camí entre dos punts buscant carrers connectats seqüencialment a la llista en comparació amb l’ús del mapa d’interseccions, en funció de la mida del mapa (però mantenint el mateix origen i destinació).


## 5.1 (a) Determineu experimentalment els resultats mesurant diverses vegades el comportament del vostre programa amb diferents escenaris rellevants a la mateixa màquina. Incloeu les dades en brut a l’informe, a més del gràfic:

TAULA DE DADES EN BRUT:

 ![Screenshot de Taula en Brut2](https://github.com/user-attachments/assets/e6be946d-87d5-4211-891f-423b07b11b50)

 GRAFIC DE LES DADES:
 
 ![Screenshot de Gráfico2](https://github.com/user-attachments/assets/157e7265-45d7-4bab-a930-605140bfbc27)

 ## 5.2 (b) Expliqueu els resultats:

El BFS amb cerca lineal de veïns té complexitat O(E·V) perquè cada crida a street_list_find_connected_linear recorre E carrers. Quan el mapa creix, el nombre de vèrtexs V i d'arestes E creixen alhora, produint un creixement quadràtic molt marcat. El BFS amb HashMap troba els veïns en O(1), reduint el total a O(V²+E) a causa del coll d'ampolla de la VisitedList encadenada es produeix un creixement molt més lent que en el BFS lineal.

La millora del BFS+HashMap (2-11×) és molt menor que la de la pregunta 4 (fins a 167.304×) perquè aquí es mesura tot el BFS, no només find_connected. El coll d'ampolla passa a ser la VisitedList encadenada, que és O(V) per crida tant en el cas lineal com en el HashMap. L'anomalia del 2xl_1 (HashMap = 366ms, més ràpid que xl_1 = 780ms malgrat tenir més segments) s'explica per la topologia real del mapa: l'origen i el destí triat estan topològicament molt a prop al graf real, i el BFS troba el camí explorant molt pocs nodes.


# 6. Un gràfic que compari la latència per trobar un camí entre dos punts buscant carrers connectats seqüencialment a la llista en comparació amb l’ús del mapa d’interseccions, en funció de la distància entre l’origen i la destinació (però utilitzant el mateix mapa):

## 6.1 (a) Determineu experimentalment els resultats mesurant diverses vegades el comportament del vostre programa amb diferents escenaris rellevants a la mateixa màquina. Incloeu les dades en brut a l’informe, a més del gràfic:

TAULA DE DADES EN BRUT: 

![Screenshot de Taula en Brut3](https://github.com/user-attachments/assets/538947f9-e5ca-47df-8ead-be80e79eb4a7)

GRAFIC DE LES DADES:

![Screenshot de Gráfico3](https://github.com/user-attachments/assets/55ec36ca-a0bc-4ff4-9634-0c97d92d79a6)

## 6.2 (b) Expliqueu els resultats:

Quan la distància O-D augmenta, el BFS ha d'explorar més nodes i arestes naturalment. Per a HashMap, la latència creix de forma accelerada amb d perquè el nombre de nodes explorats V(d) augmenta i el cost de la VisitedList encadenada s'acumula: cada crida a visited_contains recorre fins a V(d) nodes, i amb V(d) nodes explorats el cost total és O(V(d)²). Per a cerca lineal: cada consulta de veïns costa O(E), per tant el total és O(V(d)·E + V(d)²), un creixement molt més pronunciat respecte al HashMap.

El ràtio de millora disminueix quan la distància augmenta (7.3× → 2.8×) perquè per a distàncies llargues el cost de la VisitedList domina en ambdues implementacions, reduint l'avantatge relatiu del HashMap.

## 6.3 (c) Ajusteu una corba i justifiqueu-la en funció de la complexitat temporal de la pregunta 3:

La complexitat del BFS (pregunta 3) indica que el cost dominant és O(V²), on V és el nombre de nodes explorats. Com que V creix aproximadament proporcional a la distància d entre origen i destí, l'ajust natural és quadràtic:

T(d) proporcional a d^2, amb un cost de O(v^2) proporcional a d^2.

# 7. Descriviu una millora de l’estructura de dades de visitats en l’algorisme BFS per millorar la latència:

## 7.1 (a) Justifiqueu quina estructura de dades utilitzaríeu / heu utilitzat en lloc d’una llista per millorar el rendiment:

En lloc d'una llista encadenada (VisitedList), caldria fer servir un HashMap/HashSet on la clau és el parell (from_id, to_id) del segment, i el valor és simplement l'existència de la clau. Alternativament, un HashMap simple amb encadenament com el graph actual que tenim.

## 7.2 (b) Descriviu la seva complexitat temporal actual i la complexitat temporal millorada:

La complexitat temporal actual, com ja vam veure a la pregunta 3, és O(V²+E). Amb la millora, visited_contains passa de O(V) a O(1) amortitzat, de manera que el cost total del BFS queda O(V+E), que és l'òptim teòric del BFS sobre llistes d'adjacència.

## 7.3 (c) Descriviu qualsevol compromís o inconvenient del vostre enfocament pel que fa a la latència o l’ús de memòria:

Respecte a la latència, el HashSet millora el cas mitjà de O(V²+E) a O(V+E), una millora molt significativa per als mapes grans. En el cas pitjor (moltes col·lisions de hash), pot degradar-se a O(V²), però és molt improbable si la funció hash funciona bé. 

Respecte a l'ús de la memòria: el HashSet pre-assigna una taula de, per exemple, 40.000 buckets (2× el nombre màxim d'arestes esperades). Per al mapa xl_1: aproximadament 40.000 × 8 bytes (punter) = 320 KB addicionals, enfront dels V × 24 bytes de la llista encadenada. En la pràctica, el HashSet és comparable o millor en memòria si es pre-dimensiona correctament.

L'inconvenient principal és que caldria gestionar correctament el free del HashSet al final del BFS, i implementar una funció hash robusta per a parells de long long. La complexitat d'implementació és major que la llista simple.

# 8. Descriviu una millora de l’algorisme per trobar el segment de carrer donada una latitud i longitud per millorar la seva complexitat temporal / latència:

## 8.1 (a) Justifiqueu quina estructura de dades o algorisme utilitzaríeu / heu utilitzat per millorar la latència:

L'algorisme actual (street_list_find_closest) recorre linealment tots els segments calculant la distància al punt mig amb complexitat O(E). La millora natural és una estructura espacial: un arbre k-d amb latitud i longitud, que organitza els punts mig dels segments en un arbre binari de cerca espacial, permetent cerques de veïns més propers en O(log E) de mitjana.

## 8.2 (b) Descriviu la seva complexitat temporal actual i la complexitat temporal millorada:

Actualment, tenim una complexitat de O(E) sempre. Amb la implementació de la millora, obtindríem una complexitat de O(log E) de mitjana i O(E) en el pitjor cas. El cost de construcció de l'arbre és O(E log E), un cost únic que es paga en carregar el mapa i s'amortitza ràpidament.

## 8.3 (c) Descriviu qualsevol compromís o inconvenient del vostre enfocament pel que fa a la latència o l’ús de memòria:

La implementació d'un arbre K-d és significativament més complexa que la llista. Si els punts estan molt mal distribuïts (concentrats en zones), l'arbre pot degenerar i el rebalanceig és necessari per garantir O(log E) en tots els casos. 

Es requereix que el mapa no canviï dinàmicament (és el cas aquí: es carrega una sola vegada). El cost de construcció O(E log E) és negligible comparat amb el temps total d'execució.









 



  


  



