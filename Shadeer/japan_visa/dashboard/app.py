import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

def load_data():
    df = pd.read_csv('/Users/shadeer/Desktop/HOME/AI/Notebooks/kaggle/faiss-rag/notebooks/dashboard/a.csv')
    return df

df = load_data()
num_unique_cardholders = df['cardholder_id'].nunique()
num_unique_cards = df['card_id'].nunique()

# Ensure the 'card_id_count' column is created correctly
new_df = df.groupby('cardholder_id')['card_id'].count().reset_index(name='card_id_count')
value_counts = new_df['card_id_count'].value_counts().reset_index()
value_counts.columns = ['card_count', 'unique_cardholder_count']

fig_pie = px.pie(value_counts, values='unique_cardholder_count', names='card_count', 
                 title='Cardholder Distribution by Card Count')

# Create issuer_bin and group by it to get card_id_count
df['issuer_bin'] = 4
issuer_df = df.groupby('issuer_bin')['card_id'].nunique().reset_index(name='card_id_count')
print("Issuer Grouped DataFrame:\n", issuer_df.head())

# Ensure 'first_1_digits' is correctly created
df['issuer_bin'] = df['issuer_bin'].astype(str)
df['first_1_digits'] = df['issuer_bin'].str[:1]
print("DataFrame with 'first_1_digits':\n", df[['issuer_bin', 'first_1_digits']].head())

grouped_df = df.groupby("first_1_digits")["card_id"].nunique().reset_index(name='card_id_count')
print("Grouped DataFrame (first_1_digits):\n", grouped_df.head())

# Bank mapping
bank_mapping = {
    '4980': 'Sumitomo Mitsui Card Company Limited',
    '4708': 'YES BANK, LTD.',
    '4297': 'RAKUTEN KC CO., LTD.',
    '4537': 'WELLS FARGO BANK, N.A.',
    '4205': 'AEON CREDIT SERVICE CO., LTD.',
    '4534': 'DC CARD CO., LTD.',
    '4541': 'REDIT SAISON CO., LTD.',
    '4363': 'UNITED COMMERCIAL BANK',
    '4649': 'YAMAGIN CREDIT CO., LTD.',
    '4616': 'U.S. BANK N.A. ND',
    '4986': 'MITSUBISHI UFJ FINANCIAL GROUP, INC.',
    '4539': 'OSTGIROT BANK AB',
    '4097': 'CAJA AHORROS GERONA',
    '4924': 'BANK OF AMERICA, N.A.',
    '4987': 'YAMAGIN CREDIT CO., LTD.',
    '4162': 'UNKNOWN',
    '4721': 'WELLS FARGO BANK IOWA, N.A.',
    '4538': 'MITSUBISHI UFJ FINANCIAL GROUP, INC.',
    '4984': 'BANCO DO BRASIL, S.A.',
    '4122': 'UNITED BANK, LTD.',
    '4901': 'OMC CARD, INC.',
    '4': 'Latitude Bank'
}
grouped_df['Bank Name'] = grouped_df['first_1_digits'].map(bank_mapping)
grouped_df = grouped_df[['first_1_digits', 'Bank Name', 'card_id_count']].head(20)
print("Final Grouped DataFrame with Bank Names:\n", grouped_df)

fig_bar = px.bar(grouped_df, x='Bank Name', y='card_id_count', 
                 title='Top Issuers by Card ID Count')

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Dashboard", className="text-center"), className="mb-4 mt-4")
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    html.H4("Number of unique Cardholders", className="card-title"),
                    html.P(f"{num_unique_cardholders}", className="card-text")
                ]),
                color="primary", inverse=True  # Adding color to the card
            )
        ], width=6),
        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    html.H4("Number of unique Cards", className="card-title"),
                    html.P(f"{num_unique_cards}", className="card-text")
                ]),
                color="success", inverse=True  # Adding color to the card
            )
        ], width=6),
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(figure=fig_pie)
        ], width=6),
        dbc.Col([
            dcc.Graph(figure=fig_bar)
        ], width=6)
    ])
], fluid=True)

if __name__ == '__main__':
    app.run_server(debug=True)