import pytest
import sys
sys.path.append("./src/")
import rainbow_generator
import pearson


def test_hashes():
  
    assert pearson.hashN("CeQ",2)==b"\xFF\x99"
    assert pearson.hashN("kjB",2)==b"\xAA\xAA"

