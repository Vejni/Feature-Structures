import pytest
from feature_term import FeatureTerm
import operators as op

def test__most_general_sort():
    assert False

def test__subsumes():
    sorts = {
        "Rightarrow": "Arrow",
        "Leftarrow": "Arrow",
        "Arrow": "Symbol",
        "Silhouette": "Symbol"
    }
    fs = FeatureTerm(sorts, {})

    # Test basic subsumption
    assert fs._subsumes(
        op.init_FeatStruct(root = "Silhouette", rightside="Symbol", leftside="Symbol"), 
        op.init_FeatStruct(root = "Silhouette", rightside="Symbol")
    ) == True

    # Test basic subsumption
    assert fs._subsumes(
        op.init_FeatStruct(root = "Silhouette", rightside="Symbol", leftside="Symbol"), 
        op.init_FeatStruct(root = "Silhouette", rightside="Symbol", middle="Symbol")
    ) == False

    # Test equality
    assert fs._subsumes(
        op.init_FeatStruct(root = "Silhouette", rightside="Symbol"), 
        op.init_FeatStruct(root = "Silhouette", rightside="Symbol")
    ) == True

    # Test root not equal
    assert fs._subsumes(
        op.init_FeatStruct(root = "Silhouette", rightside="Symbol"), 
        op.init_FeatStruct(root = "Arrow", rightside="Symbol")
    ) == False

    # Test geeneralisation of leaves
    assert fs._subsumes(
        op.init_FeatStruct(root = "Silhouette", rightside="Silhouette"), 
        op.init_FeatStruct(root = "Silhouette", rightside="Symbol")
    ) == True

    # Test geeneralisation of leaves
    assert fs._subsumes(
        op.init_FeatStruct(root = "Silhouette", rightside="Symbol"), 
        op.init_FeatStruct(root = "Silhouette", rightside="Silhouette")
    ) == False

    # Test geeneralisation of roots
    assert fs._subsumes(
        op.init_FeatStruct(root = "Silhouette", rightside="Silhouette"), 
        op.init_FeatStruct(root = "Symbol", rightside="Symbol")
    ) == True

    # Test geeneralisation of leaves
    assert fs._subsumes(
        op.init_FeatStruct(root = "Symbol", rightside="Symbol"), 
        op.init_FeatStruct(root = "Silhouette", rightside="Silhouette")
    ) == False

    # Test with nested
    fs1 = op.init_FeatStruct(root = "Silhouette", rightside="Silhouette")
    fs2 = op.init_FeatStruct(root = "Symbol", rightside="Symbol")   
    assert fs._subsumes(
        op.init_FeatStruct(root = "Symbol", rightside="Silhouette", leftside = fs1), 
        op.init_FeatStruct(root = "Symbol", rightside="Silhouette", leftside = fs2)
    ) == True

    # Test with reentrances
    fs1 = op.init_FeatStruct(root = "Symbol", rightside="Symbol") 
    assert fs._subsumes(
        op.init_FeatStruct(root = "Symbol", rightside = op.init_FeatStruct(root = "Symbol", middle=fs1), leftside = fs1), 
        op.init_FeatStruct(root = "Symbol", rightside="Symbol", leftside = fs1)
    ) == True

def test__antiunification():
    assert False

