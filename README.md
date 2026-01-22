# Verlof Aanvraag Systeem

Een eenvoudige webapplicatie voor werknemers om verlofaanvragen in te dienen en voor teamleiders om deze goed te keuren of af te keuren.

## 📋 Wat doet deze applicatie?

Deze applicatie helpt bedrijven om verlofaanvragen te beheren:

- **Werknemers** kunnen:
  - Inloggen met hun gebruikersnaam en wachtwoord
  - Verlofaanvragen indienen (ziek, betaald verlof, onbetaald verlof, vakantie)
  - Hun verlofaanvragen zien en verwijderen (alleen als ze nog "In behandeling" zijn)

- **Teamleiders** kunnen:
  - Alle verlofaanvragen zien die nog goedgekeurd moeten worden
  - Aanvragen goedkeuren of afkeuren

## 🏗️ Hoe werkt het technisch?

De applicatie is gebouwd met deze onderdelen:

### Frontend (Wat je ziet)
- **HTML Templates** (`templates/` map): De pagina's die je in je browser ziet
  - `base.html`: De basisstructuur voor alle pagina's
  - `login.html`: De inlogpagina
  - `index.html`: De hoofdpagina met verlofaanvragen

### Backend (Achterste werk)
- **Python/Flask** (`app.py`): De logica van de applicatie
  - Verwerkt inloggen
  - Slaat verlofaanvragen op
  - Keurt verlofaanvragen goed of af

- **Database Models** (`models.py`): De structuur van de gegevens
  - `User`: Gebruikersgegevens (login info)
  - `Verlof`: Verlofaanvragen

### Database (Opslag)
- **MariaDB/MySQL**: Een database om alle gegevens op te slaan
  - `Afdelingen`: Teams/afdelingen in het bedrijf
  - `Werknemers`: Medewerkers
  - `Gebruikers`: Login accounts
  - `Verlof`: Verlofaanvragen

## 📁 Mappenstructuur

```
Afwezigheid/
├── afwezigheid/                 # Hoofdmap van de applicatie
│   ├── app.py                   # Alle routes en logica
│   ├── models.py                # Database tabellen
│   ├── .env                      # Geheime instellingen (maak je zelf)
│   └── templates/               # HTML pagina's
│       ├── base.html            # Basissjabloon
│       ├── login.html           # Inlogpagina
│       └── index.html           # Hoofdpagina
├── sql/                          # Database scripts
│   ├── init.sql                 # Database setup
│   └── insert_test_data.sql     # Test gebruikers
├── venv/                         # Python libraries (wordt aangemaakt)
├── pyproject.toml               # Afhankelijkheden
├── docker-compose.yml           # Docker configuratie
├── Dockerfile                   # Container instructies
├── .gitignore                   # Wat niet in git opslaan
└── INSTALL.md                   # Installatiehandleiding
```

## 🚀 Hoe start je het op?

### 1. Voorbereiding
Je hebt nodig:
- Docker en Docker Compose
- Python 3.9+
- Git

### 2. Project downloaden
```bash
git clone <repository-url> Afwezigheid
cd Afwezigheid
```

### 3. Python environment setup
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1      # Op Windows
source venv/bin/activate         # Op Mac/Linux

pip install -e .
```

### 4. Omgeving configureren
Maak een `.env` bestand in `afwezigheid/`:
```
SECRET_KEY=jouw-geheime-sleutel
DB_USER=verlof_gebruiker
DB_PASSWORD=verlof_wachtwoord
DB_HOST=mariadb
DB_PORT=3306
DB_NAME=verlof
FLASK_ENV=development
```

### 5. Docker starten
```bash
docker-compose up -d
```

### 6. Browser openen
Ga naar: `http://localhost:5000`

## 👥 Test accounts

**Werknemers:**
- Gebruikersnaam: `john_doe`
- Wachtwoord: `wachtwoord123`

**Teamleider:**
- Gebruikersnaam: `jane_smith`
- Wachtwoord: `wachtwoord123`

