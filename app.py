import os, uuid, requests
from flask import Flask, request, render_template_string

app = Flask(__name__)

PRIMARY_KEY = os.getenv("PRIMARY_KEY")
API_USER = os.getenv("API_USER")
API_KEY = os.getenv("API_KEY")

HTML = """
<!DOCTYPE html>
<html>
<head><title>FOOD STORE & GROCERY - MTN MoMo Pay</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{font-family:sans-serif;background:#fff8e1;display:flex;justify-content:center;padding:20px}
.card{background:white;padding:25px;border-radius:15px;box-shadow:0 6px 20px rgba(0,0,0,0.15);width:100%;max-width:420px;text-align:center;border-top:6px solid #ffcc00}
h2{color:#000;margin:5px 0;font-size:19px}
h3{color:#ff6f00;margin:0 0 10px 0;font-size:14px}
input{width:100%;padding:13px;margin:9px 0;border:1px solid #ccc;border-radius:10px;box-sizing:border-box;font-size:15px}
button{background:#ffcc00;color:#000;border:none;padding:15px;width:100%;border-radius:10px;font-weight:bold;font-size:17px;cursor:pointer;margin-top:10px}
.success{background:#d4edda;color:#155724;padding:14px;border-radius:10px;margin-top:15px;word-break:break-all;font-weight:bold}
.error{background:#f8d7da;color:#721c24;padding:14px;border-radius:10px;margin-top:15px}
small{color:#777}
.loc{background:#000;color:#ffcc00;padding:4px 10px;border-radius:20px;font-size:12px;display:inline-block;margin-bottom:10px}
</style>
</head>
<body>
<div class="card">
<div class="loc">📍 KYAMBOGO - KAMPALA UG - 256</div>
<h2>🧡 FOOD STORE & GROCERY</h2>
<h3>KAMPALA UG @ KYAMBOGO 256</h3>
<p><small>Secure Payment with MTN MoMo • UGX</small></p>
<form method="post" action="/pay">
<input name="phone" placeholder="MTN Number: 256772..." required value="{{phone}}">
<input name="amount" placeholder="Amount UGX (e.g. 5000)" type="number" required value="{{amount}}">
<button>Pay Now - MTN MoMo 🤑</button>
</form>
{% if result %}
<div class="{{'success' if 'SUCCESS' in result else 'error'}}">{{result}}</div>
{% endif %}
<br><small>Thank you for shopping with us!<br>Powered by MTN MoMo API Uganda</small>
</div>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML, result="", phone="", amount="")

@app.route("/pay", methods=["POST"])
def pay():
    phone = request.form.get("phone","").strip()
    amount = request.form.get("amount","").strip()
    try:
        r = requests.post(
            "https://sandbox.momodeveloper.mtn.com/collection/token/",
            headers={"Ocp-Apim-Subscription-Key": PRIMARY_KEY},
            auth=(API_USER, API_KEY),
            timeout=15
        )
        if r.status_code != 200:
            return render_template_string(HTML, result=f"TOKEN FAIL {r.status_code}", phone=phone, amount=amount)
        token = r.json().get("access_token")
        ref = str(uuid.uuid4())
        pay_data = {
            "amount": amount, "currency": "EUR", "externalId": ref,
            "payer": {"partyIdType": "MSISDN", "partyId": phone},
            "payerMessage": "Food Store Payment", "payeeNote": "Food Store Kyambogo"
        }
        pr = requests.post(
            "https://sandbox.momodeveloper.mtn.com/collection/v1_0/requesttopay",
            json=pay_data,
            headers={
                "Authorization": f"Bearer {token}",
                "X-Reference-Id": ref,
                "X-Target-Environment": "sandbox",
                "Ocp-Apim-Subscription-Key": PRIMARY_KEY,
                "Content-Type": "application/json"
            },
            timeout=15
        )
        if pr.status_code in [200,202]:
            return render_template_string(HTML, result=f"✅ SUCCESS! {phone} Paid {amount} UGX - Ref: {ref[:8]} - Approved!", phone="", amount="")
        else:
            return render_template_string(HTML, result=f"PAY FAIL {pr.status_code}", phone=phone, amount=amount)
    except Exception as e:
        return render_template_string(HTML, result=f"ERROR: {str(e)}", phone=phone, amount=amount)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
