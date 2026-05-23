# Setup local

## Requisitos

- Python 3.11+
- Google Chrome
- Git
- Windows PowerShell, Terminal o equivalente

## Instalación

```powershell
git clone https://github.com/alessandrostfr/lidl-offers-scraper.git
cd lidl-offers-scraper

python -m venv .venv
.\.venv\Scripts\activate

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Ejecutar

```powershell
python main.py
```

## Configuración rápida

El archivo `config.py` centraliza los valores principales:

```python
BASE_URL = "https://www.lidl.es/q/query/descuentos"
HEADLESS = False
MAX_PAGES = 50
OFFSET_STEP = 48
DEBUG_MODE = True
OUTPUT_FILE = "productos_lidl_descuentos_final.csv"
```

Para ejecutar sin abrir navegador visual:

```python
HEADLESS = True
```

Para hacer una prueba rápida:

```python
MAX_PAGES = 2
DEBUG_MODE = True
```

## Validación mínima

Después de ejecutar, debería aparecer un CSV con las columnas:

```text
id,titulo_producto,marca,precio_actual,porcentaje_descuento,precio_antiguo,url_imagen,url_producto
```
