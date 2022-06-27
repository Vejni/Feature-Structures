import re
import copy

class CASLSpecification:
    def __init__(self):
        """ Creates specification object, allocates the properties """
        self.sorts = []
        self.ops = []
        self.preds = []
        self.axioms = []
        self.f1 = None
        self.f2 = None

    def _parse_sorts(self, text):
        """ Obtain a list of sorts from the signature, sets self.sort """
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
        """ Obtain a list of operations from the signature, sets self.ops """
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
        """ Obtain a list of predicates from the signature, sets self.preds """
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
        """ Obtain a list of axioms from the signature, sets self.axioms """
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

    def _parse_views(self, text):
        """ Read the views of the specification if there are any, sets self.f1, self.f2 """
        indices = [s.start() for s in re.finditer("view", text)]
        if not len(indices):
            return

        domain = text[indices[0]:indices[1]].split("\n")[0].split("to ")[1].replace("=", "").strip()
        renamings_text = [r.strip() for r in text[indices[0]:indices[1]].split("=")[1].split(",")]
        renamings = {}
        for r in renamings_text:
            v, k = r.split("|->")
            renamings[v.strip()] = k.strip()
        self.f1 = {"domain": domain, "renamings": renamings}

        domain = text[indices[1]:].split("\n")[0].split("to ")[1].replace("=", "").strip()
        renamings_text = [r.strip() for r in text[indices[1]:].split("=")[1].split(",")]
        renamings = {}
        for r in renamings_text:
            v, k = r.split("|->")
            renamings[v.strip()] = k.strip()
        self.f2 = {"domain": domain, "renamings": renamings}     
    
    def get_morphisms(self, f):
        """ The parsed views are not split by sort, operation or predicate. Split it here manually. """
        morph_sorts, morph_preds, morph_ops = {}, {}, {}
        for k, v in f["renamings"].items():
            if k in self.sorts:
                morph_sorts[k] = v
            elif k in [p.split(":")[0] for p in self.preds]:
                morph_preds[k] = v
            elif k in [o.split(":")[0] for o in self.ops]:
                morph_ops[k] = v
        return (morph_sorts, morph_preds, morph_ops)
                
    def parse_text(self, text):
        """ Parses the casl specification by calling the relevant methods which each parse the relevant chuncks of code """

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
        """ Define how to print the specification to console """
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
            if len(list(set(self.axioms) & set(spec.axioms))) == len(self.axioms) == len(spec.axioms):
                return True
        return False
            
    def _ax_eq(self, spec, ax1, ax2, f1):
        """ Tests if two axioms are equal, not taking semantics into account """
        morph_sorts, morph_preds, morph_ops = f1
        for w1, w2 in zip(ax1.split(" "), ax2.split(" ")):
            if w1 == w2 or (w1.startswith("_v") and w2.startswith("_v")):
                continue
            elif ((w1.startswith("_s") and w2.startswith("_s")) and self._sorts[w1] in morph_sorts.keys() and morph_sorts[self._sorts[w1]] == spec._sorts[w2]):
                continue
            elif ((w1.startswith("_p") and w2.startswith("_p")) and self._preds[w1]["original"].split(":")[0] in morph_preds.keys() and morph_preds[self._preds[w1]["original"].split(":")[0]] == spec._preds[w2]["original"].split(":")[0]):
                continue
            elif ((w1.startswith("_o") and w2.startswith("_o")) and self._ops[w1]["original"].split(":")[0] in morph_ops.keys() and morph_ops[self._ops[w1]["original"].split(":")[0]] == spec._ops[w2]["original"].split(":")[0]):
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

    def has_axiom(self, spec, ax, f1):
        """ Check if spec has axiom ax from self """
        for axiom in self._axioms:
            if self._ax_eq(spec, axiom, ax, f1):
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

    def subsumes(self, spec, f):
        """ Check if self subsumes spec similar to __eq__ """
        if not isinstance(spec, CASLSpecification):
            return False
        morph_sorts, morph_preds, morph_ops = f

        # Check sorts
        for sort in self.sorts:
            if morph_sorts[sort] not in spec.sorts:
                return False

        # Check preds
        for pred in self.preds:
            if morph_preds[pred.split(":")[0]] not in [s.split(":")[0] for s in spec.preds]:
                return False

        # Check ops
        for op in self.ops:
            if morph_ops[op.split(":")[0]] not in [o.split(":")[0] for o in spec.ops]:
                return False

        # Check axioms
        for axiom in spec._axioms:
            if not self.has_axiom(spec, axiom, f):
                return False

        return True

    def intersect(self, spec, f):
        """ Computes the intersection or pullback of two specifications """
        new_spec = CASLSpecification()  
        new_spec.name = self.name  + "_X_" + spec.name
        morph_sorts, morph_preds, morph_ops = f

        for s1 in spec.sorts:
            if s1 in morph_sorts.keys() and morph_sorts[s1] in self.sorts:
                new_spec.sorts.append(s1)

        for p1 in spec.preds:
            if p1.split(":")[0] in morph_preds.keys() and morph_preds[p1.split(":")[0]] in [p.split(":")[0] for p in self.preds]:
                new_spec.preds.append(p1)

        for o1 in spec.ops:
            if o1.split(":")[0] in morph_ops.keys() and morph_ops[o1.split(":")[0]] in  [o.split(":")[0] for o in self.ops]:
                new_spec.ops.append(o1)
                
        for i, a1 in enumerate(self._axioms):
            if spec.has_axiom(self, a1, f):
                new_spec.axioms.append(self.axioms[i])

        new_spec._encode()

        return new_spec

    def disjoint_union(self, spec1, spec2, f1, f2):
        """ Computes the disjoint union or pushout of two specifications """
        new_spec = CASLSpecification() 
        new_spec.name = spec1.name  + "_+_" + spec2.name 
        axioms1 = spec1.axioms
        axioms2 = spec2.axioms
        
        morph_sorts1, morph_preds1, morph_ops1 = f1
        morph_sorts2, morph_preds2, morph_ops2 = f2
        out_morph_sorts1, out_morph_preds1, out_morph_ops1 = {}, {}, {}
        out_morph_sorts2, out_morph_preds2, out_morph_ops2 = {}, {}, {}

        # Add sorts
        dic_sorts1 = {s : True for s in spec1.sorts}
        dic_sorts2 = {s : True for s in spec2.sorts}
        for s0 in self.sorts:
            if s0 in morph_sorts1.keys() and s0 in morph_sorts2.keys():
                dic_sorts1[morph_sorts1[s0]] = False
                dic_sorts2[morph_sorts2[s0]] = False
                out_morph_sorts1[morph_sorts1[s0]] = f"{s0}"
                out_morph_sorts2[morph_sorts2[s0]] = f"{s0}"
                new_spec.sorts.append(f"{s0}")
                for i in range(len(axioms1)):
                    axioms1[i] = re.sub(rf"(?=\b|:){morph_sorts1[s0]}(\b|.)", f"{s0}", axioms1[i])
                for i in range(len(axioms2)):
                    axioms2[i] = re.sub(rf"(?=\b|:){morph_sorts2[s0]}(\b|.)", f"{s0}", axioms2[i])
        for k, v in dic_sorts1.items():
            if v:
                out_morph_sorts1[k] = f"_1_{k}"
                new_spec.sorts.append(f"_1_{k}")
                for i in range(len(axioms1)):
                    axioms1[i] = re.sub(rf"(?=\b|:){k}(\b|.)", f"_1_{k}", axioms1[i])
        for k, v in dic_sorts2.items():
            if v:
                out_morph_sorts2[k] = f"_2_{k}"
                new_spec.sorts.append(f"_2_{k}")
                for i in range(len(axioms2)):
                    axioms2[i] = re.sub(rf"(?=\b|:){k}(\b|.)", f"_2_{k}", axioms2[i])

        # Add preds
        dic_preds1 = {p : True for p in spec1.preds}
        dic_preds2 = {p : True for p in spec2.preds}
        for p0 in self.preds:
            p0, sig0 = p0.split(":")
            if p0 in morph_preds1.keys() and p0 in morph_preds2.keys():
                sig1 = [morph_sorts1[s] for s in sig0.split("*")]
                sig2 = [morph_sorts2[s] for s in sig0.split("*")]

                dic_preds1[f"{morph_preds1[p0]}:{'*'.join(sig1)}"] = False
                dic_preds2[f"{morph_preds2[p0]}:{'*'.join(sig2)}"] = False

                sig = [out_morph_sorts1[s] for s in sig1]
                out_morph_preds1[f"{morph_preds1[p0]}:{'*'.join(sig1)}"] = f"{p0}:{'*'.join(sig)}"
                out_morph_preds2[f"{morph_preds2[p0]}:{'*'.join(sig2)}"] = f"{p0}:{'*'.join(sig)}"
                new_spec.preds.append(f"{p0}:{sig0}")
                for i in range(len(axioms1)):
                    axioms1[i] = re.sub(rf"(?=\b|.){morph_preds1[p0]}(\b|.)", f"{p0}", axioms1[i])
                for i in range(len(axioms2)):
                    axioms2[i] = re.sub(rf"(?=\b|.){morph_preds2[p0]}(\b|.)", f"{p0}", axioms2[i])
        for k, v in dic_preds1.items():
            p, sig = k.split(":")
            sig = [out_morph_sorts1[s] if s in out_morph_sorts1.keys() else s for s in sig.split("*")]
            if v:
                out_morph_preds1[k] = f"_1_{p}:{'*'.join(sig)}"
                new_spec.preds.append(f"_1_{p}:{'*'.join(sig)}")
                for i in range(len(axioms1)):
                    axioms1[i] = re.sub(rf"(?=\b|.){p}(\b|.)", f"_1_{p}", axioms1[i])
        for k, v in dic_preds2.items():
            p, sig = k.split(":")
            sig = [out_morph_sorts2[s] if s in out_morph_sorts2.keys() else s for s in sig.split("*")]
            if v:
                out_morph_preds2[k] = f"_2_{p}:{'*'.join(sig)}"
                new_spec.preds.append(f"_2_{p}:{'*'.join(sig)}")
                for i in range(len(axioms2)):
                    axioms2[i] = re.sub(rf"(?=\b|.){p}(\b|.)", f"_2_{p}", axioms2[i])
    
        # Add ops
        dic_ops1 = {o : True for o in spec1.ops}
        dic_ops2 = {o : True for o in spec2.ops}
        for o0 in self.ops:
            o0, sig0 = o0.split(":")
            ret = None
            if "->" in sig0:
                sig0, ret = sig0.split("->")
            if o0 in morph_ops1.keys() and o0 in morph_ops2.keys():
                sig1 = [morph_sorts1[s] for s in sig0.split("*")]
                sig2 = [morph_sorts2[s] for s in sig0.split("*")]

                dic_ops1[f"{morph_ops1[o0]}:{'*'.join(sig1)}{'->' + morph_sorts1[ret] if ret else ''}"] = False
                dic_ops2[f"{morph_ops2[o0]}:{'*'.join(sig2)}{'->' + morph_sorts2[ret] if ret else ''}"] = False

                sig = [out_morph_sorts1[s] for s in sig1]
                out_morph_ops1[f"{morph_ops1[o0]}:{'*'.join(sig1)}{'->' + ret if ret else ''}"] = f"{o0}:{'*'.join(sig)}{'->' + out_morph_sorts1[ret] if ret else ''}"
                out_morph_ops2[f"{morph_ops2[o0]}:{'*'.join(sig2)}{'->' + ret if ret else ''}"] = f"{o0}:{'*'.join(sig)}{'->' + out_morph_sorts2[ret] if ret else ''}"
                new_spec.ops.append(f"{o0}:{'*'.join(sig)}{'->' + out_morph_sorts1[ret] if ret else ''}")
                for i in range(len(axioms1)):
                    axioms1[i] = re.sub(rf"(?=\b|.){morph_ops1[o0]}(\b|.)", f"{o0}", axioms1[i])
                for i in range(len(axioms2)):
                    axioms2[i] = re.sub(rf"(?=\b|.){morph_ops2[o0]}(\b|.)", f"{o0}", axioms2[i])
        for k, v in dic_ops1.items():
            o0, sig = k.split(":")
            ret = None
            if "->" in sig:
                sig, ret = sig.split("->")
            sig = [out_morph_sorts1[s] if s in out_morph_sorts1.keys() else s for s in sig.split("*")]
            if v:
                out_morph_ops1[k] = f"_1_{o0}:{'*'.join(sig)}{'->' + out_morph_sorts1[ret] if ret else ''}"
                new_spec.ops.append(f"_1_{o0}:{'*'.join(sig)}{'->' + out_morph_sorts1[ret] if ret else ''}")
                for i in range(len(axioms1)):
                    axioms1[i] =  re.sub(rf"(?=\b|.){o0}(\b|.)", f"_1_{o0}", axioms1[i])
        for k, v in dic_ops2.items():
            o0, sig = k.split(":")
            ret = None
            if "->" in sig:
                sig, ret = sig.split("->")
            sig = [out_morph_sorts2[s] if s in out_morph_sorts2.keys() else s for s in sig.split("*")]
            if v:
                out_morph_ops2[k] = f"_2_{o0}:{'*'.join(sig)}{'->' + out_morph_sorts2[ret] if ret else ''}"
                new_spec.ops.append(f"_2_{o0}:{'*'.join(sig)}{'->' + out_morph_sorts2[ret] if ret else ''}")
                for i in range(len(axioms2)):
                    axioms2[i] =  re.sub(rf"(?=\b|.){o0}(\b|.)", f"_2_{o0}", axioms2[i])

        # Add axioms
        new_spec.axioms = axioms1 + axioms2
        new_spec._encode()

        # Pushout morphisms
        f1 = (out_morph_sorts1, out_morph_preds1, out_morph_ops1)
        f2 = (out_morph_sorts2, out_morph_preds2, out_morph_ops2)
        return (f1, new_spec, f2)

    def axiom_elimination_operator(self):
        """ Removes one axiom at a time, both the decoded and normal version of it """
        res = []
        for _a, a in zip(self._axioms, self.axioms):
            new_spec = copy.deepcopy(self)
            new_spec.axioms.remove(a)
            new_spec._axioms.remove(_a)
            #new_spec._tidy_signature()
            res.append(new_spec)
        return res


if __name__ == "__main__":

    csp1 = CASLSpecification()
    csp1.read_from_file("CASL Specifications\specs\I.txt")
    
    csp2 = CASLSpecification()
    csp2.read_from_file("CASL Specifications\specs\J.txt")

    gen = CASLSpecification()
    gen.read_from_file("CASL Specifications\specs\G.txt")

    f1 = gen.get_morphisms(gen.f1)
    f2 = gen.get_morphisms(gen.f2)
    print(gen.disjoint_union(csp1, csp2, f2, f1)[1])
