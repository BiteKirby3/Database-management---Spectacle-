import psycopg2
import billetterie

def menu(conn):
    print("\n*Page - Gestion des spectacles*")
    action = '-1'
    while action != '0':
        print("\nVous pouvez effectuer les actions suivantes :")
        action = input("Entrez 1 pour afficher tous les spectacles,\n  2 pour rechercher des spectacles par catégorie,\n  3 pour rechercher (voir les détails) un spectacle par nom,\n  4 pour créer un spectacle,\n  5 pour modifier un spectacle,\n  6 pour gérer le personnel d'un spectacle,\n  7 pour gérer les séances d'un spectacle,\n  8 pour supprimer un spectacle(A utiliser avec précaution...opération irréversible !)\n(entrez 0 pour retourner à la page précédente) : ")
        if action == '1':
            findAll(conn) 
        elif action == '2':
            findByCategorie(conn)
        elif action == '3':
            findOneByNom(conn)
        elif action == '4':
            create(conn)
        elif action == '5':
            update(conn)
        elif action == '7':
            seance_action = input("Entrez 1 pour consulter toutes les séances d'un spectacle,\n  2 pour ajouter une séance pour un spectacle,\n  3 pour supprimer une séance d'une spectacle(A utiliser avec précaution...opération irréversible !).\n(0 pour sortir) : ")
            if seance_action == '1':
                showAllSeancesOfSpec(conn)
            elif seance_action == '2':
                addSeanceToSpec(conn) 
            elif seance_action == '3':
                removeSeanceFromSpec(conn)
        elif action == '8':
            delete(conn)
        elif action == '6':
            role_action = input("Entrez 1 pour ajouter un rôle à une personne dans un spectacle,\n  2 pour modifier le rôle d'une personne dans un spectacle,\n  3 pour supprimer le rôle d'une personne dans un spectacle.\n(0 pour sortir) : ")
            if role_action == '1':
                addRoleToSpec(conn)
            elif role_action == '2':
                modifyRoleOfSpec(conn)  
            elif role_action == '3':
                removeRoleFromSpec(conn)  
    print("*Retour à la page principale*\n")
        

def findAll(conn):
    # Open a cursor to send SQL commands
    cur = conn.cursor()
    # Execute a SQL SELECT command
    sql = "SELECT * FROM Spectacle"
    cur.execute(sql)
    # Fetch data line by line
    raw = cur.fetchone()
    if raw :
        print("Voici tous les spectacles :")
        print("[Nom]      Durée   Association")
        while raw:
            print("[%s]    %s    %s" % (raw[0], raw[1], raw[2]))
            raw = cur.fetchone()
        return
    else :
        print("Aucun spectacle enregistré！")
        response = input("Vous voulez créer un spectacle ? (y/n)")
        if response=='y':
            create(conn)
        else :
            return
    return


def findByCategorie(conn):
    print("Vous devez donner quelques informations afin qu'on puisse exécuter votre demande.")
    categorie = input("Catégorie du spectacle, vous pouvez choisir parmi concert, standup, piecetheatre (Veuillez utiliser des lettres minuscules) : ")
    cur = conn.cursor()
    if categorie=='concert':
        sql = "SELECT s.nom, s.duree, s.asso_organisatrice, c.compositeur, c.annee, c.genre FROM Spectacle s, Concert c WHERE s.nom=c.nom"
        cur.execute(sql)
        raw = cur.fetchone()
        if not raw :
            print("Pas de concert！")
        else :
             print("Concert : " )
             print("[Nom]     Durée   Association   Compositeur     Année  Genre")
             while raw:        
                 print("[%s]   %s    %s    %s    %i    %s" % (raw[0],raw[1],raw[2],raw[3],raw[4],raw[5]))
                 raw = cur.fetchone()
                 
    elif categorie=='standup':
        sql = "SELECT s.nom, s.duree, s.asso_organisatrice, su.genre FROM Spectacle s, StandUp su WHERE s.nom=su.nom "
        cur.execute(sql)
        raw = cur.fetchone()
        if not raw :
            print("Pas de standup！")
        else :
             print("StandUp : " )
             print("[Nom]      Durée   Association  Genre")
             while raw:        
                 print("[%s]   %s    %s    %s" % (raw[0],raw[1],raw[2],raw[3]))
                 raw = cur.fetchone()
                 
    elif categorie=='piecetheatre':
        sql = "SELECT s.nom, s.duree, s.asso_organisatrice, pt.auteur, pt.annee, pt.type FROM Spectacle s, PieceTheatre pt WHERE s.nom=pt.nom"
        cur.execute(sql)
        raw = cur.fetchone()
        if not raw :
            print("Pas de pièce théâtre！")
        else :
             print("Pièce théâtre : " )
             print("[Nom]     Durée   Association   Auteur     Année  Type")
             while raw:        
                 print("[%s]   %s    %s    %s    %i    %s" % (raw[0],raw[1],raw[2],raw[3],raw[4],raw[5]))
                 raw = cur.fetchone()
    else:
        print("Vous n'avez pas donné les informations correctes !")
        return
    return


