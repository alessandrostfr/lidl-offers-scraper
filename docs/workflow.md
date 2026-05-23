# Flujo de trabajo

## 1. Abrir offset

El scraper empieza en la URL base de descuentos. Después genera URLs con offset para recorrer bloques de productos.

## 2. Cargar página y aceptar cookies

Selenium espera a que cargue el `body`, intenta aceptar el banner de cookies y espera a encontrar la sección de resultados.

## 3. Scroll incremental

La página no muestra todos los productos de golpe. Por eso se hacen desplazamientos controlados y se vuelven a leer los items visibles.

## 4. Parsear productos

Cada item se pasa al parser. El parser intenta:

- detectar el nodo real del producto;
- ignorar skeletons;
- leer datos embebidos;
- extraer texto visible como fallback;
- normalizar precios;
- calcular descuento/precio antiguo cuando es posible.

## 5. Deduplicar

Se mantiene un conjunto de claves vistas para no repetir productos al hacer scroll o cambiar de offset.

## 6. Guardar CSV

Al final se asignan IDs consecutivos y se guarda el resultado en CSV con `utf-8-sig`, cómodo para abrir en Excel.
