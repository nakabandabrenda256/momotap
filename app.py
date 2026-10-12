from flask import Flask, send_from_directory, render_template_string
app = Flask(__name__)
WHATSAPP = "256791734789"
PRODUCTS = [
    {"id":1,"name":"Matooke - bunch","price":20000,"cat":"Staples"},
    {"id":2,"name":"Matooke - half bunch","price":12000,"cat":"Staples"},
    {"id":3,"name":"Cassava - bunch","price":3000,"cat":"Staples"},
    {"id":4,"name":"Sweet Potatoes - kg","price":2500,"cat":"Staples"},
    {"id":5,"name":"Yams - kg","price":4000,"cat":"Staples"},
    {"id":6,"name":"Posho - kg","price":2000,"cat":"Flour"},
    {"id":7,"name":"Posho - 5kg","price":9000,"cat":"Flour"},
    {"id":8,"name":"Rice Super - kg","price":5000,"cat":"Flour"},
    {"id":9,"name":"Rice - 5kg","price":23000,"cat":"Flour"},
    {"id":10,"name":"Beans Nambale - kg","price":6000,"cat":"Beans"},
    {"id":11,"name":"Beans Yellow - kg","price":7000,"cat":"Beans"},
    {"id":12,"name":"Cow Peas - kg","price":6500,"cat":"Beans"},
    {"id":13,"name":"G-Nuts - kg","price":8000,"cat":"Beans"},
    {"id":14,"name":"Peas - kg","price":12000,"cat":"Beans"},
    {"id":15,"name":"Tomatoes - kg","price":4000,"cat":"Vegetables"},
    {"id":16,"name":"Onions - kg","price":5000,"cat":"Vegetables"},
    {"id":17,"name":"Cabbage - head","price":3000,"cat":"Vegetables"},
    {"id":18,"name":"Carrots - kg","price":4000,"cat":"Vegetables"},
    {"id":19,"name":"Green Pepper - kg","price":6000,"cat":"Vegetables"},
    {"id":20,"name":"Eggplants - kg","price":3000,"cat":"Vegetables"},
    {"id":21,"name":"Dodo - bunch","price":1000,"cat":"Vegetables"},
    {"id":22,"name":"Nakati - bunch","price":1000,"cat":"Vegetables"},
    {"id":23,"name":"Bugga - bunch","price":1000,"cat":"Vegetables"},
    {"id":24,"name":"Avocado - pc","price":1000,"cat":"Vegetables"},
    {"id":25,"name":"Pumpkin - kg","price":2000,"cat":"Vegetables"},
    {"id":26,"name":"Cucumber - kg","price":3500,"cat":"Vegetables"},
    {"id":27,"name":"Watermelon - pc","price":8000,"cat":"Fruits"},
    {"id":28,"name":"Pineapple - pc","price":5000,"cat":"Fruits"},
    {"id":29,"name":"Mangoes - kg","price":5000,"cat":"Fruits"},
    {"id":30,"name":"Bananas sweet - bunch","price":8000,"cat":"Fruits"},
    {"id":31,"name":"Passion Fruits - kg","price":6000,"cat":"Fruits"},
    {"id":32,"name":"Oranges - kg","price":4000,"cat":"Fruits"},
    {"id":33,"name":"Lemons - kg","price":5000,"cat":"Fruits"},
    {"id":34,"name":"Cooking Oil - 1L","price":7000,"cat":"Cooking"},
    {"id":35,"name":"Cooking Oil - 5L","price":32000,"cat":"Cooking"},
    {"id":36,"name":"Salt - kg","price":2000,"cat":"Cooking"},
    {"id":37,"name":"Sugar - kg","price":5000,"cat":"Cooking"},
    {"id":38,"name":"Royco - 100g","price":2500,"cat":"Cooking"},
    {"id":39,"name":"Curry Powder","price":2000,"cat":"Cooking"},
    {"id":40,"name":"Eggs - tray 30","price":15000,"cat":"Protein"},
    {"id":41,"name":"Chicken whole","price":25000,"cat":"Protein"},
    {"id":42,"name":"Beef - kg","price":18000,"cat":"Protein"},
    {"id":43,"name":"Fish Tilapia kg","price":20000,"cat":"Protein"},
    {"id":44,"name":"Milk 500ml","price":2000,"cat":"Protein"},
]

HTML = '''
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>FOOD STORE GROCERY KYAMBOGO</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:Arial}
body{background:#f5f7f0}
.header{background:#1b5e20;color:white;padding:12px;position:sticky;top:0;z-index:100;display:flex;align-items:center;justify-content:space-between}
.logo-small{width:45px;height:45px;border-radius:50%;background:white;padding:2px}
.header-text{flex:1;margin-left:10px}
.header-text h1{font-size:13px}
.cart-btn{background:#ffeb3b;color:#000;padding:8px 12px;border-radius:20px;font-weight:bold;border:none}
.banner{text-align:center;padding:20px;background:white;margin:10px;border-radius:15px}
.banner img{width:120px;height:120px;border-radius:50%;border:3px solid #1b5e20}
.cat-bar{display:flex;overflow-x:auto;gap:8px;padding:10px;position:sticky;top:56px;background:#f5f7f0;z-index:90}
.cat-bar button{white-space:nowrap;padding:8px 15px;border-radius:20px;border:1px solid #1b5e20;background:white;color:#1b5e20;font-weight:bold}
.cat-bar button.active{background:#1b5e20;color:white}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;padding:10px}
.card{background:white;border-radius:15px;padding:12px;text-align:center}
.card h3{font-size:13px;margin:6px 0;min-height:32px}
.card .price{color:#1b5e20;font-weight:bold;font-size:14px}
.card button{background:#1b5e20;color:white;border:none;padding:8px 0;width:100%;border-radius:8px;margin-top:8px;font-weight:bold}
.cart-panel{position:fixed;bottom:0;left:0;right:0;background:white;border-top-left-radius:20px;border-top-right-radius:20px;padding:15px;max-height:85vh;overflow-y:auto;display:none;z-index:200;box-shadow:0 -5px 20px rgba(0,0,0,0.2)}
.cart-item{display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #eee}
.whatsapp-btn{background:#25D366;color:white;width:100%;padding:14px;border:none;border-radius:12px;font-size:16px;font-weight:bold;margin-top:10px}
.search{margin:10px;padding:0 10px}
.search input{width:100%;padding:12px;border-radius:25px;border:1px solid #ccc}
</style>
</head>
<body>
<div class="header">
 <img src="/logo.png" class="logo-small" alt="logo">
 <div class="header-text">
  <h1>FOOD STORE & GROCERY</h1>
  <p>KAMPALA UG @ KYAMBOGO 256<br>0791734789</p>
 </div>
 <button class="cart-btn" onclick="openCart()">Cart <span id="cart-count">0</span></button>
</div>
<div class="banner">
 <img src="/logo.png" alt="logo">
 <h2 style="color:#1b5e20">Fresh Affordable Fast Delivery</h2>
 <p style="font-size:12px;color:#666">Kyambogo Kireka Banda Ntinda Kyanja<br>Delivery in 1 hour</p>
</div>
<div class
