# ==========================================================
# config.py
# ==========================================================
# Configuración general del scraper de Lidl.
# ==========================================================

# URL base de descuentos
BASE_URL = "https://www.lidl.es/q/query/descuentos"

# Espera máxima de Selenium
WAIT_TIME = 15

# Archivo CSV final
OUTPUT_FILE = "productos_lidl_descuentos_final.csv"

# Mostrar navegador o no
HEADLESS = False

# Lidl parece trabajar en bloques de 48
OFFSET_STEP = 48

# Número máximo de offsets a recorrer por seguridad
MAX_PAGES = 50

# Scroll incremental dentro de cada offset
SCROLL_PIXELS = 700
SCROLL_PAUSE = 1.2
MAX_SCROLLS_PER_OFFSET = 80
MAX_STAGNANT_SCROLLS = 8

# Depuración
DEBUG_MODE = True