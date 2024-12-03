# from flask import Flask, render_template, request, redirect, url_for, session
# import sqlite3

# app = Flask(__name__)
# app.secret_key = 'your_secret_key'  

# def create_database():
#     conn = sqlite3.connect('users.db')
#     cursor = conn.cursor()
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS users (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             username TEXT UNIQUE NOT NULL,
#             password TEXT NOT NULL
#         )
#     ''')
#     conn.commit()
#     conn.close()

# @app.route('/', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         action = request.form['action']

#         conn = sqlite3.connect('users.db')
#         cursor = conn.cursor()

#         if action == 'register':
#             # Регистрация
#             try:
#                 cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
#                 conn.commit()
#                 session['user'] = username
#                 return redirect(url_for('main_app'))
#             except sqlite3.IntegrityError:
#                 return "Пользователь с таким именем уже существует."
#         elif action == 'login':
#             # Авторизация
#             cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
#             user = cursor.fetchone()
#             if user:
#                 session['user'] = username
#                 return redirect(url_for('main_app'))
#             else:
#                 return "Неправильный логин или пароль."

#     return render_template('login.html')

# @app.route('/main', methods=['GET', 'POST'])
# def main_app():
#     if 'user' not in session:
#         return redirect(url_for('login'))

#     result = None
#     recommendation = None
#     if request.method == 'POST':
#         try:
#             age = int(request.form['age'])
#             height = int(request.form['height'])
#             weight = float(request.form['weight'])
#             gender = request.form['gender']

#             bmi = round(weight / ((height / 100) ** 2), 1)

#             if bmi < 18.5:
#                 result = "Недостаточный вес"
#                 recommendation = "https://green-fit.org.ua/tpost/g95s0znou1-kak-nabrat-massu-tela" if gender == 'male' else "Питайтесь больше!"
#             elif 18.5 <= bmi <= 24.9:
#                 result = "Нормальный вес"
#                 recommendation = "Продолжайте в том же духе!"
#             else:
#                 result = "Ожирение"
#                 recommendation = "https://www.myprotein.ru/blog/trenirovki/programma-trenirovki-plan-pitania-dlya-mujchin/" if gender == 'male' else "https://vivasport.ru/luchshiy-sposob-pohudeniy-dly-zhenschin/"

#         except ValueError:
#             result = "Ошибка ввода. Проверьте данные."

#     return render_template('main.html', result=result, recommendation=recommendation)

# @app.route('/logout')
# def logout():
#     session.pop('user', None)
#     return redirect(url_for('login'))

# if __name__ == '__main__':
#     create_database()
#     app.run(debug=True)
from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # замените на более безопасный ключ

def create_database():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        action = request.form['action']

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        if action == 'register':
            # Регистрация
            try:
                cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
                conn.commit()
                session['user'] = username
                return redirect(url_for('main_app'))
            except sqlite3.IntegrityError:
                return "Пользователь с таким именем уже существует."
        elif action == 'login':
            # Авторизация
            cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
            user = cursor.fetchone()
            if user:
                session['user'] = username
                return redirect(url_for('main_app'))
            else:
                return "Неправильный логин или пароль."

    return render_template('login.html')

@app.route('/main', methods=['GET', 'POST'])
def main_app():
    if 'user' not in session:
        return redirect(url_for('login'))

    result = None
    recommendation = None
    obesity_level = None
    if request.method == 'POST':
        try:
            age = int(request.form['age'])
            height = int(request.form['height'])
            weight = float(request.form['weight'])
            gender = request.form['gender']

            bmi = round(weight / ((height / 100) ** 2), 1)

            if bmi < 18.5:
                result = "Недостаточный вес"
                recommendation = "Питайтесь больше!" if gender == 'female' else "Increase your food intake!"
            elif 18.5 <= bmi <= 24.9:
                result = "Нормальный вес"
                recommendation = "Продолжайте в том же духе!"
            elif 25 <= bmi <= 29.9:
                result = "Малое ожирение"
                obesity_level = "Малое ожирение"
                recommendation = "Следуйте рекомендациям для снижения веса."
            else:
                result = "Ожирение"
                obesity_level = "Ожирение"
                recommendation = "Следуйте рекомендациям для похудения."

        except ValueError:
            result = "Ошибка ввода. Проверьте данные."

    return render_template('main.html', result=result, recommendation=recommendation, obesity_level=obesity_level)

@app.route('/recommendations')
def recommendations():
    return render_template('index.html')  # отображаем index.html с рекомендациями

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    create_database()
    app.run(debug=True)
