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

def test_find_most_common_sort():
    sorts = {
        "Rightarrow": "Arrow",
        "Leftarrow": "Arrow",
        "Arrow": "Symbol",
        "Silhouette": "Symbol",
        "Symbol": "_",
        "Icon": "_",
        "_": "_"
    }
    assert fs.find_most_common_sort(sorts, "Rightarrow", "Arrow") == "Arrow"
    assert fs.find_most_common_sort(sorts, "Arrow", "Rightarrow") == "Arrow"
    assert fs.find_most_common_sort(sorts, "Rightarrow", "Leftarrow") == "Arrow"
    assert fs.find_most_common_sort(sorts, "Arrow", "Silhouette") == "Symbol"
    assert fs.find_most_common_sort(sorts, "Symbol", "Icon") == "_"

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
    
    assert fs2.subsumes(fs1)
    assert not fs1.subsumes(fs2)

    assert fs1.subsumes(fs1)
    assert fs2.subsumes(fs2)

    # Carpenter 11
    sorts = {"agr": "_", "1st": "_", "sing": "_", "_": "_"}
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

    assert fs1.subsumes(fs2)
    assert not fs2.subsumes(fs1)

    # Carpenter 12
    sorts = {"sign": "phrase", "agr": "_", "phrase": "_", "1st": "_", "sing": "_", "_": "_"}
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

    assert fs1.subsumes(fs2)
    assert not fs2.subsumes(fs1)

    # Carpenter 13
    sorts = {"sign": "_", "agr": "_", "1st": "_", "_": "_"}
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

    assert fs1.subsumes(fs2)
    assert not fs2.subsumes(fs1)

    # Carpenter 14
    sorts = {"prop": "_", "_": "_"}
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

    assert fs1.subsumes(fs2)
    assert not fs2.subsumes(fs1)

    # Carpenter 15
    sorts = {"false": "_", "_": "_"}
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

    assert fs1.subsumes(fs2)
    assert not fs2.subsumes(fs1)

    # Carpenter 16
    sorts = {"agr": "_", "sign": "_", "1st": "_", "_": "_"}
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

    assert not fs1.subsumes(fs2)
    assert not fs2.subsumes(fs1)

def test_alphabetic_variant():
    sorts = {"sign": "_", "agr": "_", "1st": "_", "_": "_"}
    feat = ["SUBJ", "PERS", "PRED"]
    nodes = ["Q1", "Q2", "Q3", "Q4", "Q5"]
    root = "Q1"
    typing_func = {"Q1": "sign", "Q2": "agr", "Q3": "agr", "Q4": "1st", "Q5": "1st"}
    trans_func = {("SUBJ", "Q1"): "Q2", ("PRED", "Q1"): "Q3", ("PERS", "Q2"): "Q4", ("PERS", "Q3"): "Q5"}
    fs1 = fs.FeatureStructure(sorts, feat, nodes, root, typing_func, trans_func)

    sorts = {"sign": "_", "agr": "_", "1st": "_", "_": "_"}
    feat = ["SUBJ", "PERS", "PRED"]
    nodes = ["q1", "q2", "q3", "q4", "q5"]
    root = "q1"
    typing_func = {"q1": "sign", "q2": "agr", "q3": "agr", "q4": "1st", "q5": "1st"}
    trans_func = {("SUBJ", "q1"): "q2", ("PRED", "q1"): "q3", ("PERS", "q2"): "q4", ("PERS", "q3"): "q5"}
    fs2 = fs.FeatureStructure(sorts, feat, nodes, root, typing_func, trans_func)

    assert fs1.alphabetic_variant(fs2)
    assert fs2.alphabetic_variant(fs1)

    # Carpenter 16
    sorts = {"agr": "_", "sign": "_", "1st": "_", "_": "_"}
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
    assert not fs1.alphabetic_variant(fs2)
    assert not fs2.alphabetic_variant(fs1)   

