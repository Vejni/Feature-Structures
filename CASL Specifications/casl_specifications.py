import re
import copy

class CASLSpecification:
    def __init__(self):
        self.sorts = []
        self.ops = []
        self.preds = []
        self.axioms = []
        self.f1 = None
        self.f2 = None

    def _parse_sorts(self, text):
        a = text.find('sorts')
        if a == -1:
            a = text.find('sort')
            if a == -1:
                return

        endings = ["ops", "preds", "%axioms%", "view"]
        i = 0
        while (((b := text.find(endings[i])) == -1) or (a > b)) and (i < len(endings)):
            i += 1

        if b == -1:
            return

        self.sorts = re.sub(re.compile(r'\s+'), '',  text[a+5:b]).split(",")

    def _parse_ops(self, text):
        a = text.find('ops')
        if a == -1:
            a = text.find('op')
            if a == -1:
                return

        endings = ["preds", "%axioms%", "view"]
        i = 0
        while (((b := text.find(endings[i])) == -1) or (a > b)) and (i < len(endings)):
            i += 1
        
        if b == -1:
            return

        ops = text[a+3:b].strip().replace(" ", "").split("\n")
        for op in ops:
            op = op.strip()
            if op:
                if "," in op:
                    ops_split = op.split(",")
                    signature = ops_split[-1].split(":")[1]
                    for o in ops_split[:-1]:
                        o += ":" + signature
                        self.ops.append(o.strip())
                    self.ops.append(ops_split[-1].strip())
                else:
                    self.ops.append(op.strip())

    def _parse_preds(self, text):
        a = text.find('preds')
        if a == -1:
            a = text.find('pred')
            if a == -1:
                return

        endings = ["%axioms%", "ops", "view"]
        i = 0
        while (((b := text.find(endings[i])) == -1) or (a > b)) and (i < len(endings)):
            i += 1

        if b == -1:
            return

        preds = text[a+5:b].strip().replace(" ", "").split("\n")
        for pred in preds:
            pred = pred.strip()
            if pred:
                if "," in pred:
                    preds_split = pred.split(",")
                    signature = preds_split[-1].split(":")[1]
                    for p in preds_split[:-1]:
                        p += ":" + signature
                        self.preds.append(p.strip())
                    self.preds.append(preds_split[-1].strip())
                else:
                    self.preds.append(pred.strip()) 

    def _parse_axioms(self, text):
        a, b = text.find('%axioms%'), text.find("end")
        if a == -1:
            return
    
        # if same quantifier used many times, place it everywhere
        axioms_text =  text[a+8:b]
        flag = False
        for line in axioms_text.split("\n"):
            line_str = line.strip()
            if line_str:
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
                        if flag:
                            self.axioms.append(quantifier + " " + line_str)
                        else:
                            self.axioms += [("." + ax).strip()  for ax in line_str.split(".")[1:]]
                    else:
                        flag = False

        print(self.axioms) 

    def _parse_views(self, text):
        indices = [s.start() for s in re.finditer("view", text)]
        if not len(indices):
            return

        domain = text[indices[0]:indices[1]].split("\n")[0].split("to ")[1].replace("=", "").strip()
        renamings_text = [r.strip() for r in text[indices[0]:indices[1]].split("=")[1].split(",")]
        renamings = {}
        for r in renamings_text:
            v, k = r.split("|->")
            renamings[k.strip()] = v.strip()
        self.f1 = {"domain": domain, "renamings": renamings}

        domain = text[indices[1]:].split("\n")[0].split("to ")[1]
        renamings_text = [r.strip() for r in text[indices[1]:].split("=")[1].split(",")]
        renamings = {}
        for r in renamings_text:
            v, k = r.split("|->")
            renamings[k.strip()] = v.strip()
        self.f2 = {"domain": domain, "renamings": renamings}       
                
    def parse_text(self, text):
        """
        Parses casl code 
        """

        # Get name of specification
        self.name = re.findall(r"(?:spec ).+\b" , text)[0].replace("spec ", "")

        # Some general formatting
        text = text.replace(",\n", ",")
        text = re.sub(',[ \t]\n', ',', text)
        text = re.sub('%\([^()]*\)%', '', text)

        # Get Sorts
        self._parse_sorts(text)

        # Get operations
        self._parse_ops(text)
            
        # Get predicates
        self._parse_preds(text)        

        # Get axioms
        self._parse_axioms(text)

        # Get views if generic
        self._parse_views(text)

        # Replace occurences
        self._encode()

    def _encode(self):
        """ Finds occurences of each sosrt / predicate / operation in axioms as well as variables """
        # Encode sorts
        dic = {}
        for i, sort in enumerate(self.sorts):
            dic[f"_s{i}_"] = sort
        self._sorts = dic
        
        # Enode ops
        dic = {}
        for i, op in enumerate(self.ops):
            symbol, signature = op.split(":")
            if "->" in signature:
                arguments, ret = signature.split("->")
            else:
                arguments, ret = "", signature
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

    def disjoint_union(self, spec1, spec2):
        """ Computes the disjoint union or pushout of two specifications """
        new_spec = CASLSpecification() 
        new_spec.name = spec1.name  + "_+_" + spec2.name 

        for s1 in spec1.sorts:
            if s1 in self.sorts and s1 in spec2.sorts:
                new_spec.sorts.append(s1)
            else:
                new_spec.sorts.append(s1 + "_1")

        

        #
        new_spec.sorts = list(set(spec1.sorts + spec2.sorts))
        new_spec.preds = list(set(spec1.preds + spec2.preds))
        new_spec.axioms = list(set(spec.axioms))

        for i, a1 in enumerate(self._axioms):
            if not (spec.has_axiom(self, a1) and spec_gen.has_axiom(self, a1)):
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

    def rename(self, renamings):
        temp = copy.copy(self.sorts)
        for i, s in enumerate(self.sorts):
            if s in renamings.keys():
                temp[i] = renamings[s]
        self.sorts = temp

        temp = copy.copy(self.ops)
        for i, o in enumerate(self.ops):
            for k in renamings.keys():
                if k in o:
                    temp[i] = temp[i].replace(k, renamings[k])
        self.ops = temp     

        temp = copy.copy(self.preds)
        for i, p in enumerate(self.preds):
            for k in renamings.keys():
                if k in p:
                    temp[i] = temp[i].replace(k, renamings[k])
        self.preds = temp    

        temp = copy.copy(self.axioms)
        for i, ax in enumerate(self.preds):
            for k in renamings.keys():
                if k in ax:
                    temp[i] = temp[i].replace(k, renamings[k])
        self.axioms = temp  

        self._encode()



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


    csp1 = CASLSpecification()
    csp1.read_from_file("CASL Specifications\specs\I.txt")
    
    gen = CASLSpecification()
    gen.read_from_file("CASL Specifications\specs\G.txt")
    csp1.rename(gen.f2["renamings"])
    print(csp1)
    #for i, spec in enumerate(source.axiom_elimination_operator()):
        #spec.write_to_file(f"CASL Specifications\specs\spec_out_{i}.txt")
