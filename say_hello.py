import pyzig

pyzig.hello("Mee")

try:
    import numpy as np

    arr = np.zeros((1, 2, 3))
    pyzig.c_test.hello_buffer(arr)
except ImportError:
    pass
