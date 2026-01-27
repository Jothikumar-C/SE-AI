from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time


def print_result(test_name, status):
    """Print Pass/Fail result for each test"""
    print(f"{test_name}: {'PASS' if status else 'FAIL'}")


def checkbox_test(driver, wait):
    try:
        # Navigate to Checkbox page
        checkbox_link = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/ul/li[6]/a'))
        )
        checkbox_link.click()

        # Locate first checkbox
        checkbox = wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="checkboxes"]/input[1]'))
        )

        # Select checkbox if not selected
        if not checkbox.is_selected():
            checkbox.click()

        print_result("Checkbox Test", checkbox.is_selected())

    except (TimeoutException, NoSuchElementException):
        print_result("Checkbox Test", False)


def drag_and_drop_test(driver, wait):
    try:
        # Navigate directly to Drag and Drop page
        driver.get("https://the-internet.herokuapp.com/drag_and_drop")

        source = wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="column-a"]'))
        )
        target = wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="column-b"]'))
        )

        # Perform drag and drop
        actions = ActionChains(driver)
        actions.click_and_hold(source).pause(1).move_to_element(target).pause(1).release().perform()

        # Validate result
        header_text = source.find_element(By.TAG_NAME, "header").text
        print_result("Drag and Drop Test", header_text == "B")

    except (TimeoutException, NoSuchElementException):
        print_result("Drag and Drop Test", False)


def horizontal_slider_test(driver, wait):
    try:
        # Navigate to Horizontal Slider page
        driver.get("https://the-internet.herokuapp.com/horizontal_slider")

        slider = wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="content"]/div/div/input'))
        )

        # Move slider to the right
        slider.click()
        for _ in range(5):
            slider.send_keys(Keys.ARROW_RIGHT)

        value = driver.find_element(By.ID, "range").text
        print_result("Horizontal Slider Test", float(value) > 0)

    except (TimeoutException, NoSuchElementException, ValueError):
        print_result("Horizontal Slider Test", False)


def main():
    # Chrome browser configuration
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)

    try:
        # Open base website
        driver.get("https://the-internet.herokuapp.com/")

        checkbox_test(driver, wait)
        time.sleep(3)
        drag_and_drop_test(driver, wait)
        time.sleep(3)
        horizontal_slider_test(driver, wait)
        time.sleep(3)

    finally:
        time.sleep(3)
        driver.quit()


if __name__ == "__main__":
    main()
