import sqlite3 


db = sqlite3.connect("crmk.db")

## 
# creation de la table fonction
# 
# 
db.execute("""

                create table if not exists fonctions(
           idFonction integer primary key autoincrement ,
           libFonction varchar(30) 
           );

           """) 
# information par defaut 
#
# 
#db.execute("insert into fonctions(libFonction) values('super administrateur'), ('administrateur'), ('sous-administrateur'),('pasteur') ,('ministre')")

##
#
# creation de la table user
#
#
# db.execute('drop table users')
db.execute("""
             create table if not exists users(
            idUser integer primary key autoincrement, 
            nomUser varchar(30),
            prenomUser varchar(30),
            sexeUser varchar(15),
            phoneUser varchar(15) , 
            fonctionUser integer ,
            adresseUser varchar(80),
            villeUser varchar(30) , 
            nomEglise varchar(40),
            passwordUser varchar(40) ,
            photoUser longtext ,
            statut varchar(3) default 'oui', 
           foreign key(fonctionUser) references fonctions(idFonction) 
             ) 
""")



#information par defaut 
#
# db.execute("insert into users(nomUser,prenomUser,sexeUser,fonctionUser,nomEglise,passwordUser) values('mukoko','gracia','M',1,'super','12345')")
# db.execute("insert into users(nomUser,prenomUser,sexeUser,fonctionUser,nomEglise,passwordUser) values('admin','admin','M',2,'demo','12345')")
#db.execute("insert into users(nomUser,prenomUser,sexeUser,fonctionUser,nomEglise,passwordUser,statut) values('gala','admin','M',2,'demo','12345','non')")

##
#
## creation de la table personnels 
#
#db.execute('drop table personnels')
db.execute("""
            create table if not exists personnels(
            idPersonnel integer primary key autoincrement ,
            nomP varchar(30),
            prenomP varchar(40),
            sexeP varchar(15),
            phoneP varchar(15) , 
            fonctionP integer ,
            adresseP varchar(80),
            villeP varchar(30) , 
            pasteurID integer ,
            userID integer , 
            photoP longtext , 
            dateDebut date , 
            foreign key(pasteurID) references users(idUser),
            foreign key(userID) references users(idUser),
            foreign key(fonctionP) references fonctions(idFonction))
 """)
# db.execute('alter table users add id integer') 

#demo 
db.execute("create table if not exists demo(idD integer primary key autoincrement , nom varchar(20), email varchar(40))")
db.commit()