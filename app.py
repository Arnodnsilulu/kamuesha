from flask import Flask , session , render_template ,request, redirect,flash
import sqlite3
import os 
import qrcode 
import io 
import pyqrcode 
import webview 
from datetime import datetime, timedelta








app = Flask(__name__)
app.secret_key="application_de_la_gestionEglise" 
app.config['UPLOAD_QRCODE'] = 'static/qrcode' 
app.config['UPLOAD_PASTEUR'] = 'static/pasteurs' 




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
                    session['fonction'] = dta[4]
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
        with sqlite3.connect("crmk.db") as con :

            # nombre des utilisateurs dans le systme cote admin et sous-admin
            nbrU = con.cursor()
            nbrU.execute("select * from users where fonctionUser in (2,3)")
            affNbr = len(nbrU.fetchall())

            # nombre des pasteurs dans le systme cote admin et sous-admin
            nbrP = con.cursor()
            nbrP.execute("select * from pasteurs")
            affNbrP = len(nbrP.fetchall())

            # nombre des ministres dans le systme cote admin et sous-admin
            nbrM = con.cursor()
            nbrM.execute("select * from pasteurs")
            affNbrM = len(nbrM.fetchall())

        return render_template('index.html', affNbr = affNbr , affNbrP = affNbrP , affNbrM = affNbrM)
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
            etat = request.form['etat']
            phone = str(request.form['phone'])
            fonction = request.form['fonction']
            commune = request.form['commune']
            adresse = request.form['adresse']
            eglise = request.form['eglise']
            postnom = request.form['postnom']
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
                    cur.execute("insert into users(nomUser,prenomUser,phoneUser,fonctionUser,adresseUser,nomEglise,passwordUser,etatcivile,postnom,commune) values(?,?,?,?,?,?,?,?,?,?)" ,[nom,prenom,phone,fonction,adresse,eglise,password,etat,postnom,commune])
                    con.commit()
                    cur.close()
                    flash("Information enregistree")    
        # call table fonction
        with sqlite3.connect('crmk.db') as con :
            cur = con.cursor()
            cur.execute("select * from fonctions where idFonction not in (1,2,4,5)")
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
            cur.execute("select idUser,nomUser,prenomUser,phoneUser,libFonction,adresseUser,nomEglise,statut , fonctionUser , etatCivile,postnom , commune from users inner join fonctions on users.fonctionUser = fonctions.idFonction where fonctionUser in (2,3) ") 
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
            
            phone = str(request.form['phone'])
            fonction = request.form['fonction']
            
            adresse = request.form['adresse']
            eglise = request.form['eglise']
            postnom = request.form['postnom']
            commune = request.form['commune']
            etat = request.form['etat']

            with sqlite3.connect('crmk.db') as con :
                cur = con.cursor()
                cur.execute("update  users set nomUser = ?,prenomUser = ?,phoneUser = ?,fonctionUser = ?,adresseUser = ?,nomEglise = ? ,postnom = ?, etatcivile = ? , commune = ? where idUser = ? " ,[nom,prenom,phone,fonction,adresse,eglise,postnom,etat,commune,idUser] )

                con.commit()

                return redirect('/lstUser') 



        with sqlite3.connect('crmk.db') as con:
            cur = con.cursor()
            cur.execute("select idUser,nomUser,prenomUser,phoneUser,libFonction,adresseUser,nomEglise,statut , fonctionUser ,etatcivile,postnom,commune from users inner join fonctions on users.fonctionUser = fonctions.idFonction  where idUser = ?",[idUser])
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
            postnom = request.form['postnom']
            adresse = request.form['adresse']
            phone = str(request.form['phone'] )
            commune = request.form['commune']
            etat = request.form['etat']
            formation = request.form['formation']
            email = request.form['email']
            photo = request.files['photo']
            eglise = request.form['eglise']

            #information ajoute
            district = request.form['district']
            paysP    = request.form['paysP']
            quartier = request.form['quartier'] 
            # information ancien pasteur

            nomAP = request.form['nomAP']
            formationA = request.form['formationA']
            ad = request.form['ad']
            provinceA = request.form['provinceA']
            pays = request.form['pays']
            egliseA = request.form['egliseA']
            phoneA = str(request.form['phoneA'])
            

            #photo pasteur
            tofe = os.path.join(app.config['UPLOAD_PASTEUR'],photo.filename) 
            photo.save(tofe) 

            #autre methode 

            folder = os.path.join('static' , 'qrcode') 
            os.makedirs(folder, exist_ok = True)

            filenames = f"{nom}.png"
            fileFolder = os.path.join(folder,filenames) 

            if not os.path.exists(fileFolder):
                image = qrcode.make("crmk-rdc.onrender.com")
                image.save(fileFolder)
                # images = image

 

           



            
            with sqlite3.connect("crmk.db") as con :
                #verification du phone 
                ver = con.cursor()
                ver.execute("select * from pasteurs where phoneP = ?", [phone])
                dataV = ver.fetchone()

                if dataV:
                    flash("le numero existe deja dans le systeme") 
                else:
                    
                    cur = con.cursor()
                    cur.execute("insert into pasteurs(nomP,postnomP,prenomP,formation,etatcivile,phoneP,emailP,nomEgise,commune_secteur,fonctionP,userID,photoP,nomAncienP,pasteurAncienFormation,nomProvince,nomAncienPays,adresseP , nomAncienEg,MonpasteurPhone,qrcode,nomAncienAdresse,quartier_village,paysP,district_territoire) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)" ,[nom,postnom,prenom,formation,etat,phone,email,eglise,commune,4,session['id'],photo.filename,nomAP,formationA,provinceA,pays,adresse,egliseA, phoneA,filenames , ad , quartier,paysP,district ])   
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
        cur.execute("select * from pasteurs where userID = ?",[session['id']]) 
        dataA = cur.fetchall()

        return render_template('lstP.html', dataA = dataA)
