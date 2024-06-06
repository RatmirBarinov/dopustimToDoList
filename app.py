from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def main_page():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/user/<username>')
def user_profile(username):
    return f"Это профиль пользователя {username}"


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username != '123' or password != '123':
            error = 'Invalid username or password. Please try again.'
        else:
            return 'Вы вошли в систему!'
    return render_template('login.html', error=error)


if __name__ == '__main__':
    app.run(debug=True)
