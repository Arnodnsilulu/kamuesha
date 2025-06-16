import sqlite3 


# db = sqlite3.connect("crmk.db")
db = sqlite3.connect("db.db")

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
db.execute("insert into fonctions(libFonction) values('super administrateur'), ('administrateur'), ('sous-administrateur'),('pasteur') ,('ministre')")

##
#
# creation de la table user
#
#
#db.execute('drop table users')
db.execute("""
            create table if not exists users(
            idUser integer primary key autoincrement, 
            nomUser varchar(30),
            prenomUser varchar(30),
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
# db.execute("alter table users drop sexeUser") 
# db.execute("alter table users drop villeUser") 
# db.execute("alter table users add postnom varchar(30)") 
# db.execute("alter table users add etatCivile varchar(30)") 
#db.execute("alter table users add commune varchar(30)") 

#information par defaut 
#
# db.execute("insert into users(nomUser,prenomUser,sexeUser,fonctionUser,nomEglise,passwordUser) values('mukoko','gracia','M',1,'super','12345')")
# db.execute("insert into users(nomUser,prenomUser,sexeUser,fonctionUser,nomEglise,passwordUser) values('admin','admin','M',2,'demo','12345')")
#db.execute("insert into users(nomUser,prenomUser,sexeUser,fonctionUser,nomEglise,passwordUser,statut) values('gala','admin','M',2,'demo','12345','non')")

##
#
## creation de la table personnels 
#
#db.execute('drop table pasteurs')
db.execute("""
            create table if not exists pasteurs(
            idP integer primary key autoincrement ,
            nomP varchar(30),
            prenomP varchar(40),
            formation char(3),
            etatCivile varchar(20),
            phoneP varchar(15) , 
            emailP varchar(50),
            nomEgise varchar(40),
            district varchar(40),
            commune varchar(30),
            quartier varchar(40),
            adresseP varchar(80),
            fonctionP integer , 
            userID integer , 
            photoP longtext , 
            dateR timestamp default current_timestamp , 
            foreign key(userID) references users(idUser),
            foreign key(fonctionP) references fonctions(idFonction))
 """)
# db.execute('alter table pasteurs add postnomP varchar(40)')
# db.execute('alter table pasteurs add nomAncienP varchar(40)') 
# db.execute('alter table pasteurs add nomAncienEg varchar(30)') 
# db.execute('alter table pasteurs add pasteurAncienFormation char(30)') 
# db.execute('alter table pasteurs add nomAncienAdresse varchar(30)')
# db.execute('alter table pasteurs add nomProvince varchar(30)') 
# db.execute('alter table pasteurs add nomAncienPays varchar(30)')  
# db.execute('alter table pasteurs add qrcode longtext') 

# db.execute('alter table users drop nomAncienP ') 
# db.execute('alter table users drop nomAncienEg ') 
# db.execute('alter table users drop pasteurAncienFormatin') 
# db.execute('alter table users drop nomAncienAdresse ')
# db.execute('alter table users drop nomProvince ') 
# db.execute('alter table users drop nomAncienPays ')

#
# creation de la table ministre 
#
# 
# db.execute("drop table ministres")
db.execute("""
            create table if not exists ministres(
            idM integer primary key autoincrement ,
            nomM varchar(40),
            prenomM varchar(40),
            idUser integer , 
            idPasteur integer , 
            dateD date,
            foreign key(idUser) references users(idUser) on delete no action on update no action,
            foreign key(idPasteur) references pasteurs(idP) on delete no action on update no action
             )

""")

# db.execute('alter table ministres add preche char(3) ') 
# db.execute('alter table ministres add formation char(3) ')

#demo 
db.execute("create table if not exists demo(idD integer primary key autoincrement , nom varchar(20), email varchar(40))")
db.commit()