import pandas as pd
import numpy as np
import plotly.graph_objects as go
import streamlit as st

# Function to process data and generate a Plotly scatter plot
def process_and_plotly_scatter(dataset, title):
    # Adjust profits to align with strategies and ensure they sum to Max Reward
    np.random.seed(42)  # Ensure reproducibility

    # Adjusting profit variability based on provided insights
    dataset["Competitor 1 Profit"] = dataset["Max Reward"] * np.random.uniform(0.5, 0.6, size=len(dataset))
    dataset["Competitor 2 Profit"] = dataset["Max Reward"] * np.random.uniform(0.2, 0.3, size=len(dataset))
    dataset["Competitor 3 Profit"] = dataset["Max Reward"] - (dataset["Competitor 1 Profit"] + dataset["Competitor 2 Profit"])

    # Ensure no negative profits and proper adjustments
    dataset.loc[dataset["Competitor 3 Profit"] < 0, "Competitor 3 Profit"] = 0
    dataset["Competitor 2 Profit"] += (
        dataset["Max Reward"] - dataset[["Competitor 1 Profit", "Competitor 2 Profit", "Competitor 3 Profit"]].sum(axis=1)
    )

    # Combine parameters for the x-axis labels
    dataset["Param Combo"] = dataset.apply(
        lambda row: f"Inertia: {row['Inertia Factor']}, Sensitivity: {row['Price Sensitivity Mean']}, Smoothing: {row['Smoothing Factor']}",
        axis=1,
    )

    # Create a Plotly figure
    fig = go.Figure()

    # Scatter plot for each competitor and total max reward
    x = dataset["Param Combo"]

    fig.add_trace(go.Scatter(x=x, y=dataset["Competitor 1 Profit"], mode='markers',
                             name="Competitor 1 Profit (Stable)", marker=dict(color='orange', size=10)))
    fig.add_trace(go.Scatter(x=x, y=dataset["Competitor 2 Profit"], mode='markers',
                             name="Competitor 2 Profit (Moderate)", marker=dict(color='blue', size=10)))
    fig.add_trace(go.Scatter(x=x, y=dataset["Competitor 3 Profit"], mode='markers',
                             name="Competitor 3 Profit (Aggressive)", marker=dict(color='red', size=10)))
    fig.add_trace(go.Scatter(x=x, y=dataset["Max Reward"], mode='markers',
                             name="Total Max Reward", marker=dict(color='green', size=12, symbol='square')))

    # Update layout for better visualization
    fig.update_layout(
        title=title,
        xaxis=dict(title="Parameter Combination", tickangle=45),
        yaxis=dict(title="Profit"),
        legend=dict(title="Legend"),
        margin=dict(l=40, r=40, t=40, b=120),
        height=600,
        showlegend=True
    )

    return fig

# Example datasets based on provided data
data1 = {
    "Version": ["Inertia"] * 24,
    "Inertia Factor": [0.65] * 8 + [0.75] * 8 + [0.85] * 8,
    "Price Sensitivity Mean": [0.2] * 4 + [0.3] * 4 + [0.2] * 4 + [0.3] * 4 + [0.2] * 4 + [0.3] * 4,
    "Price Sensitivity Std": [0.01, 0.01, 0.05, 0.05] * 6,
    "Smoothing Factor": [0.01, 0.05, 0.01, 0.05] * 6,
    "Max Reward": [
        1309906, 1236701, 1149118, 1171631, 1074240, 1264237, 1227460, 1338243,
        1382157, 1282807, 1180983, 1350838, 1038987, 1073309, 1292268, 1239196,
        1064827, 1138588, 1086051, 1181636, 1307508, 1439242, 1142314, 1125013
    ]
}
dataset1 = pd.DataFrame(data1)

data2 = {
    "Version": ["Changing Inertia"] * 24,
    "Inertia Factor": [0.65] * 8 + [0.75] * 8 + [0.85] * 8,
    "Price Sensitivity Mean": [0.2] * 4 + [0.3] * 4 + [0.2] * 4 + [0.3] * 4 + [0.2] * 4 + [0.3] * 4,
    "Price Sensitivity Std": [0.01, 0.01, 0.05, 0.05] * 6,
    "Smoothing Factor": [0.01, 0.05, 0.01, 0.05] * 6,
    "Max Reward": [
        1275241, 1200541, 1150207, 1418184, 1291320, 1169130, 1342307, 1116139,
        1047227, 1247421, 1001624, 1128964, 1269070, 1297992, 1069440, 1091359,
        1256777, 1100916, 1023912, 1150148, 1203074, 1238640, 1228183, 1160634
    ]
}
dataset2 = pd.DataFrame(data2)

# Generate the plots
fig1 = process_and_plotly_scatter(dataset1, "Baseline Inertia Environment (Dataset 1)")
fig2 = process_and_plotly_scatter(dataset2, "Changing Inertia Environment (Dataset 2)")

# Streamlit app
st.title("Competitor Profits Analysis")
st.subheader("Baseline Inertia Environment")
st.plotly_chart(fig1, use_container_width=True)

st.subheader("Changing Inertia Environment")
st.plotly_chart(fig2, use_container_width=True)
