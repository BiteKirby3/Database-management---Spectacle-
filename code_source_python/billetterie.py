import psycopg2
import spectacle
from datetime import date

def menu(conn):
    print("\n*Page - Billetterie*")
    action = '-1'
    while action != '0':
        print("\nVous pouvez effectuer les actions suivantes :")
        action = input("Entrez 1 pour afficher toutes les séances à venir,\n  2 pour vérifier l'état des ventes de billets d'une séance,\n  3 pour acheter un billet d'une séance,\n  4 pour vérifier l'état d'un billet,\n  5 pour générer des billets pour une séance,\n  6 pour Setting (catégorie de billet, prix...) \n(entrez 0 pour retourner à la page précédente) : ")
        if action == '1':
            showAllFutureSeance(conn)
        elif action == '2':
            vente_action = input("Entrez 1 pour voir la vente de billets d'une séance,\n  2 pour afficher les statistiques du box-office d'une séance.\n  (0 pour sortir) : ")
            if vente_action == '1':
                showBilletsOfASeance(conn)                
            elif vente_action == '2':
                showStatistiqueOfASeance(conn)
        elif action == '3':
            acheterBillet(conn)
        elif action == '4':
            checkBillet(conn)
        elif action == '5':
            genererBillets(conn)
        elif action == '6':
            setting_action = input("Entrez 1 pour voir des catégories de billet,\n  2 pour ajouter une catégorie de billet,\n  3 pour modifier le prix du billet par catégorie.\n(0 pour sortir) : ")
            if setting_action == '1':
                showCatBillet(conn)
            elif setting_action == '2':
                addCatBillet(conn)
            elif setting_action == '3':
                modifyPriceOfCatBillet(conn)
    print("*Retour à la page principale*\n")
    
 
    
 
def showBilletsOfASeance(conn):
    print("Vous devez donner quelques informations afin qu'on puisse exécuter votre demande.")
    idSeance = input("ID de Séance : ")
    # Vérifiez si cette séance existe déjà 
    cur = conn.cursor()
    sql = "SELECT b.identifiant, b.categorie, c.tarif, b.acheteur FROM Billet b, CatBillet c WHERE b.seance=%i AND b.categorie=c.categorie ORDER BY identifiant ASC" % int(idSeance)
    cur.execute(sql)
    raw = cur.fetchone()
    if not raw : 
        print("Il n'y a pas de billets pour cette séance.")
        response = input("Voulez-vous générer des billets pour cette séance ?(y/n)")
        if response=='y':
            genererBillets(conn)
        else :
            return
    else :
        print("[ID]     Catégorie        Tarif       Acheteur  ")
        while raw:
            print("[%i]     %s     %.2f     %s"%(raw[0],raw[1],raw[2],raw[3]))
            raw = cur.fetchone()     
    return
   


def showAllFutureSeance(conn):
    # Open a cursor to send SQL commands
    cur = conn.cursor()
    # Execute a SQL SELECT command
    sql = "SELECT * FROM Seance s WHERE s.date_time>Now()"
    cur.execute(sql)
    # Fetch data line by line
    raw = cur.fetchone()
    if raw :
        print("Voir toutes les séances à venir :")
        print("[ID]    Spectacle    Salle    Date")
        while raw:
            print("[%s]       %s       %s       %s" % (raw[0], raw[1], raw[2], raw[3]))
            raw = cur.fetchone()
        return
    else :
        print("Aucune séance trouvée！")
        response = input("Vous voulez créer une séance ? (y/n)")
        if response=='y':
            spectacle.addSeanceToSpec(conn)
        else :
            return
    return





