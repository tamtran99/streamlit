import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
from flask_ngrok import run_with_ngrok
import random
import string


# Tạo dataset
data = {
    "Date": pd.date_range(start="2023-01-01", periods=100, freq="D").tolist(),
    "Activity": [''.join(random.choices(string.ascii_uppercase, k=random.randint(7, 10))) for _ in range(100)],
    "Type": random.choices(["active", "inactive", "undefined"], k=100),
    "customer_id": [f"cust_{random.randint(1, 3)}" for _ in range(100)]  # Random customer IDs
}
df = pd.DataFrame(data)

# Mapping type -> y axis (sorting purpose)
type_mapping = {"active": 2, "inactive": 1, "undefined": 0}
df['Type_Numeric'] = df['Type'].map(type_mapping)

# Lấy danh sách customer_id duy nhất
unique_customers = df["customer_id"].unique()

# Chuyển thành danh sách options cho Dropdown
customer_options = [{"label": customer, "value": customer} for customer in unique_customers]

# Khởi tạo ứng dụng Dash
app = Dash(__name__)

# Kết nối ngrok
run_with_ngrok(app)

# Layout của ứng dụng
app.layout = html.Div([
    html.H1("Filter Chart by Customer ID"),
    dcc.Dropdown(
        id="customer_id_dropdown",
        options=customer_options,
        placeholder="Select Customer ID",
        style={"width": "50%"}
    ),
    dcc.Graph(id="activity_chart")
])

# Callback để cập nhật chart dựa trên customer_id
@app.callback(
    Output("activity_chart", "figure"),
    [Input("customer_id_dropdown", "value")]
)
def update_chart(customer_id):
    # Kiểm tra nếu "all" được chọn hoặc không có giá trị nào
    if not customer_id or customer_id == "all":
        return go.Figure()
    else:
        filtered_df = df[df['customer_id'] == customer_id]  # Lọc dữ liệu theo customer_id
        show_labels = True  # Hiển thị nhãn

    # Tạo chart
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=filtered_df['Date'],
            y=filtered_df['Type_Numeric'],
            mode="markers+lines" if not show_labels else "markers+text+lines",
            text=filtered_df['Activity'],
            textposition="top center",
            marker=dict(
                size=8,
                color=random.choices(["red", "blue"], k=len(filtered_df))
            ),
            line=dict(
                color="#333333",  # Màu line (dark gray)
                width=2  # Độ dày của đường
            )
        )
    )

    # Cấu hình trục Y
    fig.update_yaxes(
        tickvals=[0, 1, 2],
        ticktext=["undefined", "inactive", "active"]
    )

    # Cấu hình layout
    fig.update_layout(
        title=f"Activity Chart for Customer: {customer_id}" if customer_id else "Activity Chart",
        xaxis_title="Date",
        yaxis_title="Segment",
        xaxis=dict(
            rangeslider=dict(visible=True),
            rangeselector=dict(  # Giống như Power BI
                buttons=[
                    dict(count=7, label="1w", step="day", stepmode="backward"),
                    dict(count=30, label="1m", step="day", stepmode="backward"),
                    dict(count=90, label="3m", step="day", stepmode="backward"),
                    dict(step="all", label="All")
                ]
            )
        ),
        height=600,
        showlegend=False
    )
    return fig

# Chạy ứng dụng và in link ngrok
if __name__ == '__main__':
    # Start the app and get the URL from ngrok
    app.run_server()  # Chạy server và in link
