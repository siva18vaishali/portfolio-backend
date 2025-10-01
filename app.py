from flask import Flask, request, jsonify
from flask_mail import Mail, Message
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # 👈 allow requests from React frontend

CORS(app, origins=[
    "https://portfolio-gray-six-40.vercel.app/",  # ⬅️ Replace this with your actual Vercel URL
    "http://localhost:3000"
])

# Configure Flask-Mail using environment variables
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', 'siva04vaishali@gmail.com')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', '')  # Will be set in Render
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_USERNAME', 'siva04vaishali@gmail.com')

mail = Mail(app)

@app.route("/")
def home():
    return jsonify({"message": "Backend is running!"})

@app.route("/contact", methods=["POST"])
def contact():
    data = request.json
    name = data.get("name")
    email = data.get("email")
    message = data.get("message")

    # Validation
    if not all([name, email, message]):
        return jsonify({"success": False, "message": "All fields are required"}), 400

    try:
        # Create email message
        msg = Message(
            subject=f"New Contact Form Submission from {name}",
            recipients=["siva04vaishali@gmail.com"],  # Where you want to receive emails
            body=f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
        )
        mail.send(msg)

        return jsonify({"success": True, "message": "Message sent successfully!"}), 200
    except Exception as e:
        print("Error:", e)
        return jsonify({"success": False, "message": "Failed to send message."}), 500

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)