##
# #
# suppresion de pasteur 
@app.route('/deleteP/<string:idP>', methods = ['POST','GET'])
def deleteP(idP) :
    with sqlite3.connect('crmk.db') as con :
        cur = con.cursor()
        cur.execute("delete from pasteurs where idP = ?", [idP])
        con.commit()
        return redirect('/lstP')   
    
##
# #
# suppresion de pasteur cote admin 
@app.route('/deletePA/<string:idP>', methods = ['POST','GET'])
def deletePA(idP) :
    with sqlite3.connect('crmk.db') as con :
        cur = con.cursor()
        cur.execute("delete from pasteurs where idP = ?", [idP])
        con.commit()
        return redirect('/lstPA') 
#
# 
# 
# change le mot de passe 
# 
@app.route('/change' , methods = ['POST','GET'] )
def change():
    if 'session' in session:

        if request.method == 'POST':
            pwd1 = request.form['pwd1']
            pwd2 = request.form['pwd2']
            pwd3 = request.form['pwd3']

            with sqlite3.connect("crmk.db") as con :
                ver = con.cursor()
                ver.execute("select * from users where idUser = ? and passwordUser = ? ",[session['id'],pwd1])
                dataVer = ver.fetchone()

                if dataVer:
                    #verification de mot de passe identique
                    if pwd2 == pwd3:
                        cur = con.cursor()
                        cur.execute("update users set passwordUser = ? where idUser = ?",[pwd2,session['id']])
                        con.commit()
                        cur.close()
                        return redirect('/login')
                    else:
                        flash("le mot de passe doit etre conforme !!!")
                else:
                    flash("ancien mot de passe incorrecte")
        return render_template('auth-reset-password.html') 
    else:
        return redirect('/login')   
#
# #
# #
# modification cote pasteur  
#
#
@app.route("/updateP/<string:idP>", methods = ['POST','GET'])
def updateP(idP):
    if 'session' in session:
        if request.method == 'POST':
            nom = request.form['nom'] 
            postnom = request.form['postnom']
            prenom = request.form['prenom']
            adresse = request.form['adresse']
            phone = str(request.form['phone'] )
            commune = request.form['commune']
            etat = request.form['etat']
            formation = request.form['formation']
            email = request.form['email']
            eglise = request.form['eglise']
            # photo = request.files['photo']


            #information ajoute
            district = request.form['district']
            paysP    = request.form['paysP']
            quartier = request.form['quartier'] 

            
            # information ancien pasteur

            nomAP = request.form['nomAP']
            formationA = request.form['formationA']
            ad = request.form['ad']
            provinceA = request.form['provinceA']
            pays = request.form['pays']
            phoneA = str(request.form['phoneA']) 
            egliseA = request.form['egliseA']

            #send data 
            # 
            # 
            with sqlite3.connect("crmk.db") as con :
                cur = con.cursor()
                cur.execute("""
                                update pasteurs set nomP = ? , postnomP = ? , formation = ? , prenomP=?,etatCivile = ? ,phoneP = ? , emailP = ?, nomEgise = ? , commune_secteur =? , adresseP = ? , nomAncienP = ? ,pasteurAncienFormation = ? , nomAncienEg = ?  , nomAncienAdresse = ? , nomProvince = ? , nomAncienPays = ? , MonpasteurPhone = ? , quartier_village = ?  , paysP = ? , district_territoire = ? where idP = ?
                 """, [nom,postnom,formation,prenom,etat,phone,email , eglise, commune,adresse , nomAP,formationA , egliseA , ad , provinceA , pays , phoneA , quartier,paysP,district,idP]) 
                con.commit()
                return redirect('/lstP')
            
        # liste de la table pasteurs

        with sqlite3.connect('crmk.db') as con :
            cur = con.cursor()
            cur.execute("select * from pasteurs where idP = ?", [idP]) 
            data = cur.fetchone()

        return render_template("updateP.html", data = data )       


