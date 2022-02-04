import sys
# setting path
sys.path.append('../Amalgamation')
from amalgam import Category

class FeatureTermCategory(Category): 
    def __init__(self, sorts, feat):
        self.sorts = sorts
        self.feat = feat
        super().__init__()

    def generalization_step(self, fs):
        return 
      
    def pullback(self, fs, fs_gen):
        return fs.antiunify(fs_gen)
    
    def get_csp_gen(self, fs1, fs2):
        return fs1.antiunify(fs2)

    def amalgamate(self, fs1, fs2):
        return super().amalgamate(fs1, fs2)

    def _antiunification(self, fs1, fs2):
        return fs1.antiunify(fs2)



if __name__ == "__main__":
    print("hello")