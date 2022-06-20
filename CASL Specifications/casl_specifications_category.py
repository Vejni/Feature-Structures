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
      
    def pullback(self, spec1, spec2):
        return spec1.intersect(spec2)
    
    def pushout(self, span):
        return [span.csp1, span.csp_gen.disjoint_unify(span.csp1, span.csp2, span.f1, span.f2), span.csp2]
    
    def get_csp_gen(self, spec):
        return self.intersect(spec)

    def is_monic (self, spec1, spec2):
        return spec1.subsumes(spec2) or spec2.subsumes(spec1)
    
    def is_epic(self, spec1, spec2):
          return spec1.subsumes(spec2) or spec2.subsumes(spec1)

    def amalgamate(self, span):
        return super().amalgamate(span)



if __name__ == "__main__":
    csp1 = CASLSpecification()
    csp1.read_from_file("CASL Specifications\specs\I.txt")

    csp2 = CASLSpecification()
    csp2.read_from_file("CASL Specifications\specs\J.txt")
    
    gen = CASLSpecification()
    gen.read_from_file("CASL Specifications\specs\G.txt")

    span = Span(csp1, csp2, gen, gen.f1, gen.f2)

    casl = CASLSpecificationCategory()
    casl.amalgamate(span)
