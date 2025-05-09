from flask import Flask , session , render_template , redirect
import sqlite3




app = Flask(__name__)
app.secret_key="application_de_la_gestionEglise"


#acceuil 
@app.route('/')
def home():
    return render_template('front/index.html')

@app.route('/login')
def login():

    return render_template('auth-login.html')





if __name__ == '__main__':
    app.run(debug=True)