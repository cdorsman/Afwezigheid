
DROP DATABASE IF EXISTS verlof;
CREATE DATABASE IF NOT EXISTS verlof;

CREATE USER IF NOT EXISTS 'verlof_gebruiker'@'%' IDENTIFIED BY 'verlof_wachtwoord';

GRANT ALL PRIVILEGES ON verlof.* TO 'verlof_gebruiker'@'%';
FLUSH PRIVILEGES;

USE verlof;


CREATE TABLE Werknemers (
    werknemer_id INT PRIMARY KEY AUTO_INCREMENT,
    voornaam VARCHAR(50) NOT NULL,
    achternaam VARCHAR(50) NOT NULL,
    afdeling_id INT,
    positie VARCHAR(100),
    status ENUM('Actief', 'Inactief', 'Op verlof') DEFAULT 'Actief',
    aanname_datum DATE,
    FOREIGN KEY (afdeling_id) REFERENCES Afdelingen(afdeling_id)
);

CREATE TABLE Gebruikers (
    gebruiker_id INT PRIMARY KEY AUTO_INCREMENT,
    werknemer_id INT NOT NULL,
    gebruikersnaam VARCHAR(50) UNIQUE NOT NULL,
    wachtwoord_hash VARCHAR(255) NOT NULL,
    rol ENUM('werknemer', 'teamleider') NOT NULL,
    FOREIGN KEY (werknemer_id) REFERENCES Werknemers(werknemer_id)
);


CREATE TABLE Verlof (
    verlof_id INT PRIMARY KEY AUTO_INCREMENT,
    werknemer_id INT NOT NULL,
    verlof_type ENUM('Ziek', 'Betaald', 'Onbetaald', 'Vakantie') NOT NULL,
    start_datum DATE NOT NULL,
    eind_datum DATE NOT NULL,
    goedgekeurd_door INT,
    status ENUM('In behandeling', 'Goedgekeurd', 'Afgekeurd') DEFAULT 'In behandeling',
    FOREIGN KEY (werknemer_id) REFERENCES Gebruikers(werknemer_id),
    FOREIGN KEY (goedgekeurd_door) REFERENCES Gebruikers(werknemer_id)
);
