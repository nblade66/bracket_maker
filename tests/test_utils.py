from BracketMaker.utils import interleave

def test_equal_length():
    assert interleave([1, 3], [2, 4]) == [1, 2, 3, 4]

def test_first_longer():
    assert interleave(['A', 'B'], ['X']) == ['A', 'X', 'B']

def test_second_longer():
    assert interleave(['A'], ['X', 'Y']) == ['A', 'X', 'Y']

def test_much_longer():
    assert interleave([1, 2, 3, 4, 5], [6, 7]) == [1, 6, 2, 7, 3, 4, 5]

def test_empty_inputs():
    assert interleave([], []) == []

def test_one_empty():
    assert interleave(['A'], []) == ['A']
    assert interleave([], ['X']) == ['X']
