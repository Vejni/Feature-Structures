from fileinput import filename
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
        return fs.sort_generalisation_operator() + fs.variable_elimination_operator() + fs.variable_equality_elimination_operator()
      
    def pullback(self, fs, fs_gen):
        return fs.antiunify(fs_gen)
    
    def pushout(self, fs1, fs2, fs_gen, f1, f2):
        if f1 is not None and f2 is not None:
            return fs_gen.disjoint_unify(fs1, fs2, f1[0], f1[1], f2[0], f2[1])
        else:
            return fs_gen.disjoint_unify(fs1, fs2)
    
    def get_csp_gen(self, fs1, fs2):
        return fs1.antiunify(fs2)

    def reduce(self, amalgams):
        results = []
        for fs in amalgams:
            flag = True
            for res in results:
                if fs.alphabetic_variant(res) and fs != res:
                    flag = False
                    break
            if flag:
                results.append(fs)
        return results

    def reduce_minimal(self, amalgams):
        results = []
        for fs in amalgams:
            flag = True
            for res in amalgams:
                if (fs.subsumes(res) and fs != res) or (fs in results):
                    flag = False
                    break
            if flag:
                results.append(fs)
        return results

    def amalgamate(self, fs1, fs2, fs_gen, f1=None, f2=None):
        return super().amalgamate(fs1, fs2, fs_gen, f1, f2)




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
        "Q4": "Rightarrow"
    }
    trans_func = {
        ("leftside", "Q1"): "Q2",
        ("right", "Q2"): "Q4",        
        ("rightside", "Q1"): "Q3", 
        ("left", "Q3"): "Q4"         
    }
    fs1 = FeatureStructure(sorts, feat, nodes, root, typing_func, trans_func)
    
    typing_func = {
        "Q1": "Icon",
        "Q2": "Silhouette",
        "Q3": "Silhouette",
        "Q4": "Leftarrow"
    }
    fs2 = FeatureStructure(sorts, feat, nodes, root, typing_func, trans_func)

    print(fs1.antiunify(fs2))
    typing_func = {
        "Q1": "Icon",
        "Q2": "Silhouette",
        "Q3": "Silhouette",
        "Q4": "Arrow"
    }
    fs0 = FeatureStructure(sorts, feat, nodes, root, typing_func, trans_func)
    
    ft = FeatureTermCategory(sorts, feat)
    ft.amalgamate(fs1, fs2, fs0)
    #for i, f in enumerate(ft.generalization_step(fs1)):
    #    f.plot(filename = f"fs{i}.gv")
