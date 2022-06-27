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
    sorts1 = {
        "Rightarrow": "Arrow",
        "Leftarrow": "Arrow",
        "Arrow": "Symbol",
        "Silhouette": "Symbol",
        "Symbol": "_",
        "Icon": "_",
        "_": "_"
    }
    feat1 = ["leftside", "rightside", "left", "right"]
    nodes1 = ["Q1", "Q2", "Q3", "Q4"]
    root1 = "Q1"
    typing_func1 = {
        "Q1": "Icon",
        "Q2": "Silhouette",
        "Q3": "Silhouette",
        "Q4": "Arrow"
    }
    trans_func1 = {
        ("leftside", "Q1"): "Q2",
        ("right", "Q2"): "Q4",        
        ("rightside", "Q1"): "Q3", 
        ("left", "Q3"): "Q4"         
    }
    fs1 = fs.FeatureStructure(sorts1, feat1, nodes1, root1, typing_func1, trans_func1)

    
    sorts2 = {
        "RIGHTARROW": "ARROW",
        "LEFTARROW": "ARROW",
        "ARROW": "SYMBOL",
        "SILHOUETTE": "SYMBOL",
        "SYMBOL": "_",
        "ICON": "_",
        "_": "_"
    }
    feat2 = ["LEFTSIDE", "RIGHTSIDE", "LEFT", "RIGHT", "MID"]
    nodes2 = ["Q1", "Q2", "Q3", "Q4", "Q5"]
    root2 = "Q1"
    typing_func2 = {
        "Q1": "ICON",
        "Q2": "SILHOUETTE",
        "Q3": "SILHOUETTE",
        "Q4": "ARROW",
        "Q5": "ICON"
    }
    trans_func2 = {
        ("LEFTSIDE", "Q1"): "Q2",
        ("RIGHT", "Q2"): "Q4",        
        ("RIGHTSIDE", "Q1"): "Q3", 
        ("LEFT", "Q3"): "Q4",
        ("MID", "Q4"): "Q5"
    }
    fs2 = fs.FeatureStructure(sorts2, feat2, nodes2, root2, typing_func2, trans_func2)
    
    morph_f = dict(zip(feat1, feat2))
    morph_t = dict(zip(sorts1.keys(), sorts2.keys()))

    assert fs1.subsumes(fs2, (morph_f, morph_t))
    assert not fs2.subsumes(fs1, (morph_f, morph_t))

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

    morph_f = dict(zip(feat, feat))
    morph_t = dict(zip(sorts.keys(), sorts.keys()))

    assert fs1.subsumes(fs2, (morph_f, morph_t))
    assert not fs2.subsumes(fs1, (morph_f, morph_t))

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

    morph_f = dict(zip(feat, feat))
    morph_t = dict(zip(sorts.keys(), sorts.keys()))

    assert fs1.subsumes(fs2, (morph_f, morph_t))
    assert not fs2.subsumes(fs1, (morph_f, morph_t))

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

    morph_f = dict(zip(feat, feat))
    morph_t = dict(zip(sorts.keys(), sorts.keys()))

    assert fs1.subsumes(fs2, (morph_f, morph_t))
    assert not fs2.subsumes(fs1, (morph_f, morph_t))

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

    morph_f = dict(zip(feat, feat))
    morph_t = dict(zip(sorts.keys(), sorts.keys()))

    assert fs1.subsumes(fs2, (morph_f, morph_t))
    assert not fs2.subsumes(fs1, (morph_f, morph_t))

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

    morph_f = dict(zip(feat, feat))
    morph_t = dict(zip(sorts.keys(), sorts.keys()))

    assert fs1.subsumes(fs2, (morph_f, morph_t))
    assert not fs2.subsumes(fs1, (morph_f, morph_t))

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

    morph_f = dict(zip(feat, feat))
    morph_t = dict(zip(sorts.keys(), sorts.keys()))

    assert not fs1.subsumes(fs2, (morph_f, morph_t))
    assert not fs2.subsumes(fs1, (morph_f, morph_t))

def test_subsumes_monic():
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

    morph_f = dict(zip(feat, feat))
    morph_t = dict(zip(sorts.keys(), sorts.keys()))

    assert fs1.subsumes_monic(fs2, (morph_f, morph_t))
    assert fs2.subsumes_monic(fs2, (morph_f, morph_t))
    assert fs1.subsumes_monic(fs1, (morph_f, morph_t))

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

    morph_f = dict(zip(feat, feat))
    morph_t = dict(zip(sorts.keys(), sorts.keys()))

    assert not fs1.subsumes_monic(fs2, (morph_f, morph_t))
    assert not fs2.subsumes_monic(fs1, (morph_f, morph_t))

