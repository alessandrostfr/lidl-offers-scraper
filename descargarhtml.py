

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import time

options = Options()
options.add_argument("--headless")  # Sin abrir ventana

driver = webdriver.Chrome(options=options)
driver.get("https://www.lidl.es/q/query/descuentos")

time.sleep(3)  # Espera a que cargue el JS

ruta = os.path.join(os.path.dirname(__file__), "pagina.html")
with open(ruta, "w", encoding="utf-8") as f:
    f.write(driver.page_source)

driver.quit()
print(f"Página guardada en: {ruta}")