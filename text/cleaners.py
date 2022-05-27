""" from https://github.com/keithito/tacotron """

'''
Cleaners are transformations that run over the input text at both training and
eval time.
import matplotlib
%matplotlib inline
import matplotlib.pylab as plt

import IPython.display as ipd

import sys
Cleaners can be selected by passing a comma-delimited list of cleaner names
as the "cleaners"
hyperparameter. Some cleaners are English-specific. You'll typically want to use:
  1. "english_cleaners" for English text
  2. "transliteration_cleaners" for non-English text that can be transliterated
  to ASCII using
     the Unidecode library (https://pypi.python.org/pypi/Unidecode)
  3. "basic_cleaners" if you do not want to transliterate (in this case, you
  should also update
     the symbols in symbols.py to match your data).
'''

import re
from unidecode import unidecode

from .numbers import NumberToNepaliText

# Regular expression matching whitespace:
_whitespace_re = re.compile(r'\s+')


def collapse_whitespace(text):
    """Removes whitespaces"""
    return re.sub(_whitespace_re, ' ', text)


def convert_to_ascii(text):
    return unidecode(text)


def convert_sentence_number_to_text(sentence):
    """Convert numbers into numerical number. like for '१' it will
    transform this to एक"""
    ntnt = NumberToNepaliText()
    numbers = ['१', '२', '३', '४', '५', '६', '७', '८', '९', '०']
    tokens = sentence.split(" ")
    new_tokens = []
    for token in tokens:
        for number in numbers:
            if number in token:
                new_tokens.append(ntnt.NumberToText(token))
                break
        else:
            new_tokens.append(token)
    return " ".join(new_tokens)


def basic_cleaners(text):
    '''Basic pipeline that lowercases and collapses whitespace without
    transliteration.'''
    text = collapse_whitespace(text)
    text = convert_sentence_number_to_text(text)
    return text
