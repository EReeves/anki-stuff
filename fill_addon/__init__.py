from aqt import mw
from aqt.utils import showInfo, qconnect
from aqt.qt import *
from cccedict import CcCedict
from pystartdict import Dictionary
import re


## Lazy fill of cards without definition

DECK_NAME = "挖掘"
TAKE_FROM_FIELD = "Sentence"
WORD_FIELD = "Word"
DEFINITION_FIELD = "Definition"


def get_bolded_word(sentence) -> str:
    matches = re.findall(r"<b>(.*?)<\/b>", sentence)
    if len(matches) > 0:
        return str(matches[0])
    else:
        return None


def setup_dicts():
    cedict = CcCedict()  # TODO: interface backup dicts
    dicts = [cedict]
    return dicts


def get_definition(word, dicts):
    for dict in dicts:
        entry = dict.get_entry(word)
        if entry:
            return str(entry)  # TODO: better format
    return None


def fill_cards() -> None:
    dicts = setup_dicts()
    card_ids = mw.col.find_cards(f'''deck:"{DECK_NAME}"''')
    changed_ctr = 0

    for card_id in card_ids:
        note = mw.col.get_card(card_id).note()

        if not note[DEFINITION_FIELD]:  # if field empty
            word = get_bolded_word(note[TAKE_FROM_FIELD])
            if word:
                if not note[WORD_FIELD]:
                    note[WORD_FIELD] = word
                entry = get_definition(word, dicts)
                if entry:
                    note[DEFINITION_FIELD] = entry
                    changed_ctr += 1

                mw.col.update_note(note)

    showInfo(f"Filled {changed_ctr} cards.")


def add_to_menu(name, function):
    action = QAction(name, mw)
    qconnect(action.triggered, function)
    mw.form.menuTools.addAction(action)


add_to_menu("Fill Cards", fill_cards)
