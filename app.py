import os, uuid, base64, requests
from flask import Flask, request, jsonify

app = Flask(__name__)

API_USER = os.environ.get("API_USER","").strip()
API_KEY = os.environ.get("API_KEY","").strip()
PRIMARY_KEY = os.environ.get("PRIMARY_KEY","").strip()

@app.route('/')
def home():
    return '''<center style="font-family:Arial;padding:20px">
    <h2>🧡 Momotap v2</h2><p>Pay with MTN MoMo Uganda</p>
    <input id="phone" placeholder="2567..." style="padding:10px;width:85%"><br><br>
    <input id="amount" value="1000" style="padding:10px;width:85%"><br><br>
    <button onclick="pay()" style="padding:12px 30px;background:#ffcc00;border:none;border-radius:8px;font-weight:bold">Pay Now</button>
    <p id="msg" style="margin-top:20px;font-weight:bold"></p>
    <script>
    async function pay(){
      let m=document.getElementById('msg'); m.innerText='Processing...';
      let r=await fetch('/pay',{method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({phone:document.getElementById('phone').value,amount:document.getElementById('amount').value})});
      let j=await r.json(); m.innerText=j.message;
    }
    </script></center>'''

@app.route('/pay', methods=['POST'])
def pay():
    d=request.json
    phone=d.get('phone'); amount=d.get('amount','1000')
    auth=base64.b64encode(f"{API_USER}:{API_KEY}".encode()).decode()
    tr=requests.post("https://sandbox.momodeveloper.mtn.com/collection/token/",
        headers={"Authorization":f"Basic {auth}","Ocp-Apim-Subscription-Key":PRIMARY_KEY}, timeout=15)
    if tr.status_code!=200:
        return jsonify({"message":f"TOKEN FAIL {tr.status_code}: {tr.text} | USER={API_USER[:8]}... KEY={API_KEY[:5]}..."}),400
    token=tr.json()['access_token']
    ref=str(uuid.uuid4())
    pr=requests.post("https://sandbox.momodeveloper.mtn.com/collection/v1_0/requesttopay",
        headers={"Authorization":f"Bearer {token}","X-Reference-Id":ref,"X-Target-Environment":"sandbox","Ocp-Apim-Subscription-Key":PRIMARY_KEY,"Content-Type":"application/json"},
        json={"amount":str(amount),"currency":"EUR","externalId":ref,"payer":{"partyIdType":"MSISDN","partyId":phone},"payerMessage":"Momotap","payeeNote":"Momotap"}, timeout=15)
    if pr.status_code==202:
        return jsonify({"message":f"SUCCESS! Request sent to {phone}. Ref {ref}"})
    else:
        return jsonify({"message":f"PAY FAIL {pr.status_code}: {pr.text}"}),400

if __name__=="__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",10000)))
