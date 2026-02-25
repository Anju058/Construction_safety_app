"""Test COS budget allocation with AHP weights"""
from ahp import build_matrix_from_comparisons, calculate_ahp
from cos import calculate_budget_allocation

# Get AHP weights
form_data = {}
for i in range(9):
    for j in range(i+1, 9):
        form_data[f'h{i}_h{j}'] = 1.0  # All equal

matrix = build_matrix_from_comparisons(form_data, n=9)
names, weights, lambda_max, CI, CR, status = calculate_ahp(matrix)

# Test budget allocation
total_budget = 100000
allocation = calculate_budget_allocation(total_budget, weights)

print("=== Budget Allocation Test ===")
print(f"Total Budget: ${total_budget:,.2f}")
print("\nAllocations:")
for i, (name, amount) in enumerate(zip(names, allocation)):
    pct = (amount / total_budget) * 100
    print(f"  {i+1}. {name:30s} ${amount:>12,.2f} ({pct:5.1f}%)")

print(f"\nVerification:")
print(f"  Total allocated: ${sum(allocation):,.2f}")
print(f"  Matches budget:  {abs(sum(allocation) - total_budget) < 0.01}")
