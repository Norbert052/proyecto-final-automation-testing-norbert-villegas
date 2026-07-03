import pytest
from selenium.webdriver.common.by import By
from utils.data_reader import read_csv, read_json
from utils.driver_factory import get_driver
from page.cart_page import CartPage
from page.inventory_page import InventoryPage
from page.login_page import LoginPage
from utils.helpers import (
    get_text,
    wait_for_element,
    wait_for_visibility,
    take_screenshot
)

login_data = [
    (item["username"], item["password"], item["should_work"].lower() == "true")
    for item in read_csv("login.csv")
]

product_names = [product["name"] for product in read_json("products.json")["products"]]


class TestSauceDemo:
    
    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        self.driver = get_driver()
        yield
        self.driver.quit()
    
    @pytest.mark.parametrize("username,password,should_work", login_data)
    def test_login(self, username, password, should_work):
        """Test login scenarios using external data"""
        login_page = LoginPage(self.driver)
        login_page.login(username, password)

        if should_work:
            wait_for_visibility(self.driver, (By.CLASS_NAME, "title"))
            assert "/inventory.html" in self.driver.current_url, "URL should contain /inventory.html"
            page_title = get_text(self.driver, (By.CLASS_NAME, "title"))
            assert page_title == "Products", "Page title should be 'Products'"
        else:
            error_message = login_page.get_error_message()
            assert error_message, "Expected an error message for invalid login"
    
    def test_catalog_elements(self):
        """Test catalog page displays products and elements"""
        login_page = LoginPage(self.driver)
        login_page.login("standard_user", "secret_sauce")
        
        inventory_page = InventoryPage(self.driver)
        inventory_page.wait_until_loaded()
        
        page_title = inventory_page.get_title()
        assert page_title == "Products", "Page title should be 'Products'"
        
        assert inventory_page.get_products_count() > 0, "At least one product should be visible"
        
        first_product_name = inventory_page.get_first_product_name()
        assert first_product_name, "First product should have a name"
        
        first_product_price = inventory_page.get_first_product_price()
        assert first_product_price, "First product should have a price"
        
        assert inventory_page.is_menu_button_present(), "Menu button should be present"
        assert inventory_page.is_filter_dropdown_present(), "Filter dropdown should be present"
    
    @pytest.mark.parametrize("product_name", product_names)
    def test_add_to_cart(self, product_name):
        """Test adding a product to cart using external product data"""
        login_page = LoginPage(self.driver)
        login_page.login("standard_user", "secret_sauce")
        
        inventory_page = InventoryPage(self.driver)
        inventory_page.wait_until_loaded()
        inventory_page.add_product_to_cart_by_name(product_name)

        badge_count = None
        try:
            badge_count = inventory_page.get_cart_badge_count()
        except Exception:
            badge_count = None

        if badge_count is not None:
            assert badge_count == 1, "Cart badge should show 1 item"

        inventory_page.open_cart()

        assert "/cart.html" in self.driver.current_url, "URL should contain /cart.html"

        cart_page = CartPage(self.driver)
        cart_page.wait_until_loaded()

        assert cart_page.get_cart_items_count() == 1, "Cart should contain 1 item"
        assert cart_page.get_product_name() == product_name, "Expected correct product in cart"