#
#
# ajout du personnel 
#
@app.route('/addP/<string:idP>', methods = ['POST','GET'])
def addP(idP):
    if 'session' in session:
        if request.method == 'POST':
            nom = request.form['nom']
            prenom = request.form['prenom'] 
            preche = request.form['preche']
            formation = request.form['formation'] 
            dateD = request.form['dt']
            phone = str(request.form['phone'])
            
            

            with sqlite3.connect("crmk.db") as con :

                cur = con.cursor()
                cur.execute("insert into ministres(nomM,prenomM,idUser,idPasteur,dateD,preche,formation,phoneM) values(?,?,?,?,?,?,?,?)",[nom,prenom,session['id'],idP,dateD,preche,formation,phone])
                con.commit()
                cur.close()

                flash("information enregistre ")
    

        return render_template('addPersonnel.html') 
    else:
        return redirect('/login')

#
#
# liste des personnels 
@app.route("/lstPl")
def lstPl():
    if 'session' in session :
        ##
        # 
        with sqlite3.connect("crmk.db") as con :
            cur = con.cursor()
            cur.execute("select ministres.*,pasteurs.* from ministres inner join pasteurs on ministres.idPasteur = pasteurs.idP where idUser = ?" , [session['id']]) 
            dataA = cur.fetchall()


            return render_template('lstPl.html', dataA = dataA)
    else:
        return redirect('/login') 

#
#
# modification du ministre 
@app.route('/mdfM/<string:idM>', methods = ['POST','GET'])
def mdfM(idM):
    if 'session' in session:
        if request.method == 'POST':
            nom = request.form['nom']
            prenom = request.form['prenom']
            preche = request.form['preche'] 
            formation = request.form['formation'] 
            dt = request.form['dt'] 
            phone = str(request.form['phone']) 

            with sqlite3.connect('crmk.db') as con :
                cur = con.cursor()
                cur.execute("update ministres set nomM = ?,prenomM = ?,dateD = ?,preche = ?,formation = ? , phoneM = ? where idM = ?",[nom,prenom,dt,preche,formation,phone,idM]) 
                con.commit()
                return redirect('/lstPl')

       




        with sqlite3.connect('crmk.db') as con:

            cur = con.cursor()
            cur.execute("select * from ministres where idM=?",[idM])

            data = cur.fetchone()

            return render_template('mdfM.html', data = data)
    else:
        return redirect('/login')


 #
 #
 ## suppression du ministre 
 #
 #


@app.route('/deleteM/<string:idM>', methods = ['POST','GET'])
def deleteM(idM) :
    with sqlite3.connect('crmk.db') as con :
        cur = con.cursor()
        cur.execute("delete from ministres where idM = ?", [idM])
        con.commit()
        return redirect('/lstPl') 

#
#
# liste de ministre par admini 
@app.route('/lstMPA')
def lstMPA():
    if 'session' in session:
        with sqlite3.connect("crmk.db") as con :
            cur = con.cursor()
            cur.execute("select nomM, prenomM, preche,m.formation ,dateD, nomP, prenomP, nomegise, nomUser , nomEglise, idM , phoneM from ministres as m inner join pasteurs as p on  m.idPasteur = p.idP  inner join users on m.idUser = users.idUser") 
            data = cur.fetchall() 


        return render_template('lstMPA.html' , data  = data)
    else:
        return redirect('/login')


