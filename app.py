from flask import Flask , session , render_template ,request, redirect,flash
import sqlite3








app = Flask(__name__)
app.secret_key="application_de_la_gestionEglise"




#acceiul 
@app.route('/')
@app.route('/home',methods=['POST','GET'])
def home():
  
    return render_template('front/index.html')


##
#
# interface login 
@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'POST':
        user = request.form['user'] 
        pwd  = request.form['pwd'] 

        with sqlite3.connect('crmk.db') as con :
            cur = con.cursor()
            cur.execute("select * from users where nomUser = ? and passwordUser = ? ",[user , pwd])
            data = cur.fetchone()

            if data :
                #verification du statut 
                #
                ver = con.cursor()
                ver.execute("select * from users where nomUser = ? and passwordUser = ? and statut = 'oui' ",[user,pwd])
                dta = ver.fetchone()
                
                if dta :
                    session['session'] = True 
                    session['id']  = dta[0]
                    session['nom'] = dta[1]
                    session['fonction'] = dta[5]
                    session['eglise']  = dta[8]
                    session['ville']  = dta[7]

                    return redirect('/index')
                else:
                    flash("votre statut est bloque")
            else:
                flash("mot de passe ou nom erronne")


    return render_template('auth-login.html')

#
# page administrateur 
#
#
@app.route("/index")
def index():
    if 'session' in session:
        return render_template('index.html')
    else:
        return redirect('/login')
    
#
# deconnexion du systeme 
#
@app.route('/deco')
def deco():
    session.clear()
    return redirect('/')

#
##
# enregistrement des utilisateurs du systemes
@app.route('/registerU',methods = ['POST','GET'])
def registerU():
    if 'session' in session:
        if request.method == 'POST':
            nom = request.form['nom']
            prenom  = request.form['prenom']
            sexe = request.form['sexe']
            phone = str(request.form['phone'])
            fonction = request.form['fonction']
            ville = request.form['ville']
            adresse = request.form['adresse']
            eglise = request.form['eglise']
            password = 1234

            with sqlite3.connect('crmk.db') as con :
                #verification du numero de telephone
                num = con.cursor()
                num.execute("select * from users where phoneUser = ?", [phone])
                data_num = num.fetchone()

                if data_num:
                    flash(f"le numero {phone} existe deja dans le systeme ")
                else:
                    #envoie des informations
                    # 
                    cur = con.cursor()
                    cur.execute("insert into users(nomUser,prenomUser,sexeUser,phoneUser,fonctionUser,villeUser,adresseUser,nomEglise,passwordUser) values(?,?,?,?,?,?,?,?,?)" ,[nom,prenom,sexe,phone,fonction,ville,adresse,eglise,password])
                    con.commit()
                    cur.close()
                    flash("Information enregistree")    
        # call table fonction
        with sqlite3.connect('crmk.db') as con :
            cur = con.cursor()
            cur.execute("select * from fonctions where idFonction not in (1,4,5)")
            aff = cur.fetchall()

        return render_template('forms-validation.html', aff = aff)
    else:
        return redirect('/login')
##
##
# liste des utilisateur 
@app.route('/lstUser')
def lstUser():
    if 'session' in session:
        #liste des utilisateurs systeme
        with sqlite3.connect("crmk.db") as con :
            cur = con.cursor()
            cur.execute("select idUser,nomUser,prenomUser,sexeUser,phoneUser,libFonction,villeUser,adresseUser,nomEglise,statut , fonctionUser from users inner join fonctions on users.fonctionUser = fonctions.idFonction where fonctionUser in (2,3) ") 
            dataA = cur.fetchall()

        return render_template('export-table.html' , dataA = dataA)

##
# supprimer users 
@app.route('/deleteU/<string:idUser>',methods = ['POST','GET'])
def deleteU(idUser):
    with sqlite3.connect('crmk.db') as con:
        cur = con.cursor()
        cur.execute("delete from users where idUser = ?",[idUser])
        con.commit()
        
        return redirect('/lstUser')
