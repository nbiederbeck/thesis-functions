import numpy as np
import pandas as pd

from thesis_functions.intersection import get_same_indices


def test_indices():
    """ Es sollten folgende Runs übereinstimmen:

    | d1 | d2 |
    |----|----|
    | 200| 501|
    | 300| 502|
    | 400| 502|

    An diesen Indices:

    | d1 | d2 |
    |----|----|
    |  1 |  1 |
    |  2 |  2 |
    |  3 |  2 |
    """
    index_solution1 = np.array([1, 2, 3])
    index_solution2 = np.array([1, 2, 2])

    run_solution1 = np.array([200, 300, 400])
    run_solution2 = np.array([501, 502, 502])

    sl = {
        "night": [20131128, 20131128, 20131129, 20131129],
        "run_number": [100, 200, 300, 400],
        "run_start": [1, 2, 3, 4],
        "run_stop": [1.5, 2.5, 3.5, 4.5],
    }
    d1 = pd.DataFrame(sl)

    sl = {
        "night": [20131128, 20131129, 20131129],
        "run_number": [500, 501, 502],
        "run_start": [1.6, 2, 2.9],
        "run_stop": [1.9, 2.4, 4.1],
    }
    d2 = pd.DataFrame(sl)

    indices1, indices2 = get_same_indices(d1, d2)

    # Check if indices are correct
    assert (indices1 == index_solution1).all() == True
    assert (indices2 == index_solution2).all() == True

    # Check if number of matches is correct
    assert len(indices1) == len(indices2) == 3

    # Check if run_numbers at indices are correct
    assert (d1.iloc[indices1].run_number == run_solution1).all() == True
    assert (d2.iloc[indices2].run_number == run_solution2).all() == True
