import time
from selenium.common import TimeoutException
import data
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait



# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""
    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code

class UrbanRoutesPage:
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

    def __init__(self, driver):
        self.driver = driver

    def set_1from(self, from_address):
        wait = WebDriverWait(self.driver,10) #espera hasta 10s
        from_element = wait.until(EC.presence_of_element_located(self.from_1field))
        from_element.send_keys(from_address)

    def set_2to(self, to_address):
        wait = WebDriverWait(self.driver,10)
        to_element = wait.until(EC.presence_of_element_located(self.to_2field))
        to_element.send_keys(to_address)

    def get_1from(self):
        return self.driver.find_element(*self.from_1field).get_property('value')

    def get_2to(self):
        return self.driver.find_element(*self.to_2field).get_property('value')

#declarar los metodos para hacer clic en el boton pedir un taxi #3
    def click_taxi_button(self):
        wait = WebDriverWait(self.driver,10)
        # Esperar a que aparezca la duración del viaje, por ejemplo:
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "duration")))
        taxi_button_locator = (By.XPATH, "//button[@type='button' and @class='button round']")
        try:
            button_element = wait.until(EC.visibility_of_element_located(taxi_button_locator))
            clickable_button = wait.until(EC.element_to_be_clickable(button_element))
            clickable_button.click()
        except TimeoutException as e:
            print(f"Timeout al intentar hacer clic en el botón: {e}")

            raise
#metodos para interactuar con la tarifa comford #4
    def click_button_comfort(self):
        wait = WebDriverWait(self.driver,10)
        comfort_element = wait.until(EC.element_to_be_clickable(self.card_comfort))
        comfort_element.click()


# METODOS AGREGAR NUMÉRO DE TELÉFONO #5
    def click_field_number(self):
        wait = WebDriverWait(self.driver,10)
        number_element = wait.until(EC.element_to_be_clickable(self.field_number))
        number_element.click()

#AGREGAMOS EL NUMERO DE TELOFONO #6
    def set_phone_number(self,phone_number):
        wait = WebDriverWait(self.driver,10)
        phone_element = wait.until(EC.presence_of_element_located(self.phone_number_field))
        phone_element.send_keys(phone_number)

    def get_phone_number(self):
        return  self.driver.find_element(*self.phone_number_field).get_property('value')


#HACER CLICK EN EL BOTON SIGUIENTE #7
    def click_button_next(self):
        wait = WebDriverWait(self.driver,10)
        next_element = wait.until(EC.element_to_be_clickable(self.button_next))
        next_element.click()

#AGREGAR EL CODIGO EN EL CAMPO INGRESAR CODIGO #8
    def enter_verification_code(self, verification_code: str):
        wait = WebDriverWait(self.driver, 10)
        code_field = wait.until(EC.element_to_be_clickable(self.field_enter_code))
        code_field.send_keys(verification_code)
        print(f"Se ingresó el código de verificación: {verification_code}")

    def get_field_enter_code(self):
        return self.driver.find_element(*self.field_enter_code).get_property('value')



#HACER CLICK EN EL BOTON SIGUIENTE  #9

    def click_button_confirm_code(self):
        wait = WebDriverWait(self.driver,10)
        confirm_element = wait.until(EC.element_to_be_clickable(self.button_confirm_code))
        confirm_element.click()


#HACER CLICK EN METODO DE PAGO #10
    def click_payment_method(self):
        wait = WebDriverWait(self.driver,10)
        click_payment = wait.until(EC.element_to_be_clickable(self.payment_method))
        click_payment.click()


#CLICK EN AGREGAR TARJETA #11
    def add_card_click(self):
        wait = WebDriverWait(self.driver,10)
        add_card_element = wait.until(EC.element_to_be_clickable(self.add_card))
        add_card_element.click()




