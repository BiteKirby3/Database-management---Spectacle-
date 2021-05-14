import psycopg2
import etudiant
import personnel
import exterieur
import association
import spectacle
import billetterie

#BD Settings
HOST = "localhost"
USER = "postgres"
PASSWORD = "root"
DATABASE = "postgres"
#Se connecter à la base de données 
conn = psycopg2.connect("host=%s dbname=%s user=%s password=%s" %(HOST, DATABASE, USER, PASSWORD))

redirection = '-1'
while redirection != '0':
    print("*Gestion de spectacles culturels*")
    redirection = input("Entrez 1 pour gestion de Personne,\n 2 pour Association,\n 3 pour Spectacle,\n 4 pour Billeterie. \n (entrez 0 pour quitter le programme) : ")
    
    if redirection == '2':
        association.menu(conn);     
    elif redirection == '3':
        spectacle.menu(conn);
    elif redirection == '4':
        billetterie.menu(conn)
    elif redirection == '1':
        redirection = input("Quel est le type de personne ? Entrez 1 pour Etudiant, 2 pour Personnel de l'université, 3 pour Membre extérieur (entrez 0 pour quitter le programme) : ")
        if redirection == '1':
            etudiant.menu(conn);
        elif redirection == '2':
            personnel.menu(conn);
        elif redirection == '3':
            exterieur.menu(conn);
conn.close()
print("*Log out*")