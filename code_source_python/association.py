import psycopg2
from datetime import date

def menu(conn):
    print("\n*Page - Gestion des associations*")
    action = '-1'
    while action != '0':
        print("\nVous pouvez effectuer les actions suivantes :")
        action = input("Entrez 1 pour afficher toutes les associations,\n  2 pour rechercher (voir les détails) une association par nom,\n  3 pour créer une nouvelle association,\n  4 pour modifier une association,\n  5 pour ajouter un membre à une association,\n  6 pour retirer un membre d'une association,\n  7 pour Setting (catégorie de l'association, salle...) \n (entrez 0 pour retourner à la page précédente) : ")
        if action == '1':
            findAll(conn)   
        elif action == '2':
            findOneByNom(conn)
        elif action == '3':
            create(conn)
        elif action == '4':
            update(conn)
        elif action == '5':
            addMemberToAsso(conn)
        elif action == '6':
            removeMemberFromAsso(conn)
        elif action == '7':
            setting_action = input("Entrez 1 pour ajouter une salle,\n  2 pour ajouter une catégorie d'association \n  (0 pour sortir) : ")
            if setting_action == '1':
                addSalle(conn)
            elif setting_action == '2':
                addCatAsso(conn)            
    print("*Retour à la page principale*\n")
        

def findAll(conn):
    # Open a cursor to send SQL commands
    cur = conn.cursor()
    # Execute a SQL SELECT command
    sql = "SELECT a.nom, a.mail, a.date_creation, a.type, a.salle FROM Association a"
    cur.execute(sql)
    # Fetch data line by line
    raw = cur.fetchone()
    if raw:
        print("Voici toutes les associations :")
        print("[Nom]    Mail    Date de création    Catégorie    Salle")
        while raw:
            print("[%s]    %s    %s    %s    %s" % (raw[0], raw[1], raw[2], raw[3], raw[4]))
            raw = cur.fetchone()
        return
    else :
        print("Aucune association enregistrée！")
        response = input("Vous voulez créer une association ? (y/n)")
        if response=='y':
            create(conn)
        else :
            return
    return


def findOneByNom(conn):
    print("Vous devez donner quelques informations afin qu'on puisse exécuter votre demande.")
    nom = quote(input("Nom de l'association : "))
    cur = conn.cursor()
    sql = "SELECT * FROM Association a WHERE a.nom=%s" % nom
    cur.execute(sql)
    raw = cur.fetchone()
    if not raw :
        print("Association non trouvé ！")
    else :
        print("[Nom]    Mail    Date de création    Website    Catégorie    Salle    Trésorier    Président")
        print("[%s]    %s    %s    %s    %s    %s    %s    %s" % (raw[0],raw[1],raw[2],raw[3], raw[4], raw[5], raw[6], raw[7]))
        sql = "SELECT p.cin, p.prenom, p.nom FROM MembreAsso ma, Personne p WHERE ma.membre=p.cin" 
        cur.execute(sql)
        raw = cur.fetchone()
        if not raw :
            print("Aucun membre inscrit pour l'instant !")
        else :
            print("Membres de l'association : ")
            while raw :
                print("[%s]    %s %s" % (raw[0],raw[1],raw[2]))
                raw = cur.fetchone()
    return

def create(conn):
    print("!!!Attention : Pour pouvoir créer une association avec succès, certains champs doivent être pré-remplis dans la base de données. ")
    print("Petits tips : ")
    print("Etapes pour créer un étudiant depuis le menu principal : entrez 1 (gestion de personne) -> entrez 1 (Etudiant) -> 3 (créer un étudiant)")
    print("Etapes pour créer une salle depuis le menu principal : entrez 2 (gestion d'Association) -> entrez 7 (Setting) -> entrez 1 (ajouter une salle)")
    print("Etapes pour créer une catégorie d'association depuis le menu principal : entrez 2 (gestion d'Association) -> entrez 7 (Setting) -> entrez 2 (ajouter une catégorie d'association)\n")
    print("Vous devez donner quelques informations afin qu'on puisse exécuter votre demande.\n")
    nom = quote(input("Nom d'association : "))
    mail = quote(input("Mail : "))
    catAsso = quote(input("Catégorie d'association : "))
    siteWeb = quote(input("Lien de Site Web (optionnel) : "))
    salle = quote(input("Salle réservée (4 caracteres): "))
    treso = quote(input("CIN de Trésorier de l'association (36 caractères): "))
    presid = quote(input("CIN de Président de l'association (36 caractères): "))
    # Connect, execute SQL, close
    sql = "INSERT INTO Association (nom, mail, date_creation, site_web, type, salle, treso_asso, presid_asso) VALUES (%s, %s,to_date(%s,'YYYYMMDD'),%s, %s, %s, %s, %s)" % (nom, mail,quote(getCurrentDate()),siteWeb,catAsso,salle,treso,presid)
    try :
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        print(nom +" est créée avec succès !")
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)    
        conn.rollback()
    return 

