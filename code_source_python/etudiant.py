import psycopg2

def menu(conn):
    print("\n*Page - Gestion des étudiants UTX*")
    action = '-1'
    while action != '0':
        print("\nVous pouvez effectuer les actions suivantes :")
        action = input("Entrez 1 pour afficher tous les étudiants,\n  2 pour rechercher par CIN,\n  3 pour créer un étudiant,\n  4 pour modifier un étudiant.\n (entrez 0 pour retourner à la page précédente) : ")
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
    sql = "SELECT ps.cin, ps.nom, ps.prenom FROM Etudiant e JOIN Personne ps ON e.cin = ps.cin"
    cur.execute(sql)
    # Fetch data line by line
    raw = cur.fetchone()
    if raw:
        print("Voici tout les étudiants :")
        print("[CIN]                                      Nom    Prénom")
        while raw:
            print("[%s]    %s    %s" % (raw[0], raw[1], raw[2]))
            raw = cur.fetchone()
        return
    else :
        print("Aucun étudiant enregistré！")
        response = input("Vous voulez créer un étudiant ? (y/n)")
        if response=='y':
            create(conn)
        else :
            return



def findOneById(conn):
    print("Vous devez donner quelques informations afin qu'on puisse exécuter votre demande.")
    cin = quote(input("CIN (36 caractères) : "))
    cur = conn.cursor()
    sql = "SELECT  ps.cin, ps.nom, ps.prenom FROM Etudiant e JOIN Personne ps ON e.cin = ps.cin WHERE e.cin=%s" % cin
    cur.execute(sql)
    raw = cur.fetchone()
    if not raw :
        print("Etudiant non trouvé ！")
    else :
        print("[CIN]                               Nom    Prénom")
        print("[%s]    %s    %s" % (raw[0], raw[1], raw[2]))
    return

def create(conn):
    print("Vous devez donner quelques informations afin qu'on puisse exécuter votre demande.")
    cin = quote(input("CIN (36 caractères) : "))
    nom = quote(input("Nom : "))
    prenom = quote(input("Prénom : "))
    # Connect, execute SQL, close
    sql1 = "INSERT INTO personne (cin, nom, prenom) VALUES (%s, %s, %s)" % (cin, nom, prenom)
    sql2 = "INSERT INTO etudiant (cin) VALUES (%s)" % (cin)
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
    cin = quote(input("CIN de l'étudiant dont vous souhaitez modifier les informations (36 caractères): "))
    cur = conn.cursor()
    sql0 = "SELECT * FROM Etudiant WHERE cin=%s" % cin
    cur.execute(sql0)
    raw = cur.fetchone()
    if not raw :
        print("Etudiant n'exsite pas！")
        return
    champAmodifier = input("Donnez le champ que vous souhaitez modifier, vous pouvez choisir parmi cin, prenom, nom(Veuillez utiliser des lettres minuscules svp). :")
    valeurAdonner = input("Donnez la nouvelle valeur pour ce champ:")
    # Connect, execute SQL, close
    if champAmodifier=='cin' or champAmodifier=='nom' or champAmodifier=='prenom':
        sql = "UPDATE personne SET %s=%s WHERE cin=%s" % (champAmodifier, quote(valeurAdonner), cin)
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



#fonction de service
def quote(s):
  if s:
    return '\'%s\'' % s
  else:
    return 'NULL'