#LLENAR EL CAMPO NUMERO DE TARJETA #12
    def set_add_card_number(self, card_number):
        wait = WebDriverWait(self.driver, 10)
        add_card_element = wait.until(EC.element_to_be_clickable(self.add_card_number))
        add_card_element.send_keys(card_number)

    def get_add_card(self):
        return self.driver.find_element(*self.add_card_number).get_property('value')



#LLENAR CAMPO CODIGO #13

    def set_add_code(self,card_code):
        wait = WebDriverWait(self.driver,10)
        code_add = wait.until(EC.element_to_be_clickable(self.add_code))
        code_add.send_keys(card_code)

    def get_code(self):
        return self.driver.find_element(*self.add_code).get_property('value')



#CLICK PARA DESENFOCAR Y ACTIVAR EL BOTON AGREGAR #14
    def to_blur_click(self):
        wait = WebDriverWait(self.driver, 10)
        blur_element = wait.until(EC.element_to_be_clickable(self.click_to_blur))
        blur_element.click()





#CLICK EN BOTON AGREGAR #15
    def add_card_button_click(self):
        wait = WebDriverWait(self.driver,10)
        add_button = wait.until(EC.element_to_be_clickable(self.add_card_button))
        add_button.click()


#CLICK EN LA X DE LA VENTA METODO DE PAGO PARA CERRAR LA VENTANA #16
    def click_close_button(self):
        wait = WebDriverWait(self.driver,10)
        close_button_element = wait.until(EC.element_to_be_clickable(self.close_button))
        close_button_element.click()


#AGREGAR MENSAJE PARA EL CONDUCTOR #17
    def set_message_for_the_driver(self,message_for_driver):
        wait = WebDriverWait(self.driver,10)
        add_message_driver = wait.until(EC.presence_of_element_located(self.message_driver))
        add_message_driver.send_keys(message_for_driver)

    def get_message(self):
            return self.driver.find_element(*self.message_driver).get_property('value')

#hacer click en la fechita para ver los requisitos  #18


    def open_arrow_reqs(self):
        wait = WebDriverWait(self.driver,20)
        arrow_open_element = wait.until(EC.element_to_be_clickable(self.reqs_arrow))
        arrow_open_element.click()
        arrow_open_element.click()

#CLICK PARA ELEJIR MANTA Y PAÑUELOS #19

    def ask_blanket_handkerchiefs(self):
        wait = WebDriverWait(self.driver,10)
        ask_element = wait.until(EC.element_to_be_clickable(self.blanket_handkerchiefs))
        ask_element.click()


#CLICK 2 VECES PARA ELEJIR DOS HELADOS 20
    def order_ice_cream(self):
        wait = WebDriverWait(self.driver,10)
        ice_element = wait.until(EC.element_to_be_clickable(self.ice_cream))
        ice_element.click()
        ice_element.click()


#ORDENAR TAXI # 21
    def button_order_taxi(self):
        wait = WebDriverWait(self.driver,10)
        button_element = wait.until(EC.element_to_be_clickable(self.order_taxi))
        button_element.click()


#VERIFICACION DEL PANEL BUSCANDO CONDUCTOR #22
    def wait_for_searching_car_modal(self):
        # Espera a que aparezca el modal de "Buscar automóvil"
        WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located(self.searching_car_modal))


#VERIFICACION DE QUE SEA VISIBLE LA INFORMACION DEL CONDUCTOR #23
    def wait_for_driver_info_modal(self):
        # Espera a que el modal cambie a mostrar la información del conductor
        WebDriverWait(self.driver, 60).until(
            EC.visibility_of_element_located(self.DRIVER_INFO_MODAL))