def findOneByNom(conn):
    print("Vous devez donner quelques informations afin qu'on puisse exécuter votre demande.")
    #Vérifier si c'est un concert
    nom = input("Nom du specatcle : ")
    cur0 = conn.cursor()
    sql0 = "SELECT * FROM Concert WHERE nom=%s" % quote(nom)
    cur0.execute(sql0)
    raw0 = cur0.fetchone()
    #Vérifier si c'est un standup
    cur1 = conn.cursor()
    sql1 = "SELECT * FROM StandUp WHERE nom=%s" % quote(nom)
    cur1.execute(sql1)
    raw1 = cur1.fetchone()
    #Vérifier si c'est un piecetheatre
    cur2 = conn.cursor()
    sql2 = "SELECT * FROM PieceTheatre WHERE nom=%s" % quote(nom)
    cur2.execute(sql2)
    raw2 = cur2.fetchone()
    
    cur = conn.cursor()
    
    if not raw0 and not raw1 and not raw2 :
        print("Spectacle n'exsite pas！")
        return
    if raw0 :
        sql = "SELECT s.nom, s.duree, s.asso_organisatrice, c.compositeur, c.annee, c.genre FROM Spectacle s, Concert c WHERE s.nom=c.nom AND c.nom=%s" % quote(nom)
        cur.execute(sql)
        raw = cur.fetchone()
        print("Concert : " + nom)
        print("[Nom]    Durée   Association   Compositeur     Année  Genre")
        print("[%s]   %s    %s    %s    %i    %s" % (raw[0],raw[1],raw[2],raw[3],raw[4],raw[5]))
    elif raw1 :
        sql = "SELECT s.nom, s.duree, s.asso_organisatrice, su.genre FROM Spectacle s, StandUp su WHERE s.nom=su.nom AND su.nom=%s" % quote(nom)
        cur.execute(sql)
        raw = cur.fetchone()
        print("StandUp : " + nom)
        print("[Nom]    Durée   Association  Genre")
        print("[%s]   %s    %s    %s" % (raw[0],raw[1],raw[2],raw[3]))
    elif raw2 :
        sql = "SELECT s.nom, s.duree, s.asso_organisatrice, pt.auteur, pt.annee, pt.type FROM Spectacle s, PieceTheatre pt WHERE s.nom=pt.nom AND pt.nom=%s" % quote(nom)
        cur.execute(sql)
        raw = cur.fetchone()
        print("Pièce Théâtre : " + nom)
        print("[Nom]    Durée   Association   Auteur     Année  Type")
        print("[%s]   %s    %s    %s    %i    %s" % (raw[0],raw[1],raw[2],raw[3],raw[4],raw[5]))
    
    #Afficher les rôles
    sql = "SELECT p.cin, p.nom, p.prenom, r.descriptif FROM role r, personne p WHERE r.cin=p.cin AND r.nom_spec=%s" % quote(nom)
    cur.execute(sql)
    raw = cur.fetchone()
    if not raw :
        print("Il n'y a pas de rôle pour ce spectacle ！")
        response = input("Vous voulez ajouter un rôle pour ce spectacle ? (y/n)")
        if response=='y':
            addRoleToSpec(conn)
        else :
            return
    else :
        print("\n Voici les rôles :")
        print("[CIN]                                     Nom     Prénom     Rôle")
        while raw:
            print("[%s]    %s    %s    %s" % (raw[0], raw[1], raw[2], raw[3]))
            raw = cur.fetchone()    
    return




