# Handleiding: Afwezigheid-systeem opstarten (Windows + MariaDB)

## Vereisten
- Docker Desktop voor Windows geïnstalleerd
- Git for Windows geïnstalleerd
- Python 3.9+ geïnstalleerd
- VS Code (aanbevolen)

## Stap 1: Project downloaden

Open PowerShell als Administrator:

```powershell
cd C:\Users\[jouwgebruiker]\Documents\projects\python
git clone <repository-url> Afwezigheid
cd C:\Users\[jouwgebruiker]\Documents\projects\python\Afwezigheid
```

## Stap 2: Python Virtual Environment aanmaken

```powershell
python -m venv C:\Users\[jouwgebruiker]\Documents\projects\python\Afwezigheid\venv
```

## Stap 3: Virtual Environment activeren

```powershell
C:\Users\[jouwgebruiker]\Documents\projects\python\Afwezigheid\venv\Scripts\Activate.ps1
```

Je ziet nu `(venv)` aan het begin van je PowerShell prompt.

## Stap 4: Python-pakketten installeren

```powershell
pip install --upgrade pip
pip install -e C:\Users\[jouwgebruiker]\Documents\projects\python\Afwezigheid
```

Voor development tools (optioneel):
```powershell
pip install -e "C:\Users\[jouwgebruiker]\Documents\projects\python\Afwezigheid[dev]"
```

## Stap 5: Environment-bestand aanmaken

Maak een `.env` bestand in `C:\Users\[jouwgebruiker]\Documents\projects\python\Afwezigheid\afwezigheid\`:

```powershell
@"
SECRET_KEY=jouw-geheime-sleutel-hier
DB_USER=verlof_gebruiker
DB_PASSWORD=verlof_wachtwoord
DB_HOST=mariadb
DB_PORT=3306
DB_NAME=verlof
FLASK_ENV=development
"@ | Out-File "C:\Users\[jouwgebruiker]\Documents\projects\python\Afwezigheid\afwezigheid\.env" -Encoding UTF8
```

## Stap 6: Docker containers starten

```powershell
cd C:\Users\[jouwgebruiker]\Documents\projects\python\Afwezigheid
docker-compose up -d
```

De database wordt automatisch geïnitialiseerd door docker-compose.

## Stap 7: Applicatie openen

Open je browser en ga naar:
```
http://localhost:5000
```

## Inloggegevens

**Werknemers:**
- Gebruikersnaam: `jjanssen`
- Wachtwoord: `wachtwoord123`

**Teamleider:**
- Gebruikersnaam: `mmanager`
- Wachtwoord: `wachtwoord123`

## Projectstructuur

```
C:\Users\[jouwgebruiker]\Documents\projects\python\Afwezigheid\
├── afwezigheid\
│   ├── __init__.py
│   ├── app.py
│   ├── models.py
│   ├── .env
│   └── templates\
│       ├── base.html
│       ├── index.html
│       └── login.html
├── sql\
│   ├── init.sql
│   └── insert_test_data.sql
├── venv\
├── .gitignore
├── pyproject.toml
├── docker-compose.yml
├── Dockerfile
└── INSTALL.md
```

## Dagelijks gebruik

Voordat je gaat werken, activeer het virtual environment:

```powershell
C:\Users\[jouwgebruiker]\Documents\projects\python\Afwezigheid\venv\Scripts\Activate.ps1
```

## Stoppen

```powershell
cd C:\Users\[jouwgebruiker]\Documents\projects\python\Afwezigheid
docker-compose down
```

Virtual environment deactiveren:
```powershell
deactivate
```

## Logs bekijken (troubleshooting)

```powershell
cd C:\Users\[jouwgebruiker]\Documents\projects\python\Afwezigheid
docker-compose logs -f flask
docker-compose logs -f mariadb
```

## Database opnieuw initialiseren

Mocht je de database willen resetten:

```powershell
cd C:\Users\[jouwgebruiker]\Documents\projects\python\Afwezigheid
docker-compose down
docker volume rm afwezigheid_mariadb_data
docker-compose up -d
```

## Veelgestelde vragen

### PowerShell geeft fout: "cannot be loaded because running scripts is disabled"

Voer dit uit als Administrator:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Port 5000 al in gebruik

```powershell
cd C:\Users\[jouwgebruiker]\Documents\projects\python\Afwezigheid
docker-compose down
docker-compose up -d
```

### Kan geen verbinding maken met database

Controleer of Docker containers draaien:
```powershell
docker-compose ps
```

Bekijk logs:
```powershell
docker-compose logs mariadb
```