def genererBillets(conn):
    print("!!!Attention : Pour pouvoir generer des billets pour une séance, certains champs doivent être pré-remplis dans la base de données. ")
    print("Petits tips : ")
    print("Etapes pour créer une catégorie de billet depuis le menu principal : entrez 4 (Billetterie) -> entrez 6 (Setting) -> entrez 2 (ajouter une catégorie de billet)")
    print("Etapes pour créer une séance depuis le menu principal : entrez 3 (Geation de spectacle) -> entrez 7 (Gérer les séances d'un spectacle) -> entrez 2 (ajouter une séance pour un spectacle)\n")
    print("Vous devez donner quelques informations afin qu'on puisse exécuter votre demande.")
    
    idSeance = input("ID de Séance : ")
    # Vérifiez si cette séance existe déjà 
    cur0 = conn.cursor()
    sql0 = "SELECT se.id, se.nom, sa.nb_max FROM Seance se, Salle sa WHERE se.id=%i AND se.salle=sa.code AND se.date_time>Now()" % int(idSeance)
    cur0.execute(sql0)
    raw0 = cur0.fetchone()
    # Vérifiez si les billet ont été générés 
    cur1 = conn.cursor()
    sql1 = "SELECT * FROM Billet WHERE seance=%i" % int(idSeance)
    cur1.execute(sql1)
    raw1 = cur1.fetchone()
    
    if raw0 and not raw1:
       cur = conn.cursor()
       nbMaxBillet = raw0[2]
       nbCatBillet = 0
       nomCatBillet =[]
       nbBilletParCat =[]
       ok = False
       while not ok :
           nbCatBillet = 0
           nomCatBillet =[]
           nbBilletParCat =[]
           nbCatBillet = int(input("Vous souhaitez générer combien de catégories de billet pour cette séance ?: "))
           for x in range(nbCatBillet):
               nomCatBillet.append(input("Nom de Catégorie Billet "+str(x+1)+" : "))
               nbBilletParCat.append(int(input("Nombre de billets pour la Catégorie "+str(x+1)+" : ")))
           if sum(nbBilletParCat)>nbMaxBillet:
               print("La salle ne peut accueillir que "+str(nbMaxBillet)+" personnes, veuillez réinitialiser la catégorie de billet et le nombre de billets par catégorie." )
               ok = False
           else :
               ok = True
       try:
           for x in range(nbCatBillet):
               for y in range(nbBilletParCat[x]):
                   insert_sql = "INSERT INTO Billet (categorie, date_creation, seance) VALUES (%s, to_date(%s,'YYYYMMDD'), %i)" % (quote(nomCatBillet[x]), quote(getCurrentDate()), int(idSeance))
                   cur.execute(insert_sql)
           conn.commit()
           print("Les billets de séance "+str(idSeance)+" sont bien générés !")
       except (Exception, psycopg2.DatabaseError) as e:
           print(e)    
           conn.rollback()
    else :
        print("Vous ne pouvez pas générer les billets pour cette séance. ")
    return





