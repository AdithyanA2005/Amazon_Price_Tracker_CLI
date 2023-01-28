import csv
import time
import requests
from bs4 import BeautifulSoup


def get_price(url):
    """
    Returns the current price of the product at the specified URL.
    """
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    price_elem = soup.find('span', {'class': 'a-price-whole'})
    if price_elem:
        return float(price_elem.text[:].replace(',', ''))
    return None


def check_price_drop(url):
    """
    Checks if the price of the product at the specified URL has dropped
    since the last time this function was called. If it has, the new price
    and the difference in price are printed to the console.
    """
    with open('prices.csv', 'a+', newline='') as csvfile:
        csvfile.seek(0)
        reader = csv.reader(csvfile)
        rows = [row for row in reader]

        if rows:
            # Get the price of the product from the last time this function was called
            old_price = float(rows[-1][1])
        
            # Get the current price of the product
            current_price = get_price(url)
        
            # Calculate the price difference
            price_diff = old_price - current_price
        
            if price_diff > 0:
                # If the price has dropped, print the new price and the price difference
                print(f'Price drop! The new price is ₹{current_price:.2f} ({price_diff:.2f} cheaper)')
            else:
                print(f'No price drop. Current price is ₹{current_price:.2f}')
        
            # Write the current price to the CSV file
            writer = csv.writer(csvfile)
            writer.writerow([time.time(), current_price])
        else:
            # If the CSV file is empty, write the initial price to it
            initial_price = get_price(url)
            print(f'Initial price is ₹{initial_price:.2f}')
            writer = csv.writer(csvfile)
            writer.writerow([time.time(), initial_price])


def main():
    url = input("Enter product URL: ") or "https://www.amazon.in/dp/B08C56KXQJ"
    # Call the check_price_drop function every hour
    while True:
        check_price_drop(url)
        time.sleep(3600)

if __name__ == '__main__':
    main()
