from bs4 import BeautifulSoup
import book_details
from urllib.parse import urljoin
import os
import csv

# Repertoire du projet
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))


def books_href_extract(soup, one_category_books_href_list):
    ol = soup.find("ol", class_="row")
    for li in ol.find_all("li", class_="col-xs-6 col-sm-4 col-md-3 col-lg-3"):
        image_container_href = li.find("div", class_="image_container").find("a").get("href")
        image_container_href = image_container_href.split('../')[-1]    # on supprime les '../' pour adresser l'url absolue
        book_url = urljoin('https://books.toscrape.com/catalogue/', image_container_href)
        one_category_books_href_list.append(book_url)


def find_next_page_url(soup, category_page_href):
    ul_pager = soup.find("ul", class_="pager")
    if ul_pager == None:
        return False

    li_next = ul_pager.find("li", class_="next")
    if li_next:
        href_page = li_next.find("a").get("href")
        return urljoin(category_page_href, href_page)
    return False


def save_category_href_to_csv(filename, one_category_books_href_list, mode):   
    os.makedirs(book_details.DETAILS_DIR, exist_ok=True)
    path_output_filename = os.path.join(book_details.DETAILS_DIR, filename + ".csv")

    with open(path_output_filename, mode, newline="", encoding="utf-8") as output_csv:
        writer = csv.writer(output_csv, delimiter=",")
        writer.writerow(one_category_books_href_list)

def main(category_page_href):
    response = book_details.test_page_access(category_page_href)
    if response is None:
        print(f"Pas de données pour : {category_page_href}")
        return
    soup = BeautifulSoup(response.text, "html.parser")

    one_category_books_href_list = []
    next_page = False
    category_name = soup.find("head").find("title").string
    category_name = category_name.split('|')[0].strip()
    
    books_href_extract(soup, one_category_books_href_list)

    # Verification de presence de pages supplémentaires  
    next_page = find_next_page_url(soup, category_page_href)
    while next_page:
        response = book_details.test_page_access(next_page)
        if response is None:
            print(f"Pas de données pour : {next_page}")
            return
        soup = BeautifulSoup(response.text, "html.parser")

        books_href_extract(soup, one_category_books_href_list)
        
        category_page_href = next_page     # La page actuelle devient la page suivante

        next_page = find_next_page_url(soup, category_page_href)

    # Stockage dans un CSV des url de chaque livre de la catégorie
    csv_dir = os.path.join(PROJECT_ROOT, "csv_files")
    if not os.path.isdir(csv_dir):
        os.mkdir(csv_dir)
    os.chdir(csv_dir)

    category_dir = category_name.replace(' ', '_')
    if not os.path.isdir(category_dir):
        os.mkdir(category_dir)
    os.chdir(category_dir)

    category_filename = "books_by_category_" + category_dir + "_"
    save_category_href_to_csv(category_filename, one_category_books_href_list, "w")

    print("======= Extraction des données produit de chaque livre de la catégorie =======\n")
    details_filename = "details_"

    print(f"####### livre(s) dans {category_name}")
    for book_url in one_category_books_href_list:
        book_details.main(book_url, details_filename)
        
    print(f"####### Fichiers CSV de la categorie {category_name} créés #######\n")

    os.chdir("./..")
   

#================== Main script ===================

if __name__ == "__main__":
    category_page_href = "https://books.toscrape.com/catalogue/category/books/sequential-art_5/page-1.html"
    main(category_page_href)
