from flask import Flask, render_template, request, redirect, jsonify, url_for
import pymysql

app = Flask(__name__)
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='12345678',
    database='gopal',
    cursorclass=pymysql.cursors.DictCursor
)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    cursor = connection.cursor()
    try:
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        gender = request.form.get('gender')
        email = request.form.get('email')
        password = request.form.get('password')
        account_type = request.form.get('account_type')
        hobbies = ", ".join(request.form.getlist('hobbies'))
        address = request.form.get('address')
        # cursor.execute('''ALTER TABLE users
        #                 ADD COLUMN firstname VARCHAR(255) NOT NULL AFTER id,
        #                 ADD COLUMN lastname VARCHAR(255) NOT NULL AFTER firstname,
        #                 ADD COLUMN gender VARCHAR(255) NOT NULL AFTER lastname''')
        cursor.execute(
            'INSERT INTO users (firstname, lastname, gender, email, password, account_type, hobbies, address) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
            (firstname, lastname, gender, email, password, account_type, hobbies, address))
        connection.commit()
    finally:
        cursor.close()
    return render_template('index.html')


@app.route('/display')
def display():
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM users")
        user_data = cursor.fetchall()
        # print(user_data)
    finally:
        cursor.close()
    return render_template('display.html', user_data=user_data)
    # return jsonify(user_data)


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

    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    gender = request.form.get('gender')
    # email = request.form.get('email')
    # password = request.form.get('password')
    account_type = request.form.get('account_type')
    hobbies = ", ".join(request.form.getlist('hobbies'))
    address = request.form.get('address')

    cursor.execute(
        "UPDATE users SET firstname = %s, lastname = %s, gender = %s, account_type = %s, hobbies = %s, address = %s WHERE id = %s",
        (firstname, lastname, gender, account_type, hobbies, address, user_id))
    connection.commit()
    return redirect('/display')


if __name__ == '__main__':
    app.run(debug=True, threading=True)