def test_subsumes_epic():
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

    morph_f = dict(zip(feat, feat))
    morph_t = dict(zip(sorts.keys(), sorts.keys()))

    assert not fs1.subsumes_epic(fs2, (morph_f, morph_t))
    assert fs2.subsumes_epic(fs2, (morph_f, morph_t))
    assert fs1.subsumes_epic(fs1, (morph_f, morph_t))

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
    
    morph_f = dict(zip(feat, feat))
    morph_t = dict(zip(sorts.keys(), sorts.keys()))
    f = (morph_f, morph_t)
    fs_anti1 = fs1.antiunify(fs2, f)
    fs_anti2 = fs2.antiunify(fs1, f)

    assert fs1.subsumes(fs_anti1, f) and fs_anti1.subsumes(fs1, f)
    assert fs1.subsumes(fs_anti2, f) and fs_anti2.subsumes(fs1, f)
    assert not (fs2.subsumes(fs_anti1, f) and fs_anti1.subsumes(fs2, f))

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

    morph_f = dict(zip(feat, feat))
    morph_t = dict(zip(sorts.keys(), sorts.keys()))
    f = (morph_f, morph_t)
    fs_anti1 = fs1.antiunify(fs2, f)
    fs_anti2 = fs2.antiunify(fs1, f)

    assert fs1.subsumes(fs_anti1, f) and fs_anti1.subsumes(fs1, f)
    assert fs1.subsumes(fs_anti2, f) and fs_anti2.subsumes(fs1, f)
    assert not (fs2.subsumes(fs_anti1, f) and fs_anti1.subsumes(fs2, f))

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

    morph_f = dict(zip(feat, feat))
    morph_t = dict(zip(sorts.keys(), sorts.keys()))
    f = (morph_f, morph_t)
    fs_anti1 = fs1.antiunify(fs2, f)
    fs_anti2 = fs2.antiunify(fs1, f)

    assert fs1.subsumes(fs_anti1, f) and fs_anti1.subsumes(fs1, f)
    assert fs1.subsumes(fs_anti2, f) and fs_anti2.subsumes(fs1, f)
    assert not (fs2.subsumes(fs_anti1, f) and fs_anti1.subsumes(fs2, f))

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

    morph_f = dict(zip(feat, feat))
    morph_t = dict(zip(sorts.keys(), sorts.keys()))
    f = (morph_f, morph_t)
    fs_anti1 = fs1.antiunify(fs2, f)
    fs_anti2 = fs2.antiunify(fs1, f)

    assert fs1.subsumes(fs_anti1, f) and fs_anti1.subsumes(fs1, f)
    assert fs1.subsumes(fs_anti2, f) and fs_anti2.subsumes(fs1, f)
    assert not (fs2.subsumes(fs_anti1, f) and fs_anti1.subsumes(fs2, f))

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

    morph_f = dict(zip(feat, feat))
    morph_t = dict(zip(sorts.keys(), sorts.keys()))
    f = (morph_f, morph_t)
    fs_anti1 = fs1.antiunify(fs2, f)
    fs_anti2 = fs2.antiunify(fs1, f)

    assert fs1.subsumes(fs_anti1, f) and fs_anti1.subsumes(fs1, f)
    assert fs1.subsumes(fs_anti2, f) and fs_anti2.subsumes(fs1, f)
    assert not (fs2.subsumes(fs_anti1, f) and fs_anti1.subsumes(fs2, f))

def test_sort_generalisation_operator():
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

    gens = fs1.sort_generalisation_operator()
    assert fs2 in gens and fs3 in gens and fs4 in gens

def test_node_elimination_operator():
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

    assert fs1.node_elimination_operator()[0] == fs2

