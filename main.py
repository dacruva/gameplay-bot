from selenium import webdriver
from selenium.webdriver.common.by import By


import time

# ... (Chrome options setup remains the same)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get("http://orteil.dashnet.org/experiments/cookie/")

# Explicit Wait for Cookie Element (more reliable)
cookie = driver.find_element(by=By.ID, value="cookie")

# Get upgrade item ids only once (they don't change)
item_elements = driver.find_elements(By.CSS_SELECTOR, "#store div")
item_ids = [item.get_attribute("id") for item in item_elements]

timeout = time.time() + 15
five_min = time.time() + 60 * 5

while True:
    cookie.click()

    if time.time() > timeout:
        # Optimized price extraction and filtering
        item_prices = [
            int(price.text.split("-")[1].strip().replace(",", ""))
            for price in driver.find_elements(By.CSS_SELECTOR, "#store b")
            if price.text
        ]

        # Create dictionary in one step
        cookie_upgrades = {
            price: item_ids[i] for i, price in enumerate(item_prices)
        }

        money_element = driver.find_element(By.ID, "money").text
        cookie_count = int(money_element.replace(",", ""))

        # Direct purchase based on affordable upgrades
        affordable_ids = {}
        for cost, id1 in cookie_upgrades.items():
            if cookie_count > cost:
                affordable_ids[cost] = id1

        if affordable_ids:  # Only click if upgrades are available
            to_purchase_id = cookie_upgrades[max(affordable_ids)]
            driver.find_element(By.ID, to_purchase_id).click()

        timeout = time.time() + 5

    if time.time() > five_min:
        cookie_per_s = driver.find_element(By.ID, "cps").text
        print(cookie_per_s)
        break
