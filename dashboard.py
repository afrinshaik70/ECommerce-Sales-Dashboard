from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import os

from analysis import (
    get_kpis,
    category_sales,
    state_sales,
    top_products,
    sales_trend
)

# ================= LOAD DATA =================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "sales.csv")

df = pd.read_csv(DATA_PATH)

# ================= KPI DATA =================
kpis = get_kpis()
avg_order_value = df["Sales"].mean()
profit_margin = (df["Profit"].sum() / df["Sales"].sum()) * 100

# ================= APP =================
app = Dash(__name__, assets_folder="assets")

# ================= SIDEBAR =================
sidebar = html.Div([
    html.H2("Dashboard", style={"color": "white"}),

    html.Hr(),

    html.P("📊 Overview", style={"color": "white"}),
    html.P("💰 Sales", style={"color": "white"}),
    html.P("📈 Analytics", style={"color": "white"}),

], style={
    "width": "200px",
    "height": "100vh",
    "position": "fixed",
    "backgroundColor": "#0f172a",
    "padding": "20px"
})

# ================= LAYOUT =================
app.layout = html.Div([

    sidebar,

    html.Div([

        # TITLE
        html.H1("E-Commerce Sales Dashboard", className="title"),

        # FILTERS
        html.Div([

            dcc.Dropdown(
                id="state-filter",
                options=[{"label": s, "value": s} for s in df["State"].unique()],
                placeholder="Select State",
                style={"width": "200px"}
            ),

            dcc.Dropdown(
                id="category-filter",
                options=[{"label": c, "value": c} for c in df["Category"].unique()],
                placeholder="Select Category",
                style={"width": "200px"}
            ),

        ], style={
            "display": "flex",
            "justifyContent": "center",
            "gap": "20px",
            "marginTop": "10px"
        }),

        # KPI ROW
        html.Div([

            html.Div([
                html.H3("Total Sales"),
                html.H2(f"₹{kpis['total_sales']:,}")
            ], className="card"),

            html.Div([
                html.H3("Total Profit"),
                html.H2(f"₹{kpis['total_profit']:,}")
            ], className="card"),

            html.Div([
                html.H3("Total Orders"),
                html.H2(kpis['total_orders'])
            ], className="card"),

            html.Div([
                html.H3("Avg Order Value"),
                html.H2(f"₹{avg_order_value:,.2f}")
            ], className="card"),

            html.Div([
                html.H3("Profit Margin"),
                html.H2(f"{profit_margin:.2f}%")
            ], className="card"),

        ], className="kpi-container"),

        # GRAPHS WILL GO HERE (DYNAMIC)
        html.Div(id="graph-container")

    ], style={"marginLeft": "220px"})
])

# ================= CALLBACK (FILTER LOGIC) =================
@app.callback(
    Output("graph-container", "children"),
    Input("state-filter", "value"),
    Input("category-filter", "value")
)
def update_dashboard(state, category):

    filtered = df.copy()

    if state:
        filtered = filtered[filtered["State"] == state]

    if category:
        filtered = filtered[filtered["Category"] == category]

    # Monthly Sales Trend (Area Chart)
    monthly_sales = (
        filtered.groupby("Order_Date")["Sales"]
        .sum()
        .reset_index()
    )

    fig1 = px.area(
        monthly_sales,
        x="Order_Date",
        y="Sales",
        title="Monthly Sales Trend"
    )

    # Sales by State (Horizontal Bar)
    state_data = (
        filtered.groupby("State")["Sales"]
        .sum()
        .reset_index()
    )

    fig2 = px.bar(
        state_data,
        x="Sales",
        y="State",
        orientation="h",
        title="Sales by State"
    )

    # Sales by Category (Donut Chart)
    category_data = (
        filtered.groupby("Category")["Sales"]
        .sum()
        .reset_index()
    )

    fig3 = px.pie(
        category_data,
        names="Category",
        values="Sales",
        hole=0.55,
        title="Sales by Category"
    )

    # Profit Distribution (Pie Chart)
    profit_data = (
        filtered.groupby("Category")["Profit"]
        .sum()
        .reset_index()
    )

    fig4 = px.pie(
        profit_data,
        names="Category",
        values="Profit",
        title="Profit Distribution"
    )
    # Top Products (Vertical Bar Chart)

    product_data = (
    filtered.groupby("Product_Name")["Sales"]
    .sum()
    .reset_index()
    .sort_values("Sales", ascending=False)
    )

    fig5 = px.bar(
    product_data,
    x="Product_Name",
    y="Sales",
    title="Top Products Sales"
    )
    # Dark Theme
    for fig in [fig1, fig2, fig3, fig4, fig5]:
        fig.update_layout(
            paper_bgcolor="#111827",
            plot_bgcolor="#111827",
            font_color="white"
        )

    return html.Div([

        html.Div([
            html.Div(
                dcc.Graph(figure=fig1, style={"height": "400px"}),
                className="graph-card"
            ),
            html.Div(
                dcc.Graph(figure=fig2, style={"height": "400px"}),
                className="graph-card"
            ),
        ], className="graph-grid"),

        html.Div([
            html.Div(
                dcc.Graph(figure=fig3, style={"height": "400px"}),
                className="graph-card"
            ),
            html.Div(
                dcc.Graph(figure=fig4, style={"height": "400px"}),
                className="graph-card"
            ),
            html.Div(
                dcc.Graph(figure=fig5, style={"height": "400px"}),
                className="graph-card"
            ),
        ], className="graph-grid")

    ])

# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True)