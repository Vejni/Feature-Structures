import pytest
import feature_structure as fs

def test_sort_leq():
    sorts = {
        "Rightarrow": "Arrow",
        "Leftarrow": "Arrow",
        "Arrow": "Symbol",
        "Silhouette": "Symbol",
        "Symbol": "_",
        "Icon": "_",
        "_": "_"
    }

    assert fs.sort_leq(sorts, "Arrow", "Rightarrow")
    assert not fs.sort_leq(sorts, "Rightarrow", "Arrow")

    assert fs.sort_leq(sorts, "_", "Rightarrow")
    assert not fs.sort_leq(sorts, "Rightarrow", "_")

    assert not fs.sort_leq(sorts, "Icon", "Symbol")
    assert not fs.sort_leq(sorts, "foo", "bar")

    assert fs.sort_leq(sorts, "Rightarrow", "Rightarrow")
    assert fs.sort_leq(sorts, "Arrow", "Arrow")
    assert fs.sort_leq(sorts, "_", "_")

def test_subsumes():
    # Own example
    sorts = {
        "Rightarrow": "Arrow",
        "Leftarrow": "Arrow",
        "Arrow": "Symbol",
        "Silhouette": "Symbol",
        "Symbol": "_",
        "Icon": "_",
        "_": "_"
    }
    feat = ["leftside", "rightside", "left", "right"]
    nodes = ["Q1", "Q2", "Q3", "Q4"]
    root = "Q1"
    typing_func = {
        "Q1": "Icon",
        "Q2": "Silhouette",
        "Q3": "Silhouette",
        "Q4": "Arrow"
    }
    trans_func = {
        ("leftside", "Q1"): "Q2",
        ("right", "Q2"): "Q4",        
        ("rightside", "Q1"): "Q3", 
        ("left", "Q3"): "Q4"         
    }
    fs1 = fs.FeatureStructure(sorts, feat, nodes, root, typing_func, trans_func)

    
    typing_func = {
        "Q1": "Icon",
        "Q2": "Symbol",
        "Q3": "Silhouette",
        "Q4": "Arrow"
    }
    fs2 = fs.FeatureStructure(sorts, feat, nodes, root, typing_func, trans_func)
    
    assert fs2.subsumes(fs1, sorts)
    assert not fs1.subsumes(fs2, sorts)

    assert fs1.subsumes(fs1, sorts)
    assert fs2.subsumes(fs2, sorts)

    # Carpenter 11
    sorts = {"agr": "_", "1st": "_", "sing": "_"}
    feat = ["PERS", "NUM"]
    nodes = ["Q1", "Q2"]
    root = "Q1"
    typing_func = {"Q1": "agr", "Q2": "1st"}
    trans_func = {("PERS", "Q1"): "Q2"}
    fs1 = fs.FeatureStructure(sorts, feat, nodes, root, typing_func, trans_func)

    nodes = ["Q1", "Q2", "Q3"]
    typing_func = {"Q1": "agr", "Q2": "1st", "Q3": "sing"}
    trans_func = {("PERS", "Q1"): "Q2", ("NUM", "Q1"): "Q3"}
    fs2 = fs.FeatureStructure(sorts, feat, nodes, root, typing_func, trans_func)

    assert fs1.subsumes(fs2, sorts)
    assert not fs2.subsumes(fs1, sorts)

    # Carpenter 12
    sorts = {"sign": "phrase", "agr": "_", "phrase": "_", "1st": "_", "sing": "_"}
    feat = ["AGR", "PERS", "NUM"]
    nodes = ["Q1", "Q2", "Q3"]
    root = "Q1"
    typing_func = {"Q1": "sign", "Q2": "agr", "Q3": "1st"}
    trans_func = {("AGR", "Q1"): "Q2", ("PERS", "Q2"): "Q3"}
    fs1 = fs.FeatureStructure(sorts, feat, nodes, root, typing_func, trans_func)

    nodes = ["Q1", "Q2", "Q3", "Q4"]
    typing_func = {"Q1": "sign", "Q2": "agr", "Q3": "1st", "Q4": "sing"}
    trans_func = {("AGR", "Q1"): "Q2", ("PERS", "Q2"): "Q3", ("NUM", "Q2"): "Q4"}
    fs2 = fs.FeatureStructure(sorts, feat, nodes, root, typing_func, trans_func)

    assert fs1.subsumes(fs2, sorts)
    assert not fs2.subsumes(fs1, sorts)

    # Carpenter 13
    sorts = {"sign": "_", "agr": "_", "1st": "_"}
    feat = ["SUBJ", "PERS", "PRED"]
    nodes = ["Q1", "Q2", "Q3", "Q4", "Q5"]
    root = "Q1"
    typing_func = {"Q1": "sign", "Q2": "agr", "Q3": "agr", "Q4": "1st", "Q5": "1st"}
    trans_func = {("SUBJ", "Q1"): "Q2", ("PRED", "Q1"): "Q3", ("PERS", "Q2"): "Q4", ("PERS", "Q3"): "Q5"}
    fs1 = fs.FeatureStructure(sorts, feat, nodes, root, typing_func, trans_func)

    nodes = ["Q1", "Q2", "Q3"]
    typing_func = {"Q1": "sign", "Q2": "agr", "Q3": "1st"}
    trans_func = {("PRED", "Q1"): "Q2", ("SUBJ", "Q1"): "Q2", ("PERS", "Q2"): "Q3"}
    fs2 = fs.FeatureStructure(sorts, feat, nodes, root, typing_func, trans_func)

    assert fs1.subsumes(fs2, sorts)
    assert not fs2.subsumes(fs1, sorts)

    # Carpenter 14
    sorts = {"prop": "_"}
    feat = ["ARG1"]
    nodes = ["Q1", "Q2", "Q3"]
    typing_func = {"Q1": "prop", "Q2": "prop", "Q3": "prop"}
    trans_func = {("ARG1", "Q1"): "Q2", ("ARG1", "Q2"): "Q3"}
    root = "Q1"
    fs1 = fs.FeatureStructure(sorts, feat, nodes, root, typing_func, trans_func)

    nodes = ["Q"]
    root = "Q"
    typing_func = {"Q": "prop"}
    trans_func = {("ARG1", "Q"): "Q"}
    fs2 = fs.FeatureStructure(sorts, feat, nodes, root, typing_func, trans_func)

    assert fs1.subsumes(fs2, sorts)
    assert not fs2.subsumes(fs1, sorts)

    # Carpenter 15
    sorts = {"false": "_"}
    feat = ["ARG"]
    nodes = ["Q1", "Q2"]
    typing_func = {"Q1": "false", "Q2": "false"}
    trans_func = {("ARG", "Q1"): "Q2", ("ARG", "Q2"): "Q2"}
    root = "Q1"
    fs1 = fs.FeatureStructure(sorts, feat, nodes, root, typing_func, trans_func)

    nodes = ["Q"]
    root = "Q"
    typing_func = {"Q": "false"}
    trans_func = {("ARG", "Q"): "Q"}
    fs2 = fs.FeatureStructure(sorts, feat, nodes, root, typing_func, trans_func)

    assert fs1.subsumes(fs2, sorts)
    assert not fs2.subsumes(fs1, sorts)

    # Carpenter 16
    sorts = {"agr": "_", "sign": "_", "1st": "_"}
    feat = ["AGR", "PERS"]
    nodes = ["Q1", "Q2"]
    typing_func = {"Q1": "agr", "Q2": "1st"}
    trans_func = {("PERS", "Q1"): "Q2"}
    root = "Q1"
    fs1 = fs.FeatureStructure(sorts, feat, nodes, root, typing_func, trans_func)

    nodes = ["Q1", "Q2", "Q3"]
    root = "Q1"
    typing_func = {"Q1": "sign", "Q2": "agr", "Q3": "1st"}
    trans_func = {("AGR", "Q1"): "Q2", ("PERS", "Q2"): "Q3"}
    fs2 = fs.FeatureStructure(sorts, feat, nodes, root, typing_func, trans_func)

    assert not fs1.subsumes(fs2, sorts)
    assert not fs2.subsumes(fs1, sorts)

