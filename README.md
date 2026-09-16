# Scraper Books to Scrape

Ce projet contient deux scripts Python permettant de récupérer les
informations de livres sur le site [Books to Scrape](https://books.toscrape.com/).

## Fonctionnalités actuelles

### Extraction d'un livre

Le script [`book_details.py`](book_details.py) :

- télécharge la page d'un livre ;
- extrait les informations présentes dans la fiche produit ;
- convertit la note en nombre d'étoiles ;
- transforme l'URL relative de l'image en URL absolue ;
- ajoute la date et l'heure au nom du fichier de sortie ;
- enregistre les données dans un fichier CSV.

Les informations récupérées sont :

- `product_page_url` : URL de la page produit ;
- `UPC` : code produit universel ;
- `Price (excl. tax)` : prix hors taxes ;
- `Price (incl. tax)` : prix toutes taxes comprises ;
- `Tax` : montant de la taxe ;
- `Availability` : quantité disponible ;
- `title` : titre du livre ;
- `product_description` : description du livre ;
- `category` : catégorie ;
- `review_rating` : note de une à cinq étoiles ;
- `image_url` : URL absolue de l'image.

### Extraction d'une catégorie

Le script [`category.py`](category.py) :

- cible actuellement la catégorie **Art** ;
- récupère les liens des livres affichés sur la page de catégorie ;
- enregistre ces liens dans un fichier CSV ;
- appelle [`book_details.py`](book_details.py) pour extraire les informations
  de chaque livre ;
- regroupe les données détaillées dans un fichier CSV horodaté.

## Organisation des fichiers

| Fichier | Rôle |
| --- | --- |
| `book_details.py` | Extraction des informations d'un livre |
| `category.py` | Extraction des livres d'une catégorie et lancement de l'extraction détaillée |
| `requirements.txt` | Dépendances Python du projet |
| `book_detail_YYYYMMDD_HHMM.csv` | Données détaillées des livres |
| `books_by_category_Art_YYYYMMDD_HHMM.csv` | Catégorie et liens des livres récupérés |

Les fichiers CSV sont nommés avec le format `YYYYMMDD_HHMM`. Le fichier est
créé dans le dossier du projet. Lorsqu'un fichier portant le même nom existe,
les nouvelles lignes sont ajoutées en conservant l'en-tête existant.

## Installation

Il est recommandé d'utiliser un environnement virtuel :

```bash
python -m venv env
```

Activation sous Linux ou macOS :

```bash
source env/bin/activate
```

Activation sous Windows :

```powershell
env\Scripts\activate
```

Installation des dépendances :

```bash
pip install -r requirements.txt
```

Les principales bibliothèques utilisées sont :

- `requests` pour effectuer les requêtes HTTP ;
- `beautifulsoup4` pour analyser le HTML ;
- `csv` pour écrire les résultats ;
- `datetime` et `os` pour horodater et gérer les fichiers ;
- `urllib.parse.urljoin` pour construire les URLs absolues.

## Utilisation

### Extraire un seul livre

```bash
python book_details.py
```

Par défaut, le script traite la page **A Light in the Attic** :

```text
https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html
```

Le résultat est enregistré dans un fichier dont le nom commence par
`book_detail_`.

### Extraire une catégorie

```bash
python category.py
```

Le script traite par défaut la catégorie **Art** :

```text
https://books.toscrape.com/catalogue/category/books/art_25/index.html
```

Deux types de fichiers sont alors générés :

1. `books_by_category_Art_YYYYMMDD_HHMM.csv`, contenant la catégorie et les
   URLs des livres trouvés ;
2. `book_detail_YYYYMMDD_HHMM.csv`, contenant les informations détaillées de
   chaque livre.

## Limites actuelles

- Les URLs du livre et de la catégorie sont définies directement dans les
  scripts.
- La pagination des catégories n'est pas encore gérée : seule la page de
  catégorie configurée est parcourue.
- Une seule catégorie est traitée par exécution de `category.py`.
- Les images sont référencées dans le CSV, mais ne sont pas téléchargées
  localement.
- La gestion des erreurs HTTP est présente pour l'extraction d'un livre, mais
  la récupération initiale de la catégorie doit encore être renforcée.

## Encodage des fichiers

Les fichiers CSV sont écrits en UTF-8 afin de préserver les caractères
accentués présents dans les titres et les descriptions.
