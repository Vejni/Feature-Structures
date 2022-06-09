import abc

class Span:
    def __init__(self, csp1, csp2, csp_gen, f1, f2):
        self.csp1 = csp1
        self.csp2 = csp2
        self.csp_gen = csp_gen
        self.f1 = f1
        self.f2 = f2

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

    def find_maximally_integrated(self, span):
        return # span and distance

    def find_maximally_topologic(self, span):
        return # span and distance

    def integration_measure(self, span1, span2):
        if len(span1) != 5 or len(span2) != 5:
            raise Exception("Spans not correctly specified.")
        
        max_int, dist = self.find_maximally_integrated(span1)

        return

    def topology_measure(self, span1, span2):
        if len(span1) != 5 or len(span2) != 5:
            raise Exception("Spans not correctly specified.")
        
        max_top, dist = self.find_maximally_topologic(span1)
    
        return

    def amalgamate(self, span):
        csp1 = self.rename(span.csp1, span.f1)
        csp2 = self.rename(span.csp2, span.f2)
        csp1_pull = self.pullback(span.csp1, span.csp_gen)
        csp2_pull = self.pullback(span.csp2, span.csp_gen)
        csp_pull = self.pullback(csp1_pull, csp2_pull)
        return self.pushout(csp1, csp2, csp_pull)   

    def get_generalised_amalgams(self, n_gens, span):
        if (n_gens == 0):
            return self.amalgamate(span)

        results = []
        csp1 = self.rename(span.csp1, span.f1)
        csp2 = self.rename(span.csp2, span.f2)

        csp0_gens = [[self.generalisation_step(span.csp_gen)]]
        for i in range(n_gens):
            new_gens = []
            for csp in csp0_gens[i]:
                new_gens += self.generalisation_step(csp)
            csp0_gens.append(new_gens)
        csp0_gens = self.reduce(csp0_gens)

        csp1_gens = [[self.generalisation_step(csp1)]]
        for i in range(n_gens):
            new_gens = []
            for csp in csp1_gens[i]:
                new_gens += self.generalisation_step(csp)
            csp1_gens.append(new_gens)
        csp1_gens = self.reduce(csp1_gens)

        csp2_gens = [[self.generalisation_step(csp2)]]
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

        results = self.reduce(results)
        #for i, amalgam in enumerate(results):
        #    amalgam.plot(filename = f"fs{i}.gv")
        return results

