import sys
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options

# FuelTypeDDL, 37 is unleaded
# url = 'https://www.racq.com.au/cars-and-driving/driving/fair-fuel-prices?phracq_body_1_phracq_contentcontainer_0_FuelTypesDDL=37&location=4122&locationTypeId=2'
url = 'https://www.racq.com.au/cars-and-driving/driving/fair-fuel-prices?phracq_body_1_phracq_contentcontainer_0_FuelTypesDDL=37&location=4000&locationTypeId=2'

browser = Firefox()
response = browser.get(url)

element = browser.find_element_by_xpath("//tbody[@class='fn_fuelResults']")
# items = element.find_elements_by_xpath("//tr")
# print(len(items))
print('name, price, address, time')
for item in element.find_elements_by_xpath(".//tr"):
    shop_name = item.find_element_by_xpath(".//td[1]/p")
    fuel_price = item.find_element_by_xpath(".//td[1]/span")
    address = item.find_element_by_xpath(".//td[2]")
    time = item.find_element_by_xpath(".//td[3]")

    try:
        if float(fuel_price.text):
            shop_name = shop_name.text
            fuel_price = fuel_price.text
            address = address.text.replace('\n', ' ')
            time = time.text.split('\n')[0].replace(',', '')

            print('{}, {}, {}, {}'.format(shop_name, fuel_price, 
                address, time))
    except:
        print(shop_name.text)
        browser.close()
        sys.exit(0)

browser.close()