def create(conn):
    print("!!!Attention : Pour pouvoir créer un spectacle avec succès, certains champs doivent être pré-remplis dans la base de données. ")
    print("Petits tips : ")
    print("Etapes pour créer une association depuis le menu principal : entrez 2 (gestion d'Association) -> entrez 3 (créer une nouvelle association)\n")
    print("Vous devez donner quelques informations afin qu'on puisse exécuter votre demande.\n")
    nom = quote(input("Nom du spectacle : "))
    duree = quote(input("Durée (format HH:mm): "))
    asso = quote(input("Proposé par quelle association : "))
    type = input("Type du spectacle, vous pouvez choisir parmi concert, standup, piecetheatre(Veuillez utiliser des lettres minuscules svp). : ")
    sql1 = "INSERT INTO Spectacle (nom, duree, asso_organisatrice) VALUES (%s, %s, %s)" % (nom, duree,asso)
    if type == "concert":
        compositeur = quote(input("Compositeur : "))
        annee = int(input("L'année d'émission  : "))
        genre = quote(input("Genre : "))
        sql2 = "INSERT INTO Concert (nom, compositeur, annee, genre) VALUES (%s, %s, %i, %s)" % (nom, compositeur,annee, genre)
    elif type == "standup":
        genre = quote(input("Genre : "))  
        sql2 = "INSERT INTO StandUp (nom, genre) VALUES (%s, %s)" % (nom, genre)
    elif type == "piecetheatre":
        auteur = quote(input("Auteur : "))
        annee = int(input("L'année d'émission  : "))
        genre = quote(input("Type  : "))
        sql2 = "INSERT INTO PieceTheatre (nom, auteur, annee, type) VALUES (%s, %s, %i, %s)" % (nom, auteur, annee, genre)
    else :
        print("Vous n'avez pas donné les informations correctes !")
        return    
    # Connect, execute SQL, close
    try :
        cur = conn.cursor()
        cur.execute(sql1)
        cur.execute(sql2)
        conn.commit()
        print(nom +" est créé avec succès !")
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)    
        conn.rollback()
    return 



def delete(conn):
    print("Vous devez donner quelques informations afin qu'on puisse exécuter votre demande.")
    #Vérifier si c'est un concert
    nom = quote(input("Nom du specatcle dont vous souhaitez supprimer : "))
    try :
        sql = "DELETE FROM spectacle WHERE nom=%s" % nom
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        print("Le spectacle "+nom+" est bien supprimé !")
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)    
        conn.rollback()
    return 


def update(conn):
    print("!!!Attention : Pour pouvoir modifier un spectacle avec succès, certains champs doivent être pré-remplis dans la base de données. ")
    print("Petits tips : ")
    print("Etapes pour créer une association depuis le menu principal : entrez 2 (gestion d'Association) -> entrez 3 (créer une nouvelle association)\n")
    print("Vous devez donner quelques informations afin qu'on puisse exécuter votre demande.")
    #Vérifier si c'est un concert
    nom = quote(input("Nom du specatcle dont vous souhaitez modifier les informations : "))
    cur0 = conn.cursor()
    sql0 = "SELECT * FROM Concert WHERE nom=%s" % nom
    cur0.execute(sql0)
    raw0 = cur0.fetchone()
    #Vérifier si c'est un standup
    cur1 = conn.cursor()
    sql1 = "SELECT * FROM StandUp WHERE nom=%s" % nom
    cur1.execute(sql1)
    raw1 = cur1.fetchone()
    #Vérifier si c'est un piecetheatre
    cur2 = conn.cursor()
    sql2 = "SELECT * FROM PieceTheatre WHERE nom=%s" % nom
    cur2.execute(sql2)
    raw2 = cur2.fetchone()
    if not raw0 and not raw1 and not raw2 :
        print("Spectacle n'exsite pas！")
        return
    
    if raw0 :
        champAmodifier = input("Donnez le champ que vous souhaitez modifier, vous pouvez choisir parmi nom, duree, asso_organisatrice, compositeur, annee, genre (Veuillez utiliser des lettres minuscules svp). :")
        valeurAdonner = input("Donnez la nouvelle valeur pour ce champ:")
        if champAmodifier=='nom' or champAmodifier=='duree' or champAmodifier=='asso_organisatrice' :
            sql = "UPDATE Spectacle SET %s=%s WHERE nom=%s" % (champAmodifier, quote(valeurAdonner), nom)
        elif champAmodifier=='compositeur' or champAmodifier=='genre' :
            sql = "UPDATE Concert SET %s=%s WHERE nom=%s" % (champAmodifier, quote(valeurAdonner), nom)
        elif champAmodifier=='annee' :
            sql = "UPDATE Concert SET %s=%i WHERE nom=%s" % (champAmodifier, int(valeurAdonner), nom)
        else :
            print("Vous n'avez pas donné les informations correctes !")
            return 
    elif raw1 :
        champAmodifier = input("Donnez le champ que vous souhaitez modifier, vous pouvez choisir parmi nom, duree, asso_organisatrice, genre (Veuillez utiliser des lettres minuscules svp). :")
        valeurAdonner = input("Donnez la nouvelle valeur pour ce champ:")
        if champAmodifier=='nom' or champAmodifier=='duree' or champAmodifier=='asso_organisatrice' :
            sql = "UPDATE Spectacle SET %s=%s WHERE nom=%s" % (champAmodifier, quote(valeurAdonner), nom)
        elif champAmodifier=='genre' :
            sql = "UPDATE StandUp SET %s=%s WHERE nom=%s" % (champAmodifier, quote(valeurAdonner), nom)
        else :
            print("Vous n'avez pas donné les informations correctes !")
            return
    elif raw2 :
        champAmodifier = input("Donnez le champ que vous souhaitez modifier, vous pouvez choisir parmi nom, duree, asso_organisatrice, auteur, annee, type (Veuillez utiliser des lettres minuscules svp). :")
        valeurAdonner = input("Donnez la nouvelle valeur pour ce champ:")
        if champAmodifier=='nom' or champAmodifier=='duree' or champAmodifier=='asso_organisatrice' :
            sql = "UPDATE Spectacle SET %s=%s WHERE nom=%s" % (champAmodifier, quote(valeurAdonner), nom)
        elif champAmodifier=='type' or champAmodifier=='auteur':
            sql = "UPDATE PieceTheatre SET %s=%s WHERE nom=%s" % (champAmodifier, quote(valeurAdonner), nom)
        elif champAmodifier=='annee':
            sql = "UPDATE PieceTheatre SET %s=%i WHERE nom=%s" % (champAmodifier, int(valeurAdonner), nom)
        else :
            print("Vous n'avez pas donné les informations correctes !")
            return
    # Connect, execute SQL, close
    try :
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        print("L'instruction est bien exécutée !")
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)    
        conn.rollback()
    return 


