from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
from threading import Thread
import time

app = Flask(__name__)

# Carrier gateways
carriers = [
    '@vtext.com',  # Verizon
    '@txt.att.net',  # AT&T
    '@tmomail.net',  # T-Mobile
    '@messaging.sprintpcs.com',  # Sprint
    '@mymetropcs.com',  # MetroPCS
    '@sms.myboostmobile.com',  # Boost Mobile
]

# SMTP settings
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SENDER_EMAIL = 'sendunseen@gmail.com'
SENDER_PASSWORD = 'sbbq seev tumn hmkl'


def send_email(recipient, message):
    """Send an email to a specific recipient."""
    try:
        msg = MIMEText(message)
        msg['From'] = SENDER_EMAIL
        msg['To'] = recipient
        msg['Subject'] = ' '

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, recipient, msg.as_string())
            print(f"Message sent successfully to {recipient}")
    except Exception as e:
        print(f"Failed to send to {recipient}: {e}")
        raise  # Raise the error for debugging or retry mechanisms


def send_to_all_carriers(phone_number, message):
    """Send the message to all carrier email-to-SMS gateways."""
    threads = []
    for carrier in carriers:
        recipient = f"{phone_number}{carrier}"
        thread = Thread(target=send_email_with_retries, args=(recipient, message))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()


def send_email_with_retries(recipient, message, retries=3):
    """Send email with retry mechanism for reliability."""
    for attempt in range(retries):
        try:
            send_email(recipient, message)
            return  # Exit once successful
        except Exception as e:
            print(f"Retry {attempt + 1} failed for {recipient}: {e}")
            time.sleep(2)  # Add delay before retrying
    print(f"Failed to send to {recipient} after {retries} attempts.")


@app.route('/send_sms', methods=['POST'])
def handle_sms():
    """Endpoint to handle SMS requests."""
    phone_number = request.form.get('phone')
    message = request.form.get('message')

    if not phone_number or not message:
        return jsonify({"status": "error", "message": "Invalid input"}), 400

    # Ensure phone number is in the correct format
    if not phone_number.startswith("+1"):
        phone_number = f"+1{phone_number}"  # Add country code for US numbers

    # Send message to all carriers
    send_to_all_carriers(phone_number, message)
    return jsonify({"status": "success", "message": "Message sent to all carriers!"}), 200


if __name__ == "__main__":
    app.run(debug=True)
