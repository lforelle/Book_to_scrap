# Scraper de produit - Books to Scrape

Ce script Python permet de récupérer les informations d'un livre depuis la page produit de [Books to Scrape](https://books.toscrape.com/) puis de les enregistrer dans un fichier CSV.

## Objectif

Le script charge la page du livre :

- A Light in the Attic

puis extrait les données suivantes :

- URL de la page produit
- UPC
- titre
- type de produit
- prix TTC
- prix HT
- taxe
- disponibilité
- description du produit
- catégorie
- note de review
- URL de l'image

## Fonctionnement

Le programme utilise :

- `requests` pour télécharger la page HTML
- `BeautifulSoup` pour analyser le contenu HTML
- `csv` pour écrire les données dans un fichier `output.csv`

Il repère les éléments du HTML avec des sélecteurs comme :

- `table.table.table-striped` pour la table technique du produit
- `div.col-sm-6.product_main h1` pour le titre
- `h2` avec le texte `Product Description` pour la description
- `ul.breadcrumb` pour retrouver la catégorie
- `id="product_gallery"` pour l'image

## Prérequis

Installez les dépendances nécessaires :

```bash
pip install requests beautifulsoup4
```

## Utilisation

Lancez le script :

```bash
python main.py
```

Le fichier généré sera :

```bash
output.csv
```

## Exemple de sortie

Le script crée un dictionnaire contenant les informations extraites, puis l'écrit dans le CSV avec les clés comme en-têtes de colonnes.

Exemple de structure :

```python
{
    'product_page_url': 'https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html',
    'UPC': 'a897fe39b1053632',
    'title': 'A Light in the Attic',
    'category': 'Poetry',
    'product_description': '...'
}
```

## Fichier produit

Le script génère un fichier CSV nommé `output.csv`, avec les colonnes correspondant aux champs récupérés.

## Notes

- La page ciblée est codée en dur dans le script.
- Le script est adapté à un seul produit, pas encore à la récupération de plusieurs livres ou d'une catégorie complète.
- Le site de test est volontairement simple et conçu pour l'entraînement au web scraping.
