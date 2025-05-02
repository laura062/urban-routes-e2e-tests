# PROYECTO 8 'URBAN ROUTES' DE LAURA LETICIA CHAN COCOM DEL COHORT 25
  - Automatización de Pruebas Funcionales para Urban Routes

 - Este proyecto contiene scripts de automatización de pruebas funcionales desarrollados en Python utilizando la
   librería Selenium. El objetivo de estas pruebas es verificar el flujo completo
   de la aplicación web Urban Routes, desde la selección de origen y destino hasta
   la solicitud de un taxi, incluyendo la verificación del número de teléfono y la adición de un método de pago.


## pruebas positivas 
 - En estas pruebas se tuvo que verificar los llenados de campos, la visibilidad de informacion complementaria

## Tecnologías Utilizadas:

* **Python:** Lenguaje de programación principal.
* **Selenium:** Librería de Python para la automatización de navegadores web.
    * **WebDriver:** Control del navegador.
    * **By:** Localización de elementos web.
    * **WebDriverWait:** Espera explícita para la sincronización con la página web.
    * **expected\_conditions (EC):** Condiciones predefinidas para la espera.
* **`time`:** Módulo de Python para pausas en la ejecución.
* **`json`:** Módulo de Python para trabajar con datos JSON (especialmente para la recuperación del código de verificación).
* **`unittest`:** Framework de pruebas unitarias de Python (utilizado implícitamente para la estructura de las pruebas).
* **Archivo `data` (personalizado):** Contiene datos de prueba como URLs, direcciones, números de teléfono y detalles de tarjetas de pago.


## Ejecución de Pruebas:

- Para ejecutar las pruebas, se requiere tener Python instalado ,los paquetes pytest y selenium.
**WebDriver para Chrome:** Dado que la configuración en el código incluye `webdriver.Chrome`, 
  necesitas tener instalado el ChromeDriver compatible con la versión de Google Chrome que tengas instalada en tu sistema. 
  Puedes descargar el ChromeDriver desde la [página oficial de ChromeDriver](https://chromedriver.chromium.org/downloads). 
  Asegúrate de que el ejecutable de ChromeDriver esté en tu PATH o especifica la ruta al inicializar el WebDriver.

1.  **Asegúrate de tener `pytest` instalado:**
    Si no tienes `pytest` instalado, puedes instalarlo usando pip:
    ```bash
    pip install pytest
    ```

2.  **Navega al directorio del proyecto:**
    Abre tu terminal o símbolo del sistema y dirígete a la raíz del proyecto:
    ```bash
    cd qa-project-Urban-Routes-es
    ```
    o cd (C:\Users\shule\PycharmProjects\qa-project-Urban-Routes-es)

3.  **Ejecuta las pruebas:**
    Desde la raíz del proyecto, ejecuta el siguiente comando para que `pytest` descubra y ejecute las pruebas en el archivo `main.py`:
    ```bash
    pytest main.py
    ```





## Estructura del Proyecto:

- data.py: Define los datos de prueba utilizados en las pruebas y la URL. 
- main.py: contiene todo cuerpo completo 
- main.py esta dividido por clases: 
  class UrbanRoutesPage:contiene los localizadores y todos los metodos.
  class TestUrbanRoutes: contiene los tests
- locator.py:contiene los localizadores de forma separada de las pruebas, esto quiere decir que no tiene conexion
  con main.py, siemplemente lo separe para tenerlos a la vista.



# Detalles de los test.
- El caso de las pruebas  simula el siguiente flujo dentro de la aplicación Urban Routes:

* Abrir la URL de la aplicación.
* Ingresar la dirección de origen.
* Ingresar la dirección de destino.
* Hacer clic en el botón para pedir un taxi.
* Seleccionar la tarifa "Comfort".
* Hacer clic en el campo del número de teléfono.
* Ingresar un número de teléfono.
* Hacer clic en el botón "Siguiente".
* Recuperar automáticamente el código de verificación del teléfono interceptando las peticiones de la API del navegador.
* Ingresar el código de verificación.
* Hacer clic en el botón "Confirmar".
* Hacer clic en la opción de método de pago.
* Hacer clic en "Agregar tarjeta".
* Ingresar el número de tarjeta.
* Ingresar el código de seguridad de la tarjeta.
* Hacer clic para deseleccionar el campo de código (para activar el botón "Agregar").
* Hacer clic en el botón "Agregar" para guardar la tarjeta.
* Cerrar la ventana de métodos de pago.
* Ingresar un mensaje para el conductor.
* Abrir la sección de requisitos adicionales.
* Solicitar "manta y pañuelos".
* Solicitar dos "helados".
* Hacer clic en el botón para ordenar el taxi.
* Verificar la aparición del modal de "Buscando automóvil".
* Verificar la transición al modal de información del conductor.
* Verificar que el panel de información del viaje sea visible.