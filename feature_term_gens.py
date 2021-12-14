from nltk.featstruct import FeatStruct as FeatStruct

def init_FeatStruct(root, features=None, **morefeatures):
    """
    Needed to set root names of feature structures
    """
    fs = FeatStruct(features, **morefeatures)
    fs.__setattr__("root", root)
    return  fs


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


def find_matching(fs, all_paths, test, path = []):
    """ 
    Finds the path and value of the first node matching our criterion
    in depth first search order. Works recursively. 
    Reentrances supported but I don't know why.
    Returns (None, None) if no node have been found.
    """
    for feature, value in fs.items():
        if isinstance(value, FeatStruct):
            p = find_matching(value, all_paths, test, path + [feature])
            if p is not None and p not in all_paths:
                return p
            elif test(value.root):
                p = path + [feature]
                if p not in all_paths:
                    return p
        else:
            if test(value):
                p = tuple(path + [feature, value])
                if p not in all_paths:
                    return p
    return None

def find_all(fs, test):
    """ Finds all paths to nodes which have supersorts by calling find_matching iteratively using the correct test """
    all_paths = []
    while (path := find_matching(fs, all_paths, test = test)) is not None:
        all_paths.append(path)
    return all_paths

def find_all_structs(fs):
    """ Finds all paths to non-leaf nodes by calling find_struct_matching iteratively using the correct test """
    fs = fs.copy()
    all_branch_paths = []
    while (path := find_struct_matching(fs, test = lambda x: True)) is not None:
        all_branch_paths.append(path)
        del fs[path]
    return  all_branch_paths

def gen_step(fs, sorts):
    fs = fs.copy()
    if (path := find_matching(fs, test = lambda x: x in sorts.keys())) is not None:
        fs[path[:-1]] = sorts[path[-1]]
    return fs

def get_all_sort_generalizations(fs, sorts):
    paths = find_all(fs, test = lambda x: x in sorts.keys())
    result = []
    for p in paths:
        temp = fs.copy()
        temp[p[:-1]] = sorts[p[-1]]
        result.append(temp)
    return result

def get_all_variable_eliminations(fs, sorts):
    paths = find_all(fs, test = lambda x: x in sorts.values())
    result = []
    for p in paths:
        temp = fs.copy()
        del temp[p[:-1]]
        result.append(temp)
    return result
    
def get_all_variable_equality_eliminations(fs):
    paths = []
    result = []   


if __name__ == "__main__":
    icon1 = init_FeatStruct(root = "icon", leftside = init_FeatStruct( root = "Silhouette", right = "Rightarrow"), rightside="Silhouette")
    icon2 = init_FeatStruct(root = "icon", rightside = init_FeatStruct( root = "Silhouette", left = "Leftarrow"), leftside="Silhouette")

    sorts = {
        "Rightarrow": "Arrow",
        "Leftarrow": "Arrow",
        "Arrow": "Symbol",
        "Silhouette": "Symbol"
    }


    print(icon1)
    print(get_all_sort_generalizations(icon1, sorts))