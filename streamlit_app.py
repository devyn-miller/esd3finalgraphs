import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

st.set_page_config(layout="wide")
st.title("Economic Results Visualization")

st.markdown("""
This visualization shows the economic results from two different market scenarios:
1. **Baseline Inertia Environment**: First 24 scenarios where market conditions remain stable
2. **Changing Inertia Environment**: Next 24 scenarios with dynamic market conditions

Each point represents profits for three competitors:
- **Competitor 1 (Orange)**: Stable strategy
- **Competitor 2 (Blue)**: Moderate strategy
- **Competitor 3 (Red)**: Aggressive strategy
- **Total Max Reward (Green)**: Total market potential

The x-axis shows different parameter combinations:
- **Inertia Factor**: Market resistance to change (0.65,0.75,0.85)
- **Mean Price**: Average price sensitivity (0.2,0.3)
- **Price SD**: Price sensitivity variation (0.01,0.05)
- **Smoothing**: Price smoothing factor (0.01,0.05)
""")

def process_and_plot(dataset, title):
    # Combine parameters for the x-axis labels
    dataset["Param Combo"] = dataset.apply(
        lambda row: f"inertia={row['Inertia Factor']}, meanprice={row['Price Sensitivity Mean']}, pricesd={row['Price Sensitivity Std']}, smoothing={row['Smoothing Factor']}",
        axis=1,
    )

    # Create scatter plot using Plotly
    fig = go.Figure()

    # Add scatter plots for each competitor
    fig.add_trace(go.Scatter(
        x=dataset.index, 
        y=dataset["Competitor 1 Profit"], 
        mode="markers", 
        name="Competitor 1 Profit (Stable)", 
        marker=dict(symbol="circle", color="orange", size=10)
    ))
    fig.add_trace(go.Scatter(
        x=dataset.index, 
        y=dataset["Competitor 2 Profit"], 
        mode="markers", 
        name="Competitor 2 Profit (Moderate)", 
        marker=dict(symbol="x", color="blue", size=10)
    ))
    fig.add_trace(go.Scatter(
        x=dataset.index, 
        y=dataset["Competitor 3 Profit"], 
        mode="markers", 
        name="Competitor 3 Profit (Aggressive)", 
        marker=dict(symbol="triangle-up", color="red", size=10)
    ))
    fig.add_trace(go.Scatter(
        x=dataset.index, 
        y=dataset["Max Reward"], 
        mode="markers", 
        name="Total Max Reward", 
        marker=dict(symbol="square", color="green", size=10)
    ))

    # Update layout for better visualization
    fig.update_layout(
        title=title,
        xaxis=dict(
            tickmode='array',
            tickvals=dataset.index,
            ticktext=dataset["Param Combo"],
            tickangle=-90,
            showgrid=True
        ),
        yaxis=dict(title="Profit"),
        xaxis_title="Parameter Combination",
        yaxis_title="Profit",
        showlegend=True,
        height=700
    )

    return fig

# Load and process data
@st.cache_data
def load_data():
    return pd.read_csv("economic_results.csv")

df = load_data()

# Split the data into two datasets
dataset1 = df.iloc[:24, :]  # First 24 rows for baseline inertia
dataset2 = df.iloc[24:, :]  # Next 24 rows for changing inertia

# Create and display plots
st.subheader("Baseline Inertia Environment")
fig1 = process_and_plot(dataset1, "Baseline Inertia Environment")
st.plotly_chart(fig1, use_container_width=True)

st.subheader("Changing Inertia Environment")
fig2 = process_and_plot(dataset2, "Changing Inertia Environment")
st.plotly_chart(fig2, use_container_width=True)
