# Scraper Books to Scrape

Ce projet permet de récupérer les informations des livres du site [Books to
Scrape](https://books.toscrape.com/), de les enregistrer dans des fichiers CSV
et de télécharger les images associées.

## Présentation

Le projet est organisé en trois scripts Python :

- [`book_details.py`](book_details.py) : extrait et sauvegarde les détails d'un
  livre donné, ainsi que son image ;
- [`category.py`](category.py) : parcourt tous les livres d'une catégorie, y
  compris les pages de pagination, puis lance l'extraction détaillée ;
- [`all_categories.py`](all_categories.py) : récupère toutes les catégories du
  site et lance l'extraction pour chacune d'elles.

## Fonctionnalités

### 1. Extraction d'un livre

Le script [`book_details.py`](book_details.py) :

- vérifie que la page du livre est accessible ;
- parse le HTML avec BeautifulSoup ;
- récupère les informations du tableau produit ;
- extrait le titre, la description, la catégorie et la note ;
- convertit l'URL relative de l'image en URL absolue ;
- sauvegarde les données dans un fichier CSV ;
- télécharge l'image correspondante dans le même dossier de sortie ;
- limite le titre utilisé dans le nom du fichier à ses 25 premiers caractères.

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

La note est convertie en nombre entier de 1 à 5 à partir de la classe CSS
présente dans la page du livre.

Si une description n'est pas présente, le script remplace la valeur par :

```text
No description found !!
```

### 2. Extraction d'une catégorie

Le script [`category.py`](category.py) :

- consulte la page d'une catégorie ;
- récupère les liens de tous les livres présents sur cette page ;
- suit la pagination tant qu'une page suivante existe ;
- sauvegarde la liste des URLs dans un CSV de catégorie, sur une seule ligne ;
- appelle ensuite [`book_details.py`](book_details.py) pour chaque URL trouvée ;
- crée le dossier `Books_details/` dans le dossier de catégorie afin de stocker les fichiers détaillés.

Les chemins relatifs des livres et des images sont normalisés avant leur
conversion en URL absolue. L'extraction conserve le dernier élément du chemin,
ce qui évite de dépendre d'une profondeur fixe (`split('../')[-1]`).

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
└── <categorie>/
    └── Books_details/
        ├── books_by_category_<categorie>_.csv
        ├── details_<titre>_.csv
        └── details_<titre>_.jpg
```

Le nom du répertoire de catégorie remplace les espaces par des underscores.
Les noms de fichiers de détail sont construits avec le préfixe `details_`,
suivi du titre nettoyé : les caractères qui ne sont pas alphanumériques ASCII
sont remplacés par des underscores et le titre est limité à 25 caractères.

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

Le résultat est enregistré dans le dossier `Books_details/` du répertoire
courant, sous les formats :

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

Les fichiers créés dans `csv_files/<Categorie>/Books_details/` sont :

1. `books_by_category_<Categorie>_.csv` : liens des livres de la catégorie,
   écrits sur une seule ligne ;
2. `details_<titre>_.csv` : informations détaillées de chaque livre ;
3. `details_<titre>_.jpg` : image du livre.

Si l'image existe déjà, elle n'est pas téléchargée à nouveau.

### Extraire toutes les catégories

```bash
python all_categories.py
```

Cette commande parcourt la page d'accueil du site, récupère toutes les catégories et exécute le scraping de chacune d'elles.

## Notes importantes

- Les fichiers sont écrits en UTF-8 pour gérer correctement les caractères spéciaux.
- Le répertoire racine du projet est calculé avec `os.path.dirname(os.path.abspath(__file__))`, ce qui permet à l'application de fonctionner même si elle est lancée depuis un autre dossier.
- Les URLs relatives sont converties en URLs absolues avant d'être stockées ou utilisées.
- L'extraction des URLs ne dépend pas d'un nombre fixe de segments `../`.
- Les images existantes sont conservées afin d'éviter des téléchargements inutiles.
- La fonction `test_page_access()` centralise les requêtes HTTP et vérifie le
  code de statut `200` avant de poursuivre l'analyse.
- La fonction `save_book_data_to_csv()` écrit l'en-tête du CSV uniquement lors
  de la création du fichier, puis ajoute les données du livre.
- La fonction `save_category_href_to_csv()` utilise le module standard `csv`
  pour écrire la liste des URLs de la catégorie.
- Les fichiers CSV et JPG sont écrits en UTF-8 ou en mode binaire selon leur
  contenu.

