from grammar import Grammar as Gr
from mytoken import *
from mytoken import MyToken as Tk

from alg.isLanguageEmpty import isLanguageEmpty
from alg.unreachableSymbols import unreachableSymbols

def uselessSymbols(grammar: Gr) -> Gr:
    """Устранение бесполезных символов в грамматике"""
    isEmpty, gr1 = isLanguageEmpty(grammar)
    if not isEmpty:
        return unreachableSymbols(gr1)
    return grammar