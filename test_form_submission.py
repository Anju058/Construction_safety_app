"""Test AHP form submission simulation"""
from ahp import build_matrix_from_comparisons, calculate_ahp

# Simulate user form submission
# Create sample comparisons (simulating form data)
form_data = {}
for i in range(9):
    for j in range(i+1, 9):
        # Sample: varied comparisons
        if i == 0:
            form_data[f'h{i}_h{j}'] = 3.0  # Physical much more important
        elif i == j-1:
            form_data[f'h{i}_h{j}'] = 1.5  # Slightly more important
        else:
            form_data[f'h{i}_h{j}'] = 1.0  # Equal

print("Form submitted with", len(form_data), "comparisons")

# Build matrix from form data
matrix = build_matrix_from_comparisons(form_data, n=9)
print("Matrix built successfully")

# Calculate AHP
names, weights, lambda_max, CI, CR, status = calculate_ahp(matrix)

print("\n=== AHP Results ===")
print(f"Status: {status} (CR = {CR:.4f})")
print("\nHazard Weights:")
for i, (name, weight) in enumerate(zip(names, weights)):
    print(f"  {i+1}. {name:30s} {weight:.4f} ({weight*100:6.2f}%)")

print(f"\nMetrics:")
print(f"  Lambda max:       {lambda_max:.4f}")
print(f"  Consistency Index: {CI:.4f}")
print(f"  Consistency Ratio: {CR:.4f}")
print(f"  Valid (CR < 0.1): {CR < 0.1}")
