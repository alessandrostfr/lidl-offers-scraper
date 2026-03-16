# ==========================================================
# parser.py
# ==========================================================
# Parser instrumentado para depuración.
#
# Objetivo:
# - procesar cada wrapper div[id^='grid-item-']
# - soportar las dos variantes vistas en Lidl:
#   1) testselector/data-testselector + data-grid-data
#   2) .product-grid-box + data-gridbox-impression
# - ignorar skeletons
# - extraer:
#   - id
#   - titulo_producto
#   - marca
#   - precio_actual
#   - porcentaje_descuento
#   - precio_antiguo
#   - url_imagen
#   - url_producto
#
# Además:
# - imprime contadores de depuración para saber exactamente
#   dónde se están cayendo los productos
# ==========================================================

from selenium.webdriver.common.by import By

from utils import (
    safe_get_text,
    safe_get_attribute,
    parse_json_attribute,
    extract_discount_number,
    parse_price_to_float,
    format_price,
)

# ==========================================================
# DEBUG counters
# ==========================================================
DEBUG_COUNTERS = {
    "total_items": 0,
    "skeleton_items": 0,
    "tile_nodes_found": 0,
    "grid_data_items": 0,
    "impression_items": 0,
    "missing_title": 0,
    "missing_brand": 0,
    "missing_price": 0,
    "missing_url": 0,
    "valid_products": 0,
    "duplicates": 0,
}


def reset_debug_counters():
    """
    Reinicia los contadores de depuración antes de cada parseo.
    """
    for key in DEBUG_COUNTERS:
        DEBUG_COUNTERS[key] = 0


def print_debug_counters():
    """
    Imprime el resumen de depuración.
    """
    print("\n========== DEBUG PARSER ==========")
    for k, v in DEBUG_COUNTERS.items():
        print(f"{k}: {v}")
    print("==================================\n")


def get_tile_node(grid_item):
    """
    Dentro de un wrapper grid-item busca el nodo real del producto.

    Prioridad:
    1. nodo con data-grid-data
    2. nodo .product-grid-box con data-gridbox-impression
    3. fallbacks más genéricos
    """
    selectors = [
        "[data-testselector='s-product-grid__list-item'][data-grid-data]",
        "[testselector='s-product-grid__list-item'][data-grid-data]",
        ".product-grid-box[data-gridbox-impression]",
        "[data-testselector='s-product-grid__list-item']",
        "[testselector='s-product-grid__list-item']",
        ".product-grid-box",
    ]

    for selector in selectors:
        try:
            node = grid_item.find_element(By.CSS_SELECTOR, selector)
            DEBUG_COUNTERS["tile_nodes_found"] += 1
            return node
        except Exception:
            continue

    # Fallback: si el propio wrapper parece el nodo real
    try:
        if safe_get_attribute(grid_item, "data-grid-data") or safe_get_attribute(grid_item, "data-gridbox-impression"):
            DEBUG_COUNTERS["tile_nodes_found"] += 1
            return grid_item
    except Exception:
        pass

    return None


def is_skeleton_item(grid_item):
    """
    Decide si un wrapper del grid es realmente un skeleton.

    Regla correcta:
    - si el item contiene un nodo real de producto con data-grid-data
      o data-gridbox-impression, NO es skeleton
    - solo lo consideramos skeleton si no hay datos de producto
      y además sí contiene bloques skeleton
    """
    try:
        # Si ya contiene un nodo real con data-grid-data, no es skeleton
        real_nodes = grid_item.find_elements(
            By.CSS_SELECTOR,
            "[data-testselector='s-product-grid__list-item'][data-grid-data], "
            "[testselector='s-product-grid__list-item'][data-grid-data], "
            ".product-grid-box[data-gridbox-impression]"
        )
        if len(real_nodes) > 0:
            return False

        # Si no tiene nodos reales y sí tiene skeletons, lo tratamos como skeleton
        skeletons = grid_item.find_elements(By.CSS_SELECTOR, ".s-grid-box-skeleton")
        return len(skeletons) > 0

    except Exception:
        return False


def extract_grid_data(tile_node):
    """
    Extrae y parsea data-grid-data si existe.

    Parámetro:
    - tile_node: nodo del producto

    Devuelve:
    - dict o {}
    """
    raw = safe_get_attribute(tile_node, "data-grid-data")
    return parse_json_attribute(raw, url_encoded=False)


def extract_impression_data(tile_node):
    """
    Extrae y parsea data-gridbox-impression si existe.

    Este atributo suele venir URL encoded.

    Parámetro:
    - tile_node: nodo del producto

    Devuelve:
    - dict o {}
    """
    raw = safe_get_attribute(tile_node, "data-gridbox-impression")
    return parse_json_attribute(raw, url_encoded=True)


