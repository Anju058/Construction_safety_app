from ahp import build_matrix_from_comparisons, calculate_ahp
import numpy as np

# Test 1: Build a simple matrix
comparisons = {
    'h0_h1': 3,
    'h0_h2': 5,
    'h1_h2': 2,
}

# Expand to 9x9 format with defaults
for i in range(9):
    for j in range(i+1, 9):
        key = f'h{i}_h{j}'
        if key not in comparisons:
            comparisons[key] = 1.0

matrix = build_matrix_from_comparisons(comparisons, n=9)
print("Matrix shape:", matrix.shape)
print("Matrix diagonal (should be all 1s):", np.diag(matrix))
print("Matrix[0,1]:", matrix[0,1], "Matrix[1,0]:", matrix[1,0], "(should be reciprocals)")

# Test 2: Calculate AHP
names, weights, lambda_max, CI, CR, status = calculate_ahp(matrix)
print("\nAHP Results:")
print("Hazards count:", len(names))
print("Weights sum:", sum(weights))
print("Lambda max:", lambda_max)
print("CI:", CI)
print("CR:", CR)
print("Status:", status)
print("\nWeights by hazard:")
for i, (name, weight) in enumerate(zip(names, weights)):
    print(f"  {i+1}. {name}: {weight:.4f} ({weight*100:.2f}%)")
