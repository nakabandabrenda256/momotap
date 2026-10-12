from flask import Flask, send_from_directory, jsonify
app = Flask(__name__)
PRODUCTS = [
{'id':1,'name':'Matooke bunch','price':20000,'cat':'Staples'},
{'id':2,'name':'Matooke half bunch','price':12000,'cat':'Staples'},
{'id':3,'name':'Cassava bunch','price':3000,'cat':'Staples'},
{'id':4,'name':'Sweet Potatoes kg','price':2500,'cat':'Staples'},
{'id':5,'name':'Yams kg','price':4000,'cat':'Staples'},
{'id':6,'name':'Posho kg','price':2000,'cat':'Flour'},
{'id':7,'name':'Posho 5kg','price':9000,'cat':'Flour'},
{'id':8,'name':'Rice Super kg','price':5000,'cat':'Flour'},
{'id':9,'name':'Rice 5kg','price':23000,'cat':'Flour'},
{'id':10,'name':'Beans Nambale kg','price':6000,'cat':'Beans'},
{'id':11,'name':'Beans Yellow kg','price':7000,'cat':'Beans'},
{'id':12,'name':'Cow Peas kg','price':6500,'cat':'Beans'},
{'id':13,'name':'G-Nuts kg','price':8000,'cat':'Beans'},
{'id':14,'name':'Peas kg','price':12000,'cat':'Beans'},
{'id':15,'name':'Tomatoes kg','price':4000,'cat':'Vegetables'},
{'id':16,'name':'Onions kg','price':5000,'cat':'Vegetables'},
{'id':17,'name':'Cabbage head','price':3000,'cat':'Vegetables'},
{'id':18,'name':'Carrots kg','price':4000,'cat':'Vegetables'},
{'id':19,'name':'Green Pepper kg','price':6000,'cat':'Vegetables'},
{'id':20,'name':'Eggplants kg','price':3000,'cat':'Vegetables'},
{'id':21,'name':'Dodo bunch','price':1000,'cat':'Vegetables'},
{'id':22,'name':'Nakati bunch','price':1000,'cat':'Vegetables'},
{'id':23,'name':'Bugga bunch','price':1000,'cat':'Vegetables'},
{'id':24,'name':'Avocado pc','price':1000,'cat':'Vegetables'},
{'id':25,'name':'Pumpkin kg','price':2000,'cat':'Vegetables'},
{'id':26,'name':'Cucumber kg','price':3500,'cat':'Vegetables'},
{'id':27,'name':'Watermelon pc','price':8000,'cat':'Fruits'},
{'id':28,'name':'Pineapple pc','price':5000,'cat':'Fruits'},
{'id':29,'name':'Mangoes kg','price':5000,'cat':'Fruits'},
{'id':30,'name':'Bananas sweet bunch','price':8000,'cat':'Fruits'},
{'id':31,'name':'Passion Fruits kg','price':6000,'cat':'Fruits'},
{'id':32,'name':'Oranges kg','price':4000,'cat':'Fruits'},
{'id':33,'name':'Lemons kg','price':5000,'cat':'Fruits'},
{'id':34,'name':'Cooking Oil 1L','price':7000,'cat':'Cooking'},
{'id':35,'name':'Cooking Oil 5L','price':32000,'cat':'Cooking'},
{'id':36,'name':'Salt kg','price':2000,'cat':'Cooking'},
{'id':37,'name':'Sugar kg','price':5000,'cat':'Cooking'},
{'id':38,'name':'Royco 100g','price':2500,'cat':'Cooking'},
{'id':39,'name':'Curry Powder','price':2000,'cat':'Cooking'},
{'id':40,'name':'Eggs tray 30','price':15000,'cat':'Protein'},
{'id':41,'name':'Chicken whole','price':25000,'cat':'Protein'},
{'id':42,'name':'Beef kg','price':18000,'cat':'Protein'},
{'id':43,'name':'Fish Tilapia kg','price':20000,'cat':'Protein'},
{'id':44,'name':'Milk 500ml','price':2000,'cat':'Protein'},
]
@app.route('/logo.png')
def logo():
    return send_from_directory(app.root_path, 'logo.png')
@app.route('/api/products')
def api_products():
    return jsonify(PRODUCTS)
@app.route('/')
def home():
    return send_from_directory(app.root_path, 'index.html')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
