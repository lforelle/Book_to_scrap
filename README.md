# Scraper Books to Scrape

Ce projet permet de récupérer des informations sur les livres du site [Books to Scrape](https://books.toscrape.com/) et de les enregistrer dans des fichiers CSV, ainsi que les images associées.

## Présentation

Le projet est organisé en trois scripts Python :

- [`book_details.py`](book_details.py) : extrait les détails d'un livre donné.
- [`category.py`](category.py) : parcourt tous les livres d'une catégorie, y compris les pages de pagination.
- [`all_categories.py`](all_categories.py) : récupère toutes les catégories du site et lance l'extraction pour chacune d'elles.

## Fonctionnalités

### 1. Extraction d'un livre

Le script [`book_details.py`](book_details.py) :

- vérifie que la page du livre est accessible ;
- parse le HTML avec BeautifulSoup ;
- récupère les informations du tableau produit ;
- extrait le titre, la description, la catégorie et la note ;
- convertit l'URL relative de l'image en URL absolue ;
- sauvegarde les données dans un fichier CSV ;
- télécharge l'image correspondante dans le même dossier de sortie.

Les colonnes exploitées sont les suivantes :

- `product_page_url`
- `UPC`
- `Price (excl. tax)`
- `Price (incl. tax)`
- `Tax`
- `Availability`
- `title`
- `product_description`
- `category`
- `review_rating`
- `image_url`

Si une description n'est pas présente, le script remplace la valeur par :

```text
No description found !!
```

### 2. Extraction d'une catégorie

Le script [`category.py`](category.py) :

- consulte la page d'une catégorie ;
- récupère les liens de tous les livres présents sur cette page ;
- suit la pagination tant qu'une page suivante existe ;
- sauvegarde la liste des URLs dans un CSV de catégorie ;
- appelle ensuite [`book_details.py`](book_details.py) pour chaque titre trouvé ;
- crée le dossier `Books_details/` dans le dossier de catégorie afin de stocker les fichiers détaillés.

### 3. Extraction de toutes les catégories

Le script [`all_categories.py`](all_categories.py) :

- récupère la liste des catégories depuis la page d'accueil de Books to Scrape ;
- transforme les liens relatifs en URLs complètes ;
- appelle `category.main()` pour chaque catégorie ;
- permet d'exécuter le scraping de l'ensemble du catalogue.

## Structure des fichiers générés

Les résultats sont organisés comme suit :

```text
csv_files/
└── <Categorie>/
    ├── books_by_category_<Categorie>_.csv
    └── Books_details/
        ├── details_<titre>_.csv
        └── details_<titre>_.jpg
```

Le nom du fichier CSV de détail est construit à partir du titre, en supprimant les caractères interdits et en normalisant les espaces en underscores.

## Installation

Créer un environnement virtuel :

```bash
python -m venv env
```

Sous Linux/macOS :

```bash
source env/bin/activate
```

Sous Windows :

```powershell
env\Scripts\activate
```

Installer les dépendances :

```bash
pip install -r requirements.txt
```

Les bibliothèques principales utilisées sont :

- `requests` pour les requêtes HTTP ;
- `beautifulsoup4` pour parser le HTML ;
- `csv` pour écrire les données dans les fichiers CSV ;
- `os` pour gérer les dossiers et fichiers ;
- `re` pour nettoyer les noms de fichiers ;
- `urllib.parse.urljoin` pour reconstruire des URLs complètes.

## Utilisation

### Extraire un seul livre

```bash
python book_details.py
```

Le script utilise par défaut cette URL :

```text
https://books.toscrape.com/catalogue/the-argonauts_837/index.html
```

Le résultat est enregistré dans le dossier `Books_details/` du répertoire courant, sous le format :

```text
details_<titre>_.csv
```

et l'image est sauvegardée dans le même dossier sous forme :

```text
details_<titre>_.jpg
```

### Extraire une catégorie

```bash
python category.py
```

Par défaut, le script traite la catégorie suivante :

```text
https://books.toscrape.com/catalogue/category/books/sequential-art_5/page-1.html
```

Les fichiers créés dans `csv_files/<Categorie>/` sont :

1. `books_by_category_<Categorie>_.csv` : liens des livres de la catégorie ;
2. `Books_details/details_<titre>_.csv` : informations détaillées de chaque livre ;
3. `Books_details/details_<titre>_.jpg` : image du livre.

### Extraire toutes les catégories

```bash
python all_categories.py
```

Cette commande parcourt la page d'accueil du site, récupère toutes les catégories et exécute le scraping de chacune d'elles.

## Notes importantes

- Les fichiers sont écrits en UTF-8 pour gérer correctement les caractères spéciaux.
- Le répertoire racine du projet est calculé avec `os.path.dirname(os.path.abspath(__file__))`, ce qui permet à l'application de fonctionner même si elle est lancée depuis un autre dossier.
- Les URLs relatives sont converties en URLs absolues avant d'être stockées ou utilisées.
- La logique de sauvegarde des fichiers est centralisée dans `save_data_to_csv()`, ce qui évite de dupliquer la gestion CSV dans plusieurs scripts.

## Limites connues

- Les URLs de départ sont codées en dur dans les scripts ; elles ne sont pas configurées via argument en ligne de commande.
- La gestion des erreurs réseau est basique et se limite à un contrôle du code HTTP.
- Le script ne traite pas d'options avancées de configuration ni de reprise de traitement en cas d'interruption.
