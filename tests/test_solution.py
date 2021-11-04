import pytest
import sys
sys.path.append("./src/")
import rainbow_generator
import pearson


def test_generator():
    d=rainbow_generator.generateTable(["test1", "test2", "test3"], lambda x: pearson.hashN(x,2), rainbow_generator.makeGuess, 20, 3, 6, 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789')
    
    assert d=={b'fa': 'test1', b'=\xcd': 'test2', b'\x0b\n': 'test3'}
