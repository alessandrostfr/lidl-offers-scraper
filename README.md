# Lidl Offers Scraper

Scraper en Python para extraer productos en descuento desde la sección pública de ofertas de Lidl España y exportarlos a CSV.

El proyecto nació como una práctica de scraping real con una web dinámica: la página carga productos mediante JavaScript, usa grid virtualizado y no siempre expone todos los datos en el HTML de forma directa. Por eso el scraper combina Selenium, scroll incremental, lectura de atributos embebidos y una capa de parsing tolerante a cambios en el marcado.

> Repositorio de aprendizaje/proyecto técnico. No está afiliado a Lidl. El uso debe respetar las condiciones del sitio web y ejecutarse de forma responsable.

---

## Qué hace

El scraper recorre la página de descuentos de Lidl, navega por offsets y va haciendo scroll dentro de cada bloque para capturar productos que aparecen de forma progresiva.

Por cada producto intenta extraer:

- identificador interno generado por el scraper;
- título del producto;
- marca;
- precio actual;
- porcentaje de descuento;
- precio anterior calculado cuando hay datos suficientes;
- URL de imagen;
- URL del producto.

El resultado se guarda en un CSV listo para revisar, filtrar o analizar.

---

## Por qué es interesante

Aunque el alcance es pequeño, el proyecto toca problemas reales de scraping:

- páginas renderizadas por JavaScript;
- carga progresiva de productos;
- scroll virtual;
- elementos repetidos al navegar;
- datos embebidos en atributos HTML;
- normalización de precios;
- deduplicación;
- exportación estructurada.

No es solo un `requests + BeautifulSoup`, sino una extracción pensada para una web donde los productos no aparecen todos de golpe.

---

## Stack

- Python
- Selenium
- WebDriver Manager
- Pandas
- Chrome / Chromium

---

## Estructura principal

```text
lidl-offers-scraper/
├── main.py              # Orquestación del scraping completo
├── scraper.py           # Selenium: navegador, cookies, scroll y búsqueda de items
├── parser.py            # Extracción y normalización de datos de producto
├── save_data.py         # Exportación a CSV
├── utils.py             # Limpieza de texto, precios y JSON embebido
├── config.py            # Configuración del scraper
├── requirements.txt
└── docs/
```

---

## Cómo funciona el flujo

1. `main.py` crea el navegador y controla el recorrido por offsets.
2. `scraper.py` abre la página, acepta cookies si aparecen, espera la sección de resultados y realiza scroll incremental.
3. `parser.py` procesa los elementos visibles, ignora skeletons, lee datos desde atributos HTML y evita duplicados.
4. `save_data.py` genera el CSV final.
5. El proceso termina cuando alcanza el límite de páginas configurado o deja de encontrar productos nuevos.

---

## Instalación

Requisitos:

- Python 3.11 o superior recomendado.
- Google Chrome instalado.

```powershell
git clone https://github.com/alessandrostfr/lidl-offers-scraper.git
cd lidl-offers-scraper

python -m venv .venv
.\.venv\Scripts\activate

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

---

## Ejecución

```powershell
python main.py
```

El archivo de salida por defecto se define en `config.py`:

```python
OUTPUT_FILE = "productos_lidl_descuentos_final.csv"
```

También desde `config.py` se pueden ajustar:

- URL base;
- modo headless;
- número máximo de offsets;
- tamaño del scroll;
- esperas;
- modo debug.

---

## Ejemplo de salida

Columnas principales del CSV:

```text
id,titulo_producto,marca,precio_actual,porcentaje_descuento,precio_antiguo,url_imagen,url_producto
```

Ejemplo ficticio:

```csv
id,titulo_producto,marca,precio_actual,porcentaje_descuento,precio_antiguo,url_imagen,url_producto
1,Taladro inalámbrico 20V,Parkside,39.99,20,49.99,https://...,https://...
```

---

## Limitaciones conocidas

Este proyecto depende de la estructura pública de la web de Lidl. Si la web cambia selectores, atributos o estrategia de carga, será necesario ajustar el parser.

Limitaciones actuales:

- no usa una API oficial;
- depende de Chrome/Selenium;
- puede fallar si aparece protección anti-bot o cambios en cookies;
- no está pensado para scraping masivo;
- el cálculo de precio anterior solo es fiable cuando el descuento y precio actual son coherentes.

Más detalles en [`docs/limitations.md`](docs/limitations.md).

---

## Estado del proyecto

El scraper funciona como proyecto técnico y demuestra una extracción real con Selenium, parsing y CSV. Antes de considerarlo producción habría que añadir:

- tests unitarios del parser;
- logs estructurados;
- CLI con argumentos;
- configuración por `.env`;
- control más fino de errores;
- ejemplos de salida sanitizados;
- ejecución programada opcional.

---

## Documentación

- [`docs/architecture.md`](docs/architecture.md)
- [`docs/setup.md`](docs/setup.md)
- [`docs/workflow.md`](docs/workflow.md)
- [`docs/data-output.md`](docs/data-output.md)
- [`docs/technical-decisions.md`](docs/technical-decisions.md)
- [`docs/limitations.md`](docs/limitations.md)
- [`docs/repository-cleanup.md`](docs/repository-cleanup.md)
- [`docs/screenshots.md`](docs/screenshots.md)

---

## Autor

Proyecto desarrollado por [Alessandro Staiano Fernández](https://github.com/alessandrostfr) como parte de su portfolio técnico de desarrollo web, automatización y scraping.
