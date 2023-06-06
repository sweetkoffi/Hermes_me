import re
import requests
from bs4 import BeautifulSoup
#########################################################HEADER

logo = ''' _   _                                ___  ___     
| | | |                               |  \/  |     
| |_| | ___ _ __ _ __ ___   ___  ___  | .  . | ___ 
|  _  |/ _ \ '__| '_ ` _ \ / _ \/ __| | |\/| |/ _ \\
| | | |  __/ |  | | | | | |  __/\__ \ | |  | |  __/
\_| |_/\___|_|  |_| |_| |_|\___||___/ \_|  |_/\___|
                                  ______           
                                 |______|'''

# Determine the width of the rectangle
lines = logo.split("\n")
width = max(len(line) for line in lines)

# Create the top and bottom borders of the rectangle
top_border = "+" + "-" * (width + 2) + "+"
bottom_border = "+" + "-" * (width + 2) + "+"

# Print the ASCII rectangle art
print(top_border)
for line in lines:
    padding = " " * (width - len(line))
    print("| " + line + padding + " |")
print(bottom_border)


#########################################################HEADER
# Source Radio Canada
sourceRC = requests.get('https://ici.radio-canada.ca/info/en-continu').text
# Source Les Affaires
sourceAff = requests.get('https://www.lesaffaires.com/dernieres-nouvelles').text
#Main Function
def search_keyword_in_source(source, keyword, source_type):
    soup = BeautifulSoup(source, 'lxml')
    compteur = 0

    if source_type == "RC":
        container = soup.find('ul', class_="sc-dnwbae-0")

        for divGlobal in container:
            if divGlobal.find('div', class_='sc-1jhqbg-0') is not None:
                article = divGlobal.find('section', class_='sc-n0leh-0')
                lienDeArticle = "https://ici.radio-canada.ca" + article.find('a')['href']
                articleTitre = article.find('h3').text
                categorie = articleTitre.split('.')[0]
                titre = articleTitre.split('.')[1]
                autres = articleTitre.split('.')[2]
                pattern = r'.*?\d[A-Z]'
                timeDate = re.search(pattern, autres)
                if timeDate:
                    timeDate = timeDate.group(0)[:-1]
                else:
                    timeDate = "none"
                if keyword.lower() in articleTitre.lower():
                    print('Catégorie : ' + categorie + "\n" + 'Titre     :' + titre + "\n" + 'Autres    :' + timeDate + "\n" + "lien      :" + lienDeArticle)
                    compteur += 1
                    print('-' * 30)

        if compteur == 0:
            print('-' * 30)
            print("ICI RADIO CANADA")
            print("Nothing found")
            print('-' * 30)

    elif source_type == "Aff":
        articles = soup.find_all('div', class_='article')

        for divGlobal in articles:
            if divGlobal.find('span', class_='title') is not None:
                articleTitre = divGlobal.find('span', class_='title').text
                categorie = divGlobal.find('span', class_='source')
                if categorie:
                    categorie = divGlobal.find('span', class_='source').text
                else:
                    categorie = "N/A"
                autres = divGlobal.find('span', class_='excerpt').text
                lienDeArticle = divGlobal.find('a')['href']
                if keyword.lower() in articleTitre.lower() or keyword.lower() in autres.lower():
                    print('Catégorie : ' + categorie.strip() + "\n" + 'Titre     :' + articleTitre.strip() + "\n" + 'Autres    :' + autres.strip() + "\n" + "lien      :" + lienDeArticle.strip())
                    print('-' * 30)
                    compteur += 1

        if compteur == 0:
            print('-' * 30)
            print("LES AFFAIRES")
            print("Nothing found")
            print('-' * 30)


keyword = input("Entrez le keyword :")
search_keyword_in_source(sourceAff, keyword, "Aff")
search_keyword_in_source(sourceRC, keyword, "RC")

