import abc

class Category(object):
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def generalization_step(self, csp):
        """Method documentation"""
        return

    @abc.abstractmethod
    def pullback(self, csp, csp_gen, f):
        """Method documentation"""
        return
    
    @abc.abstractmethod
    def pushout(self, csp1, csp2, csp_gen, f, g):
        """Method documentation"""
        return

    @abc.abstractmethod
    def reduce(self, amalgams):
        """Method documentation"""
        return

    def amalgamate(self, csp1, csp2, csp_gen, f, g):
        results = []
        for csp0_gen in self.generalization_step(csp_gen):
            for csp1_gen in self.generalization_step(csp1):
                for csp2_gen in self.generalization_step(csp2):

                    csp1_pull = self.pullback(csp1_gen, csp0_gen)
                    csp2_pull = self.pullback(csp2_gen, csp0_gen)
                    csp_pull = self.pullback(csp1_pull, csp2_pull)
                    amalgam = self.pushout(csp1_gen, csp2_gen, csp_pull, f, g)
                    results.append(amalgam)

        results = self.reduce_minimal(results)
        for i, amalgam in enumerate(results):
            amalgam.plot(filename = f"fs{i}.gv")
        return results

