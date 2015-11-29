

def test_eq_ne_hash(left, right, *, is_equal: bool):
    assert is_equal == (left == right)
    assert is_equal == (right == left)
    assert is_equal != (left != right)
    assert is_equal != (right != left)

    assert is_equal == (hash(left) == hash(right))
    assert is_equal == (hash(right) == hash(left))
    assert is_equal != (hash(left) != hash(right))
    assert is_equal != (hash(right) != hash(left))

# Later: test_le(), test_eq_and_le()
