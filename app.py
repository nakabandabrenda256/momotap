from flask import Flask, send_from_directory, render_template_string
import os

app = Flask(__name__)

WHATSAPP_NUMBER = "256791734789"

PRODUCTS = [
    {"id":1, "name":"Matooke - bunch", "price":20000, "emoji":"🍌", "cat":"Staples"},
    {"id":2, "name":"Matooke - half bunch", "price":12000, "emoji":"🍌", "cat":"Staples"},
    {"id":3, "name":"Cassava Bunch - bunch", "price":3000, "emoji":"🥔", "cat":"Staples"},
    {"id":4, "name":"Sweet Potatoes - kg", "price":2500, "emoji":"🍠", "cat":"Staples"},
    {"id":5, "name":"Yams - kg", "price":4000, "emoji":"🍠", "cat":"Staples"},
    {"id":6, "name":"Posho - kg", "price":2000, "emoji":"🌽", "cat":"Flour"},
    {"id":7, "name":"Posho - 5kg bag", "price":9000, "emoji":"🌽", "cat":"Flour"},
    {"id":8, "name":"Rice - kg (Super)", "price":5000, "emoji":"🍚", "cat":"Flour"},
    {"id":9, "name":"Rice - 5kg", "price":23000, "emoji":"🍚", "cat":"Flour"},
    {"id":10, "name":"Beans - kg (Nambale)", "price":6000, "emoji":"Beans", "cat":"Beans"},
    {"id":11, "name":"Beans - kg (Yellow)", "price":7000, "emoji":"Beans", "cat":"Beans"},
    {"id":12, "name":"Cow Peas - kg", "price":6500, "emoji":"Beans", "cat":"Beans"},
    {"id":13, "name":"G-Nuts - kg", "price":8000, "emoji":"🥜", "cat":"Beans"},
    {"id":14, "name":"Peas - kg", "price":12000, "emoji":"Peas", "cat":"Beans"},
    {"id":15, "name":"Tomatoes - kg", "price":4000, "emoji":"🍅", "cat":"Vegetables"},
    {"id":16, "name":"Onions - kg", "price":5000, "emoji":"🧅", "cat":"Vegetables"},
    {"id":17, "name":"Cabbage - head", "price":3000, "emoji":"🥬", "cat":"Vegetables"},
    {"id":18, "name":"Carrots - kg", "price":4000, "emoji":"🥕", "cat":"Vegetables"},
    {"id":19, "name":"Green Pepper - kg", "price":6000, "emoji":"Pepper", "cat":"Vegetables"},
    {"id":20, "name":"Eggplants - kg", "price":3000, "emoji":"🍆", "cat":"Vegetables"},
    {"id":21, "name":"Dodo - bunch", "price":1000, "emoji":"🥬", "cat":"Vegetables"},
    {"id":22, "name":"Nakati - bunch", "price":1000, "emoji":"🥬", "cat":"Vegetables"},
    {"id":23, "name":"Bugga - bunch", "price":1000, "emoji":"🥬", "cat":"Vegetables"},
    {"id":24, "name":"Avocado - pc", "price":1000, "emoji":"🥑", "cat":"Vegetables"},
    {"id":25, "name":"Pumpkin - kg", "price":2000, "emoji":"Pumpkin", "cat":"Vegetables"},
    {"id":26, "name":"Cucumber - kg", "price":3500, "emoji":"🥒", "cat":"Vegetables"},
    {"id":27, "name":"Watermelon - pc", "price":8000, "emoji":"🍉", "cat":"Fruits"},
    {"id":28, "name":"Pineapple - pc", "price":5000, "emoji":"🍍", "cat":"Fruits"},
    {"id":29, "name":"Mangoes - kg", "price":5000, "emoji":"🥭", "cat":"Fruits"},
    {"id":30, "name":"Bananas - bunch (sweet)", "price":8000, "emoji":"🍌", "cat":"Fruits"},
    {"id":31, "name":"Passion Fruits - kg", "price":6000, "emoji":"Fruits", "cat":"Fruits"},
    {"id":32, "name":"Oranges - kg", "price":4000, "emoji":"🍊", "cat":"Fruits"},
    {"id":33, "name":"Lemons - kg", "price":5000, "emoji":"🍋", "cat":"Fruits"},
    {"id":34, "name":"Cooking Oil - 1L", "price":7000, "emoji":"Oil", "cat":"Cooking"},
    {"id":35, "name":"Cooking Oil - 5L", "price":32000, "emoji":"Oil", "cat":"Cooking"},
    {"id":36, "name":"Salt - kg", "price":2000, "emoji":"Salt", "cat":"Cooking"},
    {"id":37, "name":"Sugar - kg", "price":5000, "emoji":"Sugar", "cat":"Cooking"},
    {"id":38, "name":"Royco - 100g", "price":2500, "emoji":"Royco", "cat":"Cooking"},
    {"id":39, "name":"Curry Powder", "price":2000, "emoji":"Curry", "cat":"Cooking"},
    {"id":40, "name":"Eggs - tray (30)", "price":15000, "emoji":"🥚", "cat":"Protein"},
    {"id":41, "name":"Chicken - whole", "price":25000, "emoji":"🍗", "cat":"Protein"},
    {"id":42, "name":"Beef - kg", "price":18000, "emoji":"🥩", "cat":"Protein"},
    {"id":43, "name":"Fish - Tilapia kg", "price":20000, "emoji":"🐟", "cat":"Protein"},
    {"id":44, "name":"Milk - 500ml", "price":2000, "emoji":"🥛", "cat":"Protein"},
]

