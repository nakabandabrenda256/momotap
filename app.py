import os
import uuid
import requests
from flask import Flask, request, render_template_string

app = Flask(__name__)

# Get keys from Render Environment Variables (safe)
API_USER = os.environ.get("API_USER", "your_api_user")
API_KEY = os.environ.get("API_KEY", "your_api_key")
PRIMARY_KEY = os.environ.get("PRIMARY_KEY", "your_primary_key")
COLLECTION_SUBSCRIPTION_KEY = PRIMARY_KEY

# MTN SANDBOX URLs
BASE_URL = "https://sandbox.momodeveloper.mtn.com"
# For Uganda, use EUR currency in sandbox

HTML = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Momotap - Pay with MTN MoMo</title>
<style>
body{font-family:Arial; background:#fff8e1; text-align:center; padding:20px}
.card{background:white; padding:20px; border-radius:15px; box-shadow:0 4px 10px rgba(0,0,0,0.1); max-width:400px; margin:auto}
input,button{width:90%; padding:12px; margin:10px; border-radius:8px; border:1px solid #ccc}
button{background:#ffcc00; font-weight:bold; border:none}
</style>
</head>
<body>
<div class="card">
<h2>🧡 Momotap</h2>
<p>Pay with MTN MoMo Uganda</p>
<form action="/pay" method="post">
<input type="text" name="phone" placeholder="MTN Number e.g. 256771234567" required>
<input type="number" name="amount" placeholder="Amount UGX" value="1000" required>
<button type="submit">Pay Now</button>
</form>
{% if message %}<p><b>{{ message }}</b></p>{% endif %}
</div>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/pay", methods=["POST"])
def pay():
    phone = request.form.get("phone")
    amount = request.form.get("amount")
    try:
        # Step 1: Get token
        token_url = f"{BASE_URL}/collection/token/"
        r = requests.post(token_url, 
            auth=(API_USER, API_KEY),
            headers={"Ocp-Apim-Subscription-Key": COLLECTION_SUBSCRIPTION_KEY}
        )
        token = r.json().get("access_token")
        
        if not token:
            return render_template_string(HTML, message="Failed to get token. Check keys in Render.")
        
        # Step 2: Request to Pay
        x_ref = str(uuid.uuid4())
        pay_url = f"{BASE_URL}/collection/v1_0/requesttopay"
        headers = {
            "Authorization": f"Bearer {token}",
            "X-Reference-Id": x_ref,
            "X-Target-Environment": "sandbox",
            "Ocp-Apim-Subscription-Key": COLLECTION_SUBSCRIPTION_KEY,
            "Content-Type": "application/json"
        }
        data = {
            "amount": amount,
            "currency": "EUR",
            "externalId": "MOMOTAP",
            "payer": {"partyIdType": "MSISDN", "partyId": phone},
            "payerMessage": "Momotap Payment",
            "payeeNote": "Thanks for using Momotap"
        }
        requests.post(pay_url, headers=headers, json=data)
        return render_template_string(HTML, message=f"✅ Payment request sent to {phone}! Check phone to approve. Ref: {x_ref[:8]}")
    except Exception as e:
        return render_template_string(HTML, message=f"Error: {str(e)}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
