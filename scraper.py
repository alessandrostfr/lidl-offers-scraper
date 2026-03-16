# ==========================================================
# scraper.py
# ==========================================================
# Controla Selenium:
# - crear navegador
# - abrir páginas por offset
# - aceptar cookies
# - esperar resultados
# - hacer scroll incremental
# - encontrar ítems del grid reales
# ==========================================================

import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager

from config import (
    BASE_URL,
    WAIT_TIME,
    HEADLESS,
    SCROLL_PIXELS,
    SCROLL_PAUSE,
    DEBUG_MODE,
)


def create_driver():
    """
    Crea el navegador Chrome configurado para Selenium.
    """
    options = Options()

    if HEADLESS:
        options.add_argument("--headless=new")

    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    return driver


def build_offset_url(offset):
    """
    Construye la URL para un offset concreto.
    """
    if offset == 0:
        return BASE_URL

    return f"{BASE_URL}?offset={offset}"


def open_page(driver, url):
    """
    Abre una URL en el navegador.
    """
    driver.get(url)


def wait_initial_page_load(driver):
    """
    Espera a que cargue el body.
    """
    WebDriverWait(driver, WAIT_TIME).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )


def accept_cookies(driver):
    """
    Intenta aceptar el banner de cookies si aparece.
    """
    possible_xpaths = [
        "//button[contains(., 'Aceptar')]",
        "//button[contains(., 'Aceptar todas')]",
        "//button[contains(., 'Acepto')]",
        "//button[contains(., 'Permitir')]",
        "//button[contains(., 'Accept')]",
    ]

    for xpath in possible_xpaths:
        try:
            button = WebDriverWait(driver, 4).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            button.click()
            time.sleep(1)
            return
        except Exception:
            continue


def wait_results_section(driver):
    """
    Espera a que aparezca la sección de resultados.
    """
    selectors = [
        "section.s-page__results",
        "[data-testselector='s-product-grid__list']",
        ".s-product-grid",
    ]

    for selector in selectors:
        try:
            WebDriverWait(driver, WAIT_TIME).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
            return
        except Exception:
            continue

    raise Exception("No se encontró la sección de resultados.")


def find_grid_items(driver):
    """
    Busca los wrappers reales del grid.

    Estrategia:
    - usar exclusivamente los nodos wrapper 'grid-item-*'
    - así recorremos todos los elementos del grid
    - luego el parser decidirá si dentro hay producto real o skeleton

    Devuelve:
    - lista de elementos Selenium
    """
    selector = "div[id^='grid-item-']"
    items = driver.find_elements(By.CSS_SELECTOR, selector)

    if DEBUG_MODE:
        print(f"[DEBUG] Selector '{selector}' encontró {len(items)} nodos.")

    return items


def scroll_to_top(driver):
    """
    Vuelve arriba del todo.
    """
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(1)


def scroll_down_once(driver, current_position):
    """
    Hace un scroll hacia abajo una sola vez.
    """
    new_position = current_position + SCROLL_PIXELS
    driver.execute_script("window.scrollTo(0, arguments[0]);", new_position)
    time.sleep(SCROLL_PAUSE)
    return new_position


def get_scroll_height(driver):
    """
    Devuelve la altura total del documento.
    """
    return driver.execute_script("return document.body.scrollHeight")


def get_scroll_y(driver):
    """
    Devuelve la posición vertical actual del scroll.
    """
    return driver.execute_script("return window.pageYOffset;")