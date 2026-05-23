# Arquitectura

El proyecto está dividido en módulos simples para mantener separado el control del navegador, el parsing y la exportación.

```text
config.py
   ↓
main.py
   ↓
scraper.py  → Selenium / Chrome / scroll / offsets
   ↓
parser.py   → extracción, limpieza, deduplicación
   ↓
save_data.py → CSV final
```

## Módulos

### `main.py`

Orquesta el proceso completo:

- crea el driver;
- recorre offsets;
- mantiene el conjunto de productos ya vistos;
- llama al parser;
- guarda el CSV final.

### `scraper.py`

Agrupa la lógica dependiente de Selenium:

- crear el navegador;
- construir URLs con offset;
- abrir páginas;
- aceptar cookies;
- esperar la sección de resultados;
- localizar productos;
- controlar scroll incremental.

### `parser.py`

Es la parte más importante del proyecto. Intenta extraer datos desde distintas variantes de marcado detectadas en Lidl:

- elementos con `data-grid-data`;
- elementos con `data-gridbox-impression`;
- selectores fallback;
- limpieza de skeletons;
- contadores de debug para entender dónde se pierden productos.

### `utils.py`

Funciones auxiliares:

- limpiar texto;
- leer atributos de Selenium de forma segura;
- parsear JSON embebido;
- convertir precios;
- extraer descuentos;
- calcular precio antiguo.

### `save_data.py`

Convierte la lista final de productos en un DataFrame de Pandas y lo exporta a CSV con orden de columnas estable.

## Decisión principal

Se usa Selenium porque la página de Lidl es dinámica y no basta con descargar HTML estático para obtener todos los productos visibles.
