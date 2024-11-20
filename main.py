import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import random
import string

# Tạo dataset
# Create dataset
data = {
"Date": pd.date_range(start="2023-01-01", periods=100, freq="D").tolist(),
"Activity": [''.join(random.choices(string.ascii_uppercase, k=random.randint(7, 10))) for _ in range(100)],
"Type": random.choices(["active", "inactive", "undefined"], k=100),
    "customer_id": [f"cust_{random.randint(1, 3)}" for _ in range(100)]  # Random customer IDs
    "customer_id": [f"cust_{random.randint(1, 3)}" for _ in range(100)],  # Random customer IDs
    "is_key_event": [random.choice([True, False]) for _ in range(100)]  # Add boolean column
}
df = pd.DataFrame(data)

# Mapping type -> y axis (sorting purpose)
type_mapping = {"active": 2, "inactive": 1, "undefined": 0}
df['Type_Numeric'] = df['Type'].map(type_mapping)

# Lấy danh sách customer_id duy nhất
unique_customers = df["customer_id"].unique()
# Sort date and customer_id
df = df.sort_values(by=['customer_id', 'Date'])


# Function to generate product(segments) column
def assign_segment_based_on_date(group):
    # Sort date
    group = group.sort_values('Date')
    num_days = len(group)
    bin_edges = pd.cut(range(num_days), bins=3, labels=[0, 1, 2]).categories
    group['Segment'] = pd.cut(range(num_days), bins=3, labels=[0, 1, 2])

    return group


# Chuyển thành danh sách options cho Dropdown
customer_options = [{"label": customer, "value": customer} for customer in unique_customers]
# Final data
df = df.groupby('customer_id').apply(assign_segment_based_on_date)

# Get unique customers
unique_customers = df["customer_id"].unique()

# Streamlit Layout
st.title("Filter Chart by Customer ID")
st.title("Filter Chart by Customer ID and Date")

# Dropdown để chọn customer_id
# Dropdown customer_id -> always choose 1 customer
customer_id = st.selectbox(
"Select Customer ID",
    options=[""] + list(unique_customers),  # Thêm một lựa chọn trống cho "all"
    index=0
    options=list(unique_customers),
    index=0  # default customer
)

# Hàm để cập nhật chart
def update_chart(customer_id):
    # Kiểm tra nếu không có giá trị customer_id (tức là chọn "all")
    if not customer_id:
        filtered_df = df
# Date range picker to choose date
date_range = st.date_input(
    "Select Date Range",
    value=(df['Date'].min(), df['Date'].max()),
    min_value=df['Date'].min(),
    max_value=df['Date'].max()
)


# Function to update chart
def update_chart(customer_id, date_range):
    # Filter Date
    filtered_df = df[(df['Date'] >= pd.Timestamp(date_range[0])) & (df['Date'] <= pd.Timestamp(date_range[1]))]

    # Filter customer_id
    filtered_df = filtered_df[filtered_df['customer_id'] == customer_id]

    # Check if user selects "All" (from rangeselector)
    rangeselector_state = False  # Default to False (not "All")

    # Get the step from rangeselector (which can be "1w", "1m", "3m", or "all")
    if 'step' in st.session_state and st.session_state.step == 'all':
        rangeselector_state = True

    # Show label Activity when is_key_event == True (if "All" is not selected, show all)
    if rangeselector_state:
        filtered_df['Label'] = filtered_df.apply(lambda row: row['Activity'] if row['is_key_event'] else "", axis=1)
else:
        filtered_df = df[df['customer_id'] == customer_id]  # Lọc dữ liệu theo customer_id
        filtered_df['Label'] = filtered_df['Activity']  # Show all activities

    # Tạo chart
    # Create chart
fig = go.Figure()
fig.add_trace(
go.Scatter(
x=filtered_df['Date'],
y=filtered_df['Type_Numeric'],
            mode="markers+lines",
            text=filtered_df['Activity'],
            mode="markers+lines+text",
            text=filtered_df['Label'],  # Show label Activity when is_key_event == True
textposition="top center",
marker=dict(
size=8,
color=random.choices(["red", "blue"], k=len(filtered_df))
),
line=dict(
                color="#333333",  # Màu line (dark gray)
                width=2  # Độ dày của đường
                color="#333333",
                width=2
)
)
)

    # Cấu hình trục Y
    # Background color depend on Product (segment) column
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

    # Config y-axis
fig.update_yaxes(
tickvals=[0, 1, 2],
ticktext=["undefined", "inactive", "active"]
)

    # Cấu hình layout
    # Config layout
fig.update_layout(
        title=f"Activity Chart for Customer: {customer_id}" if customer_id else "Activity Chart",
        title=f"Activity Chart for Customer: {customer_id}",
xaxis_title="Date",
yaxis_title="Segment",
xaxis=dict(
rangeslider=dict(visible=True),
            rangeselector=dict(  # Giống như Power BI
            rangeselector=dict(
buttons=[
dict(count=7, label="1w", step="day", stepmode="backward"),
dict(count=30, label="1m", step="day", stepmode="backward"),
dict(count=90, label="3m", step="day", stepmode="backward"),
dict(step="all", label="All")
]
)
),
        height=600,
        height=800,
        width=1200,
showlegend=False
)

return fig

# Cập nhật chart dựa trên lựa chọn customer_id
st.plotly_chart(update_chart(customer_id))

if __name__ == "__main__":
    st.plotly_chart(update_chart(customer_id, date_range))
