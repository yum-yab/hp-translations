from bs4 import BeautifulSoup
import requests
import csv
import re
import os

# all uris from here: https://harry-potter.fandom.com/de/wiki/Originalnamen_und_-bezeichnungen

resource_uris = [
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


fanfiktion_uri_regex = re.compile(r"(https:\/\/www\.fanfiktion\.de\/s\/)([\w\d]+\/)(\d)(\/[\w-]+)")

fanfiction_replacement_regexes = {
    re.compile(r"[_]{2,}") : " ",
    re.compile(r"[-_]{2,}.{3, 50}[-_]{2,}") : "",
    re.compile(r"[ ]{2,}") : " "
}

def handle_chapter_uri(uri: str, chapter_id: int, user: str, basedir: str ="./german-translations"):
    page = requests.get(uri).text

    soup = BeautifulSoup(page, "html.parser")

    for br in soup('br'):
        br.replace_with('\n')

    raw_text = soup.find("div", class_="user-formatted-inner").text

    for regex, replacement in fanfiction_replacement_regexes.items():
        new_text = regex.sub(replacement, raw_text)
        raw_text = new_text

    target_dir = os.path.join(basedir, user)

    filepath = os.path.join(target_dir, f"{chapter_id}.txt")

    if not os.path.isdir(target_dir):
        os.makedirs(target_dir, exist_ok=True)

    with open(filepath, "w+") as newfile:
        print(raw_text, file=newfile)


def rawparse_fanfiction(uri, start_number=1, end_number=10, chapter_offset=1, skiplist=list()):

    match = fanfiktion_uri_regex.match(uri)

    if match is None:
        return

    base_uri, hash_string, _, title = match.groups()

    page = requests.get(uri).text


    soup = BeautifulSoup(page, "html.parser")

    user = soup.find("span", class_="fas fa-user fa-ffcustom").parent.text

    counter = 0

    for i in range(start_number, end_number+1):

        chapter_id = chapter_offset + counter

        if i in skiplist: 
            counter += 1
            continue

        chapter_url = base_uri + hash_string + str(i) + title

        handle_chapter_uri(chapter_url, chapter_id, user)        
        
        counter += 1


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


def parse_translations_from_uris():

    with open("./translations.csv", "w+") as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(("english", "german"))
        for uri in resource_uris:
            print(f"Handling URI {uri}")

            res = get_csv_from_site(uri)

            print(f"Found entries: {len(res)}")

            writer.writerows(res)


if __name__ == "__main__":

    # DieFuechsin
    rawparse_fanfiction("https://www.fanfiktion.de/s/5c793dfe000a402030774dc7/1/Harry-Potter-und-die-Methoden-der-Rationalitaet-Ubersetzung-HPMOR", start_number=2, end_number=46, chapter_offset=34)

    # Jost
    rawparse_fanfiction("https://www.fanfiktion.de/s/4cb8beb50000203e067007d0/6/Harry-Potter-und-die-Methoden-des-rationalen-Denkens", start_number=1, end_number=21, skiplist=[11])

    # Schneefl0cke
    rawparse_fanfiction("https://www.fanfiktion.de/s/60044849000ccc541aef297e/1/Ubersetzung-Harry-Potter-und-die-Methoden-des-rationalen-Denkens-Harry-Potter-and-the-methods-of-rationality", start_number=2, end_number=121)

    # Patneu
    rawparse_fanfiction("https://www.fanfiktion.de/s/55610c610004dede273a3811/1/Harry-Potter-und-die-Methoden-der-Rationalitaet", start_number=1, end_number=38,  skiplist=[11])