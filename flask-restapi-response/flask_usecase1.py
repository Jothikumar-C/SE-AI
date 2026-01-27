from flask import Flask, jsonify

# STEP 1: Create Flask application
print("STEP 1: Initializing Flask application...")
app = Flask(__name__)


# STEP 2: Mock database (server-side data)
print("STEP 2: Loading in-memory user data...")
users = {
    1: {"name": "Jothi", "role": "Admin"},
    2: {"name": "Kumar", "role": "User"}
}


# STEP 3: Define REST API route
@app.route("/api/user/<int:user_id>", methods=["GET"])
def get_user(user_id):
    print("\nSTEP 4: Received a GET request")
    print(f"STEP 5: Requested user_id = {user_id}")

    # STEP 6: Fetch user from mock database
    user = users.get(user_id)

    if user:
        print("STEP 6A: User found in database")
        print("STEP 7: Sending SUCCESS response (200)")
        return jsonify(user)

    # User not found
    print("STEP 6B: User NOT found in database")
    print("STEP 7: Sending ERROR response (404)")
    return jsonify({"error": "User not found"}), 404


# STEP 8: Start the Flask server
if __name__ == "__main__":
    print("\nSTEP 8: Starting Flask development server...")
    print("STEP 9: Server will listen on http://127.0.0.1:5000")
    print("STEP 10: Waiting for incoming client requests...\n")

    app.run(host="0.0.0.0", port=5000, debug=True)