INSERT INTO Batiment VALUES ('A'); 
INSERT INTO Batiment VALUES ('B'); 
INSERT INTO Batiment VALUES ('C'); 

INSERT INTO Salle  VALUES ('A101', 101, 'amphi', 200, 'A');
INSERT INTO Salle  VALUES ('A102', 102, 'cours', 30, 'A');
INSERT INTO Salle  VALUES ('B200', 200, 'bureau', 4, 'B');
INSERT INTO Salle  VALUES ('C201', 201, 'cours', 30, 'C');

INSERT INTO Personne  VALUES ('A0382748Z02928375KDJH19238', 'CUVILLER', 'Charles');
INSERT INTO Personne  VALUES ('A0734748Z01993657PPAH19238', 'BEAUMER', 'Marie');
INSERT INTO Personne  VALUES ('A0991748Z03901928NDKH19238', 'XIE', 'Sihan');
INSERT INTO Personne  VALUES ('A0221748Z049162731PZH19238', 'VERRIER', 'Garance');
INSERT INTO Personne  VALUES ('A0382fefwe2928375KDJH19238', 'Hubert', 'Anna');
INSERT INTO Personne  VALUES ('A0734748Z0fefewf7PPAH19238', 'Hubert', 'Anne');
INSERT INTO Personne  VALUES ('A0991748Z03901928NDKefewfe', 'Hubert', 'Amelie');
INSERT INTO Personne  VALUES ('fewfweewZ049162731PZH19238', 'Hubert', 'Alice');
INSERT INTO PERSONNE(cin, nom, prenom)VALUES ('A1635248Z27469735SGRT26533', 'Martin', 'Albane');
INSERT INTO PERSONNE(cin, nom, prenom)VALUES ('A7153715T71735171HJUW28287', 'Bernard', 'Alice');
INSERT INTO PERSONNE(cin, nom, prenom)VALUES ('A1673371Z32718292HHGU71633', 'Thomas', 'Lucie');
INSERT INTO PERSONNE(cin, nom, prenom)VALUES ('A7682382Z27357193UJSW85391', 'Petit', 'Nicole');
INSERT INTO PERSONNE(cin, nom, prenom)VALUES ('A2343244D32525314FSEEC1635', 'Robert', 'Odile');
INSERT INTO PERSONNE(cin, nom, prenom)VALUES ('A6755432O82631042DHQTD1763', 'Richard', 'Sylvie');
INSERT INTO PERSONNE(cin, nom, prenom)VALUES ('A2176219D12422442FTRSW2342', 'Durand', 'Lucas');

INSERT INTO Etudiant VALUES ('A0382748Z02928375KDJH19238');
INSERT INTO Etudiant VALUES ('A0991748Z03901928NDKH19238');
INSERT INTO Etudiant VALUES ('A0734748Z01993657PPAH19238');
INSERT INTO Etudiant VALUES ('A0221748Z049162731PZH19238');
INSERT INTO Etudiant VALUES ('A0382fefwe2928375KDJH19238');
INSERT INTO Etudiant VALUES ('A0734748Z0fefewf7PPAH19238');
INSERT INTO Etudiant VALUES ('A0991748Z03901928NDKefewfe');
INSERT INTO Etudiant VALUES ('fewfweewZ049162731PZH19238');

INSERT INTO personnel(cin, statut)VALUES ('A1635248Z27469735SGRT26533', 'enseignant');
INSERT INTO personnel(cin, statut)VALUES ('A7153715T71735171HJUW28287', 'enseignant');
INSERT INTO personnel(cin, statut)VALUES ('A2343244D32525314FSEEC1635', 'personnel administratif');
INSERT INTO personnel(cin, statut)VALUES ('A7682382Z27357193UJSW85391', 'personnel administratif');
INSERT INTO personnel(cin, statut)VALUES ('A1673371Z32718292HHGU71633', 'personnel technique');

INSERT INTO exterieur(cin, telephone, organisme)VALUES ('A6755432O82631042DHQTD1763','0629753891','ORMS');
INSERT INTO exterieur(cin, telephone, organisme)VALUES ('A2176219D12422442FTRSW2342','0752631864','CSI');

INSERT INTO CategorieAsso  VALUES ('musique');
INSERT INTO CategorieAsso  VALUES ('théâtre');
INSERT INTO CategorieAsso  VALUES ('arts plastiques');
INSERT INTO CategorieAsso  VALUES ('sorties');

INSERT INTO Association VALUES ('La PicaTeam', 'picateam@gmail.com', to_date('1973-12-10','YYYY-MM-DD'), 'picateam.com', 'sorties', 'A102', 'A0991748Z03901928NDKH19238', 'A0734748Z01993657PPAH19238' );
INSERT INTO Association VALUES ('UTCroute', 'cassecroute@gmail.com', to_date('2010-10-13','YYYY-MM-DD'), 'utcroute.com', 'arts plastiques', 'B200', 'A0221748Z049162731PZH19238', 'A0734748Z01993657PPAH19238' );

