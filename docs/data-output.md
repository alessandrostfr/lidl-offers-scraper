# Salida de datos

El scraper genera un CSV con productos en descuento.

## Columnas

| Columna | Descripción |
|---|---|
| `id` | Identificador consecutivo generado al final del proceso. |
| `titulo_producto` | Nombre del producto. |
| `marca` | Marca detectada si está disponible. |
| `precio_actual` | Precio actual normalizado. |
| `porcentaje_descuento` | Porcentaje de descuento si aparece. |
| `precio_antiguo` | Precio anterior calculado si es posible. |
| `url_imagen` | URL de la imagen del producto. |
| `url_producto` | URL de la ficha del producto. |

## Ejemplo ficticio

```csv
id,titulo_producto,marca,precio_actual,porcentaje_descuento,precio_antiguo,url_imagen,url_producto
1,Taladro inalámbrico 20V,Parkside,39.99,20,49.99,https://...,https://...
```

## Nota

Los datos dependen de la disponibilidad pública de Lidl en el momento de ejecución. Algunos campos pueden estar vacíos si la página no los expone o si cambia el marcado HTML.
