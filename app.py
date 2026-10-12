from flask import Flask, send_from_directory, jsonify
app = Flask(__name__)
PRODUCTS = [
    {'id':1,'name':'Matooke bunch','price':20000,'cat':'Staples'},
    {'id':2,'name':'Posho kg','price':2000,'cat':'Flour'},
    {'id':3,'name':'Tomatoes kg','price':4000,'cat':'Vegetables'},
    {'id':4,'name':'Beans Nambale kg','price':6000,'cat':'Beans'},
    {'id':5,'name':'Rice Super kg','price':5000,'cat':'Flour'},
    {'id':6,'name':'Onions kg','price':5000,'cat':'Vegetables'},
    {'id':7,'name':'Cooking Oil 1L','price':7000,'cat':'Cooking'},
    {'id':8,'name':'Eggs tray 30','price':15000,'cat':'Protein'},
]
@app.route('/logo.png')
def logo():
    return send_from_directory(app.root_path, 'logo.png')
@app.route('/api/products')
def api_products():
    return jsonify(PRODUCTS)
@app.route('/')
def home():
    return '<html><head><meta name=viewport content=width=device-width,initial-scale=1><title>FOOD STORE KYAMBOGO</title></head><body style=font-family:Arial;text-align:center;padding:20px><img src=/logo.png width=120 style=border-radius:50%;border:3px solid green><h1>FOOD STORE KYAMBOGO 0791734789</h1><p>Fresh Affordable</p><div id=g></div><script>fetch("/api/products").then(r=>r.json()).then(d=>{var h="";for(var i=0;i<d.length;i++){h+="<div style=border:1px solid #ccc;margin:10px;padding:10px>"+d[i].name+" - Shs "+d[i].price+" <button>Add</button></div>";}document.getElementById("g").innerHTML=h;});</script><br><a href=https://wa.me/256791734789 style=background:#25D366;color:white;padding:15px;border-radius:10px;text-decoration:none>Order on WhatsApp</a></body></html>'
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