## 🔍 Hoe werkt een verlofaanvraag?

### Stap 1: Werknemers indienen
1. Log in als werknemers
2. Kies verloftype (Ziek, Betaald, Onbetaald, Vakantie)
3. Kies startdatum en einddatum
4. Klik "Verlofaanvraag indienen"
5. De aanvraag staat nu in je lijst met status "In behandeling"

### Stap 2: Teamleiders keuren goed
1. Log in als teamleider
2. Je ziet alle aanvragen met status "In behandeling"
3. Klik "Goedkeuren" of "Afkeuren"
4. De status verandert nu in "Goedgekeurd" of "Afgekeurd"

## 💾 Database concepten

### Tabellen

**Werknemers**
- Opslaat medewerkersinformatie (voornaam, achternaam, positie)
- Elk record krijgt een `werknemer_id`

**Gebruikers**
- Opslaat login informatie (gebruikersnaam, wachtwoord hash)
- Verwijzing naar `Werknemers` via `werknemer_id`
- Rol: 'werknemer' of 'teamleider'

**Verlof**
- Opslaat verlofaanvragen
- `werknemer_id`: Wie vraagt verlof aan
- `verlof_type`: Soort verlof
- `start_datum` & `eind_datum`: Perioden
- `status`: In behandeling / Goedgekeurd / Afgekeurd
- `goedgekeurd_door`: Wie heeft het goedgekeurd

## 🔐 Veiligheid

- Wachtwoorden worden opgeslagen als SHA512 hash (niet leesbaar)
- CSRF tokens beschermen tegen aanvallen
- Sessies zijn beveiligd met cookies

## 🛠️ Troubleshooting

**Poort 5000 is al in gebruik:**
```bash
docker-compose down
docker-compose up -d
```

**Database fouten:**
```bash
docker-compose down
docker volume rm afwezigheid_mariadb_data
docker-compose up -d
```

**Logs bekijken:**
```bash
docker-compose logs -f flask
docker-compose logs -f mariadb
```

## 📚 Bestanden uitgelegd

### app.py
Dit is het hart van de applicatie. Het bevat:
- Routes: Pagina's die je kunt bezoeken (`/`, `/login`, `/logout`)
- POST handlers: Wat gebeurt er als je data verstuurt
- Database queries: Data ophalen en opslaan

### models.py
Beschrijft hoe de database eruit ziet:
- `User`: Login accounts
- `Verlof`: Verlofaanvragen
- Validators: Controle of data correct is

### base.html
Het sjabloon dat alle pagina's gebruiken:
- HTML structuur
- CSS styling
- Template blokken die andere pagina's vullen

### login.html
De inlogpagina met:
- Formulier voor gebruikersnaam en wachtwoord
- CSRF token voor veiligheid

### index.html
De hoofdpagina met:
- Formulier om verlofaanvraag in te dienen
- Tabel met alle aanvragen
- Knoppen om aan te passen/goedkeuren

### init.sql
Het databasescript dat:
- Database aanmaakt
- Gebruiker aanmaakt
- Tabellen aanmaakt

## 🔄 Data flow voorbeeld

```
Werknemers vult formulier in
        ↓
HTML form stuurt POST request naar Flask
        ↓
app.py verwerkt de aanvraag
        ↓
models.py maakt Verlof object
        ↓
Database slaat record op
        ↓
Pagina refreshed, tabel toont nieuwe aanvraag
```

## 🎯 Volgende stappen

Als je meer wil doen:
- Meer verloftypes toevoegen in init.sql
- Verlofdag counter toevoegen
- Notities toevoegen aan aanvragen
- Email notificaties als verlof goedgekeurd is
- Verlofhistorie rapporteren

## 📞 Vragen?

Controleer de INSTALL.md voor gedetailleerde installatie stappen.

Kijk in docker-compose logs voor foutmeldingen:
```bash
docker-compose logs flask
```
