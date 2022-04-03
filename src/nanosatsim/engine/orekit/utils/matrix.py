from numpy.typing import NDArray
import numpy as np
from numpy import array


def cross_product_matrix(x: NDArray[np.float64]) -> NDArray[np.float64]:
    return array([
        [0, -x[2], x[1]],
        [x[2], 0,  -x[0]],
        [-x[1], x[0], 0]], dtype=np.float64
    )
