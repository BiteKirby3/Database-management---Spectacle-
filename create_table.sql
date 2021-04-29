DROP TABLE IF EXISTS Billet;
DROP TABLE IF EXISTS CatBillet;
DROP TABLE IF EXISTS MembreAsso;
DROP TABLE IF EXISTS Exterieur;
DROP TABLE IF EXISTS Personnel;
DROP TABLE IF EXISTS Role;
DROP TABLE IF EXISTS PieceTheatre;
DROP TABLE IF EXISTS StandUp;
DROP TABLE IF EXISTS Concert;
DROP TABLE IF EXISTS Seance;
DROP TABLE IF EXISTS Spectacle;
DROP TABLE IF EXISTS Association;
DROP TABLE IF EXISTS Etudiant;
DROP TABLE IF EXISTS Personne;
DROP TABLE IF EXISTS CategorieAsso;
DROP TABLE IF EXISTS Salle;
DROP TABLE IF EXISTS Batiment;

CREATE TABLE Batiment
(
lettre CHAR PRIMARY KEY
);
 
CREATE TABLE Salle
(
code CHAR(4) PRIMARY KEY,
numero NUMERIC(3) NOT NULL,
type VARCHAR NOT NULL CHECK (type='cours' OR type='amphi' OR type='bureau'),
nb_max INTEGER NOT NULL CHECK (nb_max > 0),
bat CHAR NOT NULL,
FOREIGN KEY(bat) REFERENCES Batiment(lettre)
);
 
CREATE TABLE CategorieAsso
(
intitule VARCHAR PRIMARY KEY
);
 
CREATE TABLE Personne(
     CIN CHAR(36) PRIMARY KEY,
    nom  VARCHAR NOT NULL,
    prenom VARCHAR NOT NULL
);
 
CREATE TABLE Etudiant (
CIN VARCHAR(36) PRIMARY KEY,
FOREIGN KEY (CIN) REFERENCES Personne(CIN)
);
 
CREATE TABLE Association
(
nom VARCHAR PRIMARY KEY,
mail VARCHAR UNIQUE NOT NULL,
date_creation date NOT NULL,
site_web VARCHAR,
type VARCHAR NOT NULL,
salle VARCHAR(4) NOT NULL,
treso_asso VARCHAR(36) NOT NULL,
presid_asso VARCHAR(36) NOT NULL,
FOREIGN KEY(type) REFERENCES CategorieAsso(intitule),
FOREIGN KEY(salle) REFERENCES Salle(code),
FOREIGN KEY(treso_asso) REFERENCES Etudiant(CIN),
FOREIGN KEY(presid_asso) REFERENCES Etudiant(CIN),
CHECK  (treso_asso<>presid_asso)
);
 
CREATE TABLE Spectacle
(
nom VARCHAR PRIMARY KEY,
durée TIME NOT NULL, 
asso_organisatrice VARCHAR NOT NULL, 
FOREIGN KEY (asso_organisatrice) REFERENCES Association(nom)
); 
 
 
CREATE TABLE Seance
(
date_time DATE PRIMARY KEY,
nom VARCHAR NOT NULL, 
salle VARCHAR(4) NOT NULL, 
FOREIGN KEY (nom) REFERENCES Spectacle(nom),
FOREIGN KEY (salle) REFERENCES Salle(code)
);
 
CREATE TABLE Concert
(
nom VARCHAR PRIMARY KEY, 
compositeur VARCHAR NOT NULL, 
année NUMERIC(4) NOT NULL, 
genre VARCHAR NOT NULL, 
FOREIGN KEY (nom) REFERENCES Spectacle(nom)
);
 
 
CREATE TABLE StandUp
(
nom VARCHAR PRIMARY KEY, 
genre VARCHAR NOT NULL, 
FOREIGN KEY (nom) REFERENCES Spectacle(nom)
);
CREATE TABLE PieceTheatre
(
nom VARCHAR PRIMARY KEY, 
auteur VARCHAR NOT NULL, 
année NUMERIC(4) NOT NULL, 
type VARCHAR NOT NULL, 
FOREIGN KEY (nom) REFERENCES Spectacle(nom)
);

 
CREATE TABLE Role
(
descriptif VARCHAR NOT NULL, 
CIN VARCHAR(36)  NOT NULL, 
nom_spec VARCHAR  NOT NULL, 
FOREIGN KEY (CIN) REFERENCES Personne(CIN), 
FOREIGN KEY (nom_spec) REFERENCES Spectacle(nom), 
PRIMARY KEY (descriptif, CIN, nom_spec)
);
 
 
 
CREATE TABLE Personnel (
CIN VARCHAR(36) PRIMARY KEY,
statut VARCHAR NOT NULL,
FOREIGN KEY (CIN) REFERENCES Personne (CIN)
);
 
CREATE TABLE Exterieur (
CIN VARCHAR(36) PRIMARY KEY,
telephone CHAR(10) NOT NULL,
organisme VARCHAR NOT NULL,
FOREIGN KEY (CIN) REFERENCES Personne(CIN)
);
 
CREATE TABLE MembreAsso(
nom_asso VARCHAR,
membre VARCHAR(36),
PRIMARY KEY(nom_asso, membre),
FOREIGN KEY(nom_asso) REFERENCES Association(nom),    
FOREIGN KEY(membre) REFERENCES Etudiant(CIN)
);
 
CREATE TABLE CatBillet (
  categorie VARCHAR NOT NULL CHECK (categorie='invitation' OR categorie='billet étudiant' OR categorie='billet_exterieur'),
  nb_billets_dispo INTEGER NOT NULL,
  nb_billets_vendus INTEGER NOT NULL,
  Tarif FLOAT NOT NULL,
  PRIMARY KEY(Categorie)
);
 
CREATE TABLE Billet (
  categorie VARCHAR NOT NULL CHECK (categorie='invitation' OR categorie='billet étudiant' OR categorie='billet_exterieur'),
  identifiant INTEGER NOT NULL,
  date_creation DATE NOT NULL,
  seance DATE NOT NULL,
  acheteur VARCHAR(36) NOT NULL,
  PRIMARY KEY(identifiant),
  FOREIGN KEY (seance) REFERENCES Seance (date_time),
  FOREIGN KEY (categorie) REFERENCES CatBillet (categorie),
  FOREIGN KEY (acheteur) REFERENCES Personne(CIN)
);

