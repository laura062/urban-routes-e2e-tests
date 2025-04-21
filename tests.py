import main
import time
import data


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

    def setup_method(self):
        self.driver.get(data.urban_routes_url)
        self.routes_page = main.UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        self.routes_page.set_from(address_from)
        self.routes_page.set_to(address_to)

    def test_click_taxi_button(self):
        # 🛻 Hacer clic en el botón luego
        self.routes_page.click_taxi_button()
        time.sleep(5)

  #test para elegir el tarifa comford




    @classmethod
    def teardown_class(cls):
        cls.driver.quit()