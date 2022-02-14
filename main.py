from playwright.sync_api import sync_playwright
import json
import csv

data_csv = []
data_json = []

def scrape_data():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://finance.yahoo.com/most-active/")
        stock_codes = page.query_selector_all("//a[@class='Fw(600) C($linkColor)']")
        stock_names = page.query_selector_all("//td[@class='Va(m) Ta(start) Px(10px) Fz(s)']")
        stock_prices = page.query_selector_all("//tbody/tr/td[3]/fin-streamer")
        stock_volumes = page.query_selector_all("//td[@class='Va(m) Ta(end) Pstart(20px) Fz(s)']/fin-streamer")

        count = len(stock_codes)
        for x in range(count):
            code = stock_codes[x].inner_text()
            name = stock_names[x].inner_text()
            price = stock_prices[x].inner_text()
            volume = stock_volumes[x].inner_text()
            # CSV
            content_csv = [code, name, price, volume]
            data_csv.append(content_csv)
            # JSON
            content_json = {
                'code': code,
                'name': name,
                'price': price,
                'volume': volume
            }
            data_json.append(content_json)


        browser.close()

def storing_csv():
    with open('data.csv', mode='w', newline='', encoding="utf-8") as csv_file:
        # Create object
        writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        # Write
        writer.writerow(["CODE", "NAME", "PRICE", "VOLUME"])
        for d in data_csv:
            writer.writerow(d)
    print("Writing to CSV has been successful !")

def storing_json():
    # Serializing json
    json_object = json.dumps(data_json, indent=4)
    with open("data.json", "w") as outfile:
        outfile.write(json_object)
    print("Writing to JSON has been successful !")


scrape_data()
storing_csv()
storing_json()