from flask import Flask, render_template, jsonify, request
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'sm'

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/person')
def person():
    return jsonify({'name': 'reva', 'address': 'indralaya'})

@app.route('/kpop', methods=['GET', 'POST'])
def kpop():
    try:
        cursor = mysql.connection.cursor()

        if request.method == 'GET':
            cursor.execute("SELECT * FROM KPOP")
            column_names = [i[0] for i in cursor.description]
            data = [dict(zip(column_names, row)) for row in cursor.fetchall()]
            cursor.close()
            return jsonify(data)

        elif request.method == 'POST':
            data = request.get_json()
            grup = data.get('grup')
            name = data.get('name')
            position = data.get('position')

            if not grup or not name or not position:
                return jsonify({'error': 'Semua field harus diisi'}), 400

            sql = "INSERT INTO KPOP (grup, name, position) VALUES (%s, %s, %s)"
            cursor.execute(sql, (grup, name, position))
            mysql.connection.commit()
            cursor.close()
            return jsonify({'message': 'Data berhasil ditambahkan'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/kpop/<int:id>', methods=['GET'])
def get_kpop_by_id(id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM KPOP WHERE kpop_id = %s", (id,))
        row = cursor.fetchone()
        cursor.close()

        if row:
            column_names = ['kpop_id', 'grup', 'name', 'position']
            data = dict(zip(column_names, row))
            return jsonify(data)
        else:
            return jsonify({'error': 'Data tidak ditemukan'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/editkpop/<int:id>', methods=['PUT'])
def editkpop(id):
    try:
        data = request.get_json()
        cursor = mysql.connection.cursor()
        sql = "UPDATE KPOP SET grup=%s, name=%s, position=%s WHERE kpop_id=%s"
        cursor.execute(sql, (data['grup'], data['name'], data['position'], id))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Data berhasil diubah'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/deletekpop/<int:id>', methods=['DELETE'])
def deletekpop(id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM KPOP WHERE kpop_id = %s", (id,))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Data berhasil dihapus'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5002, debug=True)