def extract_title(tile_node, grid_data, impression_data):
    """
    Extrae el título del producto.

    Prioridad:
    1. atributo fulltitle
    2. data-grid-data.fullTitle / title / name
    3. keyfacts.fullTitle / keyfacts.title
    4. data-gridbox-impression.name
    5. HTML visible .product-grid-box__title
    """
    fulltitle = safe_get_attribute(tile_node, "fulltitle")
    if fulltitle:
        return fulltitle

    if isinstance(grid_data, dict):
        for key in ["fullTitle", "title", "name"]:
            value = grid_data.get(key, "")
            if value:
                return value

        keyfacts = grid_data.get("keyfacts", {})
        if isinstance(keyfacts, dict):
            for key in ["fullTitle", "title"]:
                value = keyfacts.get(key, "")
                if value:
                    return value

    if isinstance(impression_data, dict):
        value = impression_data.get("name", "")
        if value:
            return value

    try:
        element = tile_node.find_element(By.CSS_SELECTOR, ".product-grid-box__title")
        return safe_get_text(element)
    except Exception:
        return ""


def extract_brand(tile_node, grid_data, impression_data):
    """
    Extrae la marca.

    Prioridad:
    1. data-grid-data.brand.name
    2. data-gridbox-impression.brand
    3. HTML visible .product-grid-box__brand
    """
    if isinstance(grid_data, dict):
        brand = grid_data.get("brand", {})
        if isinstance(brand, dict):
            value = brand.get("name", "")
            if value:
                return value

    if isinstance(impression_data, dict):
        value = impression_data.get("brand", "")
        if value:
            return value

    try:
        element = tile_node.find_element(By.CSS_SELECTOR, ".product-grid-box__brand")
        return safe_get_text(element)
    except Exception:
        return ""


def extract_product_url(tile_node, grid_data):
    """
    Extrae la URL del producto.

    Prioridad:
    1. canonicalUrl
    2. canonicalPath
    3. href del enlace principal
    """
    if isinstance(grid_data, dict):
        canonical_url = grid_data.get("canonicalUrl", "")
        canonical_path = grid_data.get("canonicalPath", "")

        if canonical_url:
            if canonical_url.startswith("http"):
                return canonical_url
            return f"https://www.lidl.es{canonical_url}"

        if canonical_path:
            if canonical_path.startswith("http"):
                return canonical_path
            return f"https://www.lidl.es{canonical_path}"

    selectors = [
        "a.odsc-tile__link[href]",
        "a[href]",
    ]

    for selector in selectors:
        try:
            link = tile_node.find_element(By.CSS_SELECTOR, selector)
            href = safe_get_attribute(link, "href")
            if href:
                if href.startswith("http"):
                    return href
                return f"https://www.lidl.es{href}"
        except Exception:
            continue

    return ""


def extract_image_url(tile_node, grid_data):
    """
    Extrae la URL de la imagen.

    Prioridad:
    1. data-grid-data.image
    2. data-grid-data.image_V1.image
    3. data-grid-data.imageList[0]
    4. img.odsc-image-gallery__image
    """
    if isinstance(grid_data, dict):
        image = grid_data.get("image", "")
        if image:
            return image

        image_v1 = grid_data.get("image_V1", {})
        if isinstance(image_v1, dict):
            value = image_v1.get("image", "")
            if value:
                return value

        image_list = grid_data.get("imageList", [])
        if isinstance(image_list, list) and image_list:
            if isinstance(image_list[0], str):
                return image_list[0]

    selectors = [
        "img.odsc-image-gallery__image",
        ".odsc-image-gallery__image",
        "img",
    ]

    for selector in selectors:
        try:
            img = tile_node.find_element(By.CSS_SELECTOR, selector)

            src = safe_get_attribute(img, "src")
            if src:
                return src

            data_src = safe_get_attribute(img, "data-src")
            if data_src:
                return data_src

            srcset = safe_get_attribute(img, "srcset")
            if srcset:
                return srcset.split(",")[0].strip().split(" ")[0]
        except Exception:
            continue

    return ""


def extract_current_price(tile_node, grid_data, impression_data):
    """
    Extrae el precio actual.

    Prioridad:
    1. data-grid-data.price.price
    2. data-gridbox-impression.price
    3. HTML visible .ods-price__value
    """
    if isinstance(grid_data, dict):
        price_block = grid_data.get("price", {})
        if isinstance(price_block, dict):
            value = price_block.get("price", None)
            parsed = parse_price_to_float(value)
            if parsed is not None:
                return parsed

    if isinstance(impression_data, dict):
        value = impression_data.get("price", None)
        parsed = parse_price_to_float(value)
        if parsed is not None:
            return parsed

    try:
        element = tile_node.find_element(By.CSS_SELECTOR, ".ods-price__value")
        return parse_price_to_float(safe_get_text(element))
    except Exception:
        return None


