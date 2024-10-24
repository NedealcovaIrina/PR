import requests
from bs4 import BeautifulSoup
import mysql.connector
from mysql.connector import Error

# MySQL connection details from Railway
host = 'junction.proxy.rlwy.net',
port = 14991,
database = 'railway',
user = 'root',
password = 'SPHewFvAGywXaLPjYYFkiODwDOznMcFc'


# Function to connect to MySQL database
def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host='junction.proxy.rlwy.net',
            port=14991,
            database='railway',
            user='root',
            password='SPHewFvAGywXaLPjYYFkiODwDOznMcFc'
        )
        print("MySQL connection successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


# Function to create a table in the database
def create_table(connection):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS products (
        id INT AUTO_INCREMENT PRIMARY KEY,
        article VARCHAR(255) NOT NULL,
        price VARCHAR(255) DEFAULT NULL,
        link VARCHAR(255) NOT NULL,
        image_url VARCHAR(255),
        flags VARCHAR(255),
        brand VARCHAR(255),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    try:
        cursor = connection.cursor()
        cursor.execute(create_table_query)
        print("Table 'products' created successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


# Function to insert product data into the table
def insert_product(connection, product):
    insert_query = """
    INSERT INTO products (article, price, link, image_url, flags, brand)
    VALUES (%s, %s, %s, %s, %s, %s);
    """
    try:
        cursor = connection.cursor()
        cursor.execute(insert_query, product)
        connection.commit()
        print(f"Product {product[0]} inserted successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


# URL of the website
url = 'https://nlcollection.md/'

# Headers to mimic a browser request
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

    # Step 3: Connect to the MySQL database and create the table
    connection = create_connection()
    if connection:
        create_table(connection)

        # Step 4: Extract product details and insert them into the database
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

            # Prepare the product data for insertion
            product_data = (
                article_text,
                price_text,
                product_link,
                image_url,
                flag_text,
                brand_text
            )

            # Insert the product data into the database
            insert_product(connection, product_data)

        # Close the connection
        if connection.is_connected():
            connection.close()
            print("MySQL connection closed")
else:
    print(f"Failed to retrieve content. Status code: {response.status_code}")
