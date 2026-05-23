# Limpieza recomendada del repositorio

Durante la auditoría se detectó que el repomix incluía carpetas típicas de entorno virtual (`Lib/`, `Scripts/`, `pyvenv.cfg`) y varios CSV/HTML de depuración.

Para que el repo público se vea profesional, conviene limpiar lo que no debe formar parte del código fuente.

## 1. Añadir `.gitignore`

Este parche incluye un `.gitignore` para evitar subir:

- entornos virtuales;
- drivers/cache;
- CSV generados;
- HTML descargado de debug;
- logs;
- archivos temporales.

## 2. Si ya estaban trackeados por Git

Ejecuta desde la raíz del repo:

```powershell
git rm -r --cached Lib Scripts pyvenv.cfg
git rm -r --cached old_csvs html_resources
git rm --cached productos_lidl_descuentos_final.csv
```

Si alguno no existe o Git dice que no está trackeado, no pasa nada.

## 3. Mantener ejemplos limpios

Si quieres enseñar un ejemplo de salida, crea uno pequeño y ficticio en:

```text
assets/examples/sample-output.csv
```

No hace falta publicar CSVs grandes o históricos de ejecución.
