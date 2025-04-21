
import time

from selenium.common import TimeoutException

import data
from selenium import webdriver
from selenium.webdriver.common.keys import keys
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
    from_field = (By.ID,"from")
    to_field = (By.ID, "to")
    taxi_button = (By.XPATH, "//button[@type='button' and @class='button round']")

    def __init__(self, driver):
        self.driver = driver

    def set_from(self, from_address):
        wait = WebDriverWait(self.driver,10) #espera hasta 10s
        from_element = wait.until(EC.presence_of_element_located(self.from_field))
        from_element.send_keys(from_address)

    def set_to(self, to_address):
        wait = WebDriverWait(self.driver,10)
        to_element = wait.until(EC.presence_of_element_located(self.to_field))
        to_element.send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

#declarar los codigos para hacer clic en el boton pedir un taxi

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


    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_from(address_from)
        routes_page.set_to(address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

    def test_click_taxi_button(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)

        # 🧭 Ingresar direcciones primero
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_from(address_from)
        routes_page.set_to(address_to)

        # 🛻 Hacer clic en el botón luego
        routes_page.click_taxi_button()

        wait = WebDriverWait(self.driver, 5)
        taxi_panel_locator = (By.CLASS_NAME, "tariff-picker_shown")
        taxi_panel = wait.until(
            EC.visibility_of_element_located(taxi_panel_locator)
        )

        # Verificar que el panel es visible
        assert taxi_panel.is_displayed()


    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
