import requests
from bs4 import BeautifulSoup
import mysql.connector

# Database configuration
db_config = {
    'host': 'localhost',            # Replace with your MySQL host
    'user':'Irina',        # Replace with your MySQL username
    'password': 'Ari.301203',    # Replace with your MySQL password
    'database': 'MySQL'     # Replace with your MySQL database name
}

# Connect to the MySQL database
connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()

# SQL statement to create the 'products' table
create_table_query = """
CREATE TABLE IF NOT EXISTS products (
    id INT PRIMARY KEY AUTO_INCREMENT,
    article VARCHAR(255) NOT NULL,
    price VARCHAR(50),
    link TEXT NOT NULL,
    image_url TEXT,
    flags VARCHAR(100),
    brand VARCHAR(100),
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
"""

# Execute the query to create the table
cursor.execute(create_table_query)
connection.commit()
print("Table created successfully.")

# Function to insert a product into the database
def insert_product(article, price, link, image_url, flags, brand):
    cursor = connection.cursor()
    insert_query = """
    INSERT INTO products (article, price, link, image_url, flags, brand)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    values = (article, price, link, image_url, flags, brand)
    cursor.execute(insert_query, values)
    connection.commit()
    print(f"Product '{article}' inserted successfully.")
    cursor.close()

# Scraping logic
url = 'https://nlcollection.md/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
}

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

    # Step 3: Extract and insert product details
    for product in products:
        # Extract the product article
        article = product.find('div', class_='product__article')
        article_text = article.get_text(strip=True) if article else "No article found"

        # Extract the product price
        price = product.find('div', class_='product__price__current')
        price_text = price.get_text(strip=True) if price else "No price found"

        # Extract the product link
        link = product.find('a', class_='product__link')
        product_link = f"https://nlcollection.md{link['href']}" if link else "No link found"

        # Extract the image URL
        image = product.find('img', class_='product__image')
        image_url = f"https://nlcollection.md{image['src']}" if image else "No image found"

        # Extract flags (e.g., "New")
        flags = product.find('div', class_='product__flags')
        flag_text = flags.get_text(strip=True) if flags else "No flags found"

        # Extract brand
        brand = product.find('div', class_='product__brand')
        brand_text = brand.get_text(strip=True) if brand else "No brand available"

        # Insert into the database
        insert_product(article_text, price_text, product_link, image_url, flag_text, brand_text)

else:
    print(f"Failed to retrieve content. Status code: {response.status_code}")

# Close the database connection
connection.close()
print("Database connection closed.")
