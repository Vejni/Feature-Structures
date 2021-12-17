from nltk.featstruct import FeatStruct as FeatStruct

def init_FeatStruct(root, features=None, **morefeatures):
    """
    Needed to set root names of feature structures
    """
    fs = FeatStruct(features, **morefeatures)
    fs.__setattr__("root", root)
    return  fs

def fs_copy(fs):
    def _fs_copy(temp, fs):
        for (_, temp_val), (_, val) in zip(temp.items(), fs.items()):
            if isinstance(val, FeatStruct):
                temp_val.__setattr__("root", val.root)
                _fs_copy(temp_val, val)


    temp = fs.copy()
    temp.__setattr__("root", fs.root)

    # Set attributes again
    _fs_copy(temp, fs)

    return temp


def find_struct_matching(fs, test, path = []):
    """ 
    Finds the path and value of the first node matching our criterion
    in depth first search order. Works recursively. 
    Reentrances supported but I don't know why.
    Returns (None, None) if no node have been found.
    """
    for feature, value in fs.items():
        if isinstance(value, FeatStruct):
            p = find_struct_matching(value, test, path + [feature])
            if test(value):
                if p is None:
                    return tuple(path + [feature])
                else:
                    return p  
    return None


def find_matching(fs, test, path = []):
    """ 
    Finds the path and value of the first node matching our criterion
    in depth first search order. Works recursively. 
    Reentrances supported but I don't know why.
    Returns (None, None) if no node have been found.
    """
    for feature, value in fs.items():
        if isinstance(value, FeatStruct):
            p = find_matching(value, test, path + [feature])
            if p is not None:
                return p
            elif test(value.root):
                return path + [feature]
        else:
            if test(value):
                return tuple(path + [feature, value])
    return None

def find_all(fs, test):
    """ Finds all paths to nodes which have supersorts by calling find_matching iteratively using the correct test """
    fs = fs_copy(fs)
    all_paths = []
    while (path := find_matching(fs, test = test)) is not None:
        all_paths.append(path)
        if isinstance(path, tuple):
            fs[path[:-1]] = None
        else:
            fs[tuple(path)].root = None
    return all_paths

def find_all_structs(fs):
    """ Finds all paths to non-leaf nodes by calling find_struct_matching iteratively using the correct test """
    fs = fs_copy(fs)
    all_branch_paths = []
    while (path := find_struct_matching(fs, test = lambda x: True)) is not None:
        all_branch_paths.append(path)
        del fs[path]
    return  all_branch_paths

def gen_step(fs, sorts):
    fs = fs_copy(fs)
    if (path := find_matching(fs, test = lambda x: x in sorts.keys())) is not None:
        fs[path[:-1]] = sorts[path[-1]]
    return fs

def get_all_sort_generalizations(fs, sorts):
    paths = find_all(fs, test = lambda x: x in sorts.keys())
    result = []
    for p in paths:
        temp = fs_copy(fs)
        if isinstance(p, tuple):
            temp[p[:-1]] = sorts[p[-1]]
        else:
            temp[tuple(p)].root = sorts[temp[tuple(p)].root]
        result.append(temp)
    return result

def get_all_variable_eliminations(fs, sorts):
    paths = find_all(fs, test = lambda x: x in sorts.values())
    result = []
    for p in paths:
        temp = fs_copy(fs)
        if isinstance(p, tuple) and not isinstance(temp[p[:-1]], FeatStruct):
            del temp[p[:-1]]
            result.append(temp)
        elif not isinstance(temp[tuple(p)], FeatStruct):
            del temp[tuple(p)]
            result.append(temp)
    return result
    
def get_all_variable_equality_eliminations(fs, name="_copy"):
    reentrances = fs._find_reentrances({})
    if not any(reentrances.values()):
        return []

    paths = find_all_structs(fs)
    result = []
    temp = fs_copy(fs) 
    for f in fs.walk():
        if reentrances[id(f)]:
            f_temp = fs_copy(f)
            f_temp.__setattr__("root", f.root + name)

            # Need to find the path
            for p in paths:
                if fs[p] == f:
                    temp[p] = f_temp
                    break

            result.append(temp)
            temp = fs_copy(fs)

    return result


if __name__ == "__main__":
    icon1 = init_FeatStruct(root = "icon", leftside = init_FeatStruct( root = "Silhouette", right = "Rightarrow"), rightside="Silhouette")
    icon2 = init_FeatStruct(root = "icon", rightside = init_FeatStruct( root = "Silhouette", left = "Leftarrow"), leftside="Silhouette")

    sorts = {
        "Rightarrow": "Arrow",
        "Leftarrow": "Arrow",
        "Arrow": "Symbol",
        "Silhouette": "Symbol"
    }


    fs = get_all_sort_generalizations(icon1, sorts)
    for f in fs:
        print(get_all_variable_eliminations(f, sorts))
    
    f = init_FeatStruct(root="reentrant", feature="value")
    fs = init_FeatStruct(root="root", left=f, right=init_FeatStruct(root="mid", a=f))
    print(fs)

    print(get_all_variable_equality_eliminations(fs))