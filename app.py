import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import numpy as np
import os

# Initialize the app with custom styling
app = dash.Dash(
    __name__, 
    external_stylesheets=[
        dbc.themes.FLATLY,
        'https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap'
    ]
)

# This is important for Render deployment
server = app.server

# Custom CSS for consistent font styling
app.index_string = '''<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            * {
                font-family: 'Bebas Neue', sans-serif;
            }
            .regular-text {
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            }
            .card-body p, .card-body text {
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            }
            .card {
                margin-bottom: 1rem;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>'''

# Create DataFrames with the data
monthly_data = pd.DataFrame({
    'Metric': ['Total Transactions', 'Transaction Volume (KES)', 'Successful Transactions', 
               'Failed Transactions', 'Success Rate (%)', 'Unique Remitters', 
               'Unique Recipients', 'Unique Countries'],
    'October': [169780, 2230387153.64, 166597, 3183, 98.1, 34715, 80602, 64],
    'November': [138824, 1849984455.07, 131222, 7602, 94.5, 25236, 63104, 43],
    'Net Change': [-30956, -380402698.57, -35375, 4419, -3.6, -9479, -17498, -21],
    'Change %': [-18.23, -17.06, -21.23, 138.83, -3.67, -27.31, -21.71, -32.81]
})

failure_data = pd.DataFrame({
    'Reason': ['Insufficient Balance', 'Limit Exceeded', 'Other', 'Invalid Credit Party',
               'SOAP Error', 'Connectivity Error', 'Invalid Details', 'Timeout error',
               'General Failure', 'Invalid Account', 'System Error'],
    'Count': [4882, 999, 855, 339, 142, 139, 109, 81, 34, 16, 6],
    'Percentage': [64.2, 13.1, 11.2, 4.5, 1.9, 1.8, 1.4, 1.1, 0.4, 0.2, 0.1]
})

country_data = pd.DataFrame({
    'Country': ['United Kingdom', 'United States', 'Canada', 'Kenya', 'Australia',
                'Finland', 'Nigeria', 'Ireland', 'Germany', 'Norway'],
    'Volume_KES': [802066522.49, 719297609.58, 153306217.22, 124125130.12, 11658903.40,
                   11180354.93, 4211689.93, 3936772.30, 3639507.00, 3163174.00],
    'Transactions': [64941, 41419, 12616, 8594, 600, 1060, 550, 331, 209, 100]
})

client_data = pd.DataFrame({
    'Client': ['Lemfi', 'Nala', 'Cellulant', 'DLocal', 'Finpesa', 'Wapipay', 'Hello FXBud', 'Fincra'],
    'Volume_KES': [1537366902.33, 146809444.07, 120469860.90, 30770621.69, 14561502.00, 5227.08, 686.00, 211.00],
    'Transactions': [111365, 10072, 8791, 937, 23, 29, 1, 4]
})

# Create hourly data
hourly_data = pd.DataFrame({
    'Hour': [f'{i:02d}:00' for i in range(24)],
    'Volume': np.random.exponential(scale=5000000, size=24)
})
hourly_data.loc[11, 'Volume'] = 33293454.18  # Known peak
hourly_data.loc[7, 'Volume'] = 6.00  # Known minimum

