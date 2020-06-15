import nirvana

def Not(a: bool) -> bool:
    return nirvana.nand(a, a)


def And(a: bool, b: bool) -> bool:
    return Not(nirvana.nand(a, b))


def Or(a: bool, b: bool) -> bool:
    return nirvana.nand(Not(a), Not(b))


def Xor(a: bool, b: bool) -> bool:
    return And(nirvana.nand(a, b), Or(a, b))


if __name__ == "__main__":
    # TODO: write as unit tests, and more extended

    assert Not(True) == False
    assert Not(False) == True

    assert And(False, False) == False
    assert And(True, False) == False
    assert And(False, True) == False
    assert And(True, True) == True

    assert Or(False, False) == False
    assert Or(True, False) == True
    assert Or(False, True) == True
    assert Or(True, True) == True

    assert Xor(False, False) == False
    assert Xor(True, False) == True
    assert Xor(False, True) == True
    assert Xor(True, True) == False
