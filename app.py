from flask import Flask, render_template_string, request
import requests, uuid, base64

app = Flask(__name__)

# YOUR PRODUCTS - Kyambogo Market Price
PRODUCTS = [
    {"name": "Matooke", "price": 20000, "unit": "bunch", "emoji": "🍌"},
    {"name": "Cassava Bunch", "price": 3000, "unit": "bunch", "emoji": "🥔"},
    {"name": "Beans", "price": 6000, "unit": "kg", "emoji": "🫘"},
    {"name": "Posho", "price": 2000, "unit": "kg", "emoji": "🌽"},
    {"name": "Cooking Oil", "price": 3500, "unit": "1 litre", "emoji": "🛢️"},
    {"name": "Rice", "price": 4500, "unit": "kg", "emoji": "🍚"},
]

# MTN + AIRTEL KEYS - Put your real keys here
MTN_SUB_KEY = "YOUR_MTN_SUBSCRIPTION_KEY"
MTN_API_USER = "YOUR_MTN_API_USER"
MTN_API_KEY = "YOUR_MTN_API_KEY"

AIRTEL_CLIENT_ID = "YOUR_AIRTEL_CLIENT_ID"
AIRTEL_CLIENT_SECRET = "YOUR_AIRTEL_SECRET"

HTML = """
<html><head><meta name="viewport" content="width=device-width">
<style>
body{font-family:sans-serif;background:#f0fff0;padding:10px}
.card{background:white;padding:15px;margin:10px 0;border-radius:12px;box-shadow:0 2px 5px #ccc}
.btn{padding:12px 20px;border:none;border-radius:8px;color:white;font-weight:bold;width:100%;margin:5px 0}
.mtn{background:#ffcc00;color:black} .airtel{background:#ff0000}
input{width:100%;padding:12px;margin:5px 0;border-radius:8px;border:1px solid #ccc}
</style></head><body>
<h1>🟢 MomoTap - Kyambogo Market</h1>
<p>Fresh market products - Pay with MTN or Airtel</p>
{% for p in products %}
<div class="card">
<h3>{{p.emoji}} {{p.name}} - {{p.unit}}</h3>
<p><b>Shs. {{p.price}}</b></p>
<form method="POST" action="/pay">
<input type="hidden" name="amount" value="{{p.price}}">
<input type="hidden" name="product" value="{{p.name}}">
<input name="phone" placeholder="Enter 2567... MTN or 25675... Airtel" required>
<button class="btn mtn" name="method" value="mtn">Pay with MTN MoMo</button>
<button class="btn airtel" name="method" value="airtel">Pay with Airtel Money</button>
</form>
</div>
{% endfor %}
</body></html>
"""

@app.route("/")
def home():
    return render_template_string(HTML, products=PRODUCTS)

@app.route("/pay", methods=["POST"])
def pay():
    phone = request.form["phone"]
    amount = request.form["amount"]
    product = request.form["product"]
    method = request.form["method"]
    ref = str(uuid.uuid4())
    
    if method == "mtn":
        # MTN REAL PROMPT
        try:
            auth = base64.b64encode(f"{MTN_API_USER}:{MTN_API_KEY}".encode()).decode()
            token = requests.post("https://sandbox.momodeveloper.mtn.com/collection/token/",
                headers={"Authorization": f"Basic {auth}", "Ocp-Apim-Subscription-Key": MTN_SUB_KEY}).json()["access_token"]
            r = requests.post("https://sandbox.momodeveloper.mtn.com/collection/v1_0/requesttopay",
                headers={"Authorization": f"Bearer {token}", "X-Reference-Id": ref, "X-Target-Environment": "sandbox", "Ocp-Apim-Subscription-Key": MTN_SUB_KEY},
                json={"amount": amount, "currency": "UGX", "externalId": ref, "payer": {"partyIdType": "MSISDN", "partyId": phone}, "payerMessage": product, "payeeNote": "MomoTap"})
            return f"<h1>MTN Prompt Sent to {phone}!</h1><p>Check phone for PIN. Product: {product} - {amount} UGX<br>Ref: {ref}</p><a href='/'>Back</a>" if r.status_code==202 else f"MTN Error: {r.text}"
        except Exception as e:
            return f"MTN Setup Needed: {e}. Add your MTN keys first!"
    
    else:
        # AIRTEL REAL PROMPT
        try:
            token = requests.post("https://openapiuat.airtel.africa/auth/oauth2/token",
                json={"client_id": AIRTEL_CLIENT_ID, "client_secret": AIRTEL_CLIENT_SECRET, "grant_type": "client_credentials"}).json()["access_token"]
            r = requests.post("https://openapiuat.airtel.africa/merchant/v1/payments/",
                headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json", "X-Country": "UG", "X-Currency": "UGX"},
                json={"reference": ref, "subscriber": {"country": "UG", "currency": "UGX", "msisdn": phone}, "transaction": {"amount": int(amount), "country": "UG", "currency": "UGX", "id": ref}})
            return f"<h1>Airtel Prompt Sent to {phone}!</h1><p>Check phone for PIN. Product: {product} - {amount} UGX<br>Ref: {ref}</p><a href='/'>Back</a>" if r.status_code in [200,202] else f"Airtel Error: {r.text}"
        except Exception as e:
            return f"Airtel Setup Needed: {e}. Add your Airtel keys first!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
