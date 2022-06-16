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
        return ((self.csp1.alphabetic_variant(span.csp1) and self.csp2.alphabetic_variant(span.csp2)) or (self.csp2.alphabetic_variant(span.csp1) and self.csp1.alphabetic_variant(span.csp2))) and self.csp_gen == span.csp_gen

class Category(object):
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def generalisation_step(self, csp):
        """ Method to implement """
        return

    @abc.abstractmethod
    def pullback(self, csp, csp_gen):
        """ Method to implement """
        return
    
    @abc.abstractmethod
    def pushout(self, csp1, csp2, csp_gen):
        """ Method to implement """
        return

    @abc.abstractmethod
    def reduce(self, csps):
        """ Method to implement """
        return

    @abc.abstractmethod
    def is_monic(self, csp1, csp2):
        """ Method to implement """
        return

    @abc.abstractmethod
    def is_epic(self, csp1, csp2):
        """ Method to implement """
        return
    
    @abc.abstractmethod
    def rename(self, csp, f):
        """ Method to implement """
        return

    def reduce_minimal(self, amalgams):
        results = []
        for csp in amalgams:
            flag = True
            for res in amalgams:
                if (csp.subsumes(res) and csp != res) or (csp in results):
                    flag = False
                    break
            if flag:
                results.append(csp)
        return results

    def reduce(self, amalgams):
        results = []
        for csp in amalgams:
            flag = True
            for res in results:
                if csp.alphabetic_variant(res) and csp != res:
                    flag = False
                    break
            if flag:
                results.append(csp)
        return results

    def is_generalisation_of(self, ob1, ob2):
        if isinstance(ob1, Span) and isinstance(ob2, Span):
            return self.is_monic(ob1.csp1, ob2.csp1) and self.is_monic(ob1.csp_gen, ob2.csp_gen) and self.is_monic(ob1.csp2, ob2.csp2)
        else:
            return self.is_monic(ob1, ob2)

    def get_distance(self, span_to_find, span_ref):
        not_found = True
        ind_found = [sys.maxsize, 0, 0]

        gen = [([0, 0, 0], span_ref)]
        while not_found or any([sum(g[0]) < sum(ind_found) for g in gen]):
            gen = self.get_next_population_of_generalisations(gen)
            for ind, span in gen:
                if sum(ind) < sum(ind_found):
                    if span == span_to_find:
                        not_found = False
                        ind_found = ind
        return ind_found

    def similarity(self, dist1, dist_com, dist2):
        if isinstance(dist1, list) and isinstance(dist_com, list) and isinstance(dist2, list):
            for i in range(3):
                dist1[i] -= dist_com[i]
                dist2[i] -= dist_com[i]
            return sum(dist_com) / (sum(dist_com) + sum(dist1) + sum(dist2))
        else:
            return dist_com / (dist1 + dist2 - dist_com)

    def _find_maximally_integrated(self, span_ref):
        not_epic = True
        ind_epic = [sys.maxsize, 0, 0]
        span_epic = None
        gen = [([0, 0, 0], span_ref)]
        while not_epic or any([sum(g[0]) < sum(ind_epic) for g in gen]):
            gen = self.get_next_population_of_generalisations(gen)
            for ind, span in gen:
                if sum(ind) < sum(ind_epic):
                    push = self.amalgamate(span)
                    if self.is_epic(push[0], push[1]) and self.is_epic(push[2], push[1]):
                        not_epic = False
                        ind_epic = ind
                        span_epic = span

        return span_epic, ind_epic

    def _find_maximally_topologic(self, span_ref):
        not_monic = True
        ind_monic = [sys.maxsize, 0, 0]
        span_monic = None
        gen = [([0, 0, 0], span_ref)]
        while not_monic or any([sum(g[0]) < sum(ind_monic) for g in gen]):
            gen = self.get_next_population_of_generalisations(gen)
            for ind, span in gen:
                if sum(ind) < sum(ind_monic):
                    push = self.amalgamate(span)
                    if self.is_monic(push[0], push[1]) and self.is_monic(push[2], push[1]):
                        not_monic = False
                        ind_monic = ind
                        span_monic = span

        return span_monic, ind_monic

    def integration_measure(self, span_ref, span_mes):
        if not isinstance(span_ref, Span) or not isinstance(span_mes, Span):
            raise Exception("Object not a Span.")
        
        span_max_int, max_int_ind = self._find_maximally_integrated(span_ref)
        span_mes_ind = self.get_distance(span_mes, span_ref)

        not_common_gen = True
        dist_common_gen = 0
        gen = [([0, 0, 0], span_ref)]
        while not_common_gen or any([sum(g[0]) < sum(max_int_ind) for g in gen]):
            gen = self.get_next_population_of_generalisations(gen)
            for ind, span in gen:
                if sum(ind) > dist_common_gen:
                    if self.is_generalisation_of(span_max_int, span) and self.is_generalisation_of(span_mes, span):
                        not_common_gen = False
                        dist_common_gen = self.similarity(max_int_ind, ind, span_mes_ind)

        return dist_common_gen

    def topology_measure(self, span_ref, span_mes):
        if not isinstance(span_ref, Span) or not isinstance(span_mes, Span):
            raise Exception("Object not a Span.")
        
        span_max_top, max_top_int = self._find_maximally_topologic(span_ref)
        span_mes_ind = self.get_distance(span_mes, span_ref)

        not_common_gen = True
        dist_common_gen = 0
        gen = [([0, 0, 0], span_ref)]
        while not_common_gen or any([sum(g[0]) < sum(max_top_int) for g in gen]):
            gen = self.get_next_population_of_generalisations(gen)
            for ind, span in gen:
                if sum(ind) > dist_common_gen:
                    if self.is_generalisation_of(span_max_top, span) and self.is_generalisation_of(span_mes, span):
                        not_common_gen = False
                        dist_common_gen = self.similarity(max_top_int, ind, span_mes_ind)

        return dist_common_gen

    def amalgamate(self, span):
        if not isinstance(span, Span):
            raise Exception("Object not a Span.")

        if span.f1 is not None:
            self.rename(span.csp1, span.f1)
        if span.f2 is not None:
            self.rename(span.csp2, span.f2)

        if span.csp_gen is None:
            span.csp_gen = self.get_csp_gen(span.csp1, span.csp2)
            
        csp1_pull = self.pullback(span.csp1, span.csp_gen)
        csp2_pull = self.pullback(span.csp2, span.csp_gen)
        csp_pull = self.pullback(csp1_pull, csp2_pull)
        return self.pushout(span.csp1, span.csp2, csp_pull)   

    def get_generalised_amalgams(self, n_gens, span):
        if (n_gens == 0):
            return self.amalgamate(span)

        if not isinstance(span, Span):
            raise Exception("Object not a Span.")

        results = []
        if span.f1 is not None:
            self.rename(span.csp1, span.f1)
        if span.f2 is not None:
            self.rename(span.csp2, span.f2)

        if span.csp_gen is None:
            span.csp_gen = self.get_csp_gen(span.csp1, span.csp2)

        csp0_gens = [[self.generalisation_step(span.csp_gen)]]
        for i in range(n_gens):
            new_gens = []
            for csp in csp0_gens[i]:
                new_gens += self.generalisation_step(csp)
            csp0_gens.append(new_gens)
        csp0_gens = self.reduce(csp0_gens)

        csp1_gens = [[self.generalisation_step(span.csp1)]]
        for i in range(n_gens):
            new_gens = []
            for csp in csp1_gens[i]:
                new_gens += self.generalisation_step(csp)
            csp1_gens.append(new_gens)
        csp1_gens = self.reduce(csp1_gens)

        csp2_gens = [[self.generalisation_step(span.csp2)]]
        for i in range(n_gens):
            new_gens = []
            for csp in csp2_gens[i]:
                new_gens += self.generalisation_step(csp)
            csp2_gens.append(new_gens)
        csp2_gens = self.reduce(csp2_gens)

        for csp0_gen in csp0_gens:
            for csp1_gen in csp1_gens:
                for csp2_gen in csp2_gens:

                    csp1_pull = self.pullback(csp1_gen, csp0_gen)
                    csp2_pull = self.pullback(csp2_gen, csp0_gen)
                    csp_pull = self.pullback(csp1_pull, csp2_pull)
                    amalgam = self.pushout(csp1_gen, csp2_gen, csp_pull)
                    results.append(amalgam)

        results = self.reduce_minimal(results)
        #for i, amalgam in enumerate(results):
        #    amalgam.plot(filename = f"fs{i}.gv")
        return results

    def get_next_population_of_generalisations(self, spans):
        res = []
        csp1_gens = []
        csp2_gens = []
        csp_generic_gens = []
        for ind, span in spans:
            if not isinstance(span, Span):
                raise Exception("Object not a Span.")      

            csp1_gens = self.generalisation_step(span.csp1)    
            csp2_gens = self.generalisation_step(span.csp2)
            csp_generic_gens = self.generalisation_step(span.csp_gen)    

            for csp1 in csp1_gens:
                res.append(([ind[0] + 1, ind[1], ind[2]], Span(csp1, span.csp2, span.f1, span.f2, span.csp_gen)))

            for cspg in csp_generic_gens:  
                res.append(([ind[0], ind[1] + 1, ind[2]], Span(span.csp1, span.csp2, span.f1, span.f2, cspg)))

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