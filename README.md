# Resources for translating Harry Potter and the Methods of Rationality

These are resources generated for the Seminar Citicen Science at the University of Leipzig.

All data stem from https://harry-potter.fandom.com/de/wiki/Originalnamen_und_-bezeichnungen and is merged directly in one csv. The data contains various named entities and things from the Harry Potter universe, like charms, potions, figures of speech, games and many more.

## Installation
- create virtual environment with *virtualenv*
    - `python3 -m virtualenv env`
- activate virtual environment
    - `source env/bin/activate`
- download required packages
    - `pip3 -r requirements.txt`
- download spacy german core:
    - `python -m spacy download de_core_news_sm`

## Translations

German translations are available in the directory `german_translations` and are grouped by their author and named after the chapter (e.g. `german_translations/Jost/15.txt`)


## BLEU evaluation

To get the bleu score of a chapter the chapter needs to be identified with the id and the text to be evaluated needs to be in a file like `./example/dir/text.txt`

```
python bleu_eval.py -c <id> -t ./example/dir/text.txt
```