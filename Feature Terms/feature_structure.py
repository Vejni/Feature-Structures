
import queue
from pyparsing import empty


def sort_leq(sorts, s1, s2):
    """ Checks if s1 <= s2 in the sort hierarchy, that is if s2 is more specific than s1. """
    if s1 not in sorts.keys() or s2 not in sorts.keys():
        return False

    while s1 != s2 and s2 != "_":
        # Generalise sort of s2
        s2 = sorts[s2]

    if s1 == s2:
        return True
    else:
        return False

def find_most_common_sort(sorts, s1, s2):
    """ Find most specific common sort of s1 and s2, returns bottom if no sort in common """
    while s1 != s2:
        s1 = sorts[s1]
        s2 = sorts[s2]
    return s1



class FeatureStructure:
    def __init__(self, sorts, feat, nodes, root, typing_func, trans_func):
        """
        sorts:          {String: String}:           A dictionary of all possible sorts, including the most general sort, 
                                                    defining the sort hierarchy with key being more specific than value. 
                                                    If sort is already most general its value is "_"
        feat:           [String]:                   A list of possible features.
        nodes:          [String]:                   A list of node names, containing the root node. They are only for indexing, generated nodes will be of the form _Q_i, avoid these names.
        root:           String:                     Name of the root node.
        typing_func     {String: String}:           A dictionary of nodes as keys and sorts as values. 
        trans_func      {(String, String): String}: Transition function with keys as (f, q) where f is feature defined in feat, and q is a node. The values are nodes themselves.
        """
        self.sorts = sorts
        self.feat = feat
        self.nodes = nodes
        self.root = root
        self.typing_func = typing_func
        self.trans_func = trans_func

        # Check invalid structures
        # Test root
        if not root in nodes:
            raise Exception("Root not in nodes, please specify a valid feature structure.")
        
        for q in nodes:
            # Test node types
            if q not in typing_func.keys():
                raise Exception("A node does not have a sort defined, please specify a vlaid feature structure.")
            # Test types
            if not typing_func[q] in sorts.keys():
                raise Exception("A node has invalid sort, please specify a valid feature structure.")
            # Test nodes
            if not isinstance(q, tuple) and q.startswith("_"):
                raise Exception("Generated nodes will start with an underscore '_', avoid using them for node names.")
        
        for (f, q) in trans_func.keys():
            # Test features
            if not f in feat:
                raise Exception("A feature is not in Feat, please specify a valid feature structure.")
            # Test domain of transition
            if not q in nodes:
                raise Exception("A transition starts from a nonexisting node, please specify a valid feature structure.")
            # Test range of transition
            if not trans_func[(f, q)] in nodes:
                raise Exception("A transition leads to a nonexisting node, please specify a valid feature structure.")       
    
    def subsumes(self, fs, sorts):
        """ Checks feature structure subsumption in a BFS manner """

        if not isinstance(fs, FeatureStructure):
            raise Exception("Object not a feature structure.")
    
        queue1 = [self.root]
        queue2 = [fs.root]

        while len(queue1):
            q1, *queue1 = queue1
            q2, *queue2 = queue2      

            if not sort_leq(sorts, self.typing_func[q1], fs.typing_func[q2]):
                return False

            gen1 = [(f, q) for (f, q) in self.trans_func.keys() if q == q1]
            gen2 = [(f, q) for (f, q) in fs.trans_func.keys() if q == q2]

            flag = False
            for (f1, q1) in gen1:
                for (f2, q2) in gen2:
                    if(
                        f1 == f2 and 
                        sort_leq(sorts, self.typing_func[self.trans_func[(f1, q1)]], fs.typing_func[fs.trans_func[(f2, q2)]]) and
                        not (self.trans_func[(f1, q1)] == q1 and fs.trans_func[(f2, q2)] != q2)                  
                    ):
                        flag = True
                        if self.trans_func[(f1, q1)] != q1:
                            queue1.append(self.trans_func[(f1, q1)])
                            queue2.append(fs.trans_func[(f2, q2)])
                        break
                if flag and not (len(set(queue1)) != len(queue1) and len(set(queue2)) == len(queue2)):
                    flag = False
                else:
                    return False
        return True

    def alphabetic_variant(self, fs, sorts):
        """ Checks if two feature structures are alphabetic variants of each other """
        return self.subsumes(fs, sorts) and fs.subsumes(self, sorts)

    def antiunify(self, fs):
        """ Computes the antiunifier as the pair of common nodes """
        root = (self.root, fs.root)
        nodes = [root]
        typing_func, trans_func = {}, {}
        typing_func[root] = find_most_common_sort(self.sorts, self.typing_func[self.root], fs.typing_func[fs.root])

        for q0 in nodes:
            gen1 = [(f, q) for (f, q) in self.trans_func.keys() if q == q0[0]]
            gen2 = [(f, q) for (f, q) in fs.trans_func.keys() if q == q0[1]]

            flag = False
            for (f1, q1) in gen1:
                for (f2, q2) in gen2:
                    if f1 == f2:
                        flag = True
                        node = (self.trans_func[(f1, q1)], fs.trans_func[(f2, q2)])
                        nodes.append(node)
                        typing_func[node] = find_most_common_sort(self.sorts, self.typing_func[self.trans_func[(f1, q1)]], fs.typing_func[fs.trans_func[(f2, q2)]])
                        trans_func[(f1, q0)] = node
                        break
                if flag:
                    flag = False
                else:
                    return False

        return FeatureStructure(self.sorts, self.feat, nodes, root, typing_func, trans_func)


        

        

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

    
    typing_func = {
        "Q1": "Icon",
        "Q2": "Symbol",
        "Q3": "Silhouette",
        "Q4": "Arrow"
    }
    fs2 = FeatureStructure(sorts, feat, nodes, root, typing_func, trans_func)
    print(fs1.antiunify(fs2))