def showStatistiqueOfASeance(conn):
    print("Vous devez donner quelques informations afin qu'on puisse exécuter votre demande.")  
    idSeance = input("ID de Séance : ")
    cur = conn.cursor()
    sql0 = "Select categorie From Billet Where seance=%i GROUP BY categorie" %int(idSeance)
    cur.execute(sql0)
    raw = cur.fetchone()
    catBillet = []
    nbBilletVendusParCat = []
    nbBilletNonVenduParCat = []
    sumVenteParCat = []
    if not raw :
        print("Il n'y a pas de billets pour cette séance.")
        response = input("Voulez-vous générer des billets pour cette séance ?(y/n)")
        if response=='y':
            genererBillets(conn)
        else :
            return
    else :
        while raw :
            catBillet.append(raw[0])
            cur1 = conn.cursor()
            sql1 = "SELECT billet.categorie, count(identifiant) as billets_vendus, sum(tarif) FROM billet, catBillet WHERE seance=%i AND acheteur IS not null AND billet.categorie=catBillet.categorie AND billet.categorie=%s Group by billet.categorie" %(int(idSeance),quote(raw[0]))
            cur1.execute(sql1)
            raw1 = cur1.fetchone()
            if not raw1 :
                nbBilletVendusParCat.append(0)
                sumVenteParCat.append(0)
            else:
                nbBilletVendusParCat.append(raw1[1])
                sumVenteParCat.append(raw1[2])
            cur2 = conn.cursor()
            sql2 = "SELECT billet.categorie, count(identifiant) as billets_non_vendus FROM billet WHERE seance=%i AND acheteur IS null AND billet.categorie=%s Group by categorie" %(int(idSeance), quote(raw[0]))
            cur2.execute(sql2)
            raw2 = cur2.fetchone()
            if not raw2 :
                nbBilletNonVenduParCat.append(0)
            else:
                nbBilletNonVenduParCat.append(raw2[1])
            raw = cur.fetchone()
        print("Box Office de Séance ID" + str(idSeance))
        taille = len(catBillet)
        print("Catégorie      Nb total de Billets      BilletsVendus      BilletsRestants      Présence      Revenu(€)")
        for x in range(taille):
            print("\n%s    %i      %i      %i      %.2f     %.2f"%(catBillet[x],nbBilletVendusParCat[x]+nbBilletNonVenduParCat[x],nbBilletVendusParCat[x],nbBilletNonVenduParCat[x], nbBilletVendusParCat[x]/(nbBilletVendusParCat[x]+nbBilletNonVenduParCat[x]), sumVenteParCat[x]))
        print("\n Total     %i      %i      %i      %.2f      %.2f"%((sum(nbBilletVendusParCat)+sum(nbBilletNonVenduParCat)), sum(nbBilletVendusParCat), sum(nbBilletNonVenduParCat), sum(nbBilletVendusParCat)/(sum(nbBilletVendusParCat)+sum(nbBilletNonVenduParCat)) ,sum(sumVenteParCat)))
    return




    
def checkBillet(conn):
    print("Vous devez donner quelques informations afin qu'on puisse exécuter votre demande.")
    idBillet = input("ID de Billet : ")
    sql = "SELECT b.identifiant, b.categorie, c.tarif, b.acheteur, b.seance, s.nom, s.salle, s.date_time FROM Billet b, CatBillet c, Seance s WHERE b.identifiant=%i AND b.seance=s.id AND b.categorie=c.categorie" %(int(idBillet))
    cur = conn.cursor()
    cur.execute(sql)
    raw = cur.fetchone()
    if not raw :
        print("Billet non trouvé !")
    else :
        print("[ID]   Catégorie     Tarif    Acheteur                               SéanceID    Spectacle    Salle    Datetime")
        print("[%i]     %s     %.2f     %s      %i      %s       %s      %s"%(raw[0],raw[1],raw[2],raw[3],raw[4],raw[5],raw[6],raw[7]))
    return



    
def acheterBillet(conn):
    print("!!!Attention : Pour pouvoir acheter un billet d'une séance, certains champs doivent être pré-remplis dans la base de données. ")
    print("Petits tips : ")
    print("Etapes pour créer une séance depuis le menu principal : entrez 3 (Geation de spectacle) -> entrez 7 (Gérer les séances d'un spectacle) -> entrez 2 (ajouter une séance pour un spectacle)")
    print("Etapes pour créer un étudiant depuis le menu principal : entrez 1 (gestion de personne) -> entrez 1 (Etudiant) -> 3 (créer un étudiant)")
    print("Etapes pour créer un personnel depuis le menu principal : entrez 1 (gestion de personne) -> entrez 2 (Personnel) -> 3 (créer un personnel)")
    print("Etapes pour créer un membre extérieur depuis le menu principal : entrez 1 (gestion de personne) -> entrez 3 (Membre extérieur) -> 3 (créer un membre extérieur)\n")
    print("Vous devez donner quelques informations afin qu'on puisse exécuter votre demande.")
    idSeance = input("ID de Séance : ")
    cur = conn.cursor()
    # Execute a SQL SELECT command
    sql = "SELECT DISTINCT b.categorie, c.tarif  FROM Billet b, CatBillet c WHERE b.seance=%i AND b.acheteur IS NULL AND b.categorie=c.categorie" %(int(idSeance))
    cur.execute(sql)
    # Fetch data line by line
    raw = cur.fetchone()
    if not raw :
        print("Désolé, vous ne pouvez pas acheter de billets pour cette séance !")
    else :
        print("Vous pouvez choisir parmi ces catégories : ")
        print("[Catégories]    Tarif")
        while raw:
            print("%s      %.2f" % (raw[0],raw[1]))
            raw = cur.fetchone()
        catBillet = input("Votre catégorie de billet : ")
        sql = "SELECT identifiant FROM Billet WHERE seance=%i AND acheteur IS NULL AND categorie=%s ORDER BY identifiant ASC LIMIT 1" %(int(idSeance),quote(catBillet))
        cur.execute(sql)
        raw = cur.fetchone()
        if not raw :
            print("ERREUR 500")
        else :
            try:
                idBillet = raw[0]
                cin = input("CIN de l'acheteur (36 caractères) : ")
                sql = "UPDATE Billet SET acheteur=%s WHERE identifiant=%i" %(quote(cin),idBillet)
                cur.execute(sql)
                conn.commit()
                print("Le billet numéro "+str(idBillet)+" a été réservé par "+cin+" !")
            except (Exception, psycopg2.DatabaseError) as e:
                print(e)    
                conn.rollback()
    return 




