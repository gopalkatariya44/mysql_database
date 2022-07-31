from flask import Flask, render_template, request, redirect
import pymysql

app = Flask(__name__)
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='12345678',
                             database='gopal',
                             )


@app.route('/', methods=['GET', 'POST'])
def index():
    cursor = connection.cursor()
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        account_type = request.form.get('account_type')
        hobbies = ", ".join(request.form.getlist('hobbies'))
        print(hobbies)
        cursor.execute("INSERT INTO users (email, password, account_type, hobbies) VALUES (%s, %s, %s, %s)",
                       (email, password, account_type, hobbies))
        connection.commit()
        return redirect('/')
    else:
        cursor.execute("SELECT * FROM users")
        user_data = cursor.fetchall()
        print(user_data)
        return render_template('index.html', user_data=user_data)


@app.route('/delete/<int:user_id>')
def delete(user_id):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s", user_id)
    connection.commit()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
