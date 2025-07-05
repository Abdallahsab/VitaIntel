from flask import Flask, request, jsonify, render_template
import smtplib
from email.mime.text import MIMEText
import re

app = Flask(__name__)

#  Settings forGmail
EMAIL_ADDRESS = 'vitaaintel@gmail.com'
EMAIL_PASSWORD = 'ucza xuqz cpzm jdch'
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    # Honeypot check ( to prevent spam ) 
    website = request.form.get('website')
    if website:
        return jsonify({'success': False, 'message': 'Spam detected.'}), 400

    # Receive form data
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    message = request.form.get('message', '').strip()

    # Validate fields
    if not name or not email or not message:
        return jsonify({'success': False, 'message': 'All fields are required.'}), 400

    if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
        return jsonify({'success': False, 'message': 'Invalid email address.'}), 400

    # Prepare the message
    subject = 'New message from contact form'
    body = f"Name: {name}\nEmail: {email}\nMessage:\n{message}"
    msg = MIMEText(body, 'plain', 'utf-8')
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS

    # Send the email
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        return jsonify({'success': True, 'message': 'Message sent successfully!'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'An error occurred while sending the email: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
