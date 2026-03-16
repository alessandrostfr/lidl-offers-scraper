# ==========================================================
# main.py
# ==========================================================
# Control principal del scraper.
# ==========================================================

from config import (
    OUTPUT_FILE,
    OFFSET_STEP,
    MAX_PAGES,
    MAX_SCROLLS_PER_OFFSET,
    DEBUG_MODE,
)
from scraper import (
    create_driver,
    build_offset_url,
    open_page,
    wait_initial_page_load,
    accept_cookies,
    wait_results_section,
    find_grid_items,
    scroll_to_top,
    scroll_down_once,
    get_scroll_height,
    get_scroll_y,
)
from parser import parse_items, assign_ids
from save_data import save_to_csv


def scrape_single_offset(driver, offset, seen_keys):
    """
    Scrapea un offset completo de forma optimizada.

    Estrategia:
    - abre el offset
    - hace una primera lectura
    - si ya aparecen productos nuevos, hace una iteración extra
      para comprobar si hay más
    - si en la siguiente ya no hay nuevos, cierra el offset
    """
    url = build_offset_url(offset)

    print("=" * 70)
    print(f"[INFO] Procesando offset: {offset}")
    print(f"[INFO] URL: {url}")

    open_page(driver, url)
    wait_initial_page_load(driver)
    accept_cookies(driver)
    wait_results_section(driver)

    scroll_to_top(driver)

    offset_products = []
    current_scroll = 0
    had_new_products_once = False

    for scroll_index in range(1, MAX_SCROLLS_PER_OFFSET + 1):
        items = find_grid_items(driver)
        print(f"[INFO] Offset {offset} | Scroll {scroll_index} | Ítems visibles: {len(items)}")

        new_products = parse_items(items, seen_keys)

        if new_products:
            offset_products.extend(new_products)
            had_new_products_once = True

            print(f"[INFO] Offset {offset} | Scroll {scroll_index} | Nuevos productos: {len(new_products)}")
            print(f"[INFO] Offset {offset} | Total acumulado en este offset: {len(offset_products)}")

            previous_scroll = current_scroll
            current_scroll = scroll_down_once(driver, current_scroll)

            total_height = get_scroll_height(driver)
            current_y = get_scroll_y(driver)

            if DEBUG_MODE:
                print(f"[DEBUG] Offset {offset} | ScrollY: {current_y} | Altura total: {total_height}")

            if current_scroll == previous_scroll:
                print(f"[INFO] Offset {offset} finalizado porque el scroll ya no avanza.")
                break

            continue

        if had_new_products_once:
            print(f"[INFO] Offset {offset} finalizado: tras encontrar productos, ya no aparecen más nuevos.")
            break

        previous_scroll = current_scroll
        current_scroll = scroll_down_once(driver, current_scroll)

        total_height = get_scroll_height(driver)
        current_y = get_scroll_y(driver)

        if DEBUG_MODE:
            print(f"[DEBUG] Offset {offset} | ScrollY: {current_y} | Altura total: {total_height}")

        if current_scroll == previous_scroll:
            print(f"[INFO] Offset {offset} finalizado porque el scroll ya no avanza.")
            break

        if current_y >= total_height * 0.90:
            print(f"[INFO] Offset {offset} finalizado cerca del final sin productos nuevos.")
            break

    print(f"[INFO] Productos nuevos totales extraídos en offset {offset}: {len(offset_products)}")
    return offset_products


def main():
    """
    Función principal del scraper.

    Guarda el CSV incluso si falla el último offset.
    """
    driver = create_driver()
    all_products = []
    seen_keys = set()

    try:
        for page_index in range(MAX_PAGES):
            offset = page_index * OFFSET_STEP

            try:
                new_products = scrape_single_offset(driver, offset, seen_keys)

            except Exception as offset_error:
                print(f"[WARN] Error en offset {offset}: {offset_error}")
                print("[INFO] Se detiene el scraping, pero se guardarán los datos ya extraídos.")
                break

            # Solo paramos si este offset no aporta ningún producto nuevo
            if not new_products:
                print("[INFO] No se extrajeron productos nuevos en este offset. Fin del scraping.")
                break

            all_products.extend(new_products)
            print(f"[INFO] Total global acumulado: {len(all_products)}")

        all_products = assign_ids(all_products)

    except Exception as e:
        print(f"[ERROR] Ha ocurrido un problema general: {e}")

    finally:
        try:
            if all_products:
                print("=" * 70)
                print("[INFO] Guardando CSV final...")
                save_to_csv(all_products, OUTPUT_FILE)
                print("[OK] Scraping terminado correctamente.")
            else:
                print("[WARN] No hay productos para guardar en el CSV.")
        except Exception as save_error:
            print(f"[ERROR] Error guardando el CSV: {save_error}")

        print("[INFO] Cerrando navegador...")
        driver.quit()


if __name__ == "__main__":
    main()