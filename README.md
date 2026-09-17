# Scraper Books to Scrape

Ce projet contient trois scripts Python permettant de récupérer les
informations de livres sur le site [Books to Scrape](https://books.toscrape.com/).

## Fonctionnalités actuelles

### Extraction d'un livre

Le script [`book_details.py`](book_details.py) :

- télécharge la page d'un livre ;
- extrait les informations présentes dans la fiche produit ;
- convertit la note en nombre d'étoiles ;
- transforme l'URL relative de l'image en URL absolue ;
- ajoute la date et l'heure, jusqu'aux microsecondes, au nom du fichier de sortie ;
- enregistre les données dans un fichier CSV.

Lorsqu'un livre ne possède pas de section `Product Description`, la valeur
`No description found !!` est enregistrée à la place de la description.

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

- récupère les liens des livres d'une catégorie ;
- parcourt toutes les pages de la catégorie grâce à la pagination ;
- enregistre les liens de tous les livres dans un fichier CSV ;
- appelle [`book_details.py`](book_details.py) pour extraire les informations
  de chaque livre ;
- enregistre les données détaillées dans des fichiers CSV horodatés.

### Extraction de toutes les catégories

Le script [`all_categories.py`](all_categories.py) :

- récupère les liens des catégories depuis la page d'accueil ;
- lance [`category.py`](category.py) pour chaque catégorie ;
- permet ainsi de traiter l'ensemble du catalogue en une seule exécution.

## Organisation des fichiers

| Fichier | Rôle |
| --- | --- |
| `book_details.py` | Extraction des informations d'un livre |
| `category.py` | Extraction des livres d'une catégorie et lancement de l'extraction détaillée |
| `all_categories.py` | Parcours de toutes les catégories du site |
| `requirements.txt` | Dépendances Python du projet |
| `csv_files/` | Répertoire racine des résultats CSV |
| `csv_files/<catégorie>/` | Liens des livres d'une catégorie |
| `csv_files/<catégorie>/Books_details/` | Données détaillées des livres |

Les fichiers CSV sont nommés avec le format
`<préfixe>YYYYMMDD_HHMMSS_microsecondes.csv`. Le chemin racine du projet est
déterminé à partir de `__file__` dans `category.py`, indépendamment du
répertoire depuis lequel le script est lancé.

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

Le résultat est enregistré dans le sous-dossier `Books_details/`, dans un
fichier dont le nom commence par `book_details_`.

### Extraire une catégorie

```bash
python category.py
```

Le script traite par défaut la catégorie **Sequential Art** :

```text
https://books.toscrape.com/catalogue/category/books/sequential-art_5/page-1.html
```

Les résultats sont enregistrés dans `csv_files/Sequential Art/` et dans son
sous-dossier `Books_details/` :

1. `books_by_category_Sequential Art_<timestamp>.csv`, contenant la catégorie
   et les URLs des livres trouvés ;
2. `Books_details/book_details_<timestamp>.csv`, contenant les informations
   détaillées de chaque livre.

### Extraire toutes les catégories

```bash
python all_categories.py
```

Le script parcourt toutes les catégories disponibles dans la navigation de
Books to Scrape. Chaque catégorie est traitée avec sa pagination et ses
résultats sont enregistrés dans le dossier correspondant sous `csv_files/`.

## Limites actuelles

- Les URLs du livre et de la catégorie utilisées par les scripts individuels
  sont définies directement dans les fichiers Python.
- Les images sont référencées dans le CSV, mais ne sont pas téléchargées
  localement.
- La description réelle est actuellement remplacée par un texte temporaire
  lorsqu'une description est disponible.
- La gestion des erreurs HTTP de la page initiale d'une catégorie doit encore
  être renforcée.

## Encodage des fichiers

Les fichiers CSV sont écrits en UTF-8 afin de préserver les caractères
accentués présents dans les titres et les descriptions.
