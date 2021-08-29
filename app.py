from flask import Flask, request,render_template
import sqlite3
from main import main


db_file = "stored_database/api_data.db"


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/action1', methods=['POST','GET'])
def action1():
    
    if request.form.get('start_scrap') == "Start 'Public APIs' list scraping":
        main()
        return render_template('home.html')
    if request.form.get('view_database') == 'View fetched data stored in database':
        try:
            conn = sqlite3.connect(db_file)
        except Error as e:
            print(e)
        mycursor =conn.cursor()
        mycursor.execute("SELECT API_list.id2, categories.category, api_list.api_name, API_list.link, api_list.description, api_list.https, api_list.auth, api_list.cors  FROM api_list  INNER JOIN categories ON api_list.category=categories.ctgry_id")
        data = mycursor.fetchall()
        mycursor.close()
        conn.close()
        return render_template('index.html', data=data)


if __name__ == '__main__':
    app.run(host = '0.0.0.0')