HTML = """<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>FOOD STORE & GROCERY - KYAMBOGO</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:Arial}
body{background:#f5f7f0}
.header{background:#1b5e20;color:white;padding:12px;position:sticky;top:0;z-index:100;display:flex;align-items:center;justify-content:space-between}
.logo-small{width:45px;height:45px;border-radius:50%;background:white;padding:2px}
.header-text{flex:1;margin-left:10px}
.header-text h1{font-size:13px}
.header-text p{font-size:10px;opacity:0.9}
.cart-btn{background:#ffeb3b;color:#000;padding:8px 12px;border-radius:20px;font-weight:bold;border:none;cursor:pointer}
.banner{text-align:center;padding:20px;background:white;margin:10px;border-radius:15px;box-shadow:0 2px 10px rgba(0,0,0,0.1)}
.banner img{width:140px;height:140px;border-radius:50%;object-fit:cover;border:4px solid #1b5e20}
.cat-bar{display:flex;overflow-x:auto;gap:8px;padding:10px 10px;position:sticky;top:56px;background:#f5f7f0;z-index:90}
.cat-bar button{white-space:nowrap;padding:8px 15px;border-radius:20px;border:1px solid #1b5e20;background:white;color:#1b5e20;font-weight:bold;cursor:pointer}
.cat-bar button.active{background:#1b5e20;color:white}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;padding:10px}
.card{background:white;border-radius:15px;padding:12px;text-align:center;box-shadow:0 2px 8px rgba(0,0,0,0.08)}
.card .emoji{font-size:40px}
.card h3{font-size:13px;margin:6px 0;min-height:32px}
.card .price{color:#1b5e20;font-weight:bold;font-size:14px}
.card button{background:#1b5e20;color:white;border:none;padding:8px 0;width:100%;border-radius:8px;margin-top:8px;font-weight:bold;cursor:pointer}
.cart-panel{position:fixed;bottom:0;left:0;right:0;background:white;border-top-left-radius:20px;border-top-right-radius:20px;box-shadow:0 -5px 20px rgba(0,0,0,0.2);padding:15px;max-height:85vh;overflow-y:auto;display:none;z-index:200}
.cart-item{display:flex;justify-content:space-between;padding:8px 0;border-
