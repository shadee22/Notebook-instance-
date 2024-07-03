import streamlit as st

# Function to calculate the results
def calculate_results(budget, allocation_percentage, minimum_spent_multiplier, total_customers, premium_customers):
    # Allocation
    all_customers_percentage = allocation_percentage
    premium_customers_percentage = 100 - allocation_percentage
    
    all_customers_budget = (all_customers_percentage / 100) * budget
    premium_customers_budget = (premium_customers_percentage / 100) * budget
    
    # Calculate the cashback offers
    all_customers_cashback = all_customers_budget / (total_customers - premium_customers)
    premium_customers_cashback = premium_customers_budget / premium_customers
    
    # Minimum spent calculation
    all_customers_min_spent = all_customers_cashback * minimum_spent_multiplier
    premium_customers_min_spent = premium_customers_cashback * minimum_spent_multiplier
    
    return {
        "all_customers_budget": all_customers_budget,
        "premium_customers_budget": premium_customers_budget,
        "all_customers_cashback": all_customers_cashback,
        "premium_customers_cashback": premium_customers_cashback,
        "all_customers_min_spent": all_customers_min_spent,
        "premium_customers_min_spent": premium_customers_min_spent
    }

# Streamlit application
st.title("Budget Allocation and Cashback Calculation")

# Sidebar inputs
budget = st.sidebar.number_input("Total Budget", value=5000, min_value=0)
allocation_percentage = st.sidebar.slider("Allocation Percentage to All Customers", min_value=0, max_value=100, value=70)
minimum_spent_multiplier = st.sidebar.number_input("Minimum Spent Multiplier", value=5, min_value=1)
total_customers = 1312
premium_customers = 656

# Calculate button
if st.sidebar.button("Calculate"):
    results = calculate_results(budget, allocation_percentage, minimum_spent_multiplier, total_customers, premium_customers)
    
    st.subheader("Results")
    st.write(f"Budget Allocation:")
    st.write(f"- All Customers: {results['all_customers_budget']} dollars ({allocation_percentage}%)")
    st.write(f"- Premium Customers: {results['premium_customers_budget']} dollars ({100 - allocation_percentage}%)")
    
    st.write(f"Cashback Offers:")
    st.write(f"- All Customers: {results['all_customers_cashback']} dollars")
    st.write(f"- Premium Customers: {results['premium_customers_cashback']} dollars")
    
    st.write(f"Minimum Spent:")
    st.write(f"- All Customers: {results['all_customers_min_spent']} dollars")
    st.write(f"- Premium Customers: {results['premium_customers_min_spent']} dollars")
