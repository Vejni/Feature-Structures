import re
import copy

class CASLSpecification:
    def __init__(self):
        self.sorts = []
        self.ops = []
        self.preds = []
        self.axioms = []

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
                        p += ":" + signature
                        self.preds.append(p)
                    self.preds.append(preds_split[-1])
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
            if line_str.startswith("forall"):   
                line_str = line_str.replace(";", " .forall ")
                quantifier = line_str
                flag = True
            elif line_str.startswith("exists!"):
                line_str = line_str.replace(";", " .exists! ")
                quantifier = line_str
                flag = True
            elif line_str.startswith("exists"):
                line_str = line_str.replace(";", " .exists ")
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
        self._encode()

    def _encode(self):
        # Encode sorts
        dic = {}
        for i, sort in enumerate(self.sorts):
            dic[f"_s{i}_"] = sort
        self._sorts = dic
        
        # Enode ops
        dic = {}
        for i, op in enumerate(self.ops):
            symbol, signature = op.split(":")
            arguments, ret = signature.split("->")
            dic[f"_o{i}_"] = {"name": symbol, "signature":{"arguments": arguments.split(","), "return":ret}, "original":op}
        self._ops = dic

        # Enode preds
        dic = {}
        for i, pred in enumerate(self.preds):
            symbol, signature = pred.split(":")
            dic[f"_p{i}_"] = {"name": symbol, "signature":signature.split("*"), "original":pred}
        self._preds = dic

        # Encode axioms
        axioms = []
        for ax in self.axioms:
            ax_spl = ax.split(".")
            quantifiers = ax_spl[0].strip().replace(": ", ":").replace(" :", ":")
            terms = ax_spl[-1]
            for term in ax_spl[1:]:
                if term.startswith("forall") or term.startswith("exists"):
                    quantifiers += " ." + term.strip()

            quantifiers = quantifiers.replace(": ", ":").replace(" :", ":")
            # Get variables, and make dic
            # then replace sorts, preds, ops with keys
            dic = {}
            i = 0
            for term in [word for word in quantifiers.split(" ") if ":" in word]:
                vars, sort = term.split(":")
                for var in vars:
                    dic[f"_v{i}_"] = {"symbol": var, "sort": sort}
                    quantifiers = re.sub(f"{var}(?=\s*[:,])", f" _v{i}_ ", quantifiers)
                    terms = re.sub(f"{var}(?=$|[,)\s+\/\\\\<>=%])", f" _v{i}_ ", terms)
                    i += 1

            # Replace sorts
            for s_k, s_v in self._sorts.items():
                quantifiers = re.sub(f"{s_v}(?=$|[,(\s+\/\\\\<>=%])", f" {s_k} ", quantifiers)

            # Replace ops
            for op_k, op_v in self._ops.items():
                terms = re.sub(f"{op_v['name']}(?=$|[,(\s+\/\\\\<>=%])", f" {op_k} ", terms)

            # Replace preds
            for pred_k, pred_v in self._preds.items():
                terms = re.sub(f"{pred_v['name']}(?=$|[,(\s+\/\\\\<>=%])", f" {pred_k} ", terms)
            
            axioms.append((quantifiers + " " + terms).replace("  ", " "))
        self._axioms = axioms
            
    def __str__(self):
        """ Define how to print feature structures to console """
        name = f"spec: {self.name}" + "\n\n"
        sorts = f"sorts: {' '.join(self.sorts)}" + "\n\n"
        ops = "ops: \n\t" + '\n\t'.join(self.ops) + "\n\n"
        preds = "preds: \n\t" + '\n\t'.join(self.preds) + "\n\n"
        axioms = "axioms: \n\t" + '\n\t'.join(self.axioms) + "\n\n"

        return name + sorts + ops + preds + axioms

    def __repr__(self):
        """ Called from interactive prompt """
        return self.__str__()

    def __eq__(self, spec):
        """ Overrides the default implementation of equality, used for testing only """
        if not isinstance(spec, CASLSpecification):
            return False    
        if set(self.sorts) == set(spec.sorts) and set(self.ops) == set(spec.ops) and set(self.preds) == set(spec.preds):
            for axiom in self._axioms:
                if not self.has_axiom(spec, axiom):
                    return False
            for axiom in spec._axioms:
                if not spec.has_axiom(self, axiom):
                    return False
            return True

    def _ax_eq(self, spec, ax1, ax2):
        """ Tests if two axioms are equal, not taking semantics into account """
        for w1, w2 in zip(ax1.split(" "), ax2.split(" ")):
            if w1 == w2 or (w1.startswith("_v") and w2.startswith("_v")):
                continue
            elif ((w1.startswith("_s") and w2.startswith("_s")) and self._sorts[w1] == spec._sorts[w2]):
                continue
            elif ((w1.startswith("_o") and w2.startswith("_o")) and self._preds[w1] == spec._ops[w2]):
                continue
            elif ((w1.startswith("_p") and w2.startswith("_p")) and self._preds[w1] == spec._preds[w2]):
                continue
            else:
                return False
        return True

    def _tidy_signature(self):
        """ Removes unused sorts/predicates/operations from the signature """
        dic = copy.copy(self._sorts)
        for s in dic.keys():
            flag = True
            for ax in self._axioms:
                if s in ax:
                    flag = False
                    break
            if flag:
                self.sorts.remove(self._sorts[s])
                del self._sorts[s]
        
        dic = copy.copy(self._preds)
        for i, p in enumerate(dic.keys()):
            flag = True
            for ax in self._axioms:
                if p in ax:
                    flag = False
                    break
            if flag:
                del self.preds[i]
                del self._preds[p]

        dic = copy.copy(self._ops)
        for i, o in enumerate(dic.keys()):
            flag = True
            for ax in self._axioms:
                if o in ax:
                    flag = False
                    break
            if flag:
                del self.ops[i]
                del self._ops[o]
        print(self)

    def has_axiom(self, spec, ax):
        """ Check if spec has axiom ax from self """
        for axiom in self._axioms:
            if self._ax_eq(spec, axiom, ax):
                return True
        return False

    def read_from_file(self, path):
        """ Read specification from file """
        with open(path) as fin:
            text = fin.read()
        self.parse_text(text)

    def write_to_file(self, path):
        """ Write specification back to file """
        with open(path, "w") as fin:
            fin.write(self.__str__())       

    def subsumes(self, spec):
        """ Check if self subsumes spec similar to __eq__ """
        if not isinstance(spec, CASLSpecification):
            return False    

        if set(spec.sorts).issubset(set(self.sorts)) and set(spec.preds).issubset(set(self.preds)) and set(spec.ops).issubset(set(self.ops)):
            for axiom in spec._axioms:
                if not self.has_axiom(spec, axiom):
                    return False
            return True

    def intersect(self, spec):
        """ Computes the intersection or pullback of two specifications """
        new_spec = CASLSpecification()  
        new_spec.name = self.name  + "_X_" + spec.name
        for s1 in self.sorts:
            if s1 in spec.sorts:
                new_spec.sorts.append(s1)

        for p1 in self.preds:
            if p1 in spec.preds:
                new_spec.preds.append(p1)

        for o1 in self.ops:
            if o1 in spec.ops:
                new_spec.ops.append(o1)
                
        for i, a1 in enumerate(self._axioms):
            if spec.has_axiom(self, a1):
                new_spec.axioms.append(self.axioms[i])

        new_spec._encode()
        new_spec._tidy_signature()
        return new_spec

    def disjoint_union(self, spec):
        """ Computes the disjoint union or pushout of two specifications """
        new_spec = CASLSpecification() 
        new_spec.name = self.name  + "_+_" + spec.name 
        new_spec.sorts = list(set(self.sorts + spec.sorts))
        new_spec.preds = list(set(self.preds + spec.preds))
        new_spec.axioms = list(set(spec.axioms))

        for i, a1 in enumerate(self._axioms):
            if not spec.has_axiom(self, a1):
                new_spec.axioms.append(self.axioms[i])

        new_spec._encode()
        return new_spec    

    def axiom_elimination_operator(self):
        """ Removes one axiom at a time, both the decoded and normal version of it """
        res = []
        for _a, a in zip(self._axioms, self.axioms):
            new_spec = copy.deepcopy(self)
            new_spec.axioms.remove(a)
            new_spec._axioms.remove(_a)
            new_spec._tidy_signature()
            res.append(new_spec)
        return res


        

