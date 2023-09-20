from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Initialize the WebDriver (I'm using Firefox in this example)
driver = webdriver.Firefox()

# 1. Launch the application URL
driver.get("https://www.bt.com/")
driver.implicitly_wait(3)

# 2. Close accept Cookie pop-up if it appears
try:
    driver.switch_to.frame(0)
    accept_cookie = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@tabindex='0'][1]"))
    )
    accept_cookie.click()
    driver.switch_to.default_content()
except:
    pass  # Continue even if the pop-up is not present

# 3. Hover to Mobile menu
mobile_menu = driver.find_element(By.XPATH, "//a[@data-di-id='di-id-7c56fcc8-3103e56f']")
ActionChains(driver).move_to_element(mobile_menu).perform()
time.sleep(3)

# 4. From mobile menu, Select Mobile phones
mobile_phones_option = driver.find_element(By.LINK_TEXT, "Mobile phones")
mobile_phones_option.click()

# 5. Verify the number of banners present below "See Handset details" should not be less than 3
banners = driver.find_elements(By.XPATH, "//div[@class='flexpay-card_card_wrapper__Antym']")
assert len(banners) >= 3, "Number of banners is less than 3"

# 6. Scroll down and click View SIM only deals
View_SIM_only_deals = driver.find_element(By.XPATH,"//a[@class='bt-btn bt-btn-primary']")
driver.execute_script("arguments[0].scrollIntoView();", View_SIM_only_deals)
View_SIM_only_deals.click()

# 7. Validate the title for the new page
expected_title = "Mobile phone deals | New mobiles and Pay Monthly | BT Mobile"
actual_title = driver.title
assert expected_title in actual_title, f"Expected title: {expected_title}, Actual title: {actual_title}"

# 8. Validate "30% off and double data” was 125GB 250GB Essential Plan, was £27 £18.90 per month
ValidationElement = driver.find_element(By.XPATH, "(//div[@class='simo-card-ee_text_container__30ltg'])[13]").is_displayed()
assert ValidationElement, 'No such offer present'

# 9. Close the browser & exit
driver.close()