##
# #
# modification utlisateur
# 
@app.route('/updateU/<string:idUser>', methods = ['POST','GET'])
def updateU(idUser):
    if 'session' in session:
        if request.method == 'POST':
            nom = request.form['nom']
            prenom  = request.form['prenom']
            sexe = request.form['sexe']
            phone = str(request.form['phone'])
            fonction = request.form['fonction']
            ville = request.form['ville']
            adresse = request.form['adresse']
            eglise = request.form['eglise']

            with sqlite3.connect('crmk.db') as con :
                cur = con.cursor()
                cur.execute("update  users set nomUser = ?,prenomUser = ?,sexeUser = ?,phoneUser = ?,fonctionUser = ?,villeUser = ?,adresseUser = ?,nomEglise = ? where idUser = ? " ,[nom,prenom,sexe,phone,fonction,ville,adresse,eglise,idUser] )

                con.commit()

                return redirect('/lstUser') 



        with sqlite3.connect('crmk.db') as con:
            cur = con.cursor()
            cur.execute("select idUser,nomUser,prenomUser,sexeUser,phoneUser,libFonction,villeUser,adresseUser,nomEglise,statut , fonctionUser from users inner join fonctions on users.fonctionUser = fonctions.idFonction  where idUser = ?",[idUser])
            aff = cur.fetchone()

            #
            #
            af = con.cursor()
            af.execute("select * from fonctions where idFonction not in (1,4,5) ")
            dataAf = af.fetchall()

        return render_template('updateU.html' ,aff =aff , dataAff = dataAf)
    else:
        return redirect('/login')   
#
#
# statut modification 
#
@app.route('/statutU/<string:idUser>',methods = ['POST','GET'])
def statutU(idUser):
    if 'session' in session :
        if request.method == 'POST':
            statut = request.form['statut'] 
            with sqlite3.connect("crmk.db") as con :
                cur = con.cursor()
                cur.execute("update users set statut = ? where idUser = ?",[statut,idUser]) 
                con.commit()
                return redirect('/lstUser')
        return render_template('statutU.html') 
    else:
        return redirect('/login')
    
##
#
# enregistrement des pasteur par les sous-administrateurs 
#
@app.route('/pasteurR', methods = ['POST','GET'])
def pasteurR():
    if 'session' in session:
        if request.method == 'POST':
            nom = request.form['nom']
            prenom = request.form['prenom']
            sexe = request.form['sexe']
            adresse = request.form['adresse']
            phone = str(request.form['phone'] )
            ville = session['ville']
            pwd = 0000 

            
            with sqlite3.connect("crmk.db") as con :
                #verification du phone 
                ver = con.cursor()
                ver.execute("select * from users where phoneUser = ?", [phone])
                dataV = ver.fetchone()

                if dataV:
                    flash("le numero existe deja dans le systeme") 
                else:
                    cur = con.cursor()
                    cur.execute("insert into users(nomUser,prenomUser,sexeUser,villeUser,adresseUser,nomEglise,passwordUser,id,fonctionUser,phoneUser) values(?,?,?,?,?,?,?,?,?,?)" ,[nom,prenom,sexe,ville,adresse,session['eglise'],pwd,session['id'],4,phone]) 
                    con.commit()
                    cur.close()
                    flash("information enregistre")

        return render_template('pasteurR.html')
    
    else:
        return redirect('/login')
#
# 
# liste des pasteur dans le systeme 
# 
@app.route('/lstP')
def lstP():
    with sqlite3.connect("crmk.db") as con :
        cur = con.cursor()
        cur.execute("select idUser,nomUser,prenomUser,sexeUser,phoneUser,libFonction,villeUser,adresseUser,nomEglise,statut , fonctionUser from users inner join fonctions on users.fonctionUser = fonctions.idFonction where id = ?",[session['id']])
        dataA = cur.fetchall()

        return render_template('lstP.html', dataA = dataA)
##
# #
# suppresion de pasteur 
@app.route('/deleteP/<string:idUser>', methods = ['POST','GET'])
def deleteP(idUser) :
    with sqlite3.connect('crmk.db') as con :
        cur = con.cursor()
        cur.execute("delete from users where idUser = ?", [idUser])
        con.commit()
        return redirect('/lstP')   

if __name__ == '__main__':
    app.run(debug=True)