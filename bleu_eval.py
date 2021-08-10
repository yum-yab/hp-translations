import os
import argparse
from nltk.translate.bleu_score import corpus_bleu, SmoothingFunction
import json
import spacy
import csv

nlp = spacy.load("de_core_news_sm")


def get_chapter_files(chapter_id: int, basedir: str = "./german-translations"):

    results = {}

    for author in os.listdir(basedir):

        author_path = os.path.join(basedir, author)

        if not os.path.isdir(author_path):
            continue

        chapter_path = os.path.join(author_path, str(chapter_id) + ".txt")

        if not os.path.isfile(chapter_path):
            continue

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


def get_str_content(s: str):

    res = []

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
        bleu = corpus_bleu([[r]], [target_content],
                           smoothing_function=chencherry.method1)
        author = authors[i]
        print(f"{author}: {bleu=}")


def evaluate_mturk(results_mapping, target_file: str, output_file: str = "./out.json") -> None:

    authors, files = zip(*results_mapping.items())

    chencherry = SmoothingFunction()

    references = [get_file_content(path) for path in files]

    result_dict = {}

    with open(target_file) as csv_report:
        reader = csv.DictReader(csv_report)

        for hit_row in reader:
            # handle all rows and group them by HITIds
            target_content = get_str_content(hit_row.get("Answer.translation", ""))
            hit_id = hit_row.get("HITId", "")
            info_map = {}
            for i, ref in enumerate(references):
                bleu = corpus_bleu([[ref]], [target_content],
                                   smoothing_function=chencherry.method1)
                author = authors[i]
                info_map[author] = bleu

            result_dict[hit_id] = info_map

    print(f"Evaluated {len(result_dict)} translations.")
    with open(output_file, "w+") as output_file:
        json.dump(result_dict, output_file)

    


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
    )

    parser.add_argument(
        "-m",
        "--mturk_eval",
        type=str,
        help="A path to the evaluation file of MTurk"
    )
    args = parser.parse_args()

    res = get_chapter_files(args.chapter_reference)

    if args.mturk_eval:
        evaluate_mturk(res, args.mturk_eval)
    else:
        calculate_bleu(res, args.target_file)
    