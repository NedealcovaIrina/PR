import requests
from bs4 import BeautifulSoup

# URL of the website
url = 'https://nlcollection.md/'

# Headers to mimic a browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
}

try:
    # Send GET request with headers
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        print("Request successful!")
        html_content = response.text

        # Step 1: Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Step 2: Find all product elements
        products = soup.find_all('div', class_='product')

        if not products:
            print("No products found. The structure might have changed.")

        # Step 3: Extract product details (name/article number, price, and link)
        for product in products:
            # Extract the product article (acting as the product "name")
            article = product.find('div', class_='product__article')
            if article:
                article_text = article.get_text(strip=True)
            else:
                article_text = "No article found"

            # Extract the product price
            price = product.find('div', class_='product__price__current')
            if price:
                price_text = price.get_text(strip=True)
            else:
                price_text = "No price found"

            # Extract the product link (href from the <a> tag)
            link = product.find('a', class_='product__link')
            if link:
                product_link = f"https://nlcollection.md{link['href']}"
            else:
                product_link = "No link found"

            # Print or store the product details
            print(f"Product Article: {article_text}")
            print(f"Price: {price_text}")
            print(f"Link: {product_link}")
            print("=" * 40)

    else:
        print(f"Failed to retrieve content. Status code: {response.status_code}")

except requests.exceptions.RequestException as e:
    print(f"Error during requests to {url}: {e}")
