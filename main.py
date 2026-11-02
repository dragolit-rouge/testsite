import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

def get_hive_data_by_pasek(pasek_id):
    conn = sqlite3.connect('uley3_0.db')
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()
    
    # Выборка истории датчиков для всех ульев, привязанных к указанной пасеке.
    # Переименование полей через AS для совместимости с фронтендом.
    query = """
        SELECT 
            s.name AS type, 
            s.id_uley AS hive_id, 
            s.date AS value, 
            s.units AS unit, 
            s.rtime AS time 
        FROM sensor s
        JOIN uley u ON s.id_uley = u.id
        WHERE u.id_pasek = ?
        ORDER BY s.rtime DESC
    """
    
    cursor.execute(query, (pasek_id,))
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]

@app.route('/api/check-enter', methods=['POST'])
def handle_check():
    data = request.get_json()
    enter_id = data.get('id', '').strip()
    
    if not enter_id:
        return jsonify({'status': 'error', 'message': 'Пустой ID'}), 400
        
    # Получение объединенного массива данных из uley и sensor
    db_result = get_hive_data_by_pasek(enter_id)
    
    if db_result:
        # Сериализация массива истории датчиков в ключ 'hive' для фронтенда
        return jsonify({
            'status': 'success', 
            'message': 'Пасека найдена',
            'hive': db_result
        })
    else:
        return jsonify({
            'status': 'not_found', 
            'message': 'Пасека не существует или в ней нет датчиков'
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
