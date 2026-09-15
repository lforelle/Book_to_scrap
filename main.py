import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

def data_to_save_to_csv(dico_infos):
    # Horodatage
    now = datetime.now()
    current_date_time = now.strftime("%Y%m%d_%H%M%S")

    # Nom du fichier output.csv a horodater
    output_filename = "Extract_books_B2S_" + current_date_time + ".csv"
    with open(output_filename, "w", newline="", encoding="utf-8") as output_csv:
        # Les clefs en titre de colonnes
        fieldnames = dico_infos.keys()
        writer = csv.DictWriter(output_csv, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(dico_infos)


def main():
    # page du livre:'A Light in the Attic'
    page_url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
    currency = "£"

    response = requests.get(page_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        #print(soup.prettify())

        # La table contenant les informations du produit se trouve dans le tag <table> avec la classe "table table-striped"
        table = soup.find("table", class_="table table-striped")

        # les informations du produit trouvées seront ajoutées dans le dictionnaire
        dico_infos = {}
        dico_infos["product_page_url"] = page_url

        # On boucle sur les lignes <tr> et <th>. Si le contenu <th> match le motif
        # alors on copie le texte <td> correspondant dans le dico
        for tr in table.find_all("tr"):
            for th in tr.find_all("th"):
                if th.text.strip().lower() == "upc":
                    dico_infos[th.text] = tr.find("td").get_text(strip=True)
                # if th.text.strip().lower() == "product type":
                #     dico_infos[th.text] = tr.find("td").get_text(strip=True)
                if th.text.strip().lower() == "price (incl. tax)":
                    raw_taxed_price = tr.find("td").get_text(strip=True)
                    taxed_price = raw_taxed_price.split(currency)[1] + currency
                    dico_infos[th.text] = taxed_price
                if th.text.strip().lower() == "price (excl. tax)":
                    raw_free_price = tr.find("td").get_text(strip=True)
                    free_price = raw_free_price.split(currency)[1] + currency
                    dico_infos[th.text] = free_price
                if th.text.strip().lower() == "tax":
                    raw_tax = tr.find("td").get_text(strip=True)
                    tax = raw_tax.split(currency)[1] + currency
                    dico_infos[th.text] = tax
                if th.text.strip().lower() == "availability":
                    raw_availibility = tr.find("td").get_text(strip=True)
                    availibility = (raw_availibility.split("(")[1]).split(" ")[0]
                    dico_infos[th.text] = availibility

        # Le titre du produit se trouve dans le tag <h1> qui est contenu dans un <div> avec la classe "col-sm-6 product_main"
        title = soup.find("div", class_="col-sm-6 product_main").find("h1").text
        dico_infos["title"] = title

        # La description du produit se trouve dans le tag <p> qui suit le <h2> "Product Description"
        header_product_description = soup.find("h2", string="Product Description")
        product_description = header_product_description.find_next("p")
        dico_infos["product_description"] = product_description.text

        # La catégorie du produit se trouve dans le tag <ul> avec la classe "breadcrumb"
        ul = soup.find("ul", class_="breadcrumb")
        for li in ul.find_all("li"):
            a = li.find("a")
            if a:
                if a.string.lower() == "home" or a.string.lower() == "books":
                    continue
                else:
                    category = li.find("a").text
                    dico_infos["category"] = category

        # Recup du nb d'etoiles (review_rating)
        star_rating = soup.find("i", class_="icon-star").find_parent("p")
        review_rating = star_rating.get("class")
        nb_stars_en = review_rating[1].lower()
        # Conversion des notations string en numerique
        nb_stars = {"one":1, "two": 2, "three": 3, "four": 4, "five": 5}
        nb_stars_fr = nb_stars[nb_stars_en]
        dico_infos["review_rating"] = nb_stars_fr
        
        # L'url de l'image
        image_url = soup.find(id="product_gallery").find("img")

        # !!!!!!!!!!!!!!!!!!!!!!!!! ne fonctionne pas avec la ldc suivante !!!!!!!!!!!!!!!!!!!!!!!!!!
        # src_image = image_url.split('src="')[1].split('"')[0]
        src_image = image_url.get("src")
        dico_infos["image_url"] = src_image
        
        print(dico_infos, "\n")
        data_to_save_to_csv(dico_infos)

#================== Main script ===================

if __name__ == "__main__":
    main()

