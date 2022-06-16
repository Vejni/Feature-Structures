from fileinput import filename
import sys
from feature_structure import FeatureStructure
# setting path
sys.path.append('../Amalgamation')
from amalgam import Category, Span

class FeatureTermCategory(Category): 
    def __init__(self):
        super().__init__()

    def generalisation_step(self, fs):
        return fs.sort_generalisation_operator() + fs.variable_elimination_operator() + fs.variable_equality_elimination_operator()
      
    def pullback(self, fs1, fs2):
        return fs1.antiunify(fs2)
    
    def pushout(self, fs1, fs2, fs_gen):
        return [fs1, fs_gen.disjoint_unify(fs1, fs2), fs2]
    
    def get_csp_gen(self, fs1, fs2):
        return fs1.antiunify(fs2)

    def rename(self, fs1, f):
        fs1.rename(f)
        return

    def is_monic(self, fs1, fs2):
        return fs1.subsumes(fs2)
    
    def is_epic(self, fs1, fs2):
        return fs1.subsumes(fs2)

    def amalgamate(self, span):
        return super().amalgamate(span)




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

    typing_func = {
        "Q1": "Icon",
        "Q2": "Silhouette",
        "Q3": "Silhouette",
        "Q4": "Arrow"
    }
    fs0 = FeatureStructure(sorts, feat, nodes, root, typing_func, trans_func)
    span = Span(fs1, fs2, fs0.f1, fs0.f2, fs0)    

    ft = FeatureTermCategory()

    span_gen = Span(ft.generalisation_step(fs1)[0], fs2, fs0.f1, fs0.f2, fs0)
    ft.integration_measure(span, span_gen)
    #for i, f in enumerate(ft.generalization_step(fs1)):
    #    f.plot(filename = f"fs{i}.gv")