def showAllSeancesOfSpec(conn):
    print("Vous devez donner quelques informations afin qu'on puisse exécuter votre demande.")
    spec = input("Nom du spectacle : ")
    cur0 = conn.cursor()
    sql0 = "SELECT * FROM Spectacle s WHERE s.nom=%s" % quote(spec)
    cur0.execute(sql0)
    raw0 = cur0.fetchone()
    if not raw0 :
        print("Ce spectacle n'existe pas！")
        return
    cur = conn.cursor()
    sql = "SELECT * FROM Seance s WHERE s.nom=%s" % quote(spec)
    cur.execute(sql)
    raw = cur.fetchone()
    if not raw :
        print("Il n'y a pas de séances pour ce spectacle ！")
        response = input("Vous voulez générer une séance pour ce spectacle ? (y/n)")
        if response=='y':
            addSeanceToSpec(conn)
        else :
            return
    else :
        print("[id]  Spectacle    Salle  Date")
        while raw:
            print("[%s]    %s    %s    %s" % (raw[0], raw[1], raw[2], raw[3]))
            raw = cur.fetchone()    
    return

def addSeanceToSpec(conn):
    print("!!!Attention : Pour pouvoir ajouter une séance pour un spectacle, certains champs doivent être pré-remplis dans la base de données. ")
    print("Petits tips : ")
    print("Etapes pour créer une salle depuis le menu principal : entrez 2 (gestion d'Association) -> entrez 7 (Setting) -> entrez 1 (ajouter une salle)\n")
    print("Vous devez donner quelques informations afin qu'on puisse exécuter votre demande.")
    spec = input("Nom du spectacle : ")
    salle = input("Dans quelle salle (4 caractères) : ")
    date = input("Date (format YYYY-MM-DD) : ")
    time = input("Heure (format HH24:MI) : ")
    sql = "INSERT INTO Seance (nom, salle, date_time) VALUES (%s, %s, TO_TIMESTAMP(%s, 'YYYY-MM-DD HH24:MI')) RETURNING id" % (quote(spec), quote(salle), quote(date+" "+time))
    cur = conn.cursor()
    try:  
        cur.execute(sql)
        res = cur.fetchone()
        last_inserted_id = res[0]
        conn.commit()
        print( "Cette séance avec ID "+str(last_inserted_id)+" pour le spectacle "+spec+" est bien ajoutée !")
        response = input("Vous voulez ensuite générer les billets pour cette séance du spectacle ? (y/n)")
        if response=='y':
            billetterie.genererBillets(conn)
        else :
            return
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)    
        conn.rollback()
    return


