"""
Module for testing the optimizer class
"""
import pytest
import optimizer as o


def test_get_child():
    """Tests whether the correct operation depending on task input of the get child_function"""
    with pytest.raises(ValueError):
        o.get_child([], "Balance")
        o.get_child([], "Loading")
