import pytest
from feature_term import FeatureTerm
import feature_term_operators as ftgens

def test_subsumes():
    sorts = {
        "Rightarrow": "Arrow",
        "Leftarrow": "Arrow",
        "Arrow": "Symbol",
        "Silhouette": "Symbol"
    }
    fs = FeatureTerm(sorts, {})

    fs1 =  ftgens.init_FeatStruct(root = "Silhouette", rightside="Symbol", leftside="asdf")
    fs2 =  ftgens.init_FeatStruct(root = "Silhouette", rightside="Symbol", asd="asd")
    assert fs._subsumes(fs1, fs2) == False