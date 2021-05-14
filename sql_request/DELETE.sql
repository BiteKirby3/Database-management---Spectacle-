DELETE FROM Role r WHERE r.CIN='A0382748Z02928375KDJH19238' AND r.nom_spec='Marée basse';

DELETE FROM role WHERE descriptif='figurant' AND nom_spec='Classicals';

DELETE CASCADE FROM spectacle WHERE nom='Marée basse';

DELETE CASCADE FROM Seance s WHERE s.id=4;

DELETE FROM association WHERE nom='La PicaTeam';

