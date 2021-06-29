from bs4 import BeautifulSoup
import requests
import csv

# all uris from here: https://harry-potter.fandom.com/de/wiki/Originalnamen_und_-bezeichnungen

uris = [
    "https://harry-potter.fandom.com/de/wiki/Original-Namen_von_Begriffen_und_Schimpfworten",
    "https://harry-potter.fandom.com/de/wiki/Original-Namen_bekannter_magischer_Einzelwesen_der_Harry_Potter_B%C3%BCcher",
    "https://harry-potter.fandom.com/de/wiki/Original-Namen_Gesellschaftspolitische_Gruppen",
    "https://harry-potter.fandom.com/de/wiki/Original-Namen_f%C3%BCr_Gesetze_und_Verordnungen",
    "https://harry-potter.fandom.com/de/wiki/Original-Namen_von_Handlungsorten_in_den_Harry_Potter_B%C3%BCchern",
    "https://harry-potter.fandom.com/de/wiki/Original-Namen_f%C3%BCr_Magische_Kommunikations-_und_Verkehrsmittel",
    "https://harry-potter.fandom.com/de/wiki/Original-Namen_f%C3%BCr_Magische_Pflanzen_und_Naturalien",
    "https://harry-potter.fandom.com/de/wiki/Original-Namen_von_Personencharakteren_der_Harry_Potter_B%C3%BCcher",
    "https://harry-potter.fandom.com/de/wiki/Original-Namen_f%C3%BCr_Sport_und_Spiele_in_den_Harry_Potter_B%C3%BCchern",
    "https://harry-potter.fandom.com/de/wiki/Original-Bezeichnungen_von_B%C3%BCros_und_%C3%84mter_im_britischen_Zaubereiministerium",
    "https://harry-potter.fandom.com/de/wiki/Original-Titel_magischer_B%C3%BCcher_und_Medien",
    "https://harry-potter.fandom.com/de/wiki/Original-Bezeichnungen_f%C3%BCr_Magische_Gegenst%C3%A4nde_und_Gebrauchsartikel_in_den_Harry_Potter_B%C3%BCchern",
    "https://harry-potter.fandom.com/de/wiki/Original-Bezeichnungen_magischer_Tierwesen_der_Harry_Potter_B%C3%BCcher",
    "https://harry-potter.fandom.com/de/wiki/Original-Bezeichnungen_und_Namen_magischer_Wesen_der_Harry_Potter_B%C3%BCcher",
    "https://harry-potter.fandom.com/de/wiki/Original-Bezeichnungen_f%C3%BCr_Unterrichtsf%C3%A4cher_in_Hogwarts",
    "https://harry-potter.fandom.com/de/wiki/Original-Bezeichnungen_f%C3%BCr_Schulnoten_in_Hogwarts",
    "https://harry-potter.fandom.com/de/wiki/Original-Bezeichnungen_f%C3%BCr_Pr%C3%BCfungen_in_Hogwarts",
    "https://harry-potter.fandom.com/de/wiki/Original-Bezeichnungen_f%C3%BCr_Gruppen_und_%C3%84mter_in_Hogwarts",
    "https://harry-potter.fandom.com/de/wiki/Original-Bezeichnungen_f%C3%BCr_Quidditch_-_Spieler_-_Mannschaften_-_B%C3%A4lle_-_Man%C3%B6ver",
    "https://harry-potter.fandom.com/de/wiki/Original-Bezeichnungen_f%C3%BCr_Zauber_und_Zaubertr%C3%A4nke",
    "https://harry-potter.fandom.com/de/wiki/Original-Bezeichnungen_von_Wortspielen,_Parolen_und_Spr%C3%BCchen"
]


def get_csv_from_site(uri):

    page = requests.get(uri).text

    soup = BeautifulSoup(page, "html.parser")

    table = soup.find("table")
    tbody = table.find("tbody")

    rows = tbody.find_all("tr")

    result = []

    for row in rows:
        elements = row.find_all("td")

        if len(elements) != 2:
            continue

        english, german = elements[0].text, elements[1].text
        result.append((english.strip("\n"), german.strip("\n")))

    return result


if __name__ == "__main__":

    with open("./translations.csv", "w+") as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(("english", "german"))
        for uri in uris:
            print(f"Handling URI {uri}")

            res = get_csv_from_site(uri)

            print(f"Found entries: {len(res)}")

            writer.writerows(res)