def test_antiunify():
    # Carpenter 11
    sorts = {"agr": "_", "1st": "_", "sing": "_", "_": "_"}
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

    assert fs1.alphabetic_variant(fs1.antiunify(fs2))
    assert fs1.alphabetic_variant(fs2.antiunify(fs1))
    assert not fs2.alphabetic_variant(fs1.antiunify(fs2))

    # Carpenter 12
    sorts = {"sign": "phrase", "agr": "_", "phrase": "_", "1st": "_", "sing": "_", "_": "_"}
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

    assert fs1.alphabetic_variant(fs1.antiunify(fs2))
    assert fs1.alphabetic_variant(fs2.antiunify(fs1))
    assert not fs2.alphabetic_variant(fs1.antiunify(fs2))

    # Carpenter 13
    sorts = {"sign": "_", "agr": "_", "1st": "_", "_": "_"}
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

    assert fs1.alphabetic_variant(fs1.antiunify(fs2))
    assert fs1.alphabetic_variant(fs2.antiunify(fs1))
    assert not fs2.alphabetic_variant(fs1.antiunify(fs2))

    # Carpenter 14
    sorts = {"prop": "_", "_": "_"}
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

    assert fs1.alphabetic_variant(fs1.antiunify(fs2))
    assert fs1.alphabetic_variant(fs2.antiunify(fs1))
    assert not fs2.alphabetic_variant(fs1.antiunify(fs2))

    # Carpenter 15
    sorts = {"false": "_", "_": "_"}
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

    assert fs1.alphabetic_variant(fs1.antiunify(fs2))
    assert fs1.alphabetic_variant(fs2.antiunify(fs1))
    assert not fs2.alphabetic_variant(fs1.antiunify(fs2))

    # Own example
    sorts = {
        "A": "_",
        "B": "_",
        "b": "B",
        "C": "_",
        "D": "_",
        "E": "_",
        "e": "E",
        "F": "_",
        "G": "_",
        "_": "_"
    }
    feat = ["f0", "f1", "f2", "f3", "f4", "f5", "f6", "f7"]
    nodes = ["A", "B", "C", "D", "E", "G"]
    root = "A"
    typing_func = {
        "A": "A",
        "B": "B",
        "C": "C",
        "D": "D",
        "E": "E",
        "G": "G"
    }
    trans_func = {
        ("f1", "A"): "B",
        ("f2", "A"): "C",        
        ("f3", "B"): "G", 
        ("f4", "C"): "D",  
        ("f5", "C"): "E",    
        ("f6", "E"): "E", 
        ("f7", "D"): "D"       
    }
    fs1 = fs.FeatureStructure(sorts, feat, nodes, root, typing_func, trans_func)

    nodes = ["A", "B", "C", "D", "E", "F", "G"]
    typing_func = {
        "A": "A",
        "B": "b",
        "C": "C",
        "D": "D",
        "E": "e",
        "F": "F",
        "G": "G"
    }
    trans_func = {
        ("f1", "A"): "B",
        ("f2", "A"): "C",        
        ("f0", "B"): "F", 
        ("f4", "C"): "D",  
        ("f5", "C"): "E",    
        ("f6", "E"): "E", 
        ("f7", "D"): "G"       
    }
    fs2 = fs.FeatureStructure(sorts, feat, nodes, root, typing_func, trans_func)


    nodes = ["A", "B", "C", "D", "E", "G"]
    typing_func = {
        "A": "A",
        "B": "B",
        "C": "C",
        "D": "D",
        "E": "E",
        "G": "_"
    }
    trans_func = {
        ("f1", "A"): "B",
        ("f2", "A"): "C",        
        ("f4", "C"): "D",  
        ("f5", "C"): "E",    
        ("f6", "E"): "E", 
        ("f7", "D"): "G"       
    }
    f = fs.FeatureStructure(sorts, feat, nodes, root, typing_func, trans_func)
    assert f.alphabetic_variant(fs1.antiunify(fs2))

def test__sort_generalisation_operator():
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
    trans_func = {
        ("leftside", "Q1"): "Q2",
        ("right", "Q2"): "Q4",        
        ("rightside", "Q1"): "Q3", 
        ("left", "Q3"): "Q4"         
    }
    typing_func = {
        "Q1": "Icon",
        "Q2": "Silhouette",
        "Q3": "Silhouette",
        "Q4": "_"
    }
    fs1 = fs.FeatureStructure(sorts, feat, nodes, root, typing_func, trans_func)

    typing_func = {
        "Q1": "Icon",
        "Q2": "Symbol",
        "Q3": "Silhouette",
        "Q4": "_"
    }
    fs2 = fs.FeatureStructure(sorts, feat, nodes, root, typing_func, trans_func)

    typing_func = {
        "Q1": "Icon",
        "Q2": "Silhouette",
        "Q3": "Symbol",
        "Q4": "_"
    }
    fs3 = fs.FeatureStructure(sorts, feat, nodes, root, typing_func, trans_func)

    
    typing_func = {
        "Q1": "_",
        "Q2": "Silhouette",
        "Q3": "Silhouette",
        "Q4": "_"
    }
    fs4 = fs.FeatureStructure(sorts, feat, nodes, root, typing_func, trans_func)

    gens = fs1._sort_generalisation_operator()
    assert fs2 in gens and fs3 in gens and fs4 in gens

