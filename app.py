import os,uuid,base64,requests
from flask import Flask,request,jsonify
app=Flask(__name__)
A=os.environ.get("API_USER","").strip()
K=os.environ.get("API_KEY","").strip()
P=os.environ.get("PRIMARY_KEY","").strip()
@app.route('/')
def h():return '''<center style="font-family:Arial;padding:20px"><h2>🧡 Momotap v2</h2><input id="p" placeholder="2567..." style="padding:10px;width:85%"><br><br><input id="a" value="1000" style="padding:10px;width:85%"><br><br><button onclick="pay()" style="padding:12px 30px;background:#ffcc00;border:none;border-radius:8px;font-weight:bold">Pay Now</button><p id="m" style="font-weight:bold"></p><br><a href="/gen-keys">⚙️ Fix keys - TAP HERE</a></center><script>async function pay(){let m=document.getElementById('m');m.innerText='Processing...';let r=await fetch('/pay',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({phone:document.getElementById('p').value,amount:document.getElementById('a').value})});let j=await r.json();m.innerText=j.message;}</script>'''
@app.route('/gen-keys')
def g():
 new=str(uuid.uuid4())
 r1=requests.post("https://sandbox.momodeveloper.mtn.com/v1_0/apiuser",headers={"X-Reference-Id":new,"Ocp-Apim-Subscription-Key":P,"Content-Type":"application/json"},json={"providerCallbackHost":"momotap.onrender.com"},timeout=15)
 if r1.status_code not in [201,200]:return f"USER FAIL {r1.status_code}: {r1.text}",400
 r2=requests.post(f"https://sandbox.momodeveloper.mtn.com/v1_0/apiuser/{new}/apikey",headers={"Ocp-Apim-Subscription-Key":P},timeout=15)
 if r2.status_code!=201:return f"KEY FAIL {r2.status_code}: {r2.text}",400
 nk=r2.json()['apiKey']
 return f'<h2>✅ NEW KEYS!</h2><p>USER=<br><b>{new}</b></p><p>KEY=<br><b>{nk}</b></p><p>COPY THESE!</p>'
@app.route('/pay',methods=['POST'])
def pay():
 d=request.json;ph=d.get('phone');am=d.get('amount','1000')
 au=base64.b64encode(f"{A}:{K}".encode()).decode()
 tr=requests.post("https://sandbox.momodeveloper.mtn.com/collection/token/",headers={"Authorization":f"Basic {au}","Ocp-Apim-Subscription-Key":P},timeout=15)
 if tr.status_code!=200:return jsonify({"message":f"TOKEN FAIL {tr.status_code}: {tr.text} Go /gen-keys"}),400
 tk=tr.json()['access_token'];ref=str(uuid.uuid4())
 pr=requests.post("https://sandbox.momodeveloper.mtn.com/collection/v1_0/requesttopay",headers={"Authorization":f"Bearer {tk}","X-Reference-Id":ref,"X-Target-Environment":"sandbox","Ocp-Apim-Subscription-Key":P,"Content-Type":"application/json"},json={"amount":str(am),"currency":"EUR","externalId":ref,"payer":{"partyIdType":"MSISDN","partyId":ph},"payerMessage":"Momotap","payeeNote":"Momotap"},timeout=15)
 return jsonify({"message":f"SUCCESS! {ph} Ref {ref}"}) if pr.status_code==202 else (jsonify({"message":f"PAY FAIL {pr.status_code}: {pr.text}"}),400)
if __name__=="__main__":app.run(host="0.0.0.0",port=int(os.environ.get("PORT",10000)))
