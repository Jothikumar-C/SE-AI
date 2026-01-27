from flask import Flask, render_template, jsonify

# STEP 1:
# Create Flask application object
# This represents our SERVER
print("STEP 1: Initializing Flask application...")
app = Flask(__name__)


# STEP 2:
# Define server-side data (mock database)
print("STEP 2: Loading product data into memory...")
products = [
    {"id": 1, "name": "Laptop", "price": 50000},
    {"id": 2, "name": "Mouse", "price": 500}
]


# STEP 3:
# Define server-side UI route (HTML page)
# This route returns a rendered HTML page
@app.route("/")
def home():
    print("\nSTEP 4: Browser requested '/' (UI page)")
    print("STEP 5: Rendering HTML template with product data")
    return render_template("index.html", products=products)


# STEP 6:
# Define REST API endpoint (JSON response)
@app.route("/api/products", methods=["GET"])
def products_api():
    print("\nSTEP 6: Client requested '/api/products' (REST API)")
    print("STEP 7: Returning product data as JSON")
    return jsonify(products)


# STEP 8:
# Start the Flask development server
if __name__ == "__main__":
    print("\nSTEP 8: Starting Flask development server...")
    print("STEP 9: Server listening at http://127.0.0.1:5000")
    print("STEP 10: Waiting for browser / API client requests...\n")

    app.run(host="0.0.0.0", port=5000, debug=True)
