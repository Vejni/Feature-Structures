from fileinput import filename
import sys
from casl_specification import CASLSpecification
# setting path
sys.path.append('../Amalgamation')
from amalgam import Category, Span


class CASLSpecificationCategory(Category): 
    def __init__(self):
        super().__init__()

    def generalisation_step(self, csp):
        return csp.axiom_elimination_operator()
      
    def pullback(self, spec1, spec2, f1):
        if f1 is None:
            s1 = dict(zip(spec1.sorts, spec1.sorts))
            p1 = {p.split(":")[0] : p.split(":")[0] for p in spec1.preds}
            o1 = {op.split(":")[0] : op.split(":")[0] for op in spec1.ops}
            f1 = (s1, p1, o1)
        return spec1.intersect(spec2, f1)
    
    def pushout(self, span):
        return span.csp_gen.disjoint_union(span.csp1, span.csp2, span.f1, span.f2)
    
    def get_csp_gen(self, spec1, spec2):
        return self.pullback(spec1, spec2, None)

    def terminal(self, csp):
        return len(csp.axioms) == 0

    def subsumes(self, spec1, spec2, f):
        if f is None:
            s1 = dict(zip(spec1.sorts, spec1.sorts))
            p1 = {p.split(":")[0] : p.split(":")[0] for p in spec1.preds}
            o1 = {op.split(":")[0] : op.split(":")[0] for op in spec1.ops}
            f = (s1, p1, o1)
        return spec1.subsumes(spec2, f)

    def variant(self, spec1, spec2):
        return self.subsumes(spec1, spec2) and self.subsumes(spec2, spec1)

    def is_monic(self, spec1, spec2, f=None):
        if f is None:
            s1 = dict(zip(spec1.sorts, spec1.sorts))
            p1 = {p.split(":")[0] : p.split(":")[0] for p in spec1.preds}
            o1 = {op.split(":")[0] : op.split(":")[0] for op in spec1.ops}
            f = (s1, p1, o1)
        else:
            f = self.restrict(f, spec1)

        morph_sorts, morph_preds, morph_ops = f
        
        # Check sorts
        dic_s = {s: False for s in spec2.sorts}
        for s in morph_sorts.values():
            if s not in dic_s.keys() or dic_s[s]:
                return False
            dic_s[s] = True

        # Check preds
        dic_p = {p: False for p in spec2.sorts}
        for p in morph_preds.values():
            if p not in dic_p.keys() or dic_p[p]:
                return False
            dic_p[p] = True

        # Check ops
        dic_o = {o: False for o in spec2.sorts}
        for o in morph_ops.values():
            if o not in dic_o.keys() or dic_o[o]:
                return False
            dic_o[o] = True

        return True

    def is_epic(self, spec1, spec2, f):
        if f is None:
            s1 = dict(zip(spec1.sorts, spec1.sorts))
            p1 = {p.split(":")[0] : p.split(":")[0] for p in spec1.preds}
            o1 = {op.split(":")[0] : op.split(":")[0] for op in spec1.ops}
            f = (s1, p1, o1)
        else:
            f = self.restrict(f, spec1)

        morph_sorts, morph_preds, morph_ops = f
        
        # Check sorts
        for s in spec1.sorts:
            if morph_sorts[s] not in spec2.sorts:
                return False

        # Check preds
        for p in spec1.preds:
            if morph_preds[p] not in spec2.preds:
                return False

        # Check ops
        for o in spec1.ops:
            if morph_ops[o] not in spec2.ops:
                return False

        return True

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

    def get_generalised_amalgams(self, n_gens, span):
        if span.csp1.name == span.f1["domain"]:
            span.f1, span.f2 = span.csp_gen.get_morphisms(span.f1), span.csp_gen.get_morphisms(span.f2)
        else:
            span.f2, span.f1 = span.csp_gen.get_morphisms(span.f1), span.csp_gen.get_morphisms(span.f2)
        return super().get_generalised_amalgams(n_gens, span)



if __name__ == "__main__":
    csp1 = CASLSpecification()
    csp1.read_from_file("CASL Specifications\specs\I.txt")

    csp2 = CASLSpecification()
    csp2.read_from_file("CASL Specifications\specs\J.txt")
    
    gen = CASLSpecification()
    gen.read_from_file("CASL Specifications\specs\G.txt")

    span = Span(csp1, csp2, gen.f1, gen.f2, gen)

    casl = CASLSpecificationCategory()
    casl.amalgamate(span)[1].write_to_file("CASL Specifications\specs\A.txt")
