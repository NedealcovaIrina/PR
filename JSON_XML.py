import requests
from bs4 import BeautifulSoup
from functools import reduce
from datetime import datetime

# URL of the website
url = 'https://nlcollection.md/'

# Headers to mimic a browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
}

# Exchange rate (MDL to EUR) - Update with the current rate
exchange_rate = 0.05  # Example rate; update as necessary


# Function to validate product price
def validate_price(price_text):
    try:
        cleaned_price = ''.join(filter(str.isdigit, price_text))
        return int(cleaned_price) > 0  # Ensure price is greater than zero
    except ValueError:
        return False


# Function to validate product article
def validate_article(article_text):
    return bool(article_text and article_text.strip() and any(char.isalnum() for char in article_text))


# Function to convert MDL to EUR
def convert_to_euro(price_mdl):
    return round(price_mdl * exchange_rate, 2)


# Function to serialize products to JSON format
def serialize_to_json(data):
    json_str = "{\n"
    json_str += f'  "timestamp": "{data["timestamp"]}",\n'
    json_str += f'  "total_price_eur": {data["total_price_eur"]},\n'
    json_str += '  "products": [\n'
    for product in data["products"]:
        json_str += "    {\n"
        json_str += f'      "article": "{product["article"]}",\n'
        json_str += f'      "price_mdl": {product["price_mdl"]},\n'
        json_str += f'      "price_eur": {product["price_eur"]},\n'
        json_str += f'      "link": "{product["link"]}",\n'
        json_str += f'      "image_url": "{product["image_url"]}",\n'
        json_str += f'      "flags": "{product["flags"]}",\n'
        json_str += f'      "brand": "{product["brand"]}"\n'
        json_str += "    },\n"
    json_str = json_str.rstrip(",\n")  # Remove the last comma
    json_str += "\n  ]\n"
    json_str += "}"
    return json_str


# Function to serialize products to XML format
def serialize_to_xml(data):
    xml_str = "<data>\n"
    xml_str += f'  <timestamp>{data["timestamp"]}</timestamp>\n'
    xml_str += f'  <total_price_eur>{data["total_price_eur"]}</total_price_eur>\n'
    xml_str += '  <products>\n'
    for product in data["products"]:
        xml_str += "    <product>\n"
        xml_str += f'      <article>{product["article"]}</article>\n'
        xml_str += f'      <price_mdl>{product["price_mdl"]}</price_mdl>\n'
        xml_str += f'      <price_eur>{product["price_eur"]}</price_eur>\n'
        xml_str += f'      <link>{product["link"]}</link>\n'
        xml_str += f'      <image_url>{product["image_url"]}</image_url>\n'
        xml_str += f'      <flags>{product["flags"]}</flags>\n'
        xml_str += f'      <brand>{product["brand"]}</brand>\n'
        xml_str += "    </product>\n"
    xml_str += "  </products>\n"
    xml_str += "</data>"
    return xml_str


# Send GET request with headers
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    print("Request successful!")
    print("Here is the link to the main page: https://nlcollection.md/")
    html_content = response.text

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all product elements
    products = soup.find_all('div', class_='product')


    # Function to extract product details
    def extract_product(product):
        article = product.find('div', class_='product__article')
        article_text = article.get_text(strip=True) if article else None

        price = product.find('div', class_='product__price__current')
        price_text = price.get_text(strip=True) if price else None

        link = product.find('a', class_='product__link')
        product_link = f"https://nlcollection.md{link['href']}" if link else "No link found"

        image = product.find('img', class_='product__image')
        image_url = f"https://nlcollection.md{image['src']}" if image else "No image found"

        flags = product.find('div', class_='product__flags')
        flag_text = flags.get_text(strip=True) if flags else "No flags found"

        brand = product.find('div', class_='product__brand')
        brand_text = brand.get_text(strip=True) if brand else "No brand available"

        price_mdl = int(''.join(filter(str.isdigit, price_text))) if price_text and validate_price(price_text) else None

        return {
            "article": article_text,
            "price_mdl": price_mdl,
            "price_eur": convert_to_euro(price_mdl) if price_mdl else None,
            "link": product_link,
            "image_url": image_url,
            "flags": flag_text,
            "brand": brand_text,
        }


    # Extract all product details
    products_data = list(map(extract_product, products))

    # Filter products with valid prices and within the range 10 - 3000 MDL
    filtered_products = list(
        filter(lambda p: p['price_mdl'] is not None and 10 <= p['price_mdl'] <= 3000, products_data))

    # Sort products by price in EUR
    filtered_products.sort(key=lambda x: x['price_eur'])

    # Calculate total price in EUR using reduce
    total_price_eur = reduce(lambda acc, p: acc + p['price_eur'], filtered_products, 0)

    # Current UTC timestamp
    timestamp_utc = datetime.utcnow().isoformat()

    # New data model with products and total price
    result = {
        "timestamp": timestamp_utc,
        "total_price_eur": total_price_eur,
        "products": filtered_products
    }

    # Serialize to JSON
    json_output = serialize_to_json(result)
    print("JSON Output:")
    print(json_output)

    # Serialize to XML
    xml_output = serialize_to_xml(result)
    print("\nXML Output:")
    print(xml_output)


    def custom_serialize(obj):
        """
        Serializes an object (list, dictionary, string, integer, etc.) into a custom string format.
        """
        if isinstance(obj, dict):
            serialized_items = []
            for key, value in obj.items():
                key_serialized = f'Key-{{{custom_serialize(key)}}}'
                value_serialized = f'Val-{{{custom_serialize(value)}}}'
                serialized_items.append(f'{key_serialized}:: {value_serialized}')
            return '{' + ', '.join(serialized_items) + '}'

        elif isinstance(obj, list):
            serialized_items = [f'[{i}]:{custom_serialize(item)}' for i, item in enumerate(obj)]
            return '[' + ', '.join(serialized_items) + ']'

        elif isinstance(obj, str):
            return f'STR:"{obj}"'

        elif isinstance(obj, int):
            return f'INT:{obj}'

        elif isinstance(obj, float):
            return f'FLOAT:{obj}'

        else:
            raise TypeError(f"Unsupported type: {type(obj)}")


    serialized_data = custom_serialize(result)
    print(serialized_data)


else:
    print(f"Failed to retrieve content. Status code: {response.status_code}")
