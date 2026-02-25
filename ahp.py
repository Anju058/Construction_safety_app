import numpy as np

# Random Index values
RI_DICT = {
    1: 0.00,
    2: 0.00,
    3: 0.58,
    4: 0.90,
    5: 1.12,
    6: 1.24,
    7: 1.32,
    8: 1.41,
    9: 1.45,
    10: 1.49
}

# 9 Construction Hazard Categories
HAZARD_NAMES = [
    'Physical Hazards',
    'Electrical Hazards',
    'Machinery Hazards',
    'Chemical Hazards',
    'Environmental Hazards',
    'Fire & Explosion Hazards',
    'Ergonomic Hazards',
    'Biological Hazards',
    'Organizational Hazards'
]

SHORT_NAMES = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']


def build_matrix_from_comparisons(comparisons_dict, n=9):
    """Build pairwise comparison matrix from user inputs.
    
    Args:
        comparisons_dict: Dictionary with keys like 'h0_h1', 'h0_h2', etc.
                          Values are floats (1-9 scale)
        n: Matrix dimension (default 9 for 9 hazards)
    
    Returns:
        numpy array: n x n pairwise comparison matrix
    """
    # Initialize matrix with 1s on diagonal
    matrix = np.ones((n, n), dtype=float)
    
    # Fill upper triangle from user inputs
    for i in range(n):
        for j in range(i + 1, n):
            key = f'h{i}_h{j}'
            if key in comparisons_dict:
                try:
                    value = float(comparisons_dict[key])
                    # Validate value is between 1 and 9
                    if 1 <= value <= 9:
                        matrix[i][j] = value
                        matrix[j][i] = 1 / value  # Reciprocal rule
                except (ValueError, TypeError):
                    # Skip invalid values
                    pass
    
    return matrix


def calculate_ahp(matrix):
    """Calculate AHP weights from pairwise comparison matrix.
    
    Args:
        matrix: n x n pairwise comparison matrix (numpy array or list)
    
    Returns:
        tuple: (hazard_names, weights, lambda_max, CI, CR, consistency_status)
            - hazard_names: List of hazard category names
            - weights: Normalized priority weights (sum = 1)
            - lambda_max: Maximum eigenvalue
            - CI: Consistency Index
            - CR: Consistency Ratio
            - consistency_status: 'Consistent' if CR < 0.1, else 'Review Needed'
    """
    matrix = np.array(matrix, dtype=float)
    n = matrix.shape[0]

    # Eigenvalue decomposition
    eigenvalues, eigenvectors = np.linalg.eig(matrix)
    
    # Find maximum eigenvalue and corresponding eigenvector
    lambda_max = np.max(eigenvalues.real)
    max_index = np.argmax(eigenvalues.real)
    weights = eigenvectors[:, max_index].real
    
    # Normalize weights so sum = 1
    weights = weights / np.sum(weights)

    # Consistency Index
    CI = (lambda_max - n) / (n - 1)

    # Consistency Ratio
    RI = RI_DICT[n]
    CR = CI / RI if RI != 0 else 0
    
    # Consistency Status
    consistency_status = 'Consistent' if CR < 0.1 else 'Review Needed'

    return HAZARD_NAMES, weights, lambda_max, CI, CR, consistency_status