def showCatBillet(conn):
    # Open a cursor to send SQL commands
    cur = conn.cursor()
    # Execute a SQL SELECT command
    sql = "SELECT * FROM CatBillet"
    cur.execute(sql)
    # Fetch data line by line
    raw = cur.fetchone()
    if raw :
        print("Voici toutes les catégorie de billet :")
        print("[catégorie]       Tarif")
        while raw:
            print("[%s]    %f" % (raw[0], raw[1]))
            raw = cur.fetchone()
        return
    else :
        print("Pas de catégorie enregistrée！")
        response = input("Vous voulez créer une catégorie ? (y/n)")
        if response=='y':
            addCatBillet(conn)
        else :
            return
    return


def addCatBillet(conn):
    print("Vous devez donner quelques informations afin qu'on puisse exécuter votre demande.")
    cat = input("Catégorie : ")
    # Vérifiez si cette categorie existe déjà 
    cur = conn.cursor()
    sql0 = "SELECT * FROM CatBillet WHERE categorie=%s" % quote(cat)
    cur.execute(sql0)
    raw = cur.fetchone()
    try:
        if not raw :
             tarif = input("Tarif : ")
             sql1 = "INSERT INTO CatBillet (categorie, tarif) VALUES (%s,%f)" % (quote(cat),float(tarif))
             cur.execute(sql1)
             conn.commit()
             print("La catégorie "+cat+" est créée avec succès !")
        else :
            print("Cette catégorie existe déjà ！")
            response = input("Voulez-vous modifier le tarif de cette catégorie ? (y/n)")
            if response=='y':
                modifyPriceOfCatBillet(conn)
            else :
                return
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)    
        conn.rollback()
    return 



def modifyPriceOfCatBillet(conn):
    print("Vous devez donner quelques informations afin qu'on puisse exécuter votre demande.")
    cat = input("Catégorie : ")
    # Vérifiez si cette categorie existe déjà 
    cur = conn.cursor()
    sql0 = "SELECT * FROM CatBillet WHERE categorie=%s" % quote(cat)
    cur.execute(sql0)
    raw = cur.fetchone()
    try:
        if raw :
            tarif = input("Nouveau prix : ")
            sql1 = "Update CatBillet SET tarif=%f WHERE categorie=%s" % (float(tarif), quote(cat))
            cur.execute(sql1)
            conn.commit()
            print("Le tarif de catégorie "+cat+" est modifié !")
        
        else :
            print("Cette catégorie n'existe pas !")
            response = input("Voulez-vous créer cette catégorie ? (y/n)")
            if response=='y':
                addCatBillet(conn)
            else :
                return
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)    
        conn.rollback()
    return

#fonction de service
def quote(s):
  if s:
    return '\'%s\'' % s
  else:
    return 


def getCurrentDate():
    today = date.today()
    return today.strftime("%Y%m%d")