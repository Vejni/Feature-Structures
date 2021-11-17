from nltk.featstruct import FeatStruct


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
        else:
            if test(value):
                return tuple(path + [feature, value])
    return None

def find_all_subsorts(fs, sorts):
    """ Finds all paths to nodes which have supersorts by calling find_matching iteratively using the correct test """
    all_subsort_paths = []
    while (path := find_matching(fs, test = lambda x: x in sorts.keys())) is not None:
        all_subsort_paths.append(path)
        fs[path[:-1]] = sorts[path[-1]]
    return all_subsort_paths

def find_all_leaves(fs):
    """ Finds all paths to leaf nodes by calling find_matching iteratively using the correct test """
    all_leaf_paths = []
    while (path := find_matching(fs, test = lambda x: True)) is not None:
        all_leaf_paths.append(path)
        del fs[path[:-1]]
    return all_leaf_paths

def find_all_structs(fs):
    """ Finds all paths to non-leaf nodes by calling find_struct_matching iteratively using the correct t est """
    all_branch_paths = []
    while (path := find_struct_matching(fs, test = lambda x: True)) is not None:
        all_branch_paths.append(path)
        del fs[path]
    return  all_branch_paths

def find_all_branchnodes(fs):
    """ Finds all paths to non-leaf nodes that have more than 1 edges by calling find_struct_matching iteratively using the correct t est """
    all_branch_paths = []
    while (path := find_struct_matching(fs, test = lambda x: len(x.values()) > 1)) is not None:
        all_branch_paths.append(path)
        del fs[path]
    return  all_branch_paths

if __name__ == "__main__":
    fs1 = FeatStruct(number="singular", person=3)
    fs = FeatStruct(
        case1 = fs1, 
        case2 = FeatStruct(number=fs1, person=2)
    )

    # sort hierarchy could be represented via dictionaries
    # key is subsort of the value
    sorts = {
        2: "integer",
        3: "integer"
    }

    print(find_all_branchnodes(fs))
