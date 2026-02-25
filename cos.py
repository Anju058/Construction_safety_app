def calculate_budget_allocation(total_budget, risk_weights):
    """Allocate budget based on hazard risk weights.
    
    Args:
        total_budget: Total safety budget to allocate
        risk_weights: List of weights for each hazard category (should sum to 1)
    
    Returns:
        List of allocated amounts for each hazard category
    """
    allocation = []
    for weight in risk_weights:
        allocated = weight * total_budget
        allocation.append(allocated)
    return allocation


def calculate_total_cost(prevention_cost, accident_cost):
    """Calculate total safety cost (prevention + accident costs).
    
    Args:
        prevention_cost: Cost of prevention measures
        accident_cost: Cost of handling accidents
    
    Returns:
        Sum of prevention and accident costs
    """
    return prevention_cost + accident_cost
