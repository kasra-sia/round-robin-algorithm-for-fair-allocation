import pandas as pd

# Define the values for each item for each person with 9 items
items = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']

values = {
    1: {'A': 7, 'B': 6, 'C': 5, 'D': 4, 'E': 3, 'F': 2, 'G': 1, 'H': 8, 'I': 9},
    2: {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9},
    3: {'A': 8, 'B': 3, 'C': 8, 'D': 7, 'E': 6, 'F': 5, 'G': 1, 'H': 2, 'I': 3}
}


# Function to perform round-robin allocation
def round_robin_allocation(values):
    allocation = {1: [], 2: [], 3: []}
    items_remaining = set(items)

    # Round-robin order
    turn_order = [1, 2, 3] * ((len(items) + 2) // 3)

    for turn in turn_order:
        if not items_remaining:
            break

        # Choose the most valuable available item for the current player
        best_item = max(items_remaining, key=lambda x: values[turn][x])
        allocation[turn].append(best_item)
        items_remaining.remove(best_item)

    return allocation


# Function to calculate envy-freeness
def check_envy_freeness(allocation, values, preference_type):
    envy = {1: False, 2: False, 3: False}

    for i in range(1, 4):
        my_value = calculate_value(allocation[i], values[i], preference_type)
        for j in range(1, 4):
            if i != j:
                other_value = calculate_value(allocation[j], values[i], preference_type)
                if my_value < other_value:
                    envy[i] = True

    return envy


# Function to calculate the value of a bundle based on preference type
def calculate_value(bundle, values, preference_type):
    if preference_type == 'Additive':
        return sum(values[item] for item in bundle)
    elif preference_type == 'Semi-Additive':
        bonus = 0
        if 'A' in bundle and 'B' in bundle:
            bonus += 0.5
        return sum(values[item] for item in bundle) + bonus
    elif preference_type == 'Non-Additive':
        strong_combo = 0
        if 'A' in bundle and 'B' in bundle:
            strong_combo += 7  # Assuming a strong preference for this combination
        return sum(values[item] for item in bundle) + strong_combo
    return 0


# Perform round-robin allocation for each preference type and check envy-freeness
allocations = {}
envy_checks = {}

preference_types = ['Additive', 'Semi-Additive', 'Non-Additive']

for preference_type in preference_types:
    allocation = round_robin_allocation(values)
    envy = check_envy_freeness(allocation, values, preference_type)
    allocations[preference_type] = allocation
    envy_checks[preference_type] = envy

# Display results
allocations_df = pd.DataFrame(allocations)
envy_checks_df = pd.DataFrame(envy_checks)

print("Allocations:")
print(allocations_df)

print("\nEnvy Checks:")
print(envy_checks_df)
