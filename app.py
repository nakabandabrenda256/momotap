import os, uuid, requests, base64
from flask import Flask, request, render_template_string, send_from_directory

app = Flask(__name__)
PRIMARY_KEY = os.getenv("PRIMARY_KEY")
API_USER = os.getenv("API_USER")
API_KEY = os.getenv("API_KEY")

# Try to load logo.png from same folder and convert to base64
def get_logo():
    try:
        with open("logo.png", "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            return f"data:image/png;base64,{b64}"
    except:
        try:
            with open("logo.jpg", "rb") as f:
                data = f.read()
                b64 = base64.b64encode(data).decode()
                return f"data:image/jpeg;base64,{b64}"
        except:
            return ""

LOGO_B64 = get_logo()

HTML = """
<!DOCTYPE html>
<html>
<head><title>FOOD STORE & GROCERY</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{font-family:sans-serif;background:#e8f5e9;display:flex;justify-content:center;padding:15px}
.card{background:white;padding:20px;border-radius:18px;box-shadow:0 6px 20px rgba(0,0,0,0.2);width:100%;max-width:430px;text-align:center;border-top:7px solid #ffc107}
.logo{width:180px;height:180px;border-radius:50%;margin:0 auto 12px;display:block;border:5px solid #ffc107;object-fit:cover}
h2{color:#1b5e20;margin:5px 0 2px;font-size:20px}
h3{color:#ff6f00;margin:0 0 5px;font-size:13px}
.loc{background:#1b5e20;color:#ffeb3b;padding:5px 12px;border-radius:20px;font-size:11px;display:inline-block;margin-bottom:8px;font-weight:bold}
input{width:100%;padding:13px;margin:8px 0;border:1.5px solid #a5d6a7;border-radius:10px;box-sizing:border-box;font-size:15px}
button{background:#ffca28;color:#000;border:none;padding:15px;width:100%;border-radius:12px;font-weight:bold;font-size:17px;cursor:pointer;margin-top:10px}
.success{background:#d4edda;color:#155724;padding:14px;border-radius:10px;margin-top:15px;font-weight:bold;word-break:break-all}
.error{background:#f8d7da;color:#721c24;padding:14px;border-radius:10px;margin-top:15px}
</style>
</head>
<body>
<div class="card">
{% if logo %}<img src="{{logo}}" class="logo">{% endif %}
<div class="loc">📍 Kyambogo • Kampala • Jinja UG | 256791734789</div>
<h2>FOOD STORE & GROCERY</h2>
<h3>KAMPALA UG @ KYAMBOGO 256</h3>
<p><small>🔒 Secure MTN MoMo Payment • UGX</small></p>
<form method="post" action="/pay">
<input name="phone" placeholder="MTN Number: 2567..." required value="{{phone}}">
<input name="amount" placeholder="Amount UGX" type="number" required value="{{amount}}">
<button>Pay Now - MTN MoMo 🤑</button>
</form>
{% if result %}
<div class="{{'success' if 'SUCCESS' in result else 'error'}}">{{result}}</div>
{% endif %}
<br><small>✅ Fresh • Affordable • Fast Delivery<br>100% Fresh Daily</small>
</div>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML, result="", phone="", amount="", logo=get_logo())

@app.route("/pay", methods=["POST"])
def pay():
    phone = request.form.get("phone","").strip()
    amount = request.form.get("amount","").strip()
    try:
        r = requests.post("https://sandbox.momodeveloper.mtn.com/collection/token/", headers={"Ocp-Apim-Subscription-Key": PRIMARY_KEY}, auth=(API_USER, API_KEY), timeout=15)
        if r.status_code != 200:
            return render_template_string(HTML, result=f"TOKEN FAIL {r.status_code}", phone=phone, amount=amount, logo=get_logo())
        token = r.json().get("access_token")
        ref = str(uuid.uuid4())
        pay_data = {"amount": amount, "currency": "EUR", "externalId": ref, "payer": {"partyIdType": "MSISDN", "partyId": phone}, "payerMessage": "Food Store Payment", "payeeNote": "Food Store"}
        pr = requests.post("https://sandbox.momodeveloper.mtn.com/collection/v1_0/requesttopay", json=pay_data, headers={"Authorization": f"Bearer {token}", "X-Reference-Id": ref, "X-Target-Environment": "sandbox", "Ocp-Apim-Subscription-Key": PRIMARY_KEY, "Content-Type": "application/json"}, timeout=15)
        if pr.status_code in [200,202]:
            return render_template_string(HTML, result=f"✅ SUCCESS! {phone} Paid {amount} UGX Ref:{ref[:8]}", phone="", amount="", logo=get_logo())
        else:
            return render_template_string(HTML, result=f"PAY FAIL {pr.status_code}", phone=phone, amount=amount, logo=get_logo())
    except Exception as e:
        return render_template_string(HTML, result=f"ERROR: {str(e)}", phone=phone, amount=amount, logo=get_logo())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
