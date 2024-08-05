import pandas as pd
import numpy as np
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
from sklearn.ensemble import IsolationForest



# Get the data
df = pd.read_csv('camel_btc.csv')

# Create the Dash app
app = Dash(__name__)

# Define the layout
app.layout = html.Div([
    html.H1("Interactive Technical Analysis Chart"),
    dcc.Dropdown(
        id='column-selector',
        options=[{'label': col, 'value': col} for col in df.columns if col != 'Date'],
        value=['Price', 'MA10', 'MA30'],  # default value
        multi=True
    ),
    dcc.Graph(id='chart'),
    html.Div(id='anomaly-info')
])

@app.callback(
    [Output('chart', 'figure'),
     Output('anomaly-info', 'children')],
    [Input('column-selector', 'value')]
)
def update_chart(selected_columns):
    # Create the main chart
    fig = go.Figure()

    for column in selected_columns:
        fig.add_trace(go.Scatter(x=df['Date'], y=df[column], name=column))

    # Identify crosses and anomalies using machine learning
    crosses, anomalies = identify_patterns(df[selected_columns])

    # Add crosses to the chart
    for cross in crosses:
        fig.add_trace(go.Scatter(x=[df['Date'][cross]], y=[df[selected_columns[0]][cross]],
                                 mode='markers', marker=dict(size=10, symbol='star', color='red'),
                                 name='Cross'))

    # Add anomalies to the chart
    for anomaly in anomalies:
        fig.add_trace(go.Scatter(x=[df['Date'][anomaly]], y=[df[selected_columns[0]][anomaly]],
                                 mode='markers', marker=dict(size=10, symbol='x', color='green'),
                                 name='Anomaly'))

    fig.update_layout(title='Technical Analysis Chart', xaxis_title='Date', yaxis_title='Value')

    # Create info text
    info_text = f"Detected {len(crosses)} crosses and {len(anomalies)} anomalies."

    return fig, info_text

def identify_patterns(data):
    crosses = []
    for i in range(1, len(data)):
        if any(data.iloc[i-1, j] < data.iloc[i-1, k] and data.iloc[i, j] > data.iloc[i, k]
               for j in range(len(data.columns)) for k in range(j+1, len(data.columns))):
            crosses.append(i)

    # Use Isolation Forest to detect anomalies
    iso_forest = IsolationForest(contamination=0.1, random_state=42)
    anomalies = np.where(iso_forest.fit_predict(data) == -1)[0]

    return crosses, anomalies

if __name__ == '__main__':
    app.run_server(debug=True)