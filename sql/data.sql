USE verlof;

-- Insert Afdelingen
INSERT INTO Afdelingen (naam) VALUES 
    ('IT'),
    ('HR');

-- Insert Werknemers
INSERT INTO Werknemers (voornaam, achternaam, afdeling_id, positie, status, aanname_datum)
VALUES 
    ('Jan', 'Janssen', 1, 'Software Developer', 'Actief', '2024-01-15'),
    ('Petra', 'Peters', 1, 'Software Developer', 'Actief', '2024-02-01'),
    ('Mark', 'Manager', 1, 'Team Leader', 'Actief', '2023-06-01'),
    ('Sarah', 'Smith', 2, 'HR Manager', 'Actief', '2023-08-01');

-- Insert Gebruikers (password 'welkom123' hashed with SHA512)
INSERT INTO Gebruikers (werknemer_id, gebruikersnaam, wachtwoord_hash, rol)
VALUES 
    (1, 'jjanssen', '4b8735ada09db58ca0c8f95a4bf3e4452f1ef87689528745cab1d3887b350480100d82d94250775a3367ab992c0178166b34045517f682f3e37cc225d5c2a46d', 'werknemer'),
    (2, 'ppeters', '4b8735ada09db58ca0c8f95a4bf3e4452f1ef87689528745cab1d3887b350480100d82d94250775a3367ab992c0178166b34045517f682f3e37cc225d5c2a46d', 'werknemer'),
    (3, 'mmanager', '4b8735ada09db58ca0c8f95a4bf3e4452f1ef87689528745cab1d3887b350480100d82d94250775a3367ab992c0178166b34045517f682f3e37cc225d5c2a46d', 'teamleider'),
    (4, 'ssmith', '4b8735ada09db58ca0c8f95a4bf3e4452f1ef87689528745cab1d3887b350480100d82d94250775a3367ab992c0178166b34045517f682f3e37cc225d5c2a46d', 'teamleider');

-- Insert some test presence records
INSERT INTO Aanwezigheid (werknemer_id, check_in, check_uit, status, notities)
VALUES 
    (1, '2025-04-27 09:00:00', '2025-04-27 17:00:00', 'Aanwezig', 'Regular workday'),
    (2, '2025-04-27 08:30:00', NULL, 'Remote', 'Working from home'),
    (3, '2025-04-27 09:15:00', '2025-04-27 18:00:00', 'Aanwezig', NULL);

-- Insert some test leave requests
INSERT INTO Verlof (werknemer_id, verlof_type, start_datum, eind_datum, goedgekeurd_door, status)
VALUES 
    (1, 'Vakantie', '2025-05-01', '2025-05-07', 3, 'Goedgekeurd'),
    (2, 'Ziek', '2025-04-26', '2025-04-26', NULL, 'In behandeling');