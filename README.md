# Test Tech Hoortrade

Application Django permettant la gestion d'une librairie de films.

[![API Tests](https://github.com/raizestudio/test_tech_hoortrade/actions/workflows/main.yml/badge.svg)](https://github.com/raizestudio/test_tech_hoortrade/actions/workflows/main.yml)

# Table des matières

- [Installation](#installation)
- [Utilisation](#utilisation)
- [License](#license)
- [Contact](#contact)

## Installation

Instructions d'installation

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
```

### Sans Docker, automatisé

```bash
# Executer script init.sh
./init.sh
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

# Créer dossiers nécessaires
mkdir -p logs && mkdir -p media

# Effectuer migrations
uv run python manage.py migrate

# Charger fixtures
uv run python manage.py load_fixtures

# Démarrer serveur
uv run python manage.py runserver
```

## Utilisation

Instructions sur l'utilisation de l'application

## License

## Contact


