import socket
import ssl
from bs4 import BeautifulSoup
from functools import reduce
from datetime import datetime

# URL parameters
host = 'nlcollection.md'
port = 443  # HTTPS uses port 443

# Exchange rate (MDL to EUR)
exchange_rate = 0.05  # Example rate; update as necessary

# Create TCP connection to the server and wrap it in SSL for HTTPS
def create_tcp_connection(host, port):
    context = ssl.create_default_context()  # Create SSL context for secure connection
    sock = socket.create_connection((host, port))  # Create TCP connection
    ssock = context.wrap_socket(sock, server_hostname=host)  # Wrap in SSL
    return ssock  # Return SSL-wrapped socket

# Function to send HTTP request
def send_http_request(connection):
    # HTTP request for the main page
    request = f"GET / HTTP/1.1\r\nHost: {host}\r\nUser-Agent: CustomClient/1.0\r\nConnection: close\r\n\r\n"
    connection.send(request.encode())  # Send the request via the connection

# Function to receive the response from the server
def receive_response(connection):
    response = b""  # Initialize an empty byte string to accumulate response
    while True:
        data = connection.recv(4096)  # Receive 4KB chunks of data
        if not data:
            break  # Exit loop if no more data
        response += data  # Accumulate data chunks
    return response.decode()  # Decode bytes to string

# Function to validate product price
def validate_price(price_text):
    try:
        cleaned_price = ''.join(filter(str.isdigit, price_text))  # Remove non-digit characters
        return int(cleaned_price) > 0  # Ensure price is greater than zero
    except ValueError:
        return False  # Return False if conversion fails

# Function to validate product article
def validate_article(article_text):
    return bool(article_text and article_text.strip() and any(char.isalnum() for char in article_text))  # Check if article is valid

# Function to convert MDL to EUR
def convert_to_euro(price_mdl):
    return round(price_mdl * exchange_rate, 2)  # Convert price from MDL to EUR

# Create TCP connection and send the request
connection = create_tcp_connection(host, port)
send_http_request(connection)

# Receive the response
response = receive_response(connection)
connection.close()  # Close the connection

# Find the start of the HTML content (skip headers)
html_start = response.find('<!DOCTYPE')  # Locate the beginning of HTML content
html_content = response[html_start:]  # Extract the HTML content

# Check if HTML was extracted correctly
if html_content:
    print("Request successful!")
    print(f"Here is the link to the main page: https://{host}/")

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')  # Parse the HTML content

    # Find all product elements
    products = soup.find_all('div', class_='product')  # Find all product blocks

    # Debug: Check how many products are found
    print(f"Number of products found: {len(products)}")

    # Function to extract product details
    def extract_product(product):
        article = product.find('div', class_='product__article')  # Find article
        article_text = article.get_text(strip=True) if article else None  # Get article text

        price = product.find('div', class_='product__price__current')  # Find current price
        price_text = price.get_text(strip=True) if price else None  # Get price text

        link = product.find('a', class_='product__link')  # Find product link
        product_link = f"https://nlcollection.md{link['href']}" if link else "No link found"  # Get product link

        image = product.find('img', class_='product__image')  # Find product image
        image_url = f"https://nlcollection.md{image['src']}" if image else "No image found"  # Get image URL

        flags = product.find('div', class_='product__flags')  # Find product flags
        flag_text = flags.get_text(strip=True) if flags else "No flags found"  # Get flag text

        brand = product.find('div', class_='product__brand')  # Find brand
        brand_text = brand.get_text(strip=True) if brand else "No brand available"  # Get brand name

        # Ensure price is valid and convert to integer
        price_mdl = int(''.join(filter(str.isdigit, price_text))) if price_text and validate_price(price_text) else None  # Validate and parse price

        return {
            "article": article_text,
            "price_mdl": price_mdl,  # Original price in MDL
            "price_text": f"{price_mdl}MDL" if price_mdl else "No price available",  # Price as text
            "price_eur": convert_to_euro(price_mdl) if price_mdl else None,  # Price in EUR
            "link": product_link,  # Product link
            "image_url": image_url,  # Image URL
            "flags": flag_text,  # Flags
            "brand": brand_text,  # Brand
        }

    # Extract all product details
    products_data = list(map(extract_product, products))  # Map products to details

    # Filter products with valid prices and within the range 10 - 3000 MDL
    filtered_products = list(
        filter(lambda p: p['price_mdl'] is not None and 10 <= p['price_mdl'] <= 3000, products_data))  # Filter products by price range

    # Debug: Check how many products are filtered
    print(f"Number of filtered products: {len(filtered_products)}")

    # Sort products by price in EUR
    filtered_products.sort(key=lambda x: x['price_eur'])  # Sort filtered products by EUR price

    # Calculate total price in EUR using reduce
    total_price_eur = reduce(lambda acc, p: acc + p['price_eur'], filtered_products, 0)  # Sum total prices in EUR

    # Output the filtered and processed data
    for product in filtered_products:
        print(f"Product Article: {product['article']}")
        print(f"Price: {product['price_text']}")  # Original price in MDL
        print(f"Price (EUR): {product['price_eur']}")
        print(f"Link: {product['link']}")
        print(f"Image URL: {product['image_url']}")
        print(f"Flags: {product['flags']}")
        print(f"Brand: {product['brand']}")
        print("=" * 50)

    print(f"Total Price (EUR) of Filtered Products: {total_price_eur:.2f}")  # Print total price in EUR
    print(f"Timestamp: {datetime.utcnow().isoformat()}")  # Print timestamp in UTC format

else:
    print("Failed to retrieve valid HTML content.")  # Error if no valid content
