"""
Module for testing the Container class
"""
import container as c


def test_eq():
    c1 = c.Container(weight=333, description="Costco", on_ship=True)
    c2 = c.Container(weight=996, description="Costco", on_ship=True)
    c3 = c.Container(weight=996, description="Walmart", on_ship=True)
    c4 = c.Container(weight=996, description="Walmart", on_ship=True)
    c5 = c.Container(weight=333, description="Frice", on_ship=True)
    c6 = c.Container(weight=520, description="Frice", on_ship=True)

    assert c1 == c2
    assert c3 == c4
    assert c5 == c6
    assert c1 != c3
    assert c1 != c6
    assert c6 != c3
