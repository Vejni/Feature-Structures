from nltk.featstruct import FeatStruct as _FeatStruct
import feature_term_gens as ftgens
import abc

class Category(object):
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def generalization_step(self, csp):
        """Method documentation"""
        return

    @abc.abstractmethod
    def pullback(self, csp, csp_gen):
        """Method documentation"""
        return
    
    def amalgamate(self, csp1, csp2, csp_gen=None):
        # We can compute the generic space for feature terms
        if False: # csp_gen = None
            csp_gen = self.get_csp_gen(csp1, csp2)

        csp0_gen = self.generalization_step(csp_gen)
        csp1_gen = self.generalization_step(csp1)
        csp2_gen = self.generalization_step(csp2)
        csp1_pull = self.pullback(csp1_gen, csp_gen)
        csp2_pull = self.pullback(csp2_gen, csp_gen)

        csp_pull = self.pullback(csp1_pull, csp2_pull)
        csp_blend = self.pullback(csp_pull, csp0_gen)

        return csp_blend

class FeatureTerm(Category): 
    def __init__(self, sorts):
        self.sorts = sorts
        super().__init__()

    def generalization_step(self, fs):
        return ftgens.gen_step(fs, self.sorts)
      
    def pullback(self, fs, fs_gen):
        return self._antiunification(fs, fs_gen)
    
    def get_csp_gen(self, fs1, fs2):
        return self._antiunification(fs1, fs2)

    def amalgamate(self, fs1, fs2):
        return super().amalgamate(fs1, fs2)

    def _antiunification(self, fs1, fs2):
        # There should be a simpler way for this
        # Get all value paths (+ some extra)
        fs1_paths = ftgens.find_all_leaves(fs1) + ftgens.find_all_structs(fs1)
        fs2_paths = ftgens.find_all_leaves(fs2) + ftgens.find_all_structs(fs2)

        # Get common paths
        fs_paths = []
        for p1 in fs1_paths:
            for p2 in fs2_paths:
                if (p1 == p2) and (len(p1) > 1):
                    fs_paths.append(p1)
        fs_paths = set(fs_paths)

        # Create the antiunificated feature structure from common paths
        fs = ftgens.FeatStruct()
        for p in fs_paths:
            fs[p[:-1]] = p[-1]
        return fs


if __name__ == "__main__":
    icon1 = ftgens.FeatStruct(leftside = ftgens.FeatStruct(right = "Rightarrow", root = "Silhouette"), rightside="Silhouette", root = "icon")
    icon2 = ftgens.FeatStruct(rightside = ftgens.FeatStruct(left = "Leftarrow", root = "Silhouette"), leftside="Silhouette", root = "icon")

    sorts = {
        "Rightarrow": "Arrow",
        "Leftarrow": "Arrow",
        "Arrow": "Symbol"
    }

    ft = FeatureTerm(sorts)
    print(ft.amalgamate(icon1, icon2))
