from selenium import webdriver
from selenium.webdriver.edge.service import Service  
from selenium.webdriver.common.by import By
import time


driver_path = 'g:/programacion/utilidades/msedgedriver.exe'  

# Enlace de WhatsApp
whatsapp_link = 'https://web.whatsapp.com/send/?phone=34680403401&text=Mensaje+enviado+con+Wa.me+desde+python&type=phone_number&app_absent=0'


service = Service(driver_path)


edge_options = webdriver.EdgeOptions()


driver = webdriver.Edge(service=service, options=edge_options)


driver.get(whatsapp_link)
# ¿ como se guardaba la sesiónd e una a otra ?
print("Esperando a que WhatsApp Web cargue...")
time.sleep(30)  


send_button = driver.find_element(By.XPATH, '//button[@aria-label="Enviar"]')
send_button.click()

time.sleep(5)

# Confirmar que el mensaje fue enviado
print("Mensaje enviado exitosamente.")

# Cerrar el navegador
driver.quit()