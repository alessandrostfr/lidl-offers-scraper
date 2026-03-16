# ==========================================================
# save_data.py
# ==========================================================
# Guarda el CSV final con el orden exacto de columnas.
# ==========================================================

import pandas as pd


def save_to_csv(data, filename):
    """
    Guarda la lista de productos en un CSV.
    """
    df = pd.DataFrame(data)

    columns_order = [
        "id",
        "titulo_producto",
        "marca",
        "precio_actual",
        "porcentaje_descuento",
        "precio_antiguo",
        "url_imagen",
        "url_producto",
    ]

    if len(df) > 0:
        df = df[columns_order]

    df.to_csv(filename, index=False, encoding="utf-8-sig")

    print(f"[OK] CSV guardado correctamente: {filename}")
    print(f"[INFO] Total de productos guardados: {len(df)}")