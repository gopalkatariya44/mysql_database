from flask import Flask, render_template, request, redirect
import pymysql

app = Flask(__name__)
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='12345678',
                             database='gopal',
                             cursorclass=pymysql.cursors.DictCursor,
                             )


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    cursor = connection.cursor()
    email = request.form.get('email')
    password = request.form.get('password')
    account_type = request.form.get('account_type')
    hobbies = ", ".join(request.form.getlist('hobbies'))
    address = request.form.get('address')
    # print(hobbies)
    cursor.execute(
        'INSERT INTO users (email, password, account_type, hobbies, address) VALUES (%s, %s, %s, %s, %s)',
        (email, password, account_type, hobbies, address))
    connection.commit()
    return render_template('index.html')


@app.route('/display')
def display():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users")
    user_data = cursor.fetchall()
    print(user_data)
    return render_template('display.html', user_data=user_data)


@app.route('/delete/<int:user_id>', methods=['GET', 'POST'])
def delete(user_id):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s", user_id)
    connection.commit()
    return redirect('/display')


@app.route('/update_page/<int:index>', methods=['GET', 'POST'])
def update_page(index):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users")
    user_data = cursor.fetchall()
    return render_template('update.html', user_data=user_data, index=index)


@app.route('/update_user/<int:user_id>', methods=['GET', 'POST'])
def update_user(user_id):
    cursor = connection.cursor()
    email = request.form.get('email')
    password = request.form.get('password')
    account_type = request.form.get('account_type')
    hobbies = ", ".join(request.form.getlist('hobbies'))
    address = request.form.get('address')

    cursor.execute(
        'UPDATE users SET email = %s, password = %s, account_type = %s, hobbies = %s, address = %s WHERE id = %s',
        (email, password, account_type, hobbies, address, user_id))
    connection.commit()
    return redirect('/display')


if __name__ == '__main__':
    app.run(debug=True, threading=True)
