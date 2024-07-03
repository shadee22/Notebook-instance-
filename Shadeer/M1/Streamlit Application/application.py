import streamlit as st
import requests  # Import requests library for API calls
import pandas as pd
import ast

top_categories = pd.read_csv("../DataSources/top_category.csv")
merged_data = pd.read_csv("../DataSources/merged_data_with_cluster_and_label.csv")
m1_offers = pd.read_csv("../DataSources/m1_offers.csv")

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


def get_label_cluster(uid):
    label = merged_data.loc[merged_data["UID"] == uid, "ABC_Category"].iloc[0]
    cluster = merged_data.loc[merged_data["UID"] == uid, "Cluster"].iloc[0]
    matching_rows = top_categories[(top_categories["label"] == label) & (top_categories["cluster"] == int(cluster))]
    v = matching_rows["top_categories"].iloc[0]
    data_dict = ast.literal_eval(v)
    mapped_feq_cats = {}
    feq_cats = data_dict
    
    # category mapping
    for specific_cat, frequency in feq_cats.items():
        for broad_cat, specific_cats in category_mapping.items():
            if specific_cat in specific_cats:
                mapped_feq_cats[broad_cat] = mapped_feq_cats.get(broad_cat, 0) + frequency
    
    # get offers for the user
    m1_offers["category"] = m1_offers["Merchant_type"]
    keys = mapped_feq_cats.keys()
    m1_offers["category"] = m1_offers["category"].fillna("Others")
    filtered_offers = m1_offers[m1_offers['category'].isin(keys)]
    selected_columns = filtered_offers[["offer_id", "category","offer_title"]]
    
    # print(data_dict)
    if(selected_columns.empty == False):
        st.write(f"ABC value: {label}")
        st.write(f"Cluster: {cluster}")
        
        st.write("Recommendations:")
        st.write(selected_columns)
        
    return  {
        "user_id": f"{uid}",
        "user_label": "{}".format(label),
        "user_cluster": "{}".format(cluster),
        "user_segment_top_categories": data_dict,
        "user_segment_top_categories_mapped": mapped_feq_cats,
        "top_offers_for_user_segment": {
            "offers": selected_columns.to_dict(orient='records'),
        },
        "top_offers_for_specific_user": {
            "offers": []
        },
        "user_status": "Existing",
        
    }

def fake_api_call(data):
    """Simulates an API call with a predefined response based on the input data.

    Args:
        data (str): Input data to send to the API.

    Returns:
        dict: Fake API response data.
    """

    response = {
        "user_id": f"You sent: {data}",
        "top_offers": {
            "offer_1": "Offer 1 Details",
            "offer_2": "Offer 2 Details",
        },
        "user_label": "A | B | C",
        "user_status": "Existing",
        "user_cluster": "Cluster 1",
    }
    return response

def main():
    uid = st.text_input("Enter the user ID ( EX: 7229f66d-fe30-41d0-b02d-58a122bfca68 | df15d349-8cc3-46c2-9ad2-b635233c92df ):")

    if uid:
        try:
            response = get_label_cluster(uid)
            st.write("Recommendations API:")
            st.json(response)
        except IndexError:
            st.error("UID not found in the data.")



if __name__ == "__main__":
    main()