INSERT INTO MembreAsso(nom_asso, membre) VALUES ('La PicaTeam','A0382748Z02928375KDJH19238');
INSERT INTO MembreAsso(nom_asso, membre) VALUES ('La PicaTeam', 'A0991748Z03901928NDKH19238');
INSERT INTO MembreAsso(nom_asso, membre) VALUES ('La PicaTeam', 'A0734748Z01993657PPAH19238');
INSERT INTO MembreAsso(nom_asso, membre) VALUES ('La PicaTeam', 'A0991748Z03901928NDKefewfe');
INSERT INTO MembreAsso(nom_asso, membre) VALUES ('La PicaTeam', 'fewfweewZ049162731PZH19238');
INSERT INTO MembreAsso(nom_asso, membre) VALUES ('UTCroute','A0382748Z02928375KDJH19238');
INSERT INTO MembreAsso(nom_asso, membre) VALUES ('UTCroute', 'A0734748Z01993657PPAH19238');
INSERT INTO MembreAsso(nom_asso, membre) VALUES ('UTCroute', 'A0221748Z049162731PZH19238');
INSERT INTO MembreAsso(nom_asso, membre) VALUES ('UTCroute', 'A0382fefwe2928375KDJH19238');
INSERT INTO MembreAsso(nom_asso, membre) VALUES ('UTCroute', 'A0991748Z03901928NDKefewfe');

INSERT INTO CatBillet VALUES ('invitation', 20.00);
INSERT INTO CatBillet VALUES ('billet etudiant', 12.50);
INSERT INTO CatBillet VALUES ('gratuit', 0.00);
INSERT INTO CatBillet VALUES ('billet exterieur', 27.50);

INSERT INTO Spectacle VALUES ('Marée basse','01:21','La PicaTeam');
INSERT INTO Spectacle VALUES ('Rumeur','01:05','UTCroute');
INSERT INTO Spectacle VALUES ('Classicals','02:20','La PicaTeam');

INSERT INTO role(descriptif, cin, nom_spec) VALUES ('metteur en scène', 'A0382748Z02928375KDJH19238', 'Marée basse');
INSERT INTO role(descriptif, cin, nom_spec) VALUES ('acteur', 'A0991748Z03901928NDKH19238', 'Marée basse');
INSERT INTO role(descriptif, cin, nom_spec) VALUES ('acteur', 'A0221748Z049162731PZH19238', 'Marée basse');
INSERT INTO role(descriptif, cin, nom_spec) VALUES ('figurant', 'A1635248Z27469735SGRT26533', 'Marée basse');
INSERT INTO role(descriptif, cin, nom_spec) VALUES ('souffleur', 'A7153715T71735171HJUW28287', 'Rumeur');
INSERT INTO role(descriptif, cin, nom_spec) VALUES ('metteur en scène', 'A0382748Z02928375KDJH19238', 'Rumeur');
INSERT INTO role(descriptif, cin, nom_spec) VALUES ('acteur', 'A0734748Z01993657PPAH19238', 'Rumeur');
INSERT INTO role(descriptif, cin, nom_spec) VALUES ('chef éclairagiste', 'A6755432O82631042DHQTD1763', 'Rumeur');
INSERT INTO role(descriptif, cin, nom_spec) VALUES ('régisseur', 'A0734748Z01993657PPAH19238', 'Classicals');
INSERT INTO role(descriptif, cin, nom_spec) VALUES ('acteur', 'A0221748Z049162731PZH19238', 'Classicals');
INSERT INTO role(descriptif, cin, nom_spec) VALUES ('figurant', 'A6755432O82631042DHQTD1763', 'Classicals');
INSERT INTO role(descriptif, cin, nom_spec) VALUES ('maquilleuse', 'A2176219D12422442FTRSW2342', 'Classicals');

INSERT INTO Seance (nom, salle, date_time) VALUES ('Marée basse', 'A101', TO_TIMESTAMP('2022-12-20 21:00', 'YYYY-MM-DD HH24:MI'))
INSERT INTO Seance (nom, salle, date_time) VALUES ('Rumeur', 'B200', TO_TIMESTAMP('2023-01-20 21:00', 'YYYY-MM-DD HH24:MI'))
INSERT INTO Seance (nom, salle, date_time) VALUES ('Classicals', 'A101', TO_TIMESTAMP('2023-05-01 20:00', 'YYYY-MM-DD HH24:MI'))

INSERT INTO Concert VALUES ('Classicals','Mozart',1780,'Classique');

INSERT INTO StandUp VALUES ('Rumeur','Débat');

INSERT INTO PieceTheatre VALUES ('Marée basse','Beranger',2021,'Comédie');

INSERT INTO billet(categorie, date_creation, seance, acheteur) VALUES ('invitation',to_date('2021-05-19','YYYY-MM-DD'),4,'A0382748Z02928375KDJH19238');

INSERT INTO billet(categorie, date_creation, seance) VALUES ('billet etudiant',to_date('2021-05-19','YYYY-MM-DD'),4);