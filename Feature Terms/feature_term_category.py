import sys
from feature_structure import FeatureStructure
# setting path
sys.path.append('../Amalgamation')
from amalgam import Category

class FeatureTermCategory(Category): 
    def __init__(self, sorts, feat):
        self.sorts = sorts
        self.feat = feat
        super().__init__()

    def generalization_step(self, fs):
        return fs.sort_generalisation_operator() + fs.variable_elimination_operator() + fs.variable_equality_elimination_operator() + fs.variable_equality_elimination_operator(looping = False)
      
    def pullback(self, fs, fs_gen):
        return fs.antiunify(fs_gen)
    
    def get_csp_gen(self, fs1, fs2):
        return fs1.antiunify(fs2)

    def amalgamate(self, fs1, fs2):
        return super().amalgamate(fs1, fs2)

    def _antiunification(self, fs1, fs2):
        return fs1.antiunify(fs2)



if __name__ == "__main__":
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
    fs1 = FeatureStructure(sorts, feat, nodes, root, typing_func, trans_func)
    
    ft = FeatureTermCategory(sorts, feat)
    for f in ft.generalization_step(fs1):
        print(f)
