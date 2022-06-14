from fileinput import filename
import sys
from casl_specifications import CASLSpecification
# setting path
sys.path.append('../Amalgamation')
from amalgam import Category, Span


class CASLSpecificationCategory(Category): 
    def __init__(self):
        super().__init__()

    def generalization_step(self):
        return self.axiom_elimination_operator()
      
    def pullback(self, spec):
        return self.intersect(spec)
    
    def pushout(self, spec):
        return self.disjoint_union(spec)
    
    def get_csp_gen(self, spec):
        return self.intersect(spec)

    def reduce(self):
        return

    def reduce_minimal(self):
        return

    def rename(self):
        return

    def amalgamate(self, s1, s2, s_gen):
        return super().amalgamate(s1, s2, s_gen)




if __name__ == "__main__":
    print("Hello")