class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        options = Options()
        options.set_capability("goog:loggingPrefs",  {'performance': 'ALL'})
        cls.driver = webdriver.Chrome(options=options)



    def test_full_flow(self):

        self.driver.get(data.urban_routes_url)
        self.routes_page = UrbanRoutesPage(self.driver)
        self.timeout = 10

        address_from = data.address_from
        address_to = data.address_to
        self.routes_page.set_1from(address_from)
        self.routes_page.set_2to(address_to)

     # 🛻 Hacer clic en el botón PEDIR TAXI #3
        self.routes_page.click_taxi_button()
        self.timeout = 10

    #HACER CLICK EN LA TARIFA COMFORT #4
        self.routes_page.click_button_comfort()
        self.timeout = 10


     #HACER CLICK EN EL CAMPO NUMERO DE TELEFONO #5
        self.routes_page.click_field_number()
        self.timeout = 10


    #LLENAR EL CAMPO NUMERO DE TELEFONO #6
        phone_number = data.phone_number
        self.routes_page.set_phone_number(phone_number)
        self.timeout = 10


     #HACER CLICK EN EL BOTON SIGUIENTE #7
        self.routes_page.click_button_next()
        time.sleep(5)


    #AGREGAR EL CODIGO EN EL CAMPO "AGREGAR EL CODIGO" #8

        verification_code = retrieve_phone_code(self.driver)
        assert verification_code is not None, "No se recuperó el código de verificación."
        print(f"Código obtenido: {verification_code}")

        self.routes_page.enter_verification_code(verification_code)

    #HACER CLICK EN LE BOTON CONFIRMAR #9
        self.routes_page.click_button_confirm_code()
        self.timeout = 10

    # HACER CLICK EN METODO DE PAGO #10
        self.routes_page.click_payment_method()

    #CLICK EN AGREGAR TARJETA #11
        self.routes_page.add_card_click()
        time.sleep(4)

    #AGREGAR EL NUMERO DE TARJETA #12
        card_number = data.card_number
        self.routes_page.set_add_card_number(card_number)


    #AGREGAR CODIGO #13
        card_code = data.card_code
        self.routes_page.set_add_code(card_code)



     #CLICK DESENFOQUE #14
        self.routes_page.to_blur_click()


     #CLICK EN EL BOTON AGREGAR #15
        self.routes_page.add_card_button_click()
        time.sleep(5)

     #HACER CLICK EN EL BOTON X DE LA VENTANA METODO DE PAGO #16
        self.routes_page.click_close_button()
        time.sleep(5)

     #AGREGAR MENSAJE PARA EL CONDUCTOR # 17
        message_driver = data.message_for_driver
        self.routes_page.set_message_for_the_driver(message_driver)
        time.sleep(5)

     #CLICK EN FECHITA PARA LOS REQUISITOS #18
        self.routes_page.open_arrow_reqs()

     #CLICK PARA ELEJIR MANTA Y PAÑUELOS #19
        self.routes_page.ask_blanket_handkerchiefs()



     #ELEJIR DOS HELADOS #20
        self.routes_page.order_ice_cream()
        time.sleep(5)


     #ORDENAR TAXI #21
        self.routes_page.button_order_taxi()


     #VERIFICACION DEL LA APARICION DEL MODAL BUSCAR AUTOMOVIL #22

        WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[contains(@class, 'order-header-title') and contains(text(), 'Buscar automóvil')]"))
        )
        print("✅ Modal de búsqueda de automóvil mostrado correctamente.")

     # VERIFICACIÓN DEL CAMBIO AL MODAL DE INFORMACIÓN DEL VIAJE #23

        WebDriverWait(self.driver, 60).until(
            EC.visibility_of_element_located((By.XPATH,
                                              "//div[contains(@class, 'order-header-title') and contains(text(), 'El conductor llegará en')]"))
        )
        print("✅ Modal de información del conductor mostrado correctamente.")

        # Verificar que todo el panel de viaje esté visible
        assert self.driver.find_element(By.CLASS_NAME,
                                        "order-body").is_displayed(), "❌ El modal de información del viaje no se mostró."
        print("✅ Panel de información del viaje verificado.")






    @ classmethod
    def teardown_class(cls):
        cls.driver.quit()