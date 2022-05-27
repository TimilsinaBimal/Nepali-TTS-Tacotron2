""" from https://github.com/keithito/tacotron """

'''
Defines the set of symbols used in text input to the model.

The default is a set of ASCII characters that works well for English or text that has been run through Unidecode. For other data, you can modify _characters. See TRAINING_DATA.md for details. '''
from text import cmudict

_pad = '_'
_punctuation = '|!\'(),.:;? '
_special = '-'
# _letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
_letters = [
    'क', 'ख', 'ग', 'घ', 'ङ', 'च', 'छ', 'ज', 'झ', 'ञ', 'ट', 'ठ', 'ड', 'ढ', 'ण',
    'त', 'थ', 'द', 'ध', 'न', 'ऩ', 'प', 'फ', 'ब', 'भ', 'म', 'य', 'र', 'ल', 'व',
    'श', 'ॠ', 'ष', 'ष', 'स', 'ह', 'क्ष', 'त्र', 'ज्ञ', "ँ", '।', 'ा', 'ू', 'ु',
    'े', 'ो', 'ौ', 'ै', 'ृ', 'ी', 'ि', 'ं', 'ॐ', 'ः', '?', '!', '.', 'ळ', 'ण',
    ',', 'अ', 'आ', 'इ', 'ई', 'ऊ', 'उ', 'ए', 'ऐ', 'ओ', 'औ', 'ञ', ' ', '्',
    '\u200d', 'ऋ', '\u200c']

# Prepend "@" to ARPAbet symbols to ensure uniqueness (some are the same as uppercase letters):
_arpabet = ['@' + s for s in cmudict.valid_symbols]

# Export all symbols:
symbols = [
    _pad] + list(_special) + list(_punctuation) + list(_letters) + _arpabet
