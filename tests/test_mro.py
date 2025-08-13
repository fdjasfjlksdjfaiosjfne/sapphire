"""
Test cases for Method Resolution Order (MRO) algorithm using pytest
"""
import pytest
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from backend import errors
from runtime.values import Type

def test_single_inheritance():
    """Test simple single inheritance chain"""
    
    # A -> B -> C
    A = Type("A")
    B = Type("B", [A])
    C = Type("C", [B])
    
    print(f"A.mro: {[cls.name for cls in A.mro]}")
    print(f"B.mro: {[cls.name for cls in B.mro]}")
    print(f"C.mro: {[cls.name for cls in C.mro]}")
    
    # Expected: A=[A], B=[B,A], C=[C,B,A]
    assert [cls.name for cls in A.mro] == ["A"]
    assert [cls.name for cls in B.mro] == ["B", "A"]
    assert [cls.name for cls in C.mro] == ["C", "B", "A"]

def test_diamond_inheritance():
    """Test classic diamond inheritance pattern"""
    
    #     A
    #    / \
    #   B   C
    #    \ /
    #     D
    A = Type("A")
    B = Type("B", [A])
    C = Type("C", [A])
    D = Type("D", [B, C])
    
    print(f"D.mro: {[cls.name for cls in D.mro]}")
    
    # Expected: D -> B -> C -> A (C3 linearization)
    expected = ["D", "B", "C", "A"]
    actual = [cls.name for cls in D.mro]
    assert actual == expected, f"Expected {expected}, got {actual}"

def test_complex_inheritance():
    """Test more complex inheritance hierarchy"""
    
    #      A
    #     / \
    #    B   C
    #   /   / \
    #  D   E   F
    #   \ / \ /
    #    G   H
    A = Type("A")
    B = Type("B", [A])
    C = Type("C", [A])
    D = Type("D", [B])
    E = Type("E", [C])
    F = Type("F", [C])
    G = Type("G", [D, E])
    H = Type("H", [E, F])
    
    print(f"G.mro: {[cls.name for cls in G.mro]}")
    print(f"H.mro: {[cls.name for cls in H.mro]}")
    
    # G should be: G -> D -> B -> E -> C -> A
    # H should be: H -> E -> F -> C -> A
    assert [cls.name for cls in G.mro] == ["G", "D", "B", "E", "C", "A"]
    assert [cls.name for cls in H.mro] == ["H", "E", "F", "C", "A"]

def test_multiple_inheritance():
    """Test multiple inheritance without diamonds"""
    
    # A  B  C
    #  \ | /
    #   \|/
    #    D
    A = Type("A")
    B = Type("B")
    C = Type("C")
    D = Type("D", [A, B, C])
    
    print(f"D.mro: {[cls.name for cls in D.mro]}")
    
    # Expected: D -> A -> B -> C
    expected = ["D", "A", "B", "C"]
    actual = [cls.name for cls in D.mro]
    assert actual == expected, f"Expected {expected}, got {actual}"

def test_impossible_mro():
    """Test case that should fail due to inconsistent MRO"""
    
    with pytest.raises(errors.SapphireError, match="Inconsistent MRO"):
        # Create a problematic hierarchy
        A = Type("A")
        B = Type("B", [A])
        C = Type("C", [A])
        # This creates an impossible linearization
        D = Type("D", [B, C])
        E = Type("E", [C, B])  # Reversed order
        F = Type("F", [D, E])  # This should fail

if __name__ == "__main__":
    # For running without pytest
    test_single_inheritance()
    test_diamond_inheritance() 
    test_complex_inheritance()
    test_multiple_inheritance()
    test_impossible_mro()
    print("All MRO tests passed HELL YEAH")
