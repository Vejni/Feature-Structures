import sys
# setting path
sys.path.append('../Amalgamation')
from amalgam import Category

import operators as op

class FeatureTerm(Category): 
    def __init__(self, sorts, ontology):
        self.sorts = sorts
        self.ontology = ontology
        super().__init__()

    def generalization_step(self, fs):
        return op.gen_step(fs, self.sorts)
      
    def pullback(self, fs, fs_gen):
        return self._antiunification(fs, fs_gen)
    
    def get_csp_gen(self, fs1, fs2):
        return self._antiunification(fs1, fs2)

    def amalgamate(self, fs1, fs2):
        return super().amalgamate(fs1, fs2)
    
    def _root_check(self, fs1, fs2):
        return set([fs.root for fs in fs1.walk()]) == set([fs.root for fs in fs2.walk()])

    def _most_general_sort(self, fs):
        # Checks if fs is already most general with sort generalisation
        root_sorts = [f.root not in self.sorts for f in fs.walk()]
        leaf_sorts = [p[:-1] not in self.sorts for p in op.get_all_paths(fs, only_leaves=True)]
        return all(root_sorts + leaf_sorts)

    def _subsumes(self, fs1, fs2):
        # default subsumes: Return True if self subsumes other. 
        # I.e., return true If unifying self with other would result in a feature structure equal to other.
        if fs2.subsumes(fs1) and self._root_check(fs1, fs2):
            return True

        # Initialise Queue
        to_gen = [fs1]
        while bool(to_gen):
            # Dequeue
            g, *to_gen = to_gen 
            sort_gens = op.get_all_sort_generalizations(g, self.sorts)

            # Check if the generalisation subsumes the feature struct
            for g in sort_gens:
                if fs2.subsumes(g) and self._root_check(g, fs2):
                    return True
                
                # if g not most general
                if not self._most_general_sort(g):
                    # Enqueue
                    to_gen.append(g)
        return False

    def _antiunification(self, fs1, fs2):
        # There should be a simpler way for this
        # Get all value paths (+ some extra)
        fs1_paths = op.get_all_paths(fs1)
        fs2_paths = op.get_all_paths(fs2)

        # Get common paths
        fs_paths = []
        for p1 in fs1_paths:
            for p2 in fs2_paths:
                if (p1 == p2) and (len(p1) > 1):
                    fs_paths.append(p1)

        # Could try to add leftovers here

        # Remove any duplicates
        fs_paths = set(fs_paths)

        # Create the antiunificated feature structure from common paths
        fs = op.FeatStruct()
        for p in fs_paths:
            fs[p[:-1]] = p[-1]
        return fs


if __name__ == "__main__":
    icon1 = op.init_FeatStruct(root = "icon", leftside = op.init_FeatStruct(root = "Silhouette", right = "Rightarrow"), rightside="Silhouette")
    icon2 = op.init_FeatStruct(root = "icon", rightside = op.init_FeatStruct(root = "Silhouette", left = "Leftarrow"), leftside="Silhouette")

    sorts = {
        "Rightarrow": "Arrow",
        "Leftarrow": "Arrow",
        "Arrow": "Symbol",
        "Silhouette": "Symbol"
    }

    ontology = {
        ("icon", "leftside") : "Symbol",
        ("icon", "rightside") : "Symbol",
        ("Symbol", "leftside") : "Symbol",
        ("Symbol", "rightside") : "Symbol"
    }

    fs1 =  op.init_FeatStruct(root = "Silhouette", rightside = op.init_FeatStruct(root = "Symbol", rightside="Symbol"))
    fs2 =  op.init_FeatStruct(root = "Silhouette", rightside="Symbol")
    fs = FeatureTerm(sorts, ontology)
    print(fs._subsumes(fs1, fs2))