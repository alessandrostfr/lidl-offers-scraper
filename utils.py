# ==========================================================
# utils.py
# ==========================================================
# Funciones auxiliares:
# - limpiar texto
# - convertir precios
# - calcular precio antiguo
# - leer atributos con seguridad
# - decodificar JSON embebido en atributos HTML
# ==========================================================

import json
import re
from urllib.parse import unquote


def clean_text(text):
    """
    Limpia espacios repetidos y saltos de línea.
    """
    if not text:
        return ""

    return re.sub(r"\s+", " ", text).strip()


def safe_get_text(element):
    """
    Obtiene el texto de un elemento Selenium de forma segura.
    """
    try:
        return clean_text(element.text)
    except Exception:
        return ""


def safe_get_attribute(element, attr_name):
    """
    Obtiene un atributo de un elemento Selenium de forma segura.
    """
    try:
        value = element.get_attribute(attr_name)
        return value.strip() if value else ""
    except Exception:
        return ""


def parse_price_to_float(text):
    """
    Convierte un texto de precio a float.
    """
    if text is None:
        return None

    text = str(text)
    cleaned = re.sub(r"[^\d,\.]", "", text).strip()

    if not cleaned:
        return None

    cleaned = cleaned.replace(",", ".")

    try:
        return float(cleaned)
    except ValueError:
        return None


def format_price(value):
    """
    Convierte un float a texto con dos decimales.
    """
    if value is None:
        return ""

    return f"{value:.2f}"


def extract_discount_number(text):
    """
    Extrae solo el número del descuento.

    Ejemplos:
    - '-23%' -> '23'
    - '23%' -> '23'
    """
    if not text:
        return ""

    text = clean_text(text)
    match = re.search(r"-?\s*(\d{1,3})\s*%", text)

    if match:
        return match.group(1)

    return ""


def calculate_old_price(current_price, discount_percent):
    """
    Calcula el precio antiguo a partir del precio actual y el descuento.
    """
    if current_price is None:
        return None

    if discount_percent in ("", None):
        return None

    try:
        discount_percent = float(discount_percent)

        if discount_percent <= 0 or discount_percent >= 100:
            return None

        old_price = current_price / (1 - discount_percent / 100)
        return round(old_price, 2)

    except Exception:
        return None


def parse_json_attribute(raw_value, url_encoded=False):
    """
    Intenta convertir un atributo HTML que contiene JSON en un diccionario.

    Parámetros:
    - raw_value: texto crudo del atributo
    - url_encoded: si el JSON viene URL encoded

    Devuelve:
    - dict o {}
    """
    if not raw_value:
        return {}

    try:
        value = unquote(raw_value) if url_encoded else raw_value
        return json.loads(value)
    except Exception:
        return {}