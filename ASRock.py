import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Define the ProductHandler class
class ProductHandler:
    def __init__(self, products_urls):
        self.products_urls = products_urls
    
    def get_data_from_response(self):
        list_of_urls = self.products_urls
        scraped_data = []
        
        # Set up Selenium WebDriver with headless option
        options = Options()
        options.add_argument('--headless')  # Run in headless mode
        options.add_argument('--disable-gpu')  # Disable GPU acceleration
        options.add_argument('--no-sandbox')  # Bypass OS security model
        options.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems
        
        # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        # Specify the path to the manually downloaded chromedriver
        chromedriver_path = '/Users/yourth/.wdm/drivers/chromedriver/mac64/127.0.6533.88/chromedriver-mac-arm64/chromedriver'
        driver = webdriver.Chrome(service=Service(chromedriver_path), options=options)
        
        for url in list_of_urls:
            driver.get(url)
            
            # Extract products with series
            multiple_products = driver.find_elements(By.CSS_SELECTOR, 'div.AllModelList ul li a')
            if not multiple_products:
                print(f"No products found at {url}")
            for element in multiple_products:
                title = element.text.strip()
                product_url = element.get_attribute('href')
                
                # Add to data output
                if product_url:
                    scraped_data.append({
                        'Product Name': title,
                        'Product URL': product_url
                    })
        
        driver.quit()

        df = pd.DataFrame(scraped_data)
        df.drop_duplicates(inplace=True)

        return df
    
    def export_to_excel(self, df, file_path):
        df.to_excel(file_path, index=False)
        print(f"Data has been exported to {file_path}")

if __name__ == "__main__":
    products_urls = [
        'https://www.asrock.com/mb/index.us.asp#AllProduct',
        'https://www.asrock.com/nettop/index.us.asp#AllProduct'
    ]
    product_handler = ProductHandler(products_urls)
    final_df = product_handler.get_data_from_response()
    product_handler.export_to_excel(final_df, "test.xlsx")