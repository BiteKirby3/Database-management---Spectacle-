import psycopg2

def menu(conn):
    print("\n*Page - Gestion de membre extérieur*")
    action = '-1'
    while action != '0':
        print("\nVous pouvez effectuer les actions suivantes :")
        action = input("Entrez 1 pour afficher tout les membres extérieur,\n  2 pour rechercher par CIN,\n  3 pour créer un nouveau membre extérieur,\n  4 pour modifier un membre extérieur.\n (entrez 0 pour retourner à la page précédente) : ")
        if action == '1':
            findAll(conn)   
        elif action == '2':
            findOneById(conn)
        elif action == '3':
            create(conn)
        elif action == '4':
            update(conn)
    print("*Retour à la page principale*\n")
        

def findAll(conn):
    # Open a cursor to send SQL commands
    cur = conn.cursor()
    # Execute a SQL SELECT command
    sql = "SELECT  ps.cin, ps.nom, ps.prenom, ex.telephone, ex.organisme FROM Exterieur ex JOIN Personne ps ON ex.cin = ps.cin"
    cur.execute(sql)
    # Fetch data line by line
    raw = cur.fetchone()
    if raw:
        print("Voici tous les membres extérieurs :")
        print("[CIN]                                    Nom        Prénom        Téléphone      Organisme d'affiliation")
        while raw:
            print("[%s]    %s    %s    %s    %s" % (raw[0], raw[1], raw[2], raw[3], raw[4]))
            raw = cur.fetchone()
            return
    else :
        print("Aucun extérieur enregistré ！")
        response = input("Vous voulez créer un extérieur ? (y/n)")
        if response=='y':
            create(conn)
        else :
            return


def findOneById(conn):
    print("Vous devez donner quelques informations afin qu'on puisse exécuter votre demande.")
    cin = quote(input("CIN (36 caractères) : "))
    cur = conn.cursor()
    sql = "SELECT  ps.cin, ps.nom, ps.prenom, ex.telephone, ex.organisme FROM Exterieur ex JOIN Personne  ps ON ex.cin = ps.cin WHERE ps.cin=%s" % cin
    cur.execute(sql)
    raw = cur.fetchone()
    if not raw :
        print("Membre non trouvé ！")
    else :
        print("[CIN]                                Nom    Prénom    Téléphone    Organisme d'affiliation")
        print("[%s]    %s    %s    %s    %s" % (raw[0], raw[1], raw[2], raw[3], raw[4]))
    return

def create(conn):
    print("Vous devez donner quelques informations afin qu'on puisse exécuter votre demande.")
    cin = quote(input("CIN (36 caractères) : "))
    nom = quote(input("Nom : "))
    prenom = quote(input("Prénom : "))
    tele = quote(input("Numéro portable (10 caractères) : "))
    organisme = quote(input("Organisme d'affiliation : "))
    # Connect, execute SQL, close
    sql1 = "INSERT INTO personne (cin, nom, prenom) VALUES (%s, %s, %s)" % (cin, nom, prenom)
    sql2 = "INSERT INTO exterieur (cin, telephone, organisme) VALUES (%s, %s, %s)" % (cin, tele, organisme)
    try :
        cur = conn.cursor()
        cur.execute(sql1)
        cur.execute(sql2)
        conn.commit()
        print(cin+" est créé avec succès !")
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)    
        conn.rollback()
    return 

def update(conn):
    print("Vous devez donner quelques informations afin qu'on puisse exécuter votre demande.")
    cin = quote(input("CIN de l'extérieur dont vous souhaitez modifier les informations (36 caractères): "))
    cur = conn.cursor()
    sql0 = "SELECT * FROM Exterieur WHERE cin=%s" % cin
    cur.execute(sql0)
    raw = cur.fetchone()
    if not raw :
        print("Extérieur n'exsite pas！")
        return
    champAmodifier = input("Donnez le champ que vous souhaitez modifier, vous pouvez choisir parmi cin, prenom, nom, telephone, organisme(Veuillez utiliser des lettres minuscules svp). :")
    valeurAdonner = input("Donnez la nouvelle valeur pour ce champ:")
    # Connect, execute SQL, close
    if champAmodifier=='cin' or champAmodifier=='nom' or champAmodifier=='prenom':
        sql = "UPDATE personne SET %s=%s WHERE cin=%s" % (champAmodifier, quote(valeurAdonner), cin)
    elif champAmodifier=='telephone' or champAmodifier=='organisme':
        sql = "UPDATE exterieur SET %s=%s WHERE cin=%s" % (champAmodifier, quote(valeurAdonner), cin)
    else :
        print("Vous n'avez pas donné les informations correctes !")
        return
    try :
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        print("L'instruction est bien exécutée !")
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

