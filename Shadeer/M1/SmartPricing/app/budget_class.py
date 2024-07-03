# Main function
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


import warnings
warnings.filterwarnings("ignore")


class BudgetAllocation:
    def __init__(self, total_budget, base_budget_percent, premium_budget_percent, abc_split):
        self.total_budget = total_budget
        self.base_percent = base_budget_percent
        self.premium_percent = premium_budget_percent
        self.abc_split = abc_split
        self.df_path = "/Users/shadeer/Desktop/HOME/AI/PulseID/Notebook-instance/Shadeer/M1/ai-api/DataSources/Final_for_smart_pricing.csv"
        self.customers = self.ABC_analysis_df()
        self.redeemed_reward = 0

    def ABC_analysis_df(self):    
        data = pd.read_csv(self.df_path, encoding='ISO-8859-1')

        # Drop rows where 'Order Value' is missing
        data_cleaned = data.dropna(subset=['Order Value'])

        # Calculate total order value per customer
        customer_order_totals = data_cleaned.groupby('UID')['Order Value'].sum()

        # Sort customers based on total order value
        customer_order_totals_sorted = customer_order_totals.sort_values(ascending=False)
        data_cleaned = data_cleaned.drop_duplicates(subset='UID')
        data_cleaned["total_spend"] = customer_order_totals.values

        df = data_cleaned
        abc = self.abc_split
        # abc = [0, 0.8, 0.9, 1]
        df['ABC_Category'] = pd.qcut(df['total_spend'], abc, labels=['C', 'B', 'A'], duplicates='drop')

        df['is_premium'] = df['ABC_Category'].isin(['B', 'A'])
        return df
        
    def calculate_rewards(self):
        base_budget = self.total_budget * self.base_percent
        premium_budget = self.total_budget * self.premium_percent
        num_customers = len(self.customers)

        self.customers['base_reward'] = base_budget / num_customers
        premium_customers = self.customers['is_premium'].sum()
        self.customers['premium_reward'] = 0
        self.customers.loc[self.customers['is_premium'], 'premium_reward'] = premium_budget / premium_customers
        self.customers['total_reward'] = self.customers['base_reward'] + self.customers['premium_reward']

    def plot_rewards(self):
        plt.figure(figsize=(10, 6))
        plt.hist(self.customers['total_reward'], bins=30, alpha=0.7, label='Total Reward')
        plt.hist(self.customers['base_reward'], bins=30, alpha=0.7, label='Base Reward', color='r')
        plt.title('Distribution of Rewards')
        plt.xlabel('Reward Amount ($)')
        plt.ylabel('Number of Customers')
        plt.legend()
        plt.show()
    
    def summary(self):
        max_base_reward = self.customers['base_reward'].max()
        max_premium_reward = self.customers[self.customers['is_premium']]['premium_reward'].max()
        total_reward = max_base_reward + max_premium_reward
        print(f"Total Budget: ${self.total_budget}")
        print(f"Base Budget: ${self.total_budget * self.base_percent}")
        print(f"Premium Budget: ${self.total_budget * self.premium_percent}")
        print("--------------------------------------------")
        print(f"Number of Premium Customers: {self.customers['is_premium'].sum()}")
        print(f"Number of Total Unique Customers: {len(self.customers)}")
        print("--------------------------------------------")

        print(f"Average Base Reward: ${self.customers['base_reward'].mean():.2f}")
        print(f"Average Extra value for Premium Customer: ${self.customers[self.customers['is_premium']]['premium_reward'].mean():.2f}")
        print(f"Total Premium Reward: ${total_reward}")
        

        max_base_reward = self.customers['base_reward'].max()
        max_premium_reward = self.customers[self.customers['is_premium']]['premium_reward'].max()
        total_reward = max_base_reward + max_premium_reward

        summary_dict = {
            "Total Budget": f"${self.total_budget}",
            "Base Budget": f"${self.total_budget * self.base_percent}",
            "Premium Budget": f"${self.total_budget * self.premium_percent}",
            "Number of Premium Customers": self.customers['is_premium'].sum(),
            "Number of Total Unique Customers": len(self.customers),
            "Average Base Reward": f"${self.customers['base_reward'].mean():.2f}",
            "Average Extra value for Premium Customer": f"${self.customers[self.customers['is_premium']]['premium_reward'].mean():.2f}",
            "Total Premium Reward": f"${total_reward}"
        }
        
        print("TOAL BUDGET IS: ", self.total_budget)

        return summary_dict
        # print("--------------------------------------------")
        # print(self.customers['is_premium'].value_counts())
        # print("--------------------------------------------")
        # print(self.customers['ABC_Category'].value_counts())


    def redemption(self, minimum_spent, reward_premium, base_reward):
        import pandas as pd
        df = self.ABC_analysis_df()
        order_value = df['Order Value']
        
        is_prem = df[df['is_premium']== True].shape[0]
        is_prem_claimed = df[(df['is_premium']== True) & (order_value > minimum_spent)].shape[0]
        is_base_claimed = df[(df['is_premium']== False) & (order_value > minimum_spent)].shape[0]

        total_reward = (is_prem_claimed * reward_premium) + (is_base_claimed * base_reward)
        self.redeemed_amount += total_reward
        self.total_budget -= self.redeemed_amount  # Update the total budget

        print(f"Redemption Summary:")
        print(f"Total Premium Customers: {is_prem}")
        print(f"Premium Customers Claimed: {is_prem_claimed}")
        print(f"Base Customers Claimed: {is_base_claimed}")
        print(f"Total Reward: {total_reward}")
        print(f"Remaining Budget: {self.total_budget}")
        print(f"---------------------------------------")

# This use case done for the budget Allocation

# minimum spent is used for while offer creation
# if we need to use the minimum spent -> we need to create offers. 
# from transaction data only have "user total spent in lifetime". 


BA = BudgetAllocation( total_budget=2000, base_budget_percent=0.7,
                                 premium_budget_percent=0.3, abc_split=[0, 0.5, 0.8, 1]
                        )
BA.calculate_rewards()
BA.summary()