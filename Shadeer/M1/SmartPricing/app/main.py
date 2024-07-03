import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from budget_class import BudgetAllocation
import plotly.express as px
import random

# Assuming the BudgetAllocation class code is already imported or defined here
# RUN USING
##  streamlit run main.py

st.title('Budget Allocation')


# Sidebar for input parameters
st.sidebar.header('Input Parameters')

# Initialize session state variables if they are not already set
if 'base_budget_percent' not in st.session_state:
    st.session_state['base_budget_percent'] = 0.7
if 'premium_budget_percent' not in st.session_state:
    st.session_state['premium_budget_percent'] = 0.3

# Function to update premium budget based on base budget
def update_premium():
    st.session_state.premium_budget_percent = 1 - st.session_state.base_budget_percent

# Total budget input
total_budget = st.sidebar.number_input('Enter the Initial total budget', value=2000, step=100)

# Base budget percentage slider with callback to update premium budget
base_budget_percent = st.sidebar.slider(
    'Base Budget Percentage', min_value=0.0, max_value=1.0,
    value=st.session_state.base_budget_percent, step=0.01,
    on_change=update_premium, key='base_budget_percent'
)          

# Premium budget percentage slider
premium_budget_percent = st.sidebar.slider(
    'Premium Budget Percentage', min_value=0.0, max_value=1.0,
    value=st.session_state.premium_budget_percent, step=0.01,
    key='premium_budget_percent'
)

# st.sidebar.header('Redemption Parameters')
minimum_spent = st.sidebar.slider('Minimum spent', min_value=0, max_value=100, value=0, step=1)

if 'budget_allocation' not in st.session_state:
    print("Initializing budget allocation...", total_budget)
    st.session_state.budget_allocation = BudgetAllocation(total_budget, base_budget_percent, premium_budget_percent, [0, 0.5, 0.8, 1])

# def compute_and_plot_rewards(budget_allocation):
#     # BA = st.session_state.budget_allocation
#     # BA.calculate_rewards()
#     # print("BA", BA.total_budget)
#     df = budget_allocation.ABC_analysis_df()
#     print("inside total budget", budget_allocation.total_budget)
#     summary = budget_allocation.summary()
#     print("summary", summary)
#     reward_premium = summary['Total Premium Reward']
#     reward_premium = float(reward_premium.replace('$', ''))

#     base_reward = 1.07
#     base_reward = summary['Average Base Reward']
#     base_reward = float(base_reward.replace('$', ''))

#     def compute_reward(min_spent):
#         order_value = df['Order Value']
#         is_prem_claimed = df[(df['is_premium'] == True) & (order_value > min_spent)].shape[0]
#         is_base_claimed = df[(df['is_premium'] == False) & (order_value > min_spent)].shape[0]
#         total_reward = (is_prem_claimed * reward_premium) + (is_base_claimed * base_reward)
#         return total_reward, is_prem_claimed, is_base_claimed

#     min_spent_values = range(0, 500, 10)
#     results = [compute_reward(min_spent) for min_spent in min_spent_values]
#     results_df = pd.DataFrame({
#         'Minimum Spent': min_spent_values,
#         'Total Reward': [result[0] for result in results],
#         'Premium Claims': [result[1] for result in results],
#         'Base Claims': [result[2] for result in results]
#     })
    
    

#     fig = px.line(results_df, x='Minimum Spent', y='Total Reward',
#                   title='Impact of Minimum Spent on Total Rewards',
#                   labels={'Total Reward': 'Total Reward ($)', 'Minimum Spent': 'Minimum Spent ($)'})
#     fig.update_traces(mode='lines+markers', hoverinfo='text')
#     fig.update_traces(text=["Premium Claims: {}<br>Base Claims: {}".format(p, b) for p, b in zip(results_df['Premium Claims'], results_df['Base Claims'])])
#     return fig



abc_split = [0, 0.5, 0.8, 1]  # Keeping this static as per your request

# Create an instance of BudgetAllocation
budget_allocation = BudgetAllocation(total_budget, base_budget_percent, premium_budget_percent, abc_split)

if st.button('Calculate Rewards'):
    budget_allocation.calculate_rewards()
    summary_data = budget_allocation.summary()
    # budget_allocation.total_budget()
    # print("AOSD", budget_allocation.total_budget)
    # fig = compute_and_plot_rewards(budget_allocation)
    # st.plotly_chart(fig)
    # Plotting  
    # fig, ax = plt.subplots()
    # ax.hist(budget_allocation.customers['total_reward'], bins=30, alpha=0.7, label='Total Reward')
    # ax.hist(budget_allocation.customers['base_reward'], bins=30, alpha=0.7, label='Base Reward', color='r')
    # ax.set_title('Distribution of Rewards')
    # ax.set_xlabel('Reward Amount ($)')
    # ax.set_ylabel('Number of Customers')
    # ax.legend()
    # st.pyplot(fig)

    
    # Display the summary data
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Budget Information")
        st.markdown(f"**Total Budget: {summary_data['Total Budget']}**")
        st.markdown(f"**Base Budget: {summary_data['Base Budget']}**")
        st.markdown(f"**Premium Budget: {summary_data['Premium Budget']}**")
        st.divider()
    with col2:
        st.subheader("Customer Information")
        st.markdown(f"**Number of Premium Customers: {summary_data['Number of Premium Customers']}**")
        st.markdown(f"**Number of Total Unique Customers: {summary_data['Number of Total Unique Customers']}**")

    st.subheader("Reward Information")
    # st.markdown(f"**Average Base Reward: {summary_data['Average Base Reward']}**")
    st.markdown(f"**Average Base Reward:** <span style='font-size: 30px;'>{summary_data['Average Base Reward']}</span>", unsafe_allow_html=True)

    st.markdown(f"**Average Extra value for Premium Customer: {summary_data['Average Extra value for Premium Customer']}**")
    st.markdown(f"**Total Premium Reward: {summary_data['Total Premium Reward']}**")
    
    
    BA = BudgetAllocation(total_budget=1000, base_budget_percent=0.7, premium_budget_percent=0.3, abc_split=[0, 0.5, 0.8, 1])


# This section could be expanded with more functionality or analysis as needed
