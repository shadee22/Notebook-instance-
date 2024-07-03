#Collabarotive with priority frequency

import pandas as pd
from datetime import datetime
from sklearn.metrics.pairwise import cosine_similarity
df = pd.read_csv("./DataSources/M1_OptimizeFullReport.csv", encoding='latin1')

# Drop the original 'Order Value' column
df.drop(columns=['Order Value'], inplace=True)

# Rename 'Original Order Value' column to 'Order Value'
df.rename(columns={'Original Order Value': 'Order Value'}, inplace=True)

# Select only the desired columns
df = df.loc[:, ['Conversion ID', 'Advertiser', 'Order ID', 'Conversion Time', 'Timezone', 'Currency', 'Order Value', 'Country Code', 'Device Type', 'ex3/category', 'Cust Type', 'UID']]

# Clean the 'Advertiser' column to ensure consistency
df['Advertiser'] = df['Advertiser'].replace('Shopee SG', 'Shopee Singapore')

# Find distinct values and their counts in 'Advertiser'
distinct_advertisers_counts = df['Advertiser'].value_counts()

# Clean the 'Cust Type' column to ensure consistency
df['Cust Type'] = df['Cust Type'].replace('new', 'NEW').replace('existing', 'EXISTING')

# Find distinct values and their counts in 'Cust Type'
distinct_cust_types_counts = df['Cust Type'].value_counts()

# Convert 'Conversion Time' column to datetime
#df['Conversion Time'] = pd.to_datetime(df['Conversion Time'])
df['Conversion Time'] = pd.to_datetime(df['Conversion Time'], format='%d/%m/%Y %H:%M')


# Define reference date as the current date
reference_date = datetime.now()

# Recency Calculation
# Group by UID and find the most recent purchase date
recency_df = df.groupby('UID')['Conversion Time'].max().reset_index()
recency_df['Recency'] = (reference_date - recency_df['Conversion Time']).dt.days

# Frequency Calculation
# Group by UID and count the number of transactions
frequency_df = df.groupby('UID').size().reset_index(name='Frequency')

# AOV Calculation
# Group by UID and calculate the average order value
# Remove outliers based on your criteria (e.g., high-value purchases)
# For simplicity, let's remove any orders above a certain threshold
threshold = 1000  # You can adjust this threshold as per your requirement
filtered_df = df[df['Order Value'] <= threshold]
aov_df = filtered_df.groupby('UID')['Order Value'].mean().reset_index(name='AOV')

# Unique category count calculation
unique_category_count_df = df.groupby('UID')['ex3/category'].nunique().reset_index(name='Unique Category Counts')

# Total spending calculation
total_spending_df = filtered_df.groupby('UID')['Order Value'].sum().reset_index(name='Total Spending')

# Merge all calculated values into a single dataframe
result_df_2 = (
    recency_df.merge(frequency_df, on='UID').merge(aov_df, on='UID').merge(total_spending_df, on='UID').merge(unique_category_count_df, on='UID')
)

# Group by UID and category, and count the number of transactions for each category
category_transactions = df.groupby(['UID', 'ex3/category']).size().reset_index(name='Transaction Count')

# Pivot the dataframe to have UID as rows and categories as columns
transaction_count_by_category = category_transactions.pivot_table(index='UID', columns='ex3/category', values='Transaction Count', aggfunc='sum', fill_value=0)

# Reset index to make UID a column again
transaction_count_by_category.reset_index(inplace=True)

# If UID is not set as the index, you can use 'on' parameter instead
merged_df = pd.merge(result_df_2, transaction_count_by_category, on='UID')

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# Calculate user-user similarity based on RFAT and wallet share by category
def calculate_user_similarity(merged_df):
    user_features = merged_df.drop(columns=['UID', 'Conversion Time'])  # Exclude UID and Conversion Time
    user_similarity_matrix = cosine_similarity(user_features)
    return user_similarity_matrix

