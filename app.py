from flask import Flask, request, render_template, redirect, url_for # type: ignore
import pyodbc # type: ignore

app = Flask(__name__)

# Ganti <server>, <user>, dan <password> dengan info Azure SQL kamu
conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=tcp:<server>.database.windows.net,1433;DATABASE=praktik2;UID=<user>;PWD=<password>')

@app.route('/')
def index():
    cursor = conn.cursor()
    cursor.execute('SELECT AddressID, AddressLine1, City FROM SalesLT.Address')
    rows = cursor.fetchall()
    return render_template('index.html', addresses=rows)

@app.route('/add', methods=['GET', 'POST'])
def add_address():
    if request.method == 'POST':
        AddressLine1 = request.form['AddressLine1']
        City = request.form['City']
        cursor = conn.cursor()
        cursor.execute("INSERT INTO SalesLT.Address (AddressLine1, City) VALUES (?, ?)", (AddressLine1, City))
        conn.commit()
        return redirect(url_for('index'))
    return render_template('add.html')

if __name__ == '__main__':
    app.run(debug=True)
