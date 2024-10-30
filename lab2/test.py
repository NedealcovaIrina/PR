import requests
import json

# Base URLs for the Flask API
base_product_url = "http://127.0.0.1:5000/product"
base_products_url = "http://127.0.0.1:5000/products"

# Test data
test_product = {
    "article": "Test Article",
    "price": "12.99 MDL",
    "link": "https://nlcollection.md/test",
    "image_url": "https://nlcollection.md/test-image.jpg",
    "flags": "Sale",
    "brand": "Test Brand"
}


# 1. Create a new product (POST request)
def test_create_product():
    response = requests.post(base_product_url, json=test_product)
    print("Create Product Response:", response.json())
    return response.json().get("product_id")  # Return the product ID for further tests


# 2. Get product by ID (GET request)
def test_get_product_by_id(product_id):
    response = requests.get(f"{base_product_url}?id={product_id}")
    print("Get Product by ID Response:", response.json())


# 3. Get product by article (GET request)
def test_get_product_by_article(article):
    response = requests.get(f"{base_product_url}?article={article}")
    print("Get Product by Article Response:", response.json())


# 4. Update a product (PUT request)
def test_update_product(product_id):
    updated_product = {
        "article": "Updated Article",
        "price": "15.99 MDL",
        "link": "https://nlcollection.md/updated",
        "image_url": "https://nlcollection.md/updated-image.jpg",
        "flags": "New",
        "brand": "Updated Brand"
    }
    response = requests.put(f"{base_product_url}?id={product_id}", json=updated_product)
    print("Update Product Response:", response.json())


# 5. Delete a product (DELETE request)
def test_delete_product(product_id):
    response = requests.delete(f"{base_product_url}?id={product_id}")
    print("Delete Product Response:", response.json())


# 6. Get all products with optional pagination (GET request)
def test_get_all_products(offset=0, limit=5):
    response = requests.get(f"{base_products_url}?offset={offset}&limit={limit}")

    # Check if the response is successful and contains JSON data
    if response.status_code == 200:
        try:
            # Attempt to parse JSON response
            print("Get All Products Response:", response.json())
        except json.JSONDecodeError:
            # If JSON parsing fails, print the raw text response
            print("Get All Products Response (Non-JSON):", response.text)
    else:
        print(f"Failed to retrieve products. Status code: {response.status_code}")
        print("Response Text:", response.text)


# Run tests
if __name__ == "__main__":
    # Test creating a product
    product_id = test_create_product()

    if product_id:
        # Test retrieving the product by ID
        test_get_product_by_id(product_id)

        # Test retrieving the product by article
        test_get_product_by_article(test_product["article"])

        # Test updating the product
        test_update_product(product_id)

        # Test deleting the product
        test_delete_product(product_id)

        # Test retrieving all products with pagination
        test_get_all_products(offset=0, limit=5)
        test_get_all_products(offset=5, limit=5)  # Example of using different offset and limit

    else:
        print("Failed to create product. Cannot proceed with further tests.")
