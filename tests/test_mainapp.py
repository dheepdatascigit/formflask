import pytest
import mainapp


def test_output():
    assert mainapp.version() == 1.0

def test_typefloat():
    assert type(mainapp.version()) == float

def test_typeint():
    assert type(mainapp.version()) != int

#print(mainapp.version)