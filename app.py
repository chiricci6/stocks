from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

def crear_tabla():
    conn = sqlite3.connect('stock.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS productos (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      nombre TEXT,
                      cantidad INTEGER)''')
    conn.commit()
    conn.close()

crear_tabla()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/productos', methods=['GET'])
def obtener_productos():
    conn = sqlite3.connect('stock.db')
    cursor = conn.cursor()
    cursor.execute('SELECT nombre, cantidad FROM productos')
    productos = cursor.fetchall()
    conn.close()
    return jsonify(productos)

@app.route('/agregar', methods=['POST'])
def agregar():
    data = request.get_json()
    producto = data.get('producto')
    cantidad = data.get('cantidad')
    conn = sqlite3.connect('stock.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO productos (nombre, cantidad) VALUES (?, ?)', (producto, cantidad))
    conn.commit()
    conn.close()
    return jsonify({"message": "Producto agregado correctamente"})

if __name__ == '__main__':
    app.run(debug=True)