# Layout
app.layout = dbc.Container([
    # Header with logo and title
    dbc.Row([
        dbc.Col([
            html.Div([
                # Replace YOUR_IMAGE_URL with the actual URL where you'll host your image
                html.Img(src='https://github.com/Tedomari712/mockdash/blob/main/vngrd.PNG?raw=true',
                     className='logo', 
                     style={'height': '150px', 'object-fit': 'contain'})
            ], style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center', 'padding': '40px', 'marginBottom': '30px', 'width': '100%'}),
            html.H1("November Mobile Wallet Analysis", 
                   className="text-primary text-center mb-4",
                   style={'letterSpacing': '2px'})
        ])
    ]),

    # Key Metrics Cards
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Total Transactions", className="card-title text-center"),
                    html.H2(f"{monthly_data.loc[0, 'November']:,.0f}", 
                           className="text-primary text-center"),
                    html.P([
                        html.Span("MoM Change: ", className="regular-text"),
                        html.Span(f"{monthly_data.loc[0, 'Change %']}%",
                                className=f"regular-text {'text-danger' if monthly_data.loc[0, 'Change %'] < 0 else 'text-success'}")
                    ], className="text-center")
                ])
            ], className="shadow-sm")
        ]),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Success Rate", className="card-title text-center"),
                    html.H2([
                        f"{monthly_data.loc[4, 'November']}",
                        html.Small("%", className="text-muted")
                    ], className="text-primary text-center"),
                    html.P([
                        html.Span("MoM Change: ", className="regular-text"),
                        html.Span(f"{monthly_data.loc[4, 'Change %']}%",
                                className=f"regular-text {'text-danger' if monthly_data.loc[4, 'Change %'] < 0 else 'text-success'}")
                    ], className="text-center")
                ])
            ], className="shadow-sm")
        ]),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Volume (KES)", className="card-title text-center"),
                    html.H2(f"{monthly_data.loc[1, 'November']/1e9:.2f}B", 
                           className="text-primary text-center"),
                    html.P([
                        html.Span("MoM Change: ", className="regular-text"),
                        html.Span(f"{monthly_data.loc[1, 'Change %']}%",
                                className=f"regular-text {'text-danger' if monthly_data.loc[1, 'Change %'] < 0 else 'text-success'}")
                    ], className="text-center")
                ])
            ], className="shadow-sm")
        ]),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Avg. Transaction", className="card-title text-center"),
                    html.H2(f"{monthly_data.loc[1, 'November']/monthly_data.loc[0, 'November']:,.0f}", 
                           className="text-primary text-center"),
                    html.P([
                        html.Span("KES per transaction", className="regular-text")
                    ], className="text-center text-muted")
                ])
            ], className="shadow-sm")
        ])
    ], className="mb-4"),

    # Main Charts Row
    dbc.Row([
        # Left Column
        dbc.Col([
            # Daily Transaction Volume Card
            dbc.Card([
                dbc.CardHeader("Daily Transaction Volume"),
                dbc.CardBody([
                    dcc.Graph(
                        figure=go.Figure(
                            data=[
                                go.Indicator(
                                    mode="number",
                                    value=137.07142374,
                                    number={"prefix": "KES ", "suffix": "M",
                                           "valueformat": ".1f",
                                           "font": {"size": 24}},
                                    title={"text": "Peak Daily Volume",
                                           "font": {"size": 14},
                                           "align": "center"},
                                    domain={'x': [0.05, 0.45], 'y': [0.65, 0.95]}
                                ),
                                go.Indicator(
                                    mode="number",
                                    value=61.6661485,
                                    number={"prefix": "KES ", "suffix": "M",
                                           "valueformat": ".1f",
                                           "font": {"size": 24}},
                                    title={"text": "Average Daily Volume",
                                           "font": {"size": 14},
                                           "align": "center"},
                                    domain={'x': [0.55, 0.95], 'y': [0.65, 0.95]}
                                ),
                                go.Indicator(
                                    mode="number",
                                    value=9044,
                                    number={"valueformat": ",",
                                           "font": {"size": 24}},
                                    title={"text": "Peak Daily Transactions",
                                           "font": {"size": 14},
                                           "align": "center"},
                                    domain={'x': [0.05, 0.45], 'y': [0.375, 0.625]}
                                ),
                                go.Indicator(
                                    mode="number",
                                    value=4627,
                                    number={"valueformat": ",",
                                           "font": {"size": 24}},
                                    title={"text": "Average Daily Transactions",
                                           "font": {"size": 14},
                                           "align": "center"},
                                    domain={'x': [0.55, 0.95], 'y': [0.375, 0.625]}
                                ),
                                go.Indicator(
                                    mode="gauge+number",
                                    value=94.5,
                                    title={"text": "Daily Success Rate",
                                           "font": {"size": 16},
                                           "align": "center"},
                                    number={"suffix": "%",
                                           "font": {"size": 28}},
                                    gauge={
                                        'axis': {'range': [0, 100]},
                                        'bar': {'color': "darkgreen"},
                                        'steps': [
                                            {'range': [0, 85], 'color': 'rgba(255, 99, 71, 0.3)'},
                                            {'range': [85, 95], 'color': 'rgba(255, 215, 0, 0.3)'},
                                            {'range': [95, 100], 'color': 'rgba(0, 128, 0, 0.3)'}
                                        ],
                                        'threshold': {
                                            'line': {'color': "red", 'width': 2},
                                            'thickness': 0.75,
                                            'value': 94.5
                                        }
                                    },
                                    domain={'x': [0.15, 0.85], 'y': [0.02, 0.32]}
                                ),
                            ]
                        ).update_layout(
                            height=550,
                            margin=dict(t=30, b=30, l=30, r=30)
                        )
                    )
                ]),
                dbc.CardFooter([
                    html.Div([
                        dbc.Row([
                            dbc.Col([
                                html.P("Peak Volume Day: November 8, 2024", className="regular-text mb-1"),
                                html.P("Lowest Volume Day: November 12, 2024", className="regular-text mb-0")
                            ])
                        ])
                    ], className="small")
                ])
            ], className="shadow-sm mb-4"),

            # Hourly Distribution Card
            dbc.Card([
                dbc.CardHeader("Hourly Distribution"),
                dbc.CardBody([
                    dcc.Graph(
                        figure=px.line(
                            hourly_data, x='Hour', y='Volume',
                            title='Hourly Transaction Volume'
                        ).update_layout(
                            yaxis_type="log",
                            showlegend=False,
                            height=300
                        )
                    )
                ])
            ], className="shadow-sm")
        ], width=4),
        
        # Right Column
        dbc.Col([
            # Transaction Success Analysis Card
            dbc.Card([
                dbc.CardHeader("Transaction Success Analysis"),
                dbc.CardBody([
                    dcc.Graph(
                        figure=go.Figure(data=[
                            go.Bar(
                                name='Successful',
                                x=['October', 'November'],
                                y=[monthly_data.loc[2, 'October'], monthly_data.loc[2, 'November']],
                                marker_color='rgb(40, 167, 69)'
                            ),
                            go.Bar(
                                name='Failed',
                                x=['October', 'November'],
                                y=[monthly_data.loc[3, 'October'], monthly_data.loc[3, 'November']],
                                marker_color='rgb(220, 53, 69)'
                            )
                        ]).update_layout(
                            barmode='stack',
                            height=550,
                            title="Success vs Failure Comparison"
                        )
                    )
                ])
            ], className="shadow-sm mb-4"),
            
            # User Activity Metrics Card
            dbc.Card([
                dbc.CardHeader("User Activity Metrics"),
                dbc.CardBody([
                    dcc.Graph(
                        figure=go.Figure(data=[
                            # First row - Icons
                            go.Scatter(
                                x=[0.2, 0.5, 0.8],
                                y=[1.15, 1.15, 1.15],
                                mode='text',
                                text=['🌍', '👥', '👤'],
                                textfont=dict(size=24),
                                hoverinfo='none',
                                showlegend=False
                            ),
                            # Second row - Titles
                            go.Scatter(
                                x=[0.2, 0.5, 0.8],
                                y=[1, 1, 1],
                                mode='text',
                                text=['Active Countries', 'Unique Remitters', 'Unique Recipients'],
                                textfont=dict(size=14),
                                hoverinfo='none',
                                showlegend=False
                            ),
                            # Third row - Current Values
                            go.Scatter(
                                x=[0.2, 0.5, 0.8],
                                y=[0.85, 0.85, 0.85],
                                mode='text',
                                text=['43', '25,236', '63,104'],
                                textfont=dict(size=24, color='#2E86C1'),
                                hoverinfo='none',
                                showlegend=False
                            ),
                            # Fourth row - Previous Values
                            go.Scatter(
                                x=[0.2, 0.5, 0.8],
                                y=[0.7, 0.7, 0.7],
                                mode='text',
                                text=['vs 64', 'vs 34,715', 'vs 80,602'],
                                textfont=dict(size=12, color='#666'),
                                hoverinfo='none',
                                showlegend=False
                            ),
                            # Fifth row - Change Percentage
                            go.Scatter(
                                x=[0.2, 0.5, 0.8],
                                y=[0.6, 0.6, 0.6],
                                mode='text',
                                text=['-32.81%', '-27.31%', '-21.71%'],
                                textfont=dict(size=14, color='#E74C3C'),
                                hoverinfo='none',
                                showlegend=False
                            )
                        ]).update_layout(
                            height=350,
                            showlegend=False,
                            xaxis=dict(
                                showgrid=False,
                                zeroline=False,
                                showticklabels=False,
                                range=[0, 1]
                            ),
                            yaxis=dict(
                                showgrid=False,
                                zeroline=False,
                                showticklabels=False,
                                range=[0.5, 1.2]
                            ),
                            margin=dict(l=20, r=20, t=20, b=20),
                            paper_bgcolor='white',
                            plot_bgcolor='white'
                        )
                    )
                ])
            ], className="shadow-sm")
        ], width=8)
    ], className="mb-4"),

    # Geographic Distribution
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Geographic Distribution"),
                dbc.CardBody([
                    dcc.Graph(
                        figure=go.Figure(data=[
                            go.Bar(
                                name='Volume (KES)',
                                x=country_data['Country'],
                                y=country_data['Volume_KES'],
                                yaxis='y',
                                marker_color='rgba(26, 118, 255, 0.8)'
                            ),
                            go.Scatter(
                                name='Transactions',
                                x=country_data['Country'],
                                y=country_data['Transactions'],
                                yaxis='y2',
                                mode='lines+markers',
                                marker_color='rgba(255, 128, 0, 0.8)'
                            )
                        ]).update_layout(
                            yaxis=dict(title='Volume (KES)', type='log', side='left'),
                            yaxis2=dict(title='Transactions', type='log', side='right', overlaying='y'),
                            xaxis_tickangle=-45,
                            height=500,
                            legend=dict(orientation="h", yanchor="bottom", y=1.02)
                        )
                    )
                ])
            ], className="shadow-sm")
        ])
    ], className="mb-4"),
    
    # Failure Analysis and Client Market Share
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Failure Analysis"),
                dbc.CardBody([
                    dcc.Graph(
                        figure=px.treemap(
                            failure_data,
                            path=['Reason'],
                            values='Count',
                            color='Percentage',
                            hover_data=['Percentage'],
                            color_continuous_scale='RdYlBu_r'
                        ).update_layout(height=400)
                    )
                ])
            ], className="shadow-sm")
        ], width=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Client Market Share"),
                dbc.CardBody([
                    dcc.Graph(
                        figure=px.sunburst(
                            client_data,
                            path=['Client'],
                            values='Volume_KES',
                            color='Transactions',
                            hover_data=['Transactions'],
                            color_continuous_scale='Viridis'
                        ).update_layout(height=400)
                    )
                ])
            ], className="shadow-sm")
        ], width=6)
    ], className="mb-4"),

], fluid=True, className="p-4")

# Run the app
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run_server(debug=False, host='0.0.0.0', port=port)