def test__variable_elimination_operator():
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
    trans_func = {
        ("leftside", "Q1"): "Q2",
        ("right", "Q2"): "Q4",        
        ("rightside", "Q1"): "Q3", 
        ("left", "Q3"): "Q4"         
    }
    typing_func = {
        "Q1": "Icon",
        "Q2": "Silhouette",
        "Q3": "Silhouette",
        "Q4": "_"
    }
    fs1 = fs.FeatureStructure(sorts, feat, nodes, root, typing_func, trans_func)

    nodes = ["Q1", "Q2", "Q3"]
    typing_func = {
        "Q1": "Icon",
        "Q2": "Silhouette",
        "Q3": "Silhouette"
    }
    trans_func = {
        ("leftside", "Q1"): "Q2",      
        ("rightside", "Q1"): "Q3"       
    }
    fs2 = fs.FeatureStructure(sorts, feat, nodes, root, typing_func, trans_func)

    assert fs1._variable_elimination_operator()[0] == fs2

def test__variable_equality_elimination_operator():
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
    trans_func = {
        ("leftside", "Q1"): "Q2",
        ("right", "Q2"): "Q4",        
        ("rightside", "Q1"): "Q3", 
        ("left", "Q3"): "Q4"         
    }
    typing_func = {
        "Q1": "Icon",
        "Q2": "Silhouette",
        "Q3": "Silhouette",
        "Q4": "_"
    }
    fs1 = fs.FeatureStructure(sorts, feat, nodes, root, typing_func, trans_func)

    nodes = ["Q1", "Q2", "Q3", "Q4", "Q5"]
    typing_func = {
        "Q1": "Icon",
        "Q2": "Silhouette",
        "Q3": "Silhouette",
        "Q4": "_",
        "Q5": "_"
    }
    trans_func = {
        ("leftside", "Q1"): "Q2",    
        ("right", "Q2"): "Q4",    
        ("rightside", "Q1"): "Q3",    
        ("left", "Q3"): "Q5"     
    }
    fs2 = fs.FeatureStructure(sorts, feat, nodes, root, typing_func, trans_func)

    gens = fs1._variable_equality_elimination_operator()
    assert fs2.alphabetic_variant(gens[0]) and fs2.alphabetic_variant(gens[1])

    feat = ["leftside", "rightside", "left", "right", "mid"]
    nodes = ["Q1", "Q2", "Q3", "Q4"]
    trans_func = {
        ("leftside", "Q1"): "Q2",
        ("right", "Q2"): "Q4",        
        ("rightside", "Q1"): "Q3", 
        ("left", "Q3"): "Q4",
        ("mid", "Q4"): "Q1"        
    }
    typing_func = {
        "Q1": "Icon",
        "Q2": "Silhouette",
        "Q3": "Silhouette",
        "Q4": "_"
    }
    fs1 = fs.FeatureStructure(sorts, feat, nodes, root, typing_func, trans_func)

    nodes = ["Q1", "Q2", "Q3", "Q4", "Q5"]
    typing_func = {
        "Q1": "Icon",
        "Q2": "Silhouette",
        "Q3": "Silhouette",
        "Q4": "_",
        "Q5": "Icon"
    }
    trans_func = {
        ("leftside", "Q1"): "Q2",    
        ("right", "Q2"): "Q4",    
        ("rightside", "Q1"): "Q3",    
        ("left", "Q3"): "Q4",
        ("mid", "Q4"): "Q5",
        ("leftside", "Q5"): "Q2",   
        ("rightside", "Q5"): "Q3"
    }
    fs2 = fs.FeatureStructure(sorts, feat, nodes, root, typing_func, trans_func)

    gens = fs1._variable_equality_elimination_operator()
    assert fs2.alphabetic_variant(gens[2])

    nodes = ["Q1", "Q2", "Q3", "Q4", "Q5"]
    typing_func = {
        "Q1": "Icon",
        "Q2": "Silhouette",
        "Q3": "Silhouette",
        "Q4": "_",
        "Q5": "Icon"
    }
    trans_func = {
        ("leftside", "Q1"): "Q2",    
        ("right", "Q2"): "Q4",    
        ("rightside", "Q1"): "Q3",    
        ("left", "Q3"): "Q4",
        ("mid", "Q4"): "Q5"
    }
    fs2 = fs.FeatureStructure(sorts, feat, nodes, root, typing_func, trans_func)

    gens = fs1._variable_equality_elimination_operator(looping=False)
    assert fs2.alphabetic_variant(gens[2])

