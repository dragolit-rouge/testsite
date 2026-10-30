import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

def check_db(enter_id):
    conn = sqlite3.connect('uley3_0.db')
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM uley WHERE id_pasek = ?", (enter_id,))
    result = cursor.fetchone()
    
    conn.close()
    return result
    
@app.route('/api/check-enter', methods=['POST'])
def handle_check():
    data = request.get_json()
    enter_id = data.get('id', '').strip()
    
    if not enter_id:
        return jsonify({'status': 'error', 'message': 'Пустой ID'}), 400
        
    db_result = check_db(enter_id)
    
    if db_result:
        return jsonify({'status': 'success', 'message': 'Пасека найдена'})
    else:
        return jsonify({'status': 'not_found', 'message': 'Пасека не существует'})

if __name__ == '__main__':
    app.run(port=5000, debug=True)

