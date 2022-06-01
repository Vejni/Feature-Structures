import re
import copy

class CASLSpecification:
    def parse_text(self, text):
        """
        Parses casl code 
        """

        # Get name of specification
        self.name = re.findall(r"(?:spec ).+\b" , text)[0].replace("spec ", "")

        # Get Sorts
        a, b = text.find('sorts'), text.find('ops')
        if a != -1:
            if b == -1:
                b = text.find('preds')
            self.sorts = re.sub(re.compile(r'\s+'), '',  text[a+5:b]).split(",")

        # Get operations
        a, b = text.find('ops'), text.find('preds')
        self.ops = []
        if a != -1:
            if b == -1:
                b = text.find('%axioms%')
            ops = text[a+3:b].strip().replace(" ", "").split("\n")
            for op in ops:
                if "," in op:
                    ops_split = op.split(",")
                    signature = ops_split[-1].split(":")[1]
                    for o in ops_split[:-1]:
                        o += ":" + signature
                        self.ops.append(o)
                    self.ops.append(ops_split[-1])
                else:
                    self.ops.append(op)
            
        # Get predicates
        a, b = text.find('preds'), text.find('%axioms%')
        self.preds = []
        if a != -1:
            preds = text[a+5:b].strip().replace(" ", "").split("\n")
            for pred in preds:
                if "," in pred:
                    preds_split = pred.split(",")
                    signature = preds_split[-1].split(":")[1]
                    for p in preds_split[:-1]:
                        p += signature
                        self.preds.append(p)
                else:
                    self.preds.append(pred)            

        # Get axioms
        a, b = text.find('%axioms%'), text.find('end')
        axioms_text =  text[a+8:b]
        self.axioms = []

        # if same quantifier used many times, place it everywhere
        flag = False
        for line in axioms_text.split("\n"):
            line_str = line.strip()
            if line_str.startswith("forall") or line_str.startswith("exists"):
                quantifier = line_str
                flag = True
            else:
                if line_str:
                    line_str = re.sub('%[^%]+%', '', line_str).strip()
                    if flag:
                        self.axioms.append(quantifier + " " + line_str)
                    else:
                        self.axioms += line_str.split(".")
                else:
                    flag = False

    def __str__(self):
        """ Define how to print feature structures to console """
        name = f"spec: {self.name}" + "\n\n"
        sorts = f"sorts: \n {' '.join(self.sorts)}" + "\n\n"
        ops = "ops: \n" + '\n'.join(self.ops) + "\n\n"
        preds = "preds: \n" + '\n'.join(self.preds) + "\n\n"
        axioms = "axioms: \n" + '\n'.join(self.axioms) + "\n\n"

        return name + sorts + ops + preds + axioms

    def __repr__(self):
        """ Called from interactive prompt """
        return self.__str__()

    def __eq__(self, s):
        """ Overrides the default implementation of equality, used for testing only """
        if not isinstance(s, CASLSpecification):
            return False    
        return set(self.sorts) == set(s.sorts) and set(self.ops) == set(s.ops) and set(self.s) == set(s.preds) and set(self.axioms) == set(s.axioms)

    def read_from_file(self, path):
        with open(path) as fin:
            text = fin.read()
        self.parse_text(text)

    def axiom_elimination_operator(self):
        res = []
        for a in self.axioms:
            s = copy.deepcopy(self)
            s.axioms.remove(a)
            res.append(s)
        return res


        

if __name__ == "__main__":
    spec = """  
    spec Linkage =
    sorts 
        Link, Entity, LinkSchema

    ops 
        link: LinkSchema -> Link
        anEnt: LinkSchema -> Entity
        anotherEnt: LinkSchema -> Entity

    preds
        linked: Entity * Entity

    %axioms%
        forall s:LinkSchema
            .linked(anEnt(s),anotherEnt(s))

        forall l:Link
            .exists! s:LinkSchema .link(s) = l

        forall x,y : Entity; s: LinkSchema
            .linked(x,y) <=> ( anEnt(s) = x /\ anotherEnt(s) = y ) \/ ( anEnt(s) = y /\ anotherEnt(s) = x )
            .linked(x,y) <=> linked(y,x) %symmetry%
            .not linked(x,x) %irreflexivity%
    end
    """

    linkage = CASLSpecification()
    linkage.parse_text(spec)
    print(linkage)
    for spec in linkage.axiom_elimination_operator():
        print(spec)

    source = CASLSpecification()
    source.read_from_file("CASL Specifications\specs\spec.txt")
    print(source)