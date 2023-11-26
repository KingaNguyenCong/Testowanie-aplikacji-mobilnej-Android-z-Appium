import random
import unittest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CalculatorTests(unittest.TestCase):
    def setUp(self):
        options = UiAutomator2Options()
        options.platform_name = 'Android'
        options.device_name = 'emulator-5554'  # Zmień na nazwę Twojego urządzenia lub emulatora
        options.app_package = 'com.example.myapplication'  # Zaktualizuj nazwę pakietu aplikacji
        options.app_activity = '.MainActivity'  # Zaktualizuj nazwę aktywności, jeśli jest inna
        options.automation_name = 'UiAutomator2'

        self.driver = webdriver.Remote('http://localhost:4723', options=options)

    def test_calculator(self):
        for c in ['+', '-', '*', '/']:
            for _ in range(10):
                a = random.randint(0, 999)
                if c != '/':
                    b = random.randint(0, 999)
                else:
                    b = random.randint(1, 999)
                buttons = str(a) + c + str(b) + '='
                if c == '+':
                    correct = a + b
                elif c == '-':
                    correct = a - b
                elif c == '*':
                    correct = a * b
                elif c == '/':
                    correct = a / b
                for button in buttons:
                    self.click_button(button)

                result_element = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((AppiumBy.XPATH, "//*[contains(@text, 'Wynik:')]"))
                )

                result_correct = float(correct)
                result = float(result_element.text.split("Wynik: ")[1])
                self.assertEqual(result, result_correct)

                self.click_button('C')

    def click_button(self, label):
        button_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Przycisk " + label))
        )
        button_element.click()

    def tearDown(self):
        if self.driver:
            self.driver.quit()


if __name__ == '__main__':
    unittest.main()

