from flask import Flask, render_template_string, send_file, request
import os

app = Flask(__name__)

# YOUR PRODUCTS - Kyambogo Market Prices
PRODUCTS = [
    {"name": "Matooke", "price": 20000, "unit": "bunch", "emoji": "🍌"},
    {"name": "Cassava Bunch", "price": 3000, "unit": "bunch", "emoji": "🥔"},
    {"name": "Beans", "price": 6000, "unit": "kg", "emoji": "🫘"},
    {"name": "Posho", "price": 2000, "unit": "kg", "emoji": "🌽"},
    {"name": "Cooking Oil", "price": 3500, "unit": "litre", "emoji": "🛢️"},
    {"name": "Rice", "price": 4500, "unit": "kg", "emoji": "🍚"},
]

# READ KEYS FROM RENDER SECRET FILES OR ENV - SAFE!
MTN_SUB_KEY = os.environ.get("MTN_SUB_KEY") or open("/etc/secrets/MTN_SUB_KEY","r").read().strip() if os.path.exists("/etc/secrets/MTN_SUB_KEY") else "YOUR_KEY_HERE"
MTN_API_USER = os.environ.get("MTN_API_USER") or "43124307-..."
MTN_API_KEY = os.environ.get("MTN_API_KEY") or "YOUR_LIVE_KEY_FROM_MTN"

# FIX LOGO - Serve it!
@app.route('/logo.png')
def logo():
    if os.path.exists("static/logo.png"):
        return send_file("static/logo.png", mimetype='image/png')
    if os.path.exists("logo.png"):
        return send_file("logo.png", mimetype='image/png')
    return "Logo not found - upload to static/logo.png", 404

@app.route('/')
def home():
    html = """
    <!DOCTYPE html>
    <html>
    <head><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Food Store & Grocery - Kyambogo 256</title>
    <style>
    body{margin:0;font-family:system-ui;background:#F6FFF6}
    header{background:#0A6B2E;color:white;padding:12px;display:flex;justify-content:space-between;align-items:center}
    .logo{display:flex;align-items:center;gap:10px;font-weight:900}
    .logo img{width:50px;height:50px;border-radius:50%;border:3px solid #FFD700;background:white}
    .grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;padding:12px}
    .card{background:white;border-radius:16px;padding:10px;text-align:center;box-shadow:0 2px 8px rgba(0,0,0,.08)}
    .price{color:#0A6B2E;font-weight:900}
    button.add{background:#111;color:white;border:none;padding:8px 14px;border-radius:8px;margin-top:6px;width:100%}
    </style>
    </head>
    <body>
    <header>
      <div class="logo">
        <img src="/logo.png" onerror="this.src='/static/logo.png'">
        <div>FOOD STORE & GROCERY<br><small style="color:#FFD700">KAMPALA UG @ KYAMBOGO 256<br>0791734789</small></div>
      </div>
      <div>🛒</div>
    </header>
    <div style="text-align:center;padding:14px;background:white">
      <img src="/logo.png" onerror="this.src='/static/logo.png'" style="width:140px;height:140px;border-radius:50%;border:5px solid #FFD700">
      <h2 style="color:#0A6B2E">Fresh • Affordable • Fast Delivery</h2>
    </div>
    <div class="grid">
      {% for p in products %}
      <div class="card">
        <div style="font-size:40px">{{p.emoji}}</div>
        <div style="font-weight:800">{{p.name}} - {{p.unit}}</div>
        <div class="price">Shs. {{p.price}}</div>
        <button class="add" onclick="order('{{p.name}}', {{p.price}})">Add to cart</button>
      </div>
      {% endfor %}
    </div>
    <script>
    function order(name, price){
      let phone=prompt("Enter MTN/Airtel number 256...");
      let loc=prompt("Delivery location?");
      let msg=`New Order Kyambogo: ${name} UGX ${price} Phone: ${phone} Loc: ${loc}`;
      window.open(`https://wa.me/256791734789?text=${encodeURIComponent(msg)}`);
    }
    </script>
    </body>
    </html>
    """
    from flask import render_template_string as rts
    return rts(html, products=PRODUCTS)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
