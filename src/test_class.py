from selenium import webdriver
from selenium.webdriver.common.by import By

# Replace 'your_url' with the URL of the webpage you want to inspect
url = "https://www.pudelek.pl/sprawa-joanny-z-krakowa-kinga-rusin-miazdzy-pis-i-polska-policje-kazali-jej-sie-rozebrac-do-naga-choc-krwawila-6921586600442848a?fbclid=IwAR2XwfbyjdWMuq5ALuZZaQCpM0zIGyUh4wkvQPOEuu8P_-dQqNw0aZaVZGc"

# Replace 'your_class_name' with the class name you want to target
class_name = 'sc-1mskw74-0 sc-7eqdwf-0 sc-q1w81m-0'

# Initialize the WebDriver
driver = webdriver.Chrome()

# Open the webpage
driver.get(url)

try:
    # Find all elements with the specified class
    elements = driver.find_elements(By.CLASS_NAME, class_name)

    # Iterate through the elements and do something with each of them
    for element in elements:
        # For example, print the text content of each element
        print(element.text)

finally:
    # Close the browser
    driver.quit()