def update(conn):
    print("!!!Attention : Pour pouvoir modifier une association avec succès, certains champs doivent être pré-remplis dans la base de données. ")
    print("Petits tips : ")
    print("Etapes pour créer un étudiant depuis le menu principal : entrez 1 (gestion de personne) -> entrez 1 (Etudiant) -> 3 (créer un étudiant)")
    print("Etapes pour créer une salle depuis le menu principal : entrez 2 (gestion d'Association) -> entrez 7 (Setting) -> entrez 1 (ajouter une salle)")
    print("Etapes pour créer une catégorie d'association depuis le menu principal : entrez 2 (gestion d'Association) -> entrez 7 (Setting) -> entrez 2 (ajouter une catégorie d'association)\n")
    print("Vous devez donner quelques informations afin qu'on puisse exécuter votre demande.")
    nom = quote(input("Nom de l'association dont vous souhaitez modifier les informations : "))
    cur = conn.cursor()
    sql0 = "SELECT * FROM Association WHERE nom=%s" % nom
    cur.execute(sql0)
    raw = cur.fetchone()
    if not raw :
        print("Association n'exsite pas！")
        return
    champAmodifier = input("Donnez le champ que vous souhaitez modifier, vous pouvez choisir parmi nom, mail, site_web, type, salle, treso_asso, presid_asso (Veuillez utiliser des lettres minuscules svp). :")
    valeurAdonner = input("Donnez la nouvelle valeur pour ce champ:")
    # Connect, execute SQL, close
    if champAmodifier=='nom' or champAmodifier=='mail' or champAmodifier=='site_web' or champAmodifier=='type' or champAmodifier=='salle' or champAmodifier=='treso_asso' or champAmodifier=='presid_asso' :
        sql = "UPDATE Association SET %s=%s WHERE nom=%s" % (champAmodifier, quote(valeurAdonner), nom)
    else :
        print("Vous n'avez pas donné les informations correctes !")
        return
    try :
        cur.execute(sql)
        conn.commit()
        print("L'instruction est bien exécutée !")
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)    
        conn.rollback()
    return 


def addMemberToAsso(conn):
    print("!!!Attention : Pour pouvoir ajouter un membre à une association, certains champs doivent être pré-remplis dans la base de données. ")
    print("Petits tips : ")
    print("Etapes pour créer un étudiant depuis le menu principal : entrez 1 (gestion de personne) -> entrez 1 (Etudiant) -> 3 (créer un étudiant)")
    print("Etapes pour créer une association depuis le menu principal : entrez 2 (gestion d'association) -> entrez 3 (créer une association) \n")
    print("Vous devez donner quelques informations afin qu'on puisse exécuter votre demande.")
    association = input("Nom de l'association : ")
    membre = input("CIN de l'étudiant (36 caractères) : ")
    sql = "INSERT INTO MembreAsso (nom_asso, membre) VALUES (%s, %s)" % (quote(association), quote(membre))
    cur = conn.cursor()
    try:  
        cur.execute(sql)
        conn.commit()
        print(membre+" est bien ajouté à l'association "+association+ " !")
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)    
        conn.rollback()
    return


def removeMemberFromAsso(conn):
    print("Vous devez donner quelques informations afin qu'on puisse exécuter votre demande.")
    association = input("Nom de l'association : ")
    membre = input("CIN de l'étudiant (36 caractères) : ")
    sql = "SELECT * FROM MembreAsso ma WHERE ma.nom_asso=%s AND ma.membre=%s" % (quote(association), quote(membre))
    cur = conn.cursor()
    cur.execute(sql)
    raw = cur.fetchone()
    if not raw :
        print("Cet étudiant n'a pas rejoint cette association !")
    else :
        sql = "DELETE FROM MembreAsso ma WHERE ma.nom_asso=%s AND ma.membre=%s" % (quote(association), quote(membre))
        try : 
            cur.execute(sql)
            conn.commit()
            print(membre+" est bien retirée de l'association "+association+ " !")
        except (Exception, psycopg2.DatabaseError) as e:
            print(e)    
            conn.rollback()
    return

def addSalle(conn):
    print("Vous devez donner quelques informations afin qu'on puisse exécuter votre demande.")
    batiment = input("Bâtiment lettre (1 caractère) : ")
    numSalle = input("Numéro salle (3 chiffres) : ")
    typeSalle = input("Type Salle (parmi cours, amphi, bureau): ")
    nbMax = input("Nombre de personnes qu'elle peut recevoir : ")
    # Vérifiez si le bâtiment existe déjà 
    cur = conn.cursor()
    sql0 = "SELECT * FROM Batiment WHERE lettre=%s" % quote(batiment)
    cur.execute(sql0)
    raw = cur.fetchone()
    try:
        if not raw :
             sql1 = "INSERT INTO Batiment (lettre) VALUES (%s)" % (quote(batiment))
             cur.execute(sql1)
        sql2 = "INSERT INTO Salle (code, numero, type, nb_max, bat) VALUES (%s, %i, %s, %i, %s)" % (quote(batiment+numSalle), int(numSalle), quote(typeSalle),int(nbMax),quote(batiment))
        cur.execute(sql2)
        conn.commit()
        print(batiment+numSalle+" est créée avec succès !")
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)    
        conn.rollback()
    return 

def addCatAsso(conn) :
    print("Vous devez donner quelques informations afin qu'on puisse exécuter votre demande.")
    intitule = input("Intitulé : ")
    # Vérifiez si cette categorie existe déjà 
    cur = conn.cursor()
    sql0 = "SELECT * FROM CategorieAsso WHERE intitule=%s" % quote(intitule)
    cur.execute(sql0)
    raw = cur.fetchone()
    try:
        if not raw :
             sql1 = "INSERT INTO CategorieAsso (intitule) VALUES (%s)" % (quote(intitule))
             cur.execute(sql1)
             conn.commit()
             print("La catégorie "+intitule+" est créée avec succès !")
        else :
            print("Cette catégorie existe déjà ！")
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)    
        conn.rollback()
    return 


#fonction de service
def quote(s):
  if s:
    return '\'%s\'' % s
  else:
    return 'NULL'


def getCurrentDate():
    today = date.today()
    return today.strftime("%Y%m%d")

