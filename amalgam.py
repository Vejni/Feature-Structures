import abc

class Category(object):
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def generalization_step(self, csp):
        """Method documentation"""
        return

    @abc.abstractmethod
    def pullback(self, csp, csp_gen):
        """Method documentation"""
        return
    
    def amalgamate(self, csp1, csp2, csp_gen=None):
        # We can compute the generic space for feature terms
        if False: # csp_gen = None
            csp_gen = self.get_csp_gen(csp1, csp2)

        csp0_gen = self.generalization_step(csp_gen)
        csp1_gen = self.generalization_step(csp1)
        csp2_gen = self.generalization_step(csp2)

        
        csp1_pull = self.pullback(csp1_gen, csp_gen)
        csp2_pull = self.pullback(csp2_gen, csp_gen)

        csp_pull = self.pullback(csp1_pull, csp2_pull)
        csp_blend = self.pullback(csp_pull, csp0_gen)

        return csp_blend

