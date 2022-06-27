import abc
import sys

class Span:
    def __init__(self, csp1, csp2, f1, f2, csp_gen=None):
        self.csp1 = csp1
        self.csp2 = csp2
        self.f1 = f1
        self.f2 = f2
        self.csp_gen = csp_gen

    def __eq__(self, span):
        return (((self.csp1 == span.csp1) and (self.csp2 == span.csp2)) or ((self.csp2 == span.csp1) and (self.csp1 == span.csp2))) and (self.csp_gen == span.csp_gen)

class Category(object):
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def generalisation_step(self, csp):
        """ 
        Method to return all generalisation steps of a given object 
        Input: Object of the representation formalisms, which should be generated.
        Output: List of generalisations of the object, itself should not be included.
        """
        return

    @abc.abstractmethod
    def pullback(self, csp1, csp2, f1):
        """ 
        Computation of the pullback operation in the representation formalism.
        Inputs: Two objects of the category csp1, csp2, and morphism f1, mapping the types of csp1 to the types of csp2.
        Output: Pullback object of the representation formalism.
        """
        return
    
    @abc.abstractmethod
    def pushout(self, span):
        """ 
        Computation of the psuhout operation in the representation formalism.
        Inputs: Span object.
        Output: Tuple as [f1, o, f2], where o is the pushout object, and f1, f2 are the morphisms from span.csp1, span.csp2 respectively.
        """
        return

    @abc.abstractmethod
    def is_monic(self, csp1, csp2, f):
        """ 
        Determines when the morphism between two objects is monic.
        Inputs: Two objects of the category csp1 (domain), csp2 (codomain), and morphism f1.
        Output: True/False.
        """
        return

    @abc.abstractmethod
    def is_epic(self, csp1, csp2, f):
        """ 
        Determines when the morphism between two objects is epic.
        Inputs: Two objects of the category csp1 (domain), csp2 (codomain), and morphism f1.
        Output: True/False.
        """
        return

    @abc.abstractmethod
    def restrict(self, csp, f):
        """ 
        Compute the restriction of morphism f, on the domain csp.
        Inputs: Object csp of the representation formalism, and morphism f to be restricted.
        Output: Morphism f restricted to, representation depends on the formalism.
        """
        return

    @abc.abstractmethod
    def subsumes(self, csp1, csp2):
        """ 
        Determines when two objects have a subsumption relation, that is csp1 subsumes csp2.
        Inputs: Two objects of the category csp1 (domain), csp2 (codomain).
        Output: True/False.
        """
        return

    @abc.abstractmethod
    def variant(self, csp1, csp2):
        """ 
        Determines when two objects have are isomorphic variants.
        Inputs: Two objects of the category csp1, csp2.
        Output: True/False.
        """
        return

    @abc.abstractmethod
    def terminal(self, csp):
        """ 
        Determines when the object csp represents the terminal object of the representation formalism.
        Inputs: Object csp of the representation formalism.
        Output: True/False.
        """
        return

    def reduce_minimal(self, amalgams):
        """ Reduces the given objects to the ones that are not subsumed by any other in the list """
        results = []
        for csp in amalgams:
            flag = True
            for res in amalgams:
                if (self.subsumes(csp, res) and csp != res) or (csp in results):
                    flag = False
                    break
            if flag:
                results.append(csp)
        return results

    def reduce(self, amalgams):
        """ Reduces the given objects to the ones that are not isomorphic """
        results = []
        for csp in amalgams:
            flag = True
            for res in results:
                if self.variant(csp, res) and csp != res:
                    flag = False
                    break
            if flag:
                results.append(csp)
        return results

    def spans_variant(self, span1, span2):
        """ checks if two spans are alphabetic variants of each other """
        return ((self.variant(span1.csp1, span2.csp1) and self.variant(span1.csp2, span2.csp2)) or (self.variant(span1.csp1, span2.csp2) and self.variant(span1.csp2, span2.csp1))) and self.variant(span1.csp_gen, span2.csp_gen)

    def is_generalisation_of(self, ob1, ob2):
        """ Determine if an object or span is a generalisation of another one """
        if isinstance(ob1, Span) and isinstance(ob2, Span):
            return self.is_monic(ob1.csp1, ob2.csp1) and self.is_monic(ob1.csp_gen, ob2.csp_gen) and self.is_monic(ob1.csp2, ob2.csp2)
        else:
            return self.is_monic(ob1, ob2)

    def get_distance(self, span_to_find, span_ref):
        """ Return the generalisation distance of a span from a given reference span, does so by generating all generalisations until span_to_find is encountered """
        not_found = True
        ind_found = [sys.maxsize, 0, 0]

        gen = [([0, 0, 0], span_ref)]
        while not_found:
            gen = self.get_next_population_of_generalisations(gen)
            for ind, span in gen:
                if sum(ind) < sum(ind_found):
                    if span == span_to_find:
                        not_found = False
                        ind_found = ind
                        break
        return ind_found

    def similarity(self, dist1, dist_com, dist2):
        """ Computes the similarity of two spans given a reference span, it assumes that dist1 and dist2 are from the reference span, and dist_com is the shared distance """
        if isinstance(dist1, list) and isinstance(dist_com, list) and isinstance(dist2, list):
            for i in range(3):
                dist1[i] -= dist_com[i]
                dist2[i] -= dist_com[i]
            return sum(dist_com) / (sum(dist_com) + sum(dist1) + sum(dist2))
        else:
            return dist_com / (dist1 + dist2 - dist_com)

    def _find_maximally_integrated(self, span_ref):
        """ Returns a list of spans which yield a maximally integrated blend and their generalisation distances """
        spans, inds = [], []
        ind_epic = [sys.maxsize, 0, 0]
        gen = [([0, 0, 0], span_ref)]
        while any([sum(g[0]) < sum(ind_epic) for g in gen]):
            gen = self.get_next_population_of_generalisations(gen)
            for ind, span in gen:
                if sum(ind) <= sum(ind_epic):
                    push = self.pushout(span)
                    if self.is_epic(span.csp1, push[1], push[0]) and self.is_epic(span.csp2, push[1], push[2]):
                        ind_epic = ind
                        flag = True
                        for s in spans:
                            if s == span:
                                flag = False
                                break
                        if flag:
                            inds.append(ind)
                            spans.append(span)

        return spans, inds

    def _find_maximally_topologic(self, span_ref):
        """ Returns a list of spans which yield a maximally topologic blend and their generalisation distances """
        spans, inds = [], []
        ind_monic = [sys.maxsize, 0, 0]
        gen = [([0, 0, 0], span_ref)]
        while any([sum(g[0]) < sum(ind_monic) for g in gen]):
            gen = self.get_next_population_of_generalisations(gen)
            for ind, span in gen:
                if sum(ind) <= sum(ind_monic):
                    push = self.amalgamate(span)
                    if self.is_monic(span.csp1, push[1], push[0]) and self.is_monic(span.csp2, push[1], push[2]):
                        ind_monic = ind
                        flag = True
                        for s in spans:
                            if s == span:
                                flag = False
                                break
                        if flag:
                            inds.append(ind)
                            spans.append(span)

        return spans, inds

    def integration_measure(self, span_ref, span_mes):
        """ Computes the integration measure of span_mes with respect to span_ref """
        if not isinstance(span_ref, Span) or not isinstance(span_mes, Span):
            raise Exception("Object not a Span.")
        
        span_max_ints, max_int_inds = self._find_maximally_integrated(span_ref)
        span_mes_ind = self.get_distance(span_mes, span_ref)

        best_similarity = 0
        for span_max_int, max_int_ind in zip(span_max_ints, max_int_inds):
            gen = [([0, 0, 0], span_ref)]
            while any([sum(g[0]) <= min(sum(max_int_ind), sum(span_mes_ind)) for g in gen]):
                next_gen = self.get_next_population_of_generalisations(gen)
                gen = []
                for ind, span in next_gen:
                    if self.is_generalisation_of(span_max_int, span) and self.is_generalisation_of(span_mes, span):
                        gen.append((ind, span))
                        best_similarity = max(best_similarity, self.similarity(max_int_ind, ind, span_mes_ind))
        
        return best_similarity

    def topology_measure(self, span_ref, span_mes):
        """ Computes the topology measure of span_mes with respect to span_ref """
        if not isinstance(span_ref, Span) or not isinstance(span_mes, Span):
            raise Exception("Object not a Span.")
        
        span_max_tops, max_top_inds = self._find_maximally_topologic(span_ref)
        span_mes_ind = self.get_distance(span_mes, span_ref)

        best_similarity = 0
        for span_max_top, max_top_ind in zip(span_max_tops, max_top_inds):
            gen = [([0, 0, 0], span_ref)]
            while any([sum(g[0]) <= min(sum(max_top_ind), sum(span_mes_ind)) for g in gen]):
                next_gen = self.get_next_population_of_generalisations(gen)
                gen = []
                for ind, span in next_gen:
                    if self.is_generalisation_of(span_max_top, span) and self.is_generalisation_of(span_mes, span):
                        gen.append((ind, span))
                        best_similarity = max(best_similarity, self.similarity(max_top_ind, ind, span_mes_ind))
        
        return best_similarity

    def unpacking_measure(self, span_ref, span_mes):
        """ Computes the unpacking measure of span_mes with respect to span_ref """
        if not isinstance(span_ref, Span) or not isinstance(span_mes, Span):
            raise Exception("Object not a Span.")
        
        span_mes_ind = self.get_distance(span_mes, span_ref)
        gen = [([0, 0, 0], span_ref)]
        loop = True
        while loop:
            gen = self.get_next_population_of_generalisations(gen, only_gen=True)
            for ind_max_unp, span_max_unp in gen:
                if self.terminal(span_max_unp.csp_gen):
                    loop = False
                    break

        gen = [([0, 0, 0], span_ref)]
        ind_most_common = [0, 0, 0]
        while any([sum(g[0]) <= min(sum(span_mes_ind), sum(ind_max_unp)) for g in gen]):
            next_gen = self.get_next_population_of_generalisations(gen)
            gen = []
            for ind, span in next_gen:
                if self.is_generalisation_of(span_max_unp, span) and self.is_generalisation_of(span_mes, span):
                    gen.append((ind, span))
                    ind_most_common = ind

        return self.similarity(ind_max_unp, ind_most_common, span_mes_ind)

    def amalgamate(self, span):
        """ Compute the amalgam (pushout) of a span """
        if not isinstance(span, Span):
            raise Exception("Object not a Span.")

        if span.csp_gen is None:
            span.csp_gen = self.get_csp_gen(span.csp1, span.csp2)
            span.f1 = None
            span.f2 = None
            
        csp1_pull = self.pullback(span.csp1, span.csp_gen, span.f1)
        csp2_pull = self.pullback(span.csp2, span.csp_gen, span.f2)
        csp_pull = self.pullback(csp1_pull, csp2_pull, None)
        f1 = self.restrict(span.f1, csp_pull)
        f2 = self.restrict(span.f2, csp_pull)
        span_0 = Span(span.csp1, span.csp2, f1, f2, csp_pull)
        return self.pushout(span_0)   

    def get_generalised_amalgams(self, n_gens, span):
        """ Compute all generalised amalgams until depth n_gens """
        if (n_gens == 0):
            return self.amalgamate(span)

        if not isinstance(span, Span):
            raise Exception("Object not a Span.")

        results = []

        if span.csp_gen is None:
            span.csp_gen = self.get_csp_gen(span.csp1, span.csp2)            
            span.f1 = None
            span.f2 = None

        csp0_gens = [self.generalisation_step(span.csp_gen)]
        if len(csp0_gens[0]):
            for i in range(n_gens - 1):
                new_gens = []
                for csp in csp0_gens[i]:
                    new_gens += self.generalisation_step(csp)
                csp0_gens.append(new_gens)
        csp0_gens = self.reduce([x for xs in csp0_gens for x in xs]) + [span.csp_gen]

        csp1_gens = [self.generalisation_step(span.csp1)]
        if len(csp1_gens[0]):
            for i in range(n_gens - 1):
                new_gens = []
                for csp in csp1_gens[i]:
                    new_gens += self.generalisation_step(csp)
                csp1_gens.append(new_gens)
        csp1_gens = self.reduce([x for xs in csp1_gens for x in xs]) + [span.csp1]

        csp2_gens = [self.generalisation_step(span.csp2)]
        if len(csp2_gens[0]):
            for i in range(n_gens - 1):
                new_gens = []
                for csp in csp2_gens[i]:
                    new_gens += self.generalisation_step(csp)
                csp2_gens.append(new_gens)
        csp2_gens = self.reduce([x for xs in csp2_gens for x in xs]) + [span.csp2]

        for csp0_gen in csp0_gens:
            for csp1_gen in csp1_gens:
                for csp2_gen in csp2_gens:

                    csp1_pull = self.pullback(csp1_gen, csp0_gen, span.f1)
                    csp2_pull = self.pullback(csp2_gen, csp0_gen, span.f2)
                    csp_pull = self.pullback(csp1_pull, csp2_pull, None)
                    f1 = self.restrict(span.f1, csp_pull)
                    f2 = self.restrict(span.f2, csp_pull)
                    span_0 = Span(csp1_gen, csp2_gen, f1, f2, csp_pull)
                    amalgam = self.pushout(span_0)   
                    results.append(amalgam[1])
            results = self.reduce(results)

        results = self.reduce_minimal(results)
        for i, amalgam in enumerate(results):
            amalgam.plot(filename = f"fs{i}.gv")
        return results

    def get_next_population_of_generalisations(self, spans, only_gen=False):
        """ From a set of spans, and their distances, it obtains the next level of generalisations """
        res = []
        csp1_gens = []
        csp2_gens = []
        csp_generic_gens = []
        for ind, span in spans:
            if not isinstance(span, Span):
                raise Exception("Object not a Span.")      

            csp_generic_gens = self.generalisation_step(span.csp_gen)  

            for cspg in csp_generic_gens:  
                res.append(([ind[0], ind[1] + 1, ind[2]], Span(span.csp1, span.csp2, span.f1, span.f2, cspg)))

            if not only_gen:
                csp1_gens = self.generalisation_step(span.csp1)    
                csp2_gens = self.generalisation_step(span.csp2)

                for csp1 in csp1_gens:
                    res.append(([ind[0] + 1, ind[1], ind[2]], Span(csp1, span.csp2, span.f1, span.f2, span.csp_gen)))


                for csp2 in csp2_gens:
                    res.append(([ind[0], ind[1], ind[2] + 1], Span(span.csp1, csp2, span.f1, span.f2, span.csp_gen)))

                for csp1 in csp1_gens:
                    for csp2 in csp2_gens:   
                        res.append(([ind[0] + 1, ind[1], ind[2] + 1], Span(csp1, csp2, span.f1, span.f2, span.csp_gen)))

                for csp1 in csp1_gens:
                    for cspg in csp_generic_gens:    
                        res.append(([ ind[0] + 1, ind[1] + 1, ind[2]], Span(csp1, span.csp2, span.f1, span.f2, cspg)))

                for csp2 in csp2_gens:
                    for cspg in csp_generic_gens: 
                        res.append(([ind[0], ind[1] + 1, ind[2] + 1], Span(span.csp1, csp2, span.f1, span.f2, cspg)))

                for csp1 in csp1_gens:
                    for csp2 in csp2_gens:
                        for cspg in csp_generic_gens:
                            res.append(([ind[0] + 1, ind[1] + 1, ind[2] + 1], Span(csp1, csp2, span.f1, span.f2, cspg)))

        return res