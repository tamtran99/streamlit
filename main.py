import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import random
import string

# Create dataset
data = {
    "Date": pd.date_range(start="2023-01-01", periods=100, freq="D").tolist(),
    "Activity": [''.join(random.choices(string.ascii_uppercase, k=random.randint(7, 10))) for _ in range(100)],
    "Type": random.choices(["active", "inactive", "undefined"], k=100),
    "customer_id": [f"cust_{random.randint(1, 3)}" for _ in range(100)],  # Random customer IDs
    "is_key_event": [random.choice([True, False]) for _ in range(100)]  # Add boolean column
}
df = pd.DataFrame(data)

# Mapping type -> y axis (sorting purpose)
type_mapping = {"active": 2, "inactive": 1, "undefined": 0}
df['Type_Numeric'] = df['Type'].map(type_mapping)

# Get unique customers
unique_customers = df["customer_id"].unique()

# Sort date and customer_id
df = df.sort_values(by=['customer_id', 'Date'])

# Function to generate product(segments) column
def assign_segment_based_on_date(group):
    # Sort date
    group = group.sort_values('Date')
    num_days = len(group)
    group['Segment'] = pd.cut(range(num_days), bins=3, labels=[0, 1, 2])  # Assign segments based on date range
    return group

df = df.groupby('customer_id').apply(assign_segment_based_on_date)

# Streamlit Layout
st.title("Filter Chart by Customer ID")
st.title("Filter Chart by Customer ID and Date")

# Dropdown to select customer_id
customer_id = st.selectbox(
    "Select Customer ID",
    options=[""] + list(unique_customers),  # Add a blank option for "all"
    index=0  # default customer
)

# Date range picker to choose date
date_range = st.date_input(
    "Select Date Range",
    value=(df['Date'].min(), df['Date'].max()),
    min_value=df['Date'].min(),
    max_value=df['Date'].max()
)

# Function to update chart
def update_chart(customer_id, date_range):
    # Filter by date
    filtered_df = df[(df['Date'] >= pd.Timestamp(date_range[0])) & (df['Date'] <= pd.Timestamp(date_range[1]))]

    # Filter by customer_id if selected
    if customer_id:
        filtered_df = filtered_df[filtered_df['customer_id'] == customer_id]
    
    # Show label Activity when is_key_event == True
    filtered_df['Label'] = filtered_df.apply(lambda row: row['Activity'] if row['is_key_event'] else "", axis=1)

    # Create chart
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=filtered_df['Date'],
            y=filtered_df['Type_Numeric'],
            mode="markers+lines+text",
            text=filtered_df['Label'],  # Show label Activity when is_key_event == True
            textposition="top center",
            marker=dict(
                size=8,
                color=random.choices(["red", "blue"], k=len(filtered_df))
            ),
            line=dict(
                color="#333333",  # Dark gray line color
                width=2  # Line width
            )
        )
    )

    # Background color based on Segment
    colors = ["#FF6347", "#32CD32", "#1E90FF"]  # Background color
    segments = filtered_df['Segment'].unique()

    # Limit the number of background colors to 3
    segments = sorted(segments)[:3]  # Only take the first 3 segments (0, 1, 2)

    for segment in segments:
        segment_dates = filtered_df[filtered_df["Segment"] == segment]["Date"]
        if not segment_dates.empty:
            fig.add_shape(
                type="rect",
                x0=segment_dates.min(),
                x1=segment_dates.max(),
                y0=-0.5,
                y1=2.5,
                fillcolor=colors[segment],  # Background color
                opacity=0.4,
                layer="below",
                line_width=0,
            )

    # Configure y-axis
    fig.update_yaxes(
        tickvals=[0, 1, 2],
        ticktext=["undefined", "inactive", "active"]
    )

    # Configure layout
    fig.update_layout(
        title=f"Activity Chart for Customer: {customer_id}" if customer_id else "Activity Chart",
        xaxis_title="Date",
        yaxis_title="Segment",
        xaxis=dict(
            rangeslider=dict(visible=True),
            rangeselector=dict(  # Like Power BI
                buttons=[
                    dict(count=7, label="1w", step="day", stepmode="backward"),
                    dict(count=30, label="1m", step="day", stepmode="backward"),
                    dict(count=90, label="3m", step="day", stepmode="backward"),
                    dict(step="all", label="All")
                ]
            ),
        ),
        height=600,
        width=1200,
        showlegend=False
    )

    return fig

# Display chart
st.plotly_chart(update_chart(customer_id, date_range))

