from nltk.featstruct import FeatStruct as FeatStruct

def init_FeatStruct(root, features=None, **morefeatures):
    """
    Needed to set root names of feature structures
    """
    fs = FeatStruct(features, **morefeatures)
    fs.__setattr__("root", root)
    return  fs

def fs_copy(fs):
    """
    Does a deep copy, keeping the rootnames
    """
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

def get_all_paths(fs, only_leaves=False):
    """
    Gets all paths of the feature struct recurisvely.
    """
    # Recursive Function
    def _get_all_paths(fs, only_leaves, path=[]):
        for feature, value in fs.items():
            if isinstance(value, FeatStruct):
                p = _get_all_paths(value, only_leaves, path + [feature])
                if p is not None:
                    return p
                elif not only_leaves and value.root is not None:
                    return path + [feature]
            else:
                return tuple(path + [feature, value])
        return None

    # The call
    fs = fs_copy(fs)
    all_paths = []
    while (path := _get_all_paths(fs, only_leaves=only_leaves)) is not None:
        if isinstance(path, tuple):
            del fs[path[:-1]]
        else:
            fs[tuple(path)].root = None
        all_paths.append(path)
    return all_paths

def get_all_sort_generalizations(fs, sorts):
    """
    Generates all possible generalizations by replacing with sort supertypes.
    """
    result = []

    # Check root
    if fs.root in sorts.keys():
        temp = fs_copy(fs)
        temp.root = sorts[fs.root]
        result.append(temp)

    # For all paths
    paths = get_all_paths(fs, only_leaves=False)
    for p in paths:
        sort = p[-1] if isinstance(p, tuple) else fs[tuple(p)].root
        if sort in sorts.keys():
            temp = fs_copy(fs)
            if isinstance(p, tuple):
                temp[p[:-1]] = sorts[p[-1]]
            else:
                temp[tuple(p)].root = sorts[temp[tuple(p)].root]
            result.append(temp)
    return result

def get_all_variable_eliminations(fs, sorts):
    """
    Generates all possible variable eliminations.
    """
    result = []

    # Check root
    if not len(fs.keys()) and fs.root not in sorts.keys():
        temp = fs_copy(fs)
        temp.root = sorts[fs.root]
        result.append(temp)

    # For all paths
    paths = get_all_paths(fs, only_leaves=True)
    for p in paths:
        sort = p[-1] if isinstance(p, tuple) else fs[tuple(p)].root
        if sort not in sorts.keys():
            temp = fs_copy(fs)
            del temp[p[:-1]]
            result.append(temp)
    return result
    
def get_all_variable_equality_eliminations(fs, name="_copy"):
    """
    Generates all possible generalizations by breaking variable inequality. Root not considered.
    TODO repeated reentrances all possibilities
    """

    # If there are no reentrances there is nothing to check
    reentrances = fs._find_reentrances({})
    if not any(reentrances.values()):
        return []

    # Need path for breaking equality
    paths = [tuple(p) for p in get_all_paths(fs, only_leaves=False) if isinstance(p, list)]
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
                    temp = fs_copy(fs)
                    result.append(temp)
                    break

    return result

def get_all_root_variable_equality_eliminations(fs, name="_copy"):
    """
    Split root variable equality
    """
    if len(fs.keys()) < 2:
        return []

    result = []
    temp = fs_copy(fs) 
    for f in fs.keys():
        root_copy = init_FeatStruct(fs.root + name, {f: fs[f]})
        del temp[f]
        root_fs = init_FeatStruct(root="new", root1=root_copy, root2=temp)
        result.append(root_fs)
        temp = fs_copy(fs)

    return result

def gen_step(fs, sorts):
    return 

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
    fs = init_FeatStruct(root="root", left=f, middle=init_FeatStruct(root="asd", b=f), right=init_FeatStruct(root="mid", a=f))
    print(fs)

    print(get_all_variable_equality_eliminations(fs))

    for i in get_all_root_variable_equality_eliminations(fs):
        print(i)