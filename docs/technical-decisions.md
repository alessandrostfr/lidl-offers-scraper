# Decisiones técnicas

## Selenium frente a requests

Se usa Selenium porque la página de Lidl carga productos de forma dinámica. Descargar el HTML inicial no garantiza tener todos los productos disponibles.

## WebDriver Manager

`webdriver-manager` evita tener que instalar manualmente el driver de Chrome y reduce fricción para ejecutar el proyecto en local.

## Parser tolerante

El parser soporta más de una variante de estructura HTML porque Lidl puede exponer datos en distintos atributos o componentes.

## Debug counters

Los contadores de `parser.py` ayudan a saber cuántos items se han encontrado, cuántos son skeletons, cuántos tienen datos útiles y cuántos se descartan.

## CSV como salida

CSV es suficiente para el alcance del proyecto y permite abrir el resultado en Excel, Google Sheets o procesarlo después con Pandas.
