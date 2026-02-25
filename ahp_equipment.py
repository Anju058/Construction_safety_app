import numpy as np


EQUIPMENT_NAMES = [
    'Personal Protective Equipment (PPE)',
    'Site Safety & Protection Systems',
    'Machinery & Electrical Safety',
    'Helmets'
]


def build_equipment_matrix(comparisons):
    """
    Build a 4x4 pairwise comparison matrix from provided comparisons.

    comparisons: dict with keys: 'A_B','A_C','A_D','B_C','B_D','C_D'
    Values are numeric (Saaty 1-9)
    """
    n = 4
    mat = np.ones((n, n), dtype=float)

    # mapping indices
    idx = {
        ('A', 'B'): (0, 1),
        ('A', 'C'): (0, 2),
        ('A', 'D'): (0, 3),
        ('B', 'C'): (1, 2),
        ('B', 'D'): (1, 3),
        ('C', 'D'): (2, 3),
    }

    for key, (i, j) in idx.items():
        k = f"{key[0]}_{key[1]}"
        if k in comparisons:
            try:
                val = float(comparisons[k])
                if val <= 0:
                    val = 1.0
            except Exception:
                val = 1.0
        else:
            val = 1.0

        mat[i, j] = val
        mat[j, i] = 1.0 / val

    return mat


def calculate_equipment_ahp(matrix):
    """Calculate AHP using eigen method for the equipment matrix.

    Returns: (equipment_names, weights, lambda_max, CI, CR, consistency_status)
    """
    n = matrix.shape[0]
    eigenvalues, eigenvectors = np.linalg.eig(matrix)

    # consider real parts (matrix should be positive reciprocal, eigenvalues real)
    eigvals_real = eigenvalues.real
    max_idx = int(np.argmax(eigvals_real))
    lambda_max = eigvals_real[max_idx]

    principal_eigvec = eigenvectors[:, max_idx].real
    # ensure non-negative
    principal_eigvec = np.abs(principal_eigvec)

    weights = principal_eigvec / np.sum(principal_eigvec)

    CI = (lambda_max - n) / (n - 1)
    RI = 0.90  # given for n=4
    CR = CI / RI if RI != 0 else float('inf')
    consistency_status = CR < 0.1

    return EQUIPMENT_NAMES, weights, float(lambda_max), float(CI), float(CR), consistency_status
