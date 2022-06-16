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
    
    def pushout(self, spec1, spec2, spec_gen):
        return [spec1, spec_gen.disjoint_union(spec1, spec2), spec2]
    
    def get_csp_gen(self, spec):
        return self.intersect(spec)

    def rename(self, spec, f):
        spec.rename(f["renamings"])
        return

    def is_monic(self, spec1, spec2):
        return spec1.subsumes(spec2) or spec2.subsumes(spec1)
    
    def is_epic(self, spec1, spec2):
          return spec1.subsumes(spec2) or spec2.subsumes(spec1)

    def amalgamate(self, s1, s2, s_gen):
        if s_gen.f1["domain"] == s1.name:
            span = Span(s1, s2, s_gen.f1, s_gen.f2, s_gen)
        else:
            span = Span(s1, s2, s_gen.f2, s_gen.f1, s_gen)
        return super().amalgamate(span)



if __name__ == "__main__":
    csp1 = CASLSpecification()
    csp1.read_from_file("CASL Specifications\specs\I.txt")

    csp2 = CASLSpecification()
    csp2.read_from_file("CASL Specifications\specs\J.txt")
    
    gen = CASLSpecification()
    gen.read_from_file("CASL Specifications\specs\G.txt")

    casl = CASLSpecificationCategory()
    casl.amalgamate(csp1, csp2, gen)
