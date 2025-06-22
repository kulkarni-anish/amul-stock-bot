from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import os
import time
from dotenv import load_dotenv

load_dotenv()

PRODUCT_URL = "https://shop.amul.com/en/browse/protein"
PINCODE = os.environ.get('PINCODE')
EMAIL = os.environ.get('EMAIL')
PASSWORD = os.environ.get('PASSWORD')
TO_EMAIL = os.environ.get('TO_EMAIL')

PRODUCT_NAMES = [
    "Amul Whey Protein, 32 g | Pack of 30 Sachets",
    "Amul Whey Protein Gift Pack, 32 g | Pack of 10 sachets",
    "Amul Chocolate Whey Protein, 34 g | Pack of 30 sachets",
    "Amul Kool Protein Milkshake | Kesar, 180 mL | Pack of 8"
]

def check_stock():
    options = Options()
    options.add_argument('--headless')  # Remove this line if you want to see the browser
    driver = webdriver.Chrome(options=options)
    driver.get(PRODUCT_URL)

    wait = WebDriverWait(driver, 15)

    # Wait until the pincode input is clickable (not just present)
    pincode_input = wait.until(EC.element_to_be_clickable((By.ID, "search")))
    pincode_input.clear()
    pincode_input.send_keys(PINCODE)
    time.sleep(1)  # Wait for dropdown to appear

    # 2. Wait for the dropdown and select the first result
    first_result = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#automatic .searchitem-name")))
    first_result.click()

    # 3. Wait for the modal to disappear and products to load
    wait.until(EC.invisibility_of_element_located((By.ID, "locationWidgetModal")))
    time.sleep(2)  # Give a little extra time for products to load

    # 4. Scrape the page
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    in_stock_products = []
    for product_name in PRODUCT_NAMES:
        product = None
        for item in soup.select('.product-grid-item'):
            name_tag = item.select_one('.product-grid-name a')
            if name_tag and product_name.lower() in name_tag.text.strip().lower():
                product = item
                break
        if not product:
            print(f"Product not found: {product_name}")
            continue
        sold_out = product.select_one('.stock-indicator-text')
        if sold_out and "sold out" in sold_out.text.strip().lower():
            print(f"Still sold out: {product_name}")
        else:
            print(f"In stock: {product_name}")
            in_stock_products.append(product_name)
    driver.quit()
    return in_stock_products

def send_email(in_stock_products):
    product_list = "\n".join(in_stock_products)
    msg = MIMEText(f'The following products are back in stock:\n\n{product_list}\n\nCheck them here: {PRODUCT_URL}')
    msg['Subject'] = 'Product(s) Back in Stock!'
    msg['From'] = EMAIL
    msg['To'] = TO_EMAIL
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(EMAIL, PASSWORD)
        server.sendmail(EMAIL, TO_EMAIL, msg.as_string())

if __name__ == '__main__':
    in_stock = check_stock()
    if in_stock:
        send_email(in_stock)
    else:
        print("No products in stock.")