def test_node_equality_elimination_operator():
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

    morph_f = dict(zip(feat, feat))
    morph_t = dict(zip(sorts.keys(), sorts.keys()))
    gens = fs1.node_equality_elimination_operator()
    assert fs2.subsumes(gens[0], (morph_f, morph_t)) and gens[0].subsumes(fs2, (morph_f, morph_t))
    assert fs2.subsumes(gens[1], (morph_f, morph_t)) and gens[1].subsumes(fs2, (morph_f, morph_t))

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

    morph_f = dict(zip(feat, feat))
    morph_t = dict(zip(sorts.keys(), sorts.keys()))
    gens = fs1.node_equality_elimination_operator()
    assert fs2.subsumes(gens[2], (morph_f, morph_t)) and gens[2].subsumes(fs2, (morph_f, morph_t))

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

    morph_f = dict(zip(feat, feat))
    morph_t = dict(zip(sorts.keys(), sorts.keys()))
    gens = fs1.node_equality_elimination_operator(looping=False)
    assert fs2.subsumes(gens[2], (morph_f, morph_t)) and gens[2].subsumes(fs2, (morph_f, morph_t))

def test_disjoint_unify():
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
        "Q4": "Rightarrow"
    }
    trans_func = {
        ("leftside", "Q1"): "Q2",
        ("rightside", "Q1"): "Q3",
        ("right", "Q2"): "Q4",
        ("left", "Q3"): "Q4"           
    }
    fs1 = fs.FeatureStructure(sorts, feat, nodes, root, typing_func, trans_func)

    typing_func = {
        "Q1": "Icon",
        "Q2": "Silhouette",
        "Q3": "Silhouette",
        "Q4": "Leftarrow"
    }
    fs2 = fs.FeatureStructure(sorts, feat, nodes, root, typing_func, trans_func)

    typing_func = {
        "Q1": "Icon",
        "Q2": "Silhouette",
        "Q3": "Silhouette",
        "Q4": "Arrow"
    }
    fs0 = fs.FeatureStructure(sorts, feat, nodes, root, typing_func, trans_func)

    sorts = {
        "Rightarrow": "Arrow",
        "Leftarrow": "Arrow",
        "_1_Rightarrow": "Arrow",
        "_2_Leftarrow": "Arrow",
        "Arrow": "Symbol",
        "Silhouette": "Symbol",
        "Symbol": "_",
        "Icon": "_",
        "_": "_"
    }
    feat = ["leftside", "rightside", "_1_left", "_1_right", "_2_left", "_2_right"]
    nodes = ["Q1", "Q2", "Q3", "_1_Q4", "_2_Q4"]
    root = "Q1"
    typing_func = {
        "Q1": "Icon",
        "Q2": "Silhouette",
        "Q3": "Silhouette",
        "_1_Q4": "_1_Rightarrow",
        "_2_Q4": "_2_Leftarrow"
    }
    trans_func = {
        ("leftside", "Q1"): "Q2",
        ("rightside", "Q1"): "Q3",
        ("_1_right", "Q2"): "_1_Q4",
        ("_2_right", "Q2"): "_2_Q4",
        ("_1_left", "Q3"): "_1_Q4",  
        ("_2_left", "Q3"): "_2_Q4"     
    }
    fs_uni = fs.FeatureStructure(sorts, feat, nodes, root, typing_func, trans_func)

    morph_f1 = {
        "leftside": "leftside",
        "rightside": "rightside",
        "left": "_1_left",
        "right": "_1_right"
    }
    morph_t1 = {
        "Rightarrow": "_1_Rightarrow",
        "Leftarrow": "_1_Leftarrow",
        "Arrow": "Arrow",
        "Symbol": "Symbol",
        "Icon": "Icon",
        "Silhouette": "Silhouette",
        "_":"_"
    }
    f1 = (morph_f1, morph_t1)

    morph_f2 = {
        "leftside": "leftside",
        "rightside": "rightside",
        "left": "_2_left",
        "right": "_2_right"
    }
    morph_t2 = {
        "Rightarrow": "_2_Rightarrow",
        "Leftarrow": "_2_Leftarrow",
        "Arrow": "Arrow",
        "Symbol": "Symbol",
        "Icon": "Icon",
        "Silhouette": "Silhouette",
        "_":"_"
    }
    f2 = (morph_f2, morph_t2)

    morph_f = dict(zip(fs_uni.feat, fs_uni.feat))
    morph_t = dict(zip(fs_uni.sorts.keys(), fs_uni.sorts.keys()))
    fs_unif = fs0.disjoint_unify(fs1, fs2, f1, f2)[1]
    assert fs_uni.subsumes(fs_unif, (morph_f, morph_t)) and fs_unif.subsumes(fs_uni, (morph_f, morph_t))
