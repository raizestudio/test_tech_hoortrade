# Test Tech Hoortrade

Application Django permettant la gestion d'une librairie de films.

[![API Tests](https://github.com/raizestudio/test_tech_hoortrade/actions/workflows/main.yml/badge.svg)](https://github.com/raizestudio/test_tech_hoortrade/actions/workflows/main.yml)

# Table des matières

- [Installation](#installation)
- [Utilisation](#utilisation)
- [Exigences Techniques)(#exigences techniques)
- [Contribuer](#contribuer)
- [License](#license)
- [Contact](#contact)

## Installation

Instructions d'installation.

```bash
# Cloner le repo
git clone https://github.com/raizestudio/test_tech_hoortrade.git

# Accédez au répertoire du projet
cd test_tech_hoortrade
```

### Avec Docker

```bash
# Avec script init.sh
./init.sh --docker

# Possible de relancer avec la commande
./init.sh --docker-reset

# Dans les deux cas un fichier .env est crée (s'il n'existe pas) à partir du .env.example
# Vous serez invité à entrer votre clé API TMDB
```

### Sans Docker, automatisé

```bash
# Installer uv si nécessaire
curl -Ls https://astral.sh/uv/install.sh | sh

# ou avec pip
pip install uv

# Installer dépendances
uv sync

# Activer venv
source .venv/bin/activate

# Executer script init.sh
./init.sh

# Un fichier .env est crée (s'il n'existe pas) à partir du .env.examplei
# Vous serez invité à entrer votre clé API TMDB
```

### Sans Docker, manuellement

```bash
# Installer uv si nécessaire
curl -Ls https://astral.sh/uv/install.sh | sh

# ou avec pip
pip install uv

# Installer dépendances
uv sync

# Activer venv
source .venv/bin/activate

# Créer une copie de .env.example
mv .env.example .env

# Créer dossiers nécessaires
mkdir -p logs && mkdir -p media

# Effectuer migrations
uv run manage.py migrate

# Créer utilisateur administrateur et/ou autres utlisateurs
uv run manage.py create_super_user email username password
uv run manage.py create_user email username password --spectator

# Charger fixtures
uv run manage.py load_fixtures

# Génerer films afin de populer la bd
uv run manage.py generate_fake_movies count

# Démarrer serveur
uv run manage.py runserver
```

## Utilisation

Instructions sur l'utilisation de l'application

### Endpoints

Il est possible de visualiser les points de terminaisons disponibles de plusieurs façons.

> 1. En exportant le schema au format yaml -> api/schema/
> 2. Avec Swagger -> api/schema/swagger-ui/
> 3. Avec Redoc -> api/schema/redoc/

## Exigences Techniques

[comment]: <> (TODO)

## Contribuer

[comment]: <> (TODO)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

Joel P. - [raizetvision@gmail.com](mailto:joel.pinho16@icloud.com)

Project Link: [https://github.com/raizestudio/test_tech_hoortrade](https://github.com/raizestudio/test_tech_hoortrade)