if __name__ == "__main__":
    spec1 = """  
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
        forall x,y : Entity; s: LinkSchema
            .linked(x,y) <=> ( anEnt(s) = x /\ anotherEnt(s) = y ) \/ ( anEnt(s) = y /\ anotherEnt(s) = x )
            .linked(x,y) <=> linked(y,x) %symmetry%
            .not linked(x,x) %irreflexivity%

        forall l:Link
            .exists! s:LinkSchema .link(s) = l
    end
    """

    spec2 = """  
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
        forall x,y : Entity; s: LinkSchema
            .linked(x,y) <=> ( anEnt(s) = x /\ anotherEnt(s) = y ) \/ ( anEnt(s) = y /\ anotherEnt(s) = x )
            .linked(x,y) <=> linked(y,x) %symmetry%
            .not linked(x,x) %irreflexivity%

        forall s:LinkSchema
            .linked(anEnt(s),anotherEnt(s))

    end
    """

    linkage1 = CASLSpecification()
    linkage1.parse_text(spec1)

    linkage2 = CASLSpecification()
    linkage2.parse_text(spec2)

    a = linkage1.intersect(linkage2)
    print(a)

    b = linkage1.disjoint_union(linkage2)
    print(b)

    source = CASLSpecification()
    source.read_from_file("CASL Specifications\specs\spec.txt")
    #for i, spec in enumerate(source.axiom_elimination_operator()):
        #spec.write_to_file(f"CASL Specifications\specs\spec_out_{i}.txt")
