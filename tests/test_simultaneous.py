import numpy as np
from thesis_functions.simultaneous import get_indices_of_simultaneous_event


def test_single_simultaneous_event():
    a = np.array([[0.00, 1.00, 2.00, 3.00]])
    b = np.array([[0.10, 0.90, 2.01, 3.10]])

    index_a, index_b = get_indices_of_simultaneous_event(a, b, tol=0.01)

    assert index_a == np.array([3])
    assert index_b == np.array([3])


def test_multiple_simultaneous_event():
    a = np.array([[0.00, 1.00, 2.00, 3.00]])
    b = np.array([[0.01, 0.90, 2.01, 1.01]])

    index_a, index_b = get_indices_of_simultaneous_event(a, b, tol=0.01)

    assert index_a == np.array([0, 3, 1])
    assert index_b == np.array([0, 3, 4])
