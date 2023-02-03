import builtins
import unittest

import a1ece650



def test_checkIntersect_1():
    s1 = a1ece650.StreetPart((0, 0), (5, 0))
    s2 = a1ece650.StreetPart((5, 0), (5, 5))
    result = a1ece650.checkIntersect(s1, s2)
    assert result == (5.0, 0.0)


def test_checkIntersect_2():
    s1 = a1ece650.StreetPart((0, 0), (4, 0))
    s2 = a1ece650.StreetPart((5, 0), (5, 5))
    result = a1ece650.checkIntersect(s1, s2)
    assert result is None


def test_checkIntersect_3():
    s1 = a1ece650.StreetPart((0, 0), (4, 0))
    s2 = a1ece650.StreetPart((5, 4), (4, 4))
    result = a1ece650.checkIntersect(s1, s2)
    assert result is None


def test_checkIntersect_4():
    s1 = a1ece650.StreetPart((0, 0), (4, 0))
    s2 = a1ece650.StreetPart((4, 0), (8, 0))
    result = a1ece650.checkIntersect(s1, s2)
    assert result is (4, 0)