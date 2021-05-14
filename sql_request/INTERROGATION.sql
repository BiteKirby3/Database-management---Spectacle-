--Tous les étudiants
SELECT ps.cin, ps.nom, ps.prenom 
FROM Etudiant e JOIN Personne ps ON e.cin = ps.cin;

--Tout le personnel 
SELECT  ps.cin, ps.nom, ps.prenom, pl.statut 
FROM Personnel pl JOIN Personne  ps ON pl.cin = ps.cin;

--Tous les membres extérieurs
SELECT  ps.cin, ps.nom, ps.prenom, ex.telephone, ex.organisme 
FROM Exterieur ex JOIN Personne ps ON ex.cin = ps.cin;

--Rechercher un extérieur par CIN 
SELECT  ps.cin, ps.nom, ps.prenom, ex.telephone, ex.organisme 
FROM Exterieur ex JOIN Personne  ps ON ex.cin = ps.cin 
WHERE ps.cin='A6755432O82631042DHQTD1763';

--Rechercher un étudiant par nom et prénom
SELECT  ps.cin, ps.nom, ps.prenom 
FROM Etudiant et JOIN Personne  ps ON et.cin = ps.cin 
WHERE ps.nom='BEAUMER' AND ps.prenom='Marie';

--Nombre de salle dans chaque bâtiment 
SELECT Salle.Bat,COUNT(code)
FROM Salle
GROUP BY Salle.Bat;

--Tous les spectacles de type Concert
SELECT s.nom, s.duree, s.asso_organisatrice, c.compositeur, c.annee, c.genre 
FROM Spectacle s, Concert c 
WHERE s.nom=c.nom;

--Tous les spectacles de type StandUp
SELECT s.nom, s.duree, s.asso_organisatrice, su.genre 
FROM Spectacle s, StandUp su 
WHERE s.nom=su.nom;

--Tous les spectacles de type PieceTheatre
SELECT s.nom, s.duree, s.asso_organisatrice, pt.auteur, pt.annee, pt.type 
FROM Spectacle s, PieceTheatre pt 
WHERE s.nom=pt.nom;

--Afficher les rôles d'un spectacle
SELECT p.cin, p.nom, p.prenom, r.descriptif 
FROM role r, personne p 
WHERE r.cin=p.cin AND r.nom_spec='Marée basse';

--Afficher le rôle d'une personne dans un spectacle
SELECT descriptif
FROM Role r 
WHERE r.CIN='A0382748Z02928375KDJH19238' AND r.nom_spec='Marée basse';

--Toutes les séances d'un spectacle
SELECT *
FROM Seance s 
WHERE s.nom='Marée basse';

--Tous les billets d'une séance
SELECT b.identifiant, b.categorie, c.tarif, b.acheteur 
FROM Billet b, CatBillet c 
WHERE b.seance=3 AND b.categorie=c.categorie 
ORDER BY identifiant ASC;

--Toutes les séances à venir
SELECT * FROM 
Seance s 
WHERE s.date_time>Now();

--Nombre de billets vendus et le revenu par catégorie pour une séance donnée
SELECT billet.categorie, count(identifiant) as billets_vendus, sum(tarif) 
FROM billet, catBillet WHERE seance='3' AND acheteur IS not null AND billet.categorie=catBillet.categorie
Group by billet.categorie;

--Nombre de billets restants par catégorie pour une séance donnée
SELECT billet.categorie, count(identifiant) as billets_non_vendus 
FROM billet 
WHERE seance=3 AND acheteur IS null
Group by categorie;

--Les informations concernant un billet
SELECT b.identifiant, b.categorie, c.tarif, b.acheteur, b.seance, s.nom, s.salle, s.date_time 
FROM Billet b, CatBillet c, Seance s 
WHERE b.identifiant=1 AND b.seance=s.id AND b.categorie=c.categorie;

--Types de billets qui peuvent encore être achetés pour une séance donnée
SELECT DISTINCT b.categorie, c.tarif  
FROM Billet b, CatBillet c 
WHERE b.seance=3 AND b.acheteur IS NULL AND b.categorie=c.categorie