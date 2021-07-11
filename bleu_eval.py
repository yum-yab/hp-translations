import os
import argparse
from nltk.translate.bleu_score import corpus_bleu, SmoothingFunction
import json
import spacy

nlp = spacy.load("de_core_news_sm")

def get_chapter_files(chapter_id: int, basedir: str = "./german-translations"):

    results = {}

    for author in os.listdir(basedir):

        author_path = os.path.join(basedir, author)

        if not os.path.isdir(author_path): continue

        chapter_path = os.path.join(author_path, str(chapter_id) + ".txt")

        if not os.path.isfile(chapter_path): continue

        results[author] = chapter_path

    return results

def get_file_content(path):

    res = []

    with open(path) as f:
        s = f.read()
        s = s.replace("\n", " ")
        doc = nlp(s)

    for token in doc: 
        if not token.is_stop and not token.is_punct and not token.is_space:
            res.append(token.text)
    
    return res


def calculate_bleu(results_mapping, target_file):

    authors, files = zip(*results_mapping.items())

    chencherry = SmoothingFunction()

    references = [get_file_content(path) for path in files]

    target_content = get_file_content(target_file)

    for i, r in enumerate(references):
        bleu = corpus_bleu([[r]], [target_content], smoothing_function=chencherry.method1)
        author = authors[i]
        print(f"{author}: {bleu=}")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="A tool for evaluating the BLEU score of the german HPMOR translation. WORK IN PROGRESS"
    )
    parser.add_argument(
        "-c",
        "--chapter_reference",
        type=int,
        help="An integer to indicate the chapter to be compared to.",
        required=True,
    )
    parser.add_argument(
        "-t",
        "--target_file",
        type=str,
        help="A path to a file which should be evaluated",
        required=True,
    )
    args = parser.parse_args()


    res = get_chapter_files(args.chapter_reference) 


    calculate_bleu(res, args.target_file)