# Example: Get top N similar users for a given user
def get_top_similar_users(merged_df, user_similarity_matrix, user_id, n=5):
    if user_id not in merged_df['UID'].values:
        print(f"User ID {user_id} does not exist. Using default recommendations.")
        return []
    user_index = merged_df.index[merged_df['UID'] == user_id][0]
    similar_users = user_similarity_matrix[user_index].argsort()[::-1][1:n+1]
    return similar_users

# Example: Aggregate top categories from similar users
def aggregate_top_categories_from_similar_users(merged_df, similar_users, n=10):
    category_columns = [col for col in merged_df.columns if col not in ['UID', 'Conversion Time', 'Recency', 'Frequency', 'AOV', 'Total Spending','Unique Category Counts']]
    top_categories = merged_df.iloc[similar_users][category_columns].sum().nlargest(n).index.tolist()
    return top_categories

# Example: Recommend top categories for a given user
def recommend_top_categories(merged_df, user_similarity_matrix, user_id, n=10):
    similar_users = get_top_similar_users(merged_df, user_similarity_matrix, user_id)
    if len(similar_users) == 0:  # Check if no similar users were found
        return default_recommendations(merged_df), []  # Fallback to default recommendations and empty offer categories
    top_categories = aggregate_top_categories_from_similar_users(merged_df, similar_users, n)
    return top_categories

# Example: Default recommendations for new users based on frequency
def default_recommendations(df, n=10):
    # Provide default recommendations based on popular or trending categories using frequency
    # Group by category and count the occurrences of each UID within each category
    top_categories = df.groupby('ex3/category').size().nlargest(n).index.tolist()
    return top_categories

# Example: Format output nicely
def format_output(user_id, top_categories):
    output = f"Top {len(top_categories)} categories for user: {user_id}"
    for i, category in enumerate(top_categories, start=1):
        output += f"\n{i}. {category}"
    return output

# Load the offer dataset from the CSV file
offer_df = pd.read_csv("./DataSources/M1_offers.csv")

# Define the mapping between transaction sub-categories and offer main categories
category_mapping = {
    'Beauty': ['Beauty'],
    'Electronics': ['Audio', 'Mobile & Gadgets', 'Cameras & Drones', 'Computers & Accessories', 'Electronics Accessories', 'Monitors & Printers', 'Smart Devices', 'Digital Utilities', 'Televisions & Videos', 'Digital Goods', 'Data Storage', 'Mobiles & Tablets'],
    'Entertainment': ['Gaming & Consoles', 'Media, Music & Books'],
    'Fashion & Retail': ['Fashion Accessories', 'Women Shoes', 'Women Clothes', 'Men Clothes', 'Baby & Kids Fashion', 'Women Bags', 'Muslim Fashion', 'Men Bags', 'Men Shoes', "Women's Shoes and Clothing", "Men's Shoes and Clothing", "Kids' Shoes and Clothing"],
    'Health and Wellness': ['Health'],
    'Hobbies': ['Hobbies & Collections', 'Toys & Games'],
    'Home Improvement/Furniture': ['Home & Living', 'Home Appliances', 'Kitchen & Dining', 'Lighting & Décor', 'Small Appliances', 'Household Supplies', 'Bedding & Bath', 'Outdoor & Garden', 'Furniture & Organization', 'Tools & Home Improvement', 'Laundry & Cleaning Equipment', 'Large Appliances'],
    'Jewelry & Timepieces': ['Watches', 'Watches Sunglasses Jewellery'],
    'Miscellaneous': ['Automobiles', 'Pets', 'Mom & Baby', 'Books & Magazines', 'Stationery', 'Tickets, Vouchers & Services', 'Motorcycles', 'Free Sample (Flexi Combo)', 'Pet Supplies', 'Mother & Baby', 'Stationery, Craft & Gift Cards', 'Motors', 'Surprise Box', 'Telco', 'Stationery & Craft', 'Local Service', 'Services'],
    'Sports and Fitness': ['Sports & Outdoors', 'Sports Shoes and Clothing'],
    'Supermarkets': ['Food & Beverage', 'Groceries'],
    'Travel': ['Travel & Luggage', 'Bags and Travel'],
    'Retailers': [],
    'Marketplace': [],
    'Cafe': [],
    'Finance and Banking': [],
    'Department Stores': [],
    'Visa Generic': [],
    'Real Estate': [],
    'Restaurants': []
}

# Map transaction sub-categories to offer main categories
def map_to_offer_category(sub_categories):
    offer_categories = set()
    for sub_category in sub_categories:
        for offer_category, mapped_sub_categories in category_mapping.items():
            if sub_category in mapped_sub_categories:
                offer_categories.add(offer_category)
    return list(offer_categories)

# Map top categories to offer categories
def map_top_categories_to_offers(top_categories):
    offer_categories = []
    for category in top_categories:
        mapped_category = map_to_offer_category([category])[0]
        if mapped_category not in offer_categories:
            offer_categories.append(mapped_category)
    return offer_categories

# Example: Get top category recommendations for a user using collaborative filtering
def get_top_and_offer_categories(merged_df, user_similarity_matrix, user_id, offer_df):
    if user_id not in merged_df['UID'].values:
        print(f"User ID {user_id} does not exist. Using default recommendations.")
        default_categories = default_recommendations(df)
        default_offer_categories = map_top_categories_to_offers(default_categories)
        return default_categories, default_offer_categories
    top_categories_collaborative = recommend_top_categories(merged_df, user_similarity_matrix, user_id)
    offer_categories_collaborative = map_top_categories_to_offers(top_categories_collaborative)
    return top_categories_collaborative, offer_categories_collaborative

# Define function to recommend offers for each offer category
def recommend_offers_for_category(offer_df, offer_category):
    # Filter offers based on the "Merchant_type" column to match the offer category
    matching_offers = offer_df[offer_df['Merchant_type'] == offer_category]
    return matching_offers

# Define function to recommend offers for each offer category
def recommend_offers_for_categories(offer_df, offer_categories):
    recommended_offers = {}
    for category in offer_categories:
        recommended_offers[category] = recommend_offers_for_category(offer_df, category)
    return recommended_offers

# Example: Print top and offer categories for a user
def print_top_and_offer_categories(merged_df, user_similarity_matrix, user_id, offer_df):
    top_categories, offer_categories = get_top_and_offer_categories(merged_df, user_similarity_matrix, user_id, offer_df)
    
    print(f"Top categories for user {user_id}:")
    for i, category in enumerate(top_categories, start=1):
        print(f"{i}. {category}")

    print("\nOffer categories:")
    for i, category in enumerate(offer_categories, start=1):
        print(f"{i}. {category}")

    recommended_offers = recommend_offers_for_categories(offer_df, offer_categories)

    print(f"\nOffers we recommend for user {user_id}:")
    for i, category in enumerate(offer_categories, start=1):
        print(f"\n{i}. {category}")
        if not recommended_offers[category].empty:
            print(recommended_offers[category][['offer_id', 'merchant_name', 'offer_title', 'Offer_amount(%)']].to_string(index=False))
        else:
            print("No offers available for this category.")



# Example: Get top category recommendations for a user
#003d363e-5e74-4bd9-9b7f-77d1ddf0ad62 Unique Category Counts 1
#05e3cacf-ce64-488f-9f42-f8c1c0a78fd5 Unique Category Counts 22
#009caacf-c094-4b84-adde-424c584b0b33 Unique Category Counts 3
#01 New User
user_id = '05e3cacf-ce64-488f-9f42-f8c1c0a78fd5'
user_similarity_matrix = calculate_user_similarity(merged_df)
print_top_and_offer_categories(merged_df, user_similarity_matrix, user_id, offer_df)
