import pytest
import operators as op
from nltk.featstruct import FeatStruct as FeatStruct

def test_init_FeatStruct():
    fs_orig = FeatStruct(leftside = "Left", middle = FeatStruct(feature = "value"), rightside = "Right")
    fs_custom = op.init_FeatStruct(root = "root1", leftside = "Left", middle = op.init_FeatStruct(root = "root2", feature = "value"), rightside = "Right")

    assert fs_orig == fs_custom
    assert fs_custom.root == "root1"
    assert fs_custom["middle"].root == "root2"

def test_fs_copy():
    fs = op.init_FeatStruct(root = "root1", leftside = "Left", middle = op.init_FeatStruct(root = "root2", feature = "value"), rightside = "Right")
    fs_copy = op.fs_copy(fs)

    assert fs == fs_copy
    assert fs_copy.root == "root1"
    assert fs_copy["middle"].root == "root2"

def test_get_all_paths():
    fs = op.init_FeatStruct(root = "root1", leftside = "Left", middle = op.init_FeatStruct(root = "root2", feature = "value"), rightside = "Right")
    paths = op.get_all_paths(fs, only_leaves=False)
    leaves = op.get_all_paths(fs, only_leaves=True)

    assert [('leftside', 'Left'), ('middle', 'feature', 'value'), ['middle'], ('rightside', 'Right')] == paths
    assert [('leftside', 'Left'), ('middle', 'feature', 'value'), ('rightside', 'Right')] == leaves

    # Try with reentrance
    fs1 = op.init_FeatStruct(root = "root3", f = "value")
    fs = op.init_FeatStruct(root = "root1", leftside = "Left", middle = op.init_FeatStruct(root = "root2", feature = fs1), rightside = fs1)
    paths = op.get_all_paths(fs, only_leaves=False)
    leaves = op.get_all_paths(fs, only_leaves=True)

    assert [('leftside', 'Left'), ('middle', 'feature', 'f', 'value'), ['middle', 'feature'], ['middle']] == paths
    assert [('leftside', 'Left'), ('middle', 'feature', 'f', 'value')] == leaves

def test_get_all_sort_generalizations():
    assert False

def test_get_all_variable_eliminations():
    assert False

def test_get_all_variable_equality_eliminations():
    assert False

def test_get_all_root_variable_equality_eliminations():
    assert False