def extract_old_price(tile_node, grid_data):
    """
    Extrae el precio antiguo.

    Prioridad:
    1. data-grid-data.price.oldPrice
    2. data-grid-data.price.discount.deletedPrice
    3. HTML visible .ods-price__stroke-price s
    """
    if isinstance(grid_data, dict):
        price_block = grid_data.get("price", {})
        if isinstance(price_block, dict):
            old_price = price_block.get("oldPrice", None)
            parsed = parse_price_to_float(old_price)
            if parsed is not None:
                return parsed

            discount = price_block.get("discount", {})
            if isinstance(discount, dict):
                deleted_price = discount.get("deletedPrice", None)
                parsed = parse_price_to_float(deleted_price)
                if parsed is not None:
                    return parsed

    try:
        element = tile_node.find_element(By.CSS_SELECTOR, ".ods-price__stroke-price s")
        return parse_price_to_float(safe_get_text(element))
    except Exception:
        return None


def extract_discount(tile_node, grid_data):
    """
    Extrae el porcentaje de descuento sin signo ni %.

    Prioridad:
    1. data-grid-data.price.discount.percentageDiscount
    2. HTML visible .ods-price__box-content-text-el
    """
    if isinstance(grid_data, dict):
        price_block = grid_data.get("price", {})
        if isinstance(price_block, dict):
            discount = price_block.get("discount", {})
            if isinstance(discount, dict):
                percentage = discount.get("percentageDiscount", None)
                if percentage is not None:
                    return str(percentage).replace("-", "").replace("%", "").strip()

    try:
        element = tile_node.find_element(By.CSS_SELECTOR, ".ods-price__box-content-text-el")
        return extract_discount_number(safe_get_text(element))
    except Exception:
        return ""


def build_product_from_item(grid_item):
    """
    Construye el producto a partir de un wrapper grid-item.
    Incluye instrumentación de depuración.
    """
    DEBUG_COUNTERS["total_items"] += 1

    if is_skeleton_item(grid_item):
        DEBUG_COUNTERS["skeleton_items"] += 1
        return None

    tile_node = get_tile_node(grid_item)
    if tile_node is None:
        return None

    grid_data = extract_grid_data(tile_node)
    impression_data = extract_impression_data(tile_node)

    if grid_data:
        DEBUG_COUNTERS["grid_data_items"] += 1

    if impression_data:
        DEBUG_COUNTERS["impression_items"] += 1

    titulo_producto = extract_title(tile_node, grid_data, impression_data)
    marca = extract_brand(tile_node, grid_data, impression_data)
    precio_actual = extract_current_price(tile_node, grid_data, impression_data)
    precio_antiguo = extract_old_price(tile_node, grid_data)
    porcentaje_descuento = extract_discount(tile_node, grid_data)
    url_imagen = extract_image_url(tile_node, grid_data)
    url_producto = extract_product_url(tile_node, grid_data)

    if not titulo_producto:
        DEBUG_COUNTERS["missing_title"] += 1
        return None

    if not marca:
        DEBUG_COUNTERS["missing_brand"] += 1
        return None

    if precio_actual is None:
        DEBUG_COUNTERS["missing_price"] += 1
        return None

    if not url_producto:
        DEBUG_COUNTERS["missing_url"] += 1
        return None

    DEBUG_COUNTERS["valid_products"] += 1

    return {
        "id": None,
        "titulo_producto": titulo_producto,
        "marca": marca,
        "precio_actual": format_price(precio_actual),
        "porcentaje_descuento": porcentaje_descuento,
        "precio_antiguo": format_price(precio_antiguo),
        "url_imagen": url_imagen,
        "url_producto": url_producto,
    }


def is_valid_product(product):
    """
    Comprueba si el producto tiene lo mínimo necesario.
    """
    if not product:
        return False

    if not product["titulo_producto"]:
        return False

    if not product["marca"]:
        return False

    if not product["precio_actual"]:
        return False

    if not product["url_producto"]:
        return False

    return True


def normalize_title(title):
    """
    Normaliza el título para deduplicar mejor.
    """
    if not title:
        return ""

    return " ".join(title.strip().lower().split())


def make_product_key(product):
    """
    Clave única por título normalizado.
    """
    return ("title", normalize_title(product.get("titulo_producto", "")))


def parse_items(items, seen_keys):
    """
    Parsea los wrappers del grid y devuelve solo productos nuevos.
    También imprime el resumen de depuración.
    """
    reset_debug_counters()
    new_products = []

    for item in items:
        try:
            product = build_product_from_item(item)

            if not is_valid_product(product):
                continue

            key = make_product_key(product)

            if key in seen_keys:
                DEBUG_COUNTERS["duplicates"] += 1
                continue

            seen_keys.add(key)
            new_products.append(product)

            print(f"[DEBUG] Nuevo producto detectado: {product['titulo_producto']}")

        except Exception as e:
            print(f"[DEBUG] Error parseando item: {e}")
            continue

    print_debug_counters()
    return new_products


def assign_ids(products):
    """
    Reasigna IDs consecutivos.
    """
    for index, product in enumerate(products, start=1):
        product["id"] = index

    return products