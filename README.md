# Compu-pararela-tarea 1

Lo primero que hay que empezar mencionando sobre este código es se implmentaron los patrones clásicos de glider como toad. Estos patrones, la forma o estruc
tura de ellos están en unos archivos TXT del mismo nombre en esta carpeta y son necesarios para que en el código cuando se decida si hacerlo de forma random
o con patrón, si se selecciona lo segundo se puedan cargar al código y poder jugarlos.

Ya despúes se inicia el código, se hace la calse del juego de la vida, y luego se proceden con las funciones que podrán poner a correr el juego,
primero se muestra el menú general, luego se crea la opción del tablero aleatorio, en esta función se le da la opción al usuario de elegir un número
random de células vivas para empezar el juego. UNa vez creado en el primer caso el tablero aleatorio, se puede jugar con las funciones de Step y ejectuarSimulacion.
En esta función, mediante un kernel similar al kernel de una convulución, va contando los 8 vecinos que tendría una solo célula para ver si están vivas o no,
Como se mencionó inicialmente, hay opciones para la carga de los patrones clásicos de Toad y Glider, los cuales son TXT con la forma ya guardada,
si alguno de estos patrones es seleccionado el código no pide cantidad de células vivas, solo de cargalo y luego ejecutarlo en la siguiente opción.
Ya despúes en ejecutar simulación, dependiendo de la opción si se seleccionó de forma random o con patrón, se le preguntará al usuario que cuantas genera
ciones desea jugar como máximo, se empieza en 1 y termina en las seleccionadas por el jugador, ya despúes el resultado que se grafica al final de la
simulación es como fue quedando el tablero a lo largo de las generaciones, la distribución y cnatidad de células vivas.
Finalmente hay un función que lo que hace es mostrar las estadísticas de la simualación en diferentes tamaños de tablero, que van desde 32 a 512 junto con
la cantidad de células vivas para al ejecución, la idea es usar una misma cantidad de células vivas para comparar los tiempos de diferentes tamaños,se ad
juntan unos ejemplos de resultados de las simulaciones y luego las estadísticas:
La imagen ejemplo 1 tiene 25 células vivas, con 25 generaciones en un tmañano 64x64
Ejemplo 2 fue con el patrón Toad, ese fue el resultado con 45 generaciones.

De último se evaluó el rendimiento con los tamaños como el ejemplo 1, con 25 células vivas y estos fueron los resultados:
32x32 - Tiempo promedio por paso: 0.000351 segundos
64x64 - Tiempo promedio por paso: 0.000421 segundos
128x128 - Tiempo promedio por paso: 0.000470 segundos
256x256 - Tiempo promedio por paso: 0.000884 segundos
512x512 - Tiempo promedio por paso: 0.012537 segundos

EL resultado gráficamente se observa en la imagen ejemplo3.
Con estos resultados, podemos ver que el tiempo va aumentando de duración según el tamaño del
tablero, por eso en 512 es dura mucho más que un tamaño menor como 32x32 porque toma en cuenta
todo el tablero, no solo las células vivas.
Y con la imagen podemos observar como el tiempo va incrementando de pasos según el tamaño del ta
blero seleccionado, a pura y simple vista, yo creo que el cálculo de su O grande sería un O(n2).

## Tarea 2


