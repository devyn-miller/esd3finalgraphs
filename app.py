import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Function to generate the scatter plot using Plotly
def process_and_scatter_plot_plotly(csv_file):
    # Load CSV data
    df = pd.read_csv(csv_file)

    # Split the data into two datasets: Inertia and Changing Inertia
    dataset1 = df.iloc[:24, :]  # First 24 rows for baseline inertia
    dataset2 = df.iloc[24:, :]  # Next 24 rows for changing inertia

    # Function to adjust profits and plot
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
            height=700,
            width=1200
        )

        # Show the plot
        fig.show()

    # Plot for Dataset 1 (Baseline Inertia)
    process_and_plot(dataset1, "Baseline Inertia Environment")

    # Plot for Dataset 2 (Changing Inertia)
    process_and_plot(dataset2, "Changing Inertia Environment")

# Example usage
# Replace 'your_file.csv' with the actual file path to your CSV
process_and_scatter_plot_plotly("/Users/devynmiller/Downloads/Inertia_and_Changing_Inertia_Economic_Results - Inertia_and_Changing_Inertia_Economic_Results.csv")
