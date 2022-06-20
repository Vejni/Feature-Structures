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
      
    def pullback(self, spec1, spec2, f1):
        if f1 is None:
            s1 = dict(zip(spec1.sorts, spec1.sorts))
            p1 = {p.split(":")[0] : p.split(":")[0] for p in spec1.preds}
            o1 = {op.split(":")[0] : op.split(":")[0] for op in spec1.ops}
            f1 = (s1, p1, o1)
        return spec1.intersect(spec2, f1)
    
    def pushout(self, span):
        return [span.csp1, span.csp_gen.disjoint_union(span.csp1, span.csp2, span.f1, span.f2), span.csp2]
    
    def get_csp_gen(self, spec1, spec2):
        return self.pullback(spec1, spec2, None)

    def is_monic(self, spec1, spec2, f):
        pass
    
    def is_epic(self, spec1, spec2, f):
        pass

    def restrict(self, f, spec):
        morph_sorts, morph_preds, morph_ops = {}, {}, {}
        for k, v in f[0].items():
            if k in spec.sorts:
                morph_sorts[k] = v
        for k, v in f[1].items():
            if k in [p.split(":")[0] for p in spec.preds]:
                morph_preds[k] = v
        for k, v in f[2].items():
            if k in [o.split(":")[0] for o in spec.ops]:
                morph_ops[k] = v
        return (morph_sorts, morph_preds, morph_ops)

    def amalgamate(self, span):
        if span.csp1.name == span.f1["domain"]:
            span.f1, span.f2 = span.csp_gen.get_morphisms(span.f1), span.csp_gen.get_morphisms(span.f2)
        else:
            span.f2, span.f1 = span.csp_gen.get_morphisms(span.f1), span.csp_gen.get_morphisms(span.f2)
        return super().amalgamate(span)



if __name__ == "__main__":
    csp1 = CASLSpecification()
    csp1.read_from_file("CASL Specifications\specs\I.txt")

    csp2 = CASLSpecification()
    csp2.read_from_file("CASL Specifications\specs\J.txt")
    
    gen = CASLSpecification()
    gen.read_from_file("CASL Specifications\specs\G.txt")

    span = Span(csp1, csp2, gen.f1, gen.f2, gen)

    casl = CASLSpecificationCategory()
    casl.amalgamate(span)
