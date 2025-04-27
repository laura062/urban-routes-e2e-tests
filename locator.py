from selenium.webdriver.common.by import By

#LOCALIZADORES
from_1field = (By.ID,"from")
to_2field = (By.ID, "to")
taxi_button = (By.XPATH, "//button[@type='button' and @class='button round']")#3
card_comfort = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[1]/div[5]/div[2]')#4
field_number = (By.CLASS_NAME,"np-button")#5
phone_number_field = (By.XPATH, "//*[@id='phone']")#6
button_next = (By.XPATH, '//*[@id="root"]/div/div[1]/div[2]/div[1]/form/div[2]/button')#7
field_enter_code = (By.XPATH, '//form/div/div/input[@id="code"]')#8
button_confirm_code = (By.XPATH, '//button[text()="Confirmar"]')#9
payment_method = (By.CLASS_NAME, "pp-text")#1o
add_card = (By.CLASS_NAME, "pp-plus")#11
add_card_number = (By.ID, "number") #12
add_code = (By.XPATH, '//input[@placeholder="12"]')#13
click_to_blur = (By.CLASS_NAME, "plc")#14
add_card_button = (By.XPATH, '//button[text()="Agregar"]') #15
close_button = (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[1]/button') #16
message_driver = (By.ID, "comment") # 17
reqs_arrow = (By.CLASS_NAME, "reqs-arrow.open") #18
blanket_handkerchiefs = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[1]/div/div[2]/div') #19
ice_cream = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[3]/div/div[2]/div[1]/div/div[2]/div/div[3]') #20
order_taxi = (By.CLASS_NAME, "smart-button-main") #21
searching_car_modal = (By.XPATH, "//div[contains(@class, 'order-header-title') and contains(text(), 'Buscar automóvil')]") #22
DRIVER_INFO_MODAL = (By.XPATH, "//div[contains(@class, 'order-header-title') and contains(text(), 'El conductor llegará en')]") #23
TRIP_INFO_PANEL = (By.CLASS_NAME, "order-body")  # Usaremos toda la estructura del modal #24