#
# #
# modification du ministre cote admin 
# 
@app.route('/mdfMA/<string:idM>',methods = ['GET','POST']) 
def mdfMA(idM):
    if 'session' in session:
        if request.method == 'POST':
            nom = request.form['nom']
            prenom = request.form['prenom']
            preche = request.form['preche'] 
            formation = request.form['formation'] 
            dt = request.form['dt'] 
            phone = str(request.form['phone'])

            with sqlite3.connect('crmk.db') as con :
                cur = con.cursor()
                cur.execute("update ministres set nomM = ?,prenomM = ?,dateD = ?,preche = ?,formation = ? , phoneM = ? where idM = ?",[nom,prenom,dt,preche,formation,phone,idM]) 
                con.commit()
                return redirect('/lstMPA')

       




        with sqlite3.connect('crmk.db') as con:

            cur = con.cursor()
            cur.execute("select * from ministres where idM=?",[idM])

            data = cur.fetchone()

            return render_template('mdfMA.html', data = data)
    else:
        return redirect('/login')       

#
#
# liste des pasteurs code admin
@app.route('/lstPA')
def lstPA():
    if 'session' in session:
        with sqlite3.connect("crmk.db") as con :
            cur = con.cursor()
            cur.execute("select pasteurs.* , users.*  from pasteurs inner join users on pasteurs.userID = users.idUser") 
            data = cur.fetchall()

        return render_template("lstPA.html" , data = data) 
    else:
        return redirect('/login')
#
# 
# moficiation des informations dans la table pasteurs par l'admin 
# 
@app.route('/updatePA/<string:idP>', methods = ['POST','GET']) 
def updatePA(idP) :
    if 'session' in session:
        if request.method == 'POST':

            nom = request.form['nom'] 
            postnom = request.form['postnom']
            prenom = request.form['prenom']
            adresse = request.form['adresse']
            phone = str(request.form['phone'] )
            commune = request.form['commune']
            etat = request.form['etat']
            formation = request.form['formation']
            email = request.form['email']
            # photo = request.files['photo']
            eglise = request.form['eglise']

            #information ajoute
            district = request.form['district']
            paysP    = request.form['paysP']
            quartier = request.form['quartier'] 

            # information ancien pasteur

            nomAP = request.form['nomAP']
            formationA = request.form['formationA']
            ad = request.form['ad']
            provinceA = request.form['provinceA']
            pays = request.form['pays']
            phoneA = str(request.form['phoneA']) 
            egliseA = request.form['egliseA']

            #send data 
            # 
            # 
            with sqlite3.connect("crmk.db") as con :
                cur = con.cursor()
                cur.execute("""
                                update pasteurs set nomP = ? , postnomP = ? , formation = ? , prenomP=?,etatCivile = ? ,phoneP = ? , emailP = ?, nomEgise = ? , commune_secteur =? , adresseP = ? , nomAncienP = ? ,pasteurAncienFormation = ? , nomAncienEg = ?  , nomAncienAdresse = ? , nomProvince = ? , nomAncienPays = ? , MonpasteurPhone = ? ,district_territoire =? , quartier_village = ? , paysP = ? where idP = ?
                 """, [nom,postnom,formation,prenom,etat,phone,email , eglise, commune,adresse , nomAP,formationA , egliseA , ad , provinceA , pays , phoneA ,district,quartier,paysP ,idP]) 
                con.commit()
                return redirect('/lstPA')
            
        # liste de la table pasteurs

        with sqlite3.connect('crmk.db') as con :
            cur = con.cursor()
            cur.execute("select * from pasteurs where idP = ?", [idP]) 
            data = cur.fetchone()

        return render_template("updatePA.html", data = data )       
#
#liste de  ministre par pasteurs
@app.route("/lstMPP/<string:idM>" , methods =['GET'])
def lstMPP(idM):
    if 'session' in session:
        with sqlite3.connect("crmk.db") as con :
            cur = con.cursor()
            cur.execute("select ministres.*,pasteurs.* from ministres inner join pasteurs on ministres.idPasteur = pasteurs.idP where idPasteur =?" , [idM]) 
            dataA = cur.fetchall()
            return render_template('lstMPP.html' , dataA = dataA)
    else:
        return redirect('/login')

webview.create_window('apk' , app)    

if __name__ == '__main__':
    app.run(debug=True)
    # webview.start() 