from . import morse_lib
import re

# dictionary for signals
inputData = {
    "0": ".",
    "1": "-",
    "2": "",  # space between symbols
    "3": ",",  # space between letters <--- don't change this key
    "4": " ",
}

To_inputData = {value: key for key, value in inputData.items()}


def _signalToMorse_(sequence):
    """
        converts signal (ex : '123123') to morse ( ex: ..---)
    """

    _morsed_word = ''

    for number in sequence:
        _morsed_word += inputData[number]

    morsed_word = list(filter(None, re.split(",|(\s)", _morsed_word)))  # split by letters

    # print(morsed_word)  # for debugging
    return morsed_word


def _morseToEnglish_(morse_seq):
    """
        converts morse code to words/letters (ex: . --> e)
    """
    _translated = ''
    # print(morse_seq)
    for morse in morse_seq:
        _translated += morse_lib.from_morse[morse]  # call for the module

    return _translated


def _englishToMorse_(word_seq):
    """
            converts letters/words to morse (ex: e --> .)
    """
    _translated = []
    for char in word_seq:
        _translated.append(morse_lib.to_morse[char])

    return _translated


def _morseToSignal_(morse):
    """
            converts morse (ex : '..---') to signal ( ex:123123)
    """

    _translated = []
    for i_id, i in enumerate(morse):
        for j_id, j in enumerate(i):
            _translated.append(To_inputData[j])  # convert... (. --> 0)
            if j_id != len(i) - 1:
                _translated.append("2")  # space between 2 morse codes (ex: a --> .()- --> 021 )

        if i_id < len(morse) - 1 and i != ' ' and morse[i_id + 1] != ' ':
            _translated.append("3")  # space between 2 morse words (ex: et --> .()- --> 031 , e e --> .[ ]. --> 040)

    return "".join(_translated)  # join the list and converts to a string (ex:  [ 012 , 012 ...] --> '012012...')


# call those
def convertToWords(morse):
    """
    Converts morse code to english words

    Args:

        morse (str): string containing 0,1,2,3 each representing a different symbol in morse
    """
    return _morseToEnglish_(_signalToMorse_(morse))


def convertToMorse(words):
    """
    Converts plaint text to morse

    Args:

        words (str): any string containing characters supported

    This is mainly used for testing purposes
    """
    return _morseToSignal_(_englishToMorse_(words))
