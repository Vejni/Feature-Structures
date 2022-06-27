from fileinput import filename
import sys
from feature_structure import FeatureStructure
# setting path
sys.path.append('../Amalgamation')
from amalgam import Category, Span

class FeatureStructureCategory(Category): 
    def __init__(self):
        super().__init__()

    def generalisation_step(self, fs):
        return fs.sort_generalisation_operator() + fs.node_elimination_operator() + fs.node_equality_elimination_operator()

    def subsumes(self, fs1, fs2, f=None):
        if f is None:
            f = dict(zip(fs1.feat, fs1.feat))
            t = dict(zip(fs1.sorts.keys(), fs1.sorts.keys()))
            f = (f, t)
        return fs1.subsumes(fs2, f)

    def variant(self, fs1, fs2):
        return self.subsumes(fs1, fs2) and self.subsumes(fs2, fs1)

    def pullback(self, fs1, fs2, f1):
        if f1 is None:
            f = dict(zip(fs1.feat, fs1.feat))
            t = dict(zip(fs1.sorts.keys(), fs1.sorts.keys()))
            f1 = (f, t)

        return fs1.antiunify(fs2, f1)
    
    def pushout(self, span):
        return span.csp_gen.disjoint_unify(span.csp1, span.csp2, span.f1, span.f2)

    def terminal(sefl, fs):
        return len(fs.nodes) == 0

    def get_csp_gen(self, fs1, fs2):
        return self.pullback(fs1, fs2, None, None)

    def restrict(self, f, fs):
        feat_morph = {}
        for k, v in f[0].items():
            if k in fs.feat:
                feat_morph[k] = v

        sort_morph = {}
        for k, v in f[1].items():
            if k in fs.sorts.keys():
                sort_morph[k] = v
        return (feat_morph, sort_morph)

    def is_monic(self, fs1, fs2, f=None):
        if f is None:
            f = dict(zip(fs1.feat, fs1.feat))
            t = dict(zip(fs1.sorts.keys(), fs1.sorts.keys()))
            f = (f, t)
        else:
            f = self.restrict(f, fs1)

            # Check morph_f
            dic_f = {f: False for f in fs2.feat}
            for fe in f[0].values():
                if dic_f[fe]:
                    return False
                dic_f[fe] = True

            # Check morph_t
            dic_t = {s: False for s in fs2.sorts.keys()}
            for s in f[1].values():
                if dic_t[s]:
                    return False
                dic_t[s] = True

        # Check subsumption morph       
        return fs1.subsumes_monic(fs2, f)
    
    def is_epic(self, fs1, fs2, f=None):
        if f is None:
            f = dict(zip(fs1.feat, fs1.feat))
            t = dict(zip(fs1.sorts.keys(), fs1.sorts.keys()))
            f = (f, t)
        else:
            f = self.restrict(f, fs1)

        # Check morph_f
        for fe in fs2.feat:
            if not fe in f[0].values():
                return False

        # Check morph_t
        for s in fs2.typing_func.values():
            if not s in f[1].values():
                return False

        # Check subsumption morph
        return fs1.subsumes_epic(fs2, f)

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

    f = dict(zip(feat, feat))
    t = dict(zip(sorts.keys(), sorts.keys()))
    span = Span(fs1, fs2, (f, t), (f, t), fs0)    

    ft = FeatureStructureCategory()
    ft.get_generalised_amalgams(1, span)