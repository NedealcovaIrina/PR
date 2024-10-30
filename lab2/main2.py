from flask import Flask, request, jsonify
import mysql.connector

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'Irina',
    'password': 'Ari.301203',
    'database': 'MySQL'
}

# Initialize the Flask application
app = Flask(__name__)


# Database connection function
def get_db_connection():
    connection = mysql.connector.connect(**db_config)
    return connection


# CREATE: Add a new product
@app.route('/product', methods=['POST'])
def create_product():
    data = request.json
    connection = get_db_connection()
    cursor = connection.cursor()

    insert_query = """
    INSERT INTO products (article, price, link, image_url, flags, brand)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    values = (data['article'], data['price'], data['link'], data['image_url'], data['flags'], data['brand'])

    cursor.execute(insert_query, values)
    connection.commit()

    product_id = cursor.lastrowid
    cursor.close()
    connection.close()

    return jsonify({'message': 'Product created', 'product_id': product_id}), 201


# READ: Get product by ID or name
@app.route('/product', methods=['GET'])
def get_product():
    product_id = request.args.get('id')
    article = request.args.get('article')
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    if product_id:
        cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
    elif article:
        cursor.execute("SELECT * FROM products WHERE article = %s", (article,))
    else:
        return jsonify({'error': 'No identifier provided'}), 400

    product = cursor.fetchone()
    cursor.close()
    connection.close()

    if product:
        return jsonify(product), 200
    else:
        return jsonify({'error': 'Product not found'}), 404


@app.route('/products', methods=['GET'])
def get_products():
    offset = request.args.get('offset', default=0, type=int)
    limit = request.args.get('limit', default=5, type=int)

    # Enforce a reasonable maximum limit
    MAX_LIMIT = 50
    if limit > MAX_LIMIT:
        limit = MAX_LIMIT

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    query = "SELECT * FROM products LIMIT %s OFFSET %s"
    cursor.execute(query, (limit, offset))

    products = cursor.fetchall()
    cursor.close()
    connection.close()

    return jsonify(products), 200


# UPDATE: Update a product by ID
@app.route('/product', methods=['PUT'])
def update_product():
    product_id = request.args.get('id')
    if not product_id:
        return jsonify({'error': 'Product ID required'}), 400

    data = request.json
    connection = get_db_connection()
    cursor = connection.cursor()

    update_query = """
    UPDATE products SET article = %s, price = %s, link = %s, image_url = %s, flags = %s, brand = %s
    WHERE id = %s
    """
    values = (data['article'], data['price'], data['link'], data['image_url'], data['flags'], data['brand'], product_id)

    cursor.execute(update_query, values)
    connection.commit()

    cursor.close()
    connection.close()

    return jsonify({'message': 'Product updated'}), 200


# DELETE: Delete a product by ID
@app.route('/product', methods=['DELETE'])
def delete_product():
    product_id = request.args.get('id')
    if not product_id:
        return jsonify({'error': 'Product ID required'}), 400

    connection = get_db_connection()
    cursor = connection.cursor()

    delete_query = "DELETE FROM products WHERE id = %s"
    cursor.execute(delete_query, (product_id,))
    connection.commit()

    cursor.close()
    connection.close()

    return jsonify({'message': 'Product deleted'}), 200


# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
