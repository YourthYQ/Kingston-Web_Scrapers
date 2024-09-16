import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

class ResponseHandler:
    @staticmethod
    def get_response(url):
        # Set up Selenium WebDriver
        options = Options()
        options.headless = True  # Run in headless mode

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        # Specify the path to the manually downloaded chromedriver
        # chromedriver_path = '/Users/yourth/.wdm/drivers/chromedriver/mac64/127.0.6533.88/chromedriver-mac-arm64/chromedriver'
        # driver = webdriver.Chrome(service=Service(chromedriver_path), options=options)
        
        driver.get(url)
        return driver

class ProductHandler:
    def __init__(self, first_page_url_list):
        self.first_page_url_list = first_page_url_list

    def get_page_number(self, first_page_url):
        """Get the total number of pages for a given product URL."""
        driver = ResponseHandler.get_response(first_page_url)
        div = driver.find_element(By.CSS_SELECTOR, 'div[style="float:left;padding-top:5px;"]')

        # Get the text inside the div element
        total_pages_text = div.text
        if total_pages_text:
            total_page = int(total_pages_text.split('/')[1].strip())
        else:
            total_page = 1

        # Close the driver
        driver.quit()

        # Testing
        print(total_page)
        return total_page
    
    def get_data_from_response(self):
        scraped_data = []
        url_roots = [
            'https://www.asrockrack.com/general/products-ajax.asp?Model=&Type=Server&CPU=&Category=&Usage=&Socket=&CPUnum=&DIMM=&Form=&BuildingBlocks=&Bricks=&Form2=&Acc=&Life=&p=',
            'https://www.asrockrack.com/general/products-ajax.asp?Model=&Type=WS&CPU=&Category=&Usage=&Socket=&CPUnum=&DIMM=&Form=&BuildingBlocks=&Bricks=&Form2=&Acc=&Life=&p='
        ]

        for url_root in url_roots:
            total_page = self.get_page_number(url_root + '1')
            for i in range(total_page):
                current_url = url_root + f'{i + 1}'

                # Testing
                # print(i+1)
                # print(current_url)

                driver = ResponseHandler.get_response(current_url)
                if driver:
                    products = driver.find_elements(By.CSS_SELECTOR, 'div.ModelName a')
                    
                    # Testing
                    print(products)
                    
                    for product in products:
                        title = product.text
                        product_url = product.get_attribute('href')
                        # Add to data output
                        scraped_data.append({
                            'Product Name': title,
                            'Product URL': product_url
                        })
                    driver.quit()
                else:
                    print(f"Failed to retrieve or parse data from {current_url}")

        df = pd.DataFrame(scraped_data)
        df.drop_duplicates(inplace=True)

        return df
    
    def export_to_excel(self, df, file_path):
        df.to_excel(file_path, index=False)
        print(f"Data has been exported to {file_path}")

if __name__ == "__main__":
    first_page_url_list = [
        'https://www.asrockrack.com/general/products-ajax.asp?Model=&Type=Server&CPU=&Category=&Usage=&Socket=&CPUnum=&DIMM=&Form=&BuildingBlocks=&Bricks=&Form2=&Acc=&Life=&p=1',
        'https://www.asrockrack.com/general/products-ajax.asp?Model=&Type=WS&CPU=&Category=&Usage=&Socket=&CPUnum=&DIMM=&Form=&BuildingBlocks=&Bricks=&Form2=&Acc=&Life=&p=1'
    ]
    product_handler = ProductHandler(first_page_url_list)
    df = product_handler.get_data_from_response()
    product_handler.export_to_excel(df, "test.xlsx")
