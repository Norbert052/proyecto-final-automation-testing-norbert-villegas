from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from utils.helpers import wait_for_element
from utils.logger import logger


class CartPage:
    CART_LIST = (By.CLASS_NAME, "cart_list")
    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    PRODUCT_NAME = (By.CLASS_NAME, "inventory_item_name")

    def __init__(self, driver):
        self.driver = driver

    def wait_until_loaded(self):
        logger.info("Esperando carga de carrito")
        wait = WebDriverWait(self.driver, 20)
        wait.until(EC.url_contains("/cart.html"))
        wait.until(lambda driver: driver.find_elements(*self.CART_LIST) or driver.find_elements(*self.CART_ITEMS))
        return wait_for_element(self.driver, self.CART_LIST)

    def get_cart_items_count(self):
        count = len(self.driver.find_elements(*self.CART_ITEMS))
        logger.info("Elementos en carrito: %s", count)
        return count

    def get_product_name(self):
        return wait_for_element(self.driver, self.PRODUCT_NAME).text
