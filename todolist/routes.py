from flask import Blueprint, jsonify, request, abort
import sqlite3


todolist = Blueprint('todolist', __name__)


@todolist.route('/api/v1/todolist', methods=['GET'])
def get_to_do_list():
    try:
        with sqlite3.connect('my.db') as conn:
            cur = conn.cursor()
            cur.execute('SELECT id, name, content FROM tasks')
            rows = cur.fetchall()
            tasks = []
            for row in rows:
                tasks.append({"id": row[0], "name": row[1], "content": row[2]})
    except sqlite3.Error as e:
        print(e)
        abort(500)
    return jsonify(tasks)


@todolist.route('/api/v1/todolist', methods=['POST'])
def add_task():
    try:
        with sqlite3.connect('my.db') as conn:
            tasks = (request.json['name'], request.json['content'])
            sql = '''INSERT INTO tasks (name,content)
                     VALUES (?,?) 
                     RETURNING *'''  # прикольчик
            cur = conn.cursor()
            res = cur.execute(sql, tasks)
            new_row = res.fetchone()
            conn.commit()
            return jsonify({
                'id': new_row[0],
                'name': new_row[1],
                'content': new_row[2]
            })
    except sqlite3.Error as e:
        print(e)
        abort(500)


# CHANGE
@todolist.route('/api/v1/todolist/<int:list_id>', methods=['PUT'])
def put_to_do_list(list_id):
    try:
        with sqlite3.connect('my.db') as conn:
            cur = conn.cursor()

            # Проверяем, существует ли запись с данным id
            cur.execute("SELECT 1 FROM tasks WHERE id = ?", (list_id,))
            task_exists = cur.fetchone()  # Если строка существует, task_exists будет содержать (1,)
            if not task_exists:
                return jsonify({"error": f"Task with id={list_id} doesn't exist"}), 404

            # получаем данные из запроса
            name = request.json['name']
            content = request.json['content']
            # SQL-запрос для обновления
            update_stmt = '''   UPDATE tasks 
                                  SET name    = ?, 
                                      content = ?
                                WHERE id=?'''

            # Выполняем запрос с параметрами
            cur.execute(update_stmt, (name, content, list_id))
            conn.commit()
            # Возвращаем обновленные данные
            return jsonify({
                "id": list_id,
                "name": name,
                "content": content
            })
    except sqlite3.Error as e:
        print(e)
        abort(500)


# DELETE
@todolist.route('/api/v1/todolist/<int:list_id>', methods=['DELETE'])
def delete_to_do_list(list_id):
    try:
        with sqlite3.connect('my.db') as conn:
            cur = conn.cursor()
            # SQL-запрос для обновления

            # Проверяем, существует ли запись с данным id
            cur.execute("SELECT 1 FROM tasks WHERE id = ?", (list_id,))
            task_exists = cur.fetchone()  # Если строка существует, task_exists будет содержать (1,)

            if not task_exists:
                return jsonify({"error": f"Task with id={list_id} doesn't exist"}), 404

            # Выполняем удаление
            delete_stmt = f'DELETE FROM tasks WHERE id = {list_id}'
            cur.execute(delete_stmt)
            conn.commit()
            # Возвращаем обновленные данные
            return jsonify({"message": f"Task with id={list_id} was successfully deleted"})
    except sqlite3.Error as e:
        print(e)
        abort(500)


