import numpy as np


class CumSumCalculator:
    @staticmethod
    def get_cumsum(cube: np.ndarray, kernel_size: int) -> np.array:
        cube = np.hstack([np.zeros((cube.shape[0], kernel_size)), cube])
        cube = np.cumsum(cube, axis=1)
        cube = cube[:, kernel_size:] - cube[:, :-kernel_size]
        return cube / kernel_size