def removeSeanceFromSpec(conn):
    print("Vous devez donner quelques informations afin qu'on puisse exécuter votre demande.")
    seance = input("ID de séance : ")
    cur0 = conn.cursor()
    sql0 = "SELECT * FROM Seance s WHERE s.id=%i" % int(seance)
    cur0.execute(sql0)
    raw0 = cur0.fetchone()
    if not raw0 :
        print("Cette séance n'existe pas！")
        return
    else :
        sql = "DELETE FROM Seance s WHERE s.id=%i" % (int(seance))
        cur = conn.cursor()
        try : 
            cur.execute(sql)
            conn.commit()
            print("Séance avec ID "+ seance +" est bien retirée du spectacle !")
        except (Exception, psycopg2.DatabaseError) as e:
            print(e)    
            conn.rollback()  
    return


def addRoleToSpec(conn):
    print("!!!Attention : Pour pouvoir ajouter un rôle à un spectacle, certains champs doivent être pré-remplis dans la base de données. ")
    print("Petits tips : ")
    print("Etapes pour créer un étudiant depuis le menu principal : entrez 1 (gestion de personne) -> entrez 1 (Etudiant) -> 3 (créer un étudiant)")
    print("Etapes pour créer un personnel depuis le menu principal : entrez 1 (gestion de personne) -> entrez 2 (Personnel) -> 3 (créer un personnel)")
    print("Etapes pour créer un membre extérieur depuis le menu principal : entrez 1 (gestion de personne) -> entrez 3 (Membre extérieur) -> 3 (créer un membre extérieur)")
    print("Etapes pour créer un Spectacle depuis le menu principal : entrez 3 (gestion de spectacle) -> entrez 4 (créer un spectacle) \n")
    print("Vous devez donner quelques informations afin qu'on puisse exécuter votre demande.")
    spec = input("Nom du spectacle : ")
    cin = input("CIN de la personne (36 caractères) : ")
    role = input("Rôle qu'il(elle) va jouer dans ce spectacle : ")
    sql = "INSERT INTO Role (descriptif, cin, nom_spec) VALUES (%s, %s, %s)" % (quote(role), quote(cin), quote(spec))
    cur = conn.cursor()
    try:  
        cur.execute(sql)
        conn.commit()
        print( "Le rôle "+role+" de "+cin+" est bien ajouté au Spectacle "+spec+ " !")
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)    
        conn.rollback()
    return

def modifyRoleOfSpec(conn):
    print("Vous devez donner quelques informations afin qu'on puisse exécuter votre demande.")
    spec = input("Nom du spectacle : ")
    cin = input("CIN de la personne (36 caractères) : ")
    sql = "SELECT * FROM Role r WHERE r.CIN=%s AND r.nom_spec=%s" % (quote(cin), quote(spec))
    cur = conn.cursor()
    cur.execute(sql)
    raw = cur.fetchone()
    if not raw :
        print("Cette personne ne joue aucun rôle dans ce spectacle !")
    else :
        role = input("Rôle qu'il(elle) va jouer dans ce spectacle : ")
        sql = "UPDATE Role SET descriptif=%s WHERE CIN=%s AND nom_spec=%s" % (quote(role), quote(cin), quote(spec))
        try : 
            cur.execute(sql)
            conn.commit()
            print( "Le rôle "+role+" de "+cin+" est bien ajouté au Spectacle "+spec+ " !")
        except (Exception, psycopg2.DatabaseError) as e:
            print(e)    
            conn.rollback()
    return


def removeRoleFromSpec(conn):
    print("Vous devez donner quelques informations afin qu'on puisse exécuter votre demande.")
    spec = input("Nom du spectacle : ")
    cin = input("CIN de la personne (36 caractères) : ")
    sql = "SELECT * FROM Role r WHERE r.CIN=%s AND r.nom_spec=%s" % (quote(cin), quote(spec))
    cur = conn.cursor()
    cur.execute(sql)
    raw = cur.fetchone()
    if not raw :
        print("Cette personne ne joue aucun rôle dans ce spectacle !")
    else :
        sql = "DELETE FROM Role r WHERE r.CIN=%s AND r.nom_spec=%s" % (quote(cin), quote(spec))
        try : 
            cur.execute(sql)
            conn.commit()
            print(cin+" est bien retirée du spectacle "+spec+ " !")
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

