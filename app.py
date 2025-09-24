from flask import Flask, request, jsonify
from flask_mail import Mail, Message
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 👈 allow requests from React frontend

# Configure Flask-Mail (using Gmail SMTP here)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = "siva04vaishali@gmail.com"   # <-- replace with your email
app.config['MAIL_PASSWORD'] = "swfl yxgf lujr nxmg"      # <-- use Gmail App Password
app.config['MAIL_DEFAULT_SENDER'] = "your_email@gmail.com"

mail = Mail(app)

@app.route("/contact", methods=["POST"])
def contact():
    data = request.json
    name = data.get("name")
    email = data.get("email")
    message = data.get("message")

    try:
        # Create email message
        msg = Message(
            subject=f"New Contact Form Submission from {name}",
            recipients=["siva04vaishali@gmail.com"],  # <-- where YOU want to receive
            body=f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
        )
        mail.send(msg)

        return jsonify({"success": True, "message": "Message sent successfully!"}), 200
    except Exception as e:
        print("Error:", e)
        return jsonify({"success": False, "message": "Failed to send message."}), 500

if __name__ == "__main__":
    app.run(debug=True)
