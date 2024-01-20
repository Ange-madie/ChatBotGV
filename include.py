def test_in_tab(tab1: list | tuple, tab2: list | tuple):
    for value in tab1:
        if value in tab2:
            return True

    return False


def all_test_in_tab(tab1: list | tuple, tab2: list | tuple):
    for value in tab1:
        if value not in tab2:
            return False

    return True

def separateur_mot(phrase: str):
    """Fonction pour diviser une phrase en mots."""
    mots = []
    ignorer = ["?", "-", ".", "!", "_", " ", ","]
    l = []
    for letter in phrase:
        if letter not in ignorer:
            l.append(letter)
        else:
            if l:
                mots.append(''.join(l))
            l = []
    if l:
        mots.append(''.join(l))

    return tuple(mots)
