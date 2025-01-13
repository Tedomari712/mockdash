# Import required libraries
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import numpy as np
import os

# Initialize the app
app = dash.Dash(
    __name__, 
    external_stylesheets=[
        dbc.themes.FLATLY,
        'https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap'
    ]
)

# This is important for Render deployment
server = app.server

# Custom CSS
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

# Monthly data
monthly_data = pd.DataFrame({
    'Month': ['January', 'February', 'March', 'April', 'May', 'June', 
             'July', 'August', 'September', 'October', 'November', 'December'],
    'Transactions': [133641, 171044, 200841, 204680, 197654, 189258, 
                    182504, 183429, 84383, 169780, 138824, 68452],
    'Volume': [2013687811.26, 2490772705.46, 2776712059.66, 2771003331.42, 2732297727.71, 
               2539282672.75, 2551967296.20, 2890018921.76, 1411203322.06, 2230387153.64, 
               1849984455.07, 987131225.49],
    'Success_Rate': [95.47, 97.72, 96.65, 97.87, 99.05, 98.17, 
                    95.36, 95.11, 94.85, 98.13, 94.52, 94.03],
    'Unique_Remitters': [20610, 20219, 17487, 26118, 16178, 23345, 
                        28163, 28799, 23795, 34715, 25236, 18104],
    'Unique_Recipients': [34553, 50852, 75630, 85424, 66600, 73019, 
                         67567, 71636, 42967, 80602, 63104, 38295]
})

# Failure data
failure_data = pd.DataFrame({
    'Reason': ['General Failure', 'Limit Exceeded', 'Invalid Credit Party', 
               'Insufficient Balance', 'SOAP Error', 'Timed Out', 'System Error',
               'Connectivity Error', 'Invalid Account', 'Invalid Details', 'Other'],
    'Total': [833, 11376, 5416, 31173, 1248, 1640, 485, 194, 557, 4695, 2312],
    'Percentage': [1.39, 18.98, 9.04, 52.02, 2.08, 2.74, 0.81, 0.32, 0.93, 7.83, 3.86]
})

# Country data
country_data = pd.DataFrame({
    'Country': ['CAN', 'FIN', 'GBR', 'GER', 'IRL', 'KEN', 'NGA', 'UGA', 'USA', 'Unknown'],
    'Volume': [1517951948.64, 307421630.62, 11315946583.70, 101630751.00, 153890861.47,
               846415656.43, 101777855.36, 896761980.11, 6791147045.70, 4772819388.13],
    'Transactions': [118717, 28193, 864380, 6034, 10630, 68183, 9028, 1609, 402476, 327200],
    'Market_Share': [5.66, 1.15, 42.21, 0.38, 0.57, 3.16, 0.38, 3.35, 25.33, 17.81]
})

# Daily data from the PDF
daily_data = pd.DataFrame({
    'Day': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
    'Volume': [3446887082.69, 3542203701.92, 3856600588.57, 4174561072.82, 
               5582156391.24, 3962547257.90, 2679492587.34],
    'Count': [231857, 236668, 249814, 264715, 348966, 297996, 231426]
})

# Client data
client_data = pd.DataFrame({
    'Client': ['Lemfi', 'Cellulant', 'Nala', 'DLocal', 'Wapipay', 'Hello FXBud', 
              'Finpesa', 'Tangent', 'Others'],
    'Volume': [11606556833.85, 6280089643.65, 8055904624.99, 248808932.68, 
               1510015.74, 617699.08, 973692826.00, 76931592.49, 0.00],
    'Transactions': [836080, 443517, 560706, 16028, 174, 103, 1571, 3090, 0],
    'Market_Share': [42.60, 23.05, 29.57, 0.91, 0.01, 0.00, 3.57, 0.28, 0.00]
})

# Start App Layout
app.layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H1(
                    "2024 Mobile Wallet Transfer Analysis", 
                    className="text-primary text-center mb-4",
                    style={'letterSpacing': '2px'}
                )
            ])
        ])
    ]),

    # Key Metrics Cards
    dbc.Row([
        # Total Transactions Card
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Total Annual Transactions", className="card-title text-center"),
                    html.H2(
                        f"{monthly_data['Transactions'].sum():,.0f}", 
                        className="text-primary text-center"
                    ),
                    html.P([
                        html.Span("Monthly Average: ", className="regular-text"),
                        html.Span(
                            f"{monthly_data['Transactions'].mean():,.0f}",
                            className="regular-text text-success"
                        )
                    ], className="text-center")
                ])
            ], className="shadow-sm")
        ]),
        
        # Success Rate Card
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Average Success Rate", className="card-title text-center"),
                    html.H2([
                        f"{monthly_data['Success_Rate'].mean():.1f}",
                        html.Small("%", className="text-muted")
                    ], className="text-primary text-center"),
                    html.P([
                        html.Span("Peak: ", className="regular-text"),
                        html.Span(
                            f"{monthly_data['Success_Rate'].max():.1f}%",
                            className="regular-text text-success"
                        )
                    ], className="text-center")
                ])
            ], className="shadow-sm")
        ]),
        
        # Total Volume Card
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Total Volume (KES)", className="card-title text-center"),
                    html.H2(
                        f"{monthly_data['Volume'].sum()/1e9:.2f}B", 
                        className="text-primary text-center"
                    ),
                    html.P([
                        html.Span("Monthly Average: ", className="regular-text"),
                        html.Span(
                            f"KES {monthly_data['Volume'].mean()/1e6:.1f}M",
                            className="regular-text text-success"
                        )
                    ], className="text-center")
                ])
            ], className="shadow-sm")
        ]),
        
        # Unique Users Card
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Total Unique Users", className="card-title text-center"),
                    html.H2(
                        f"{monthly_data['Unique_Remitters'].sum():,.0f}", 
                        className="text-primary text-center"
                    ),
                    html.P([
                        html.Span("Recipients: ", className="regular-text"),
                        html.Span(
                            f"{monthly_data['Unique_Recipients'].sum():,.0f}",
                            className="regular-text text-success"
                        )
                    ], className="text-center")
                ])
            ], className="shadow-sm")
        ])
    ], className="mb-4"),

    # Monthly Trends
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Monthly Transaction Analysis"),
                dbc.CardBody([
                    dcc.Graph(
                        figure=go.Figure(data=[
                            go.Bar(
                                name='Volume',
                                x=monthly_data['Month'],
                                y=monthly_data['Volume']/1e6,
                                marker_color='rgba(26, 118, 255, 0.8)',
                                yaxis='y'
                            ),
                            go.Scatter(
                                name='Success Rate',
                                x=monthly_data['Month'],
                                y=monthly_data['Success_Rate'],
                                mode='lines+markers',
                                marker=dict(
                                    size=8,
                                    color='rgba(255, 128, 0, 0.8)'
                                ),
                                line=dict(
                                    width=2,
                                    color='rgba(255, 128, 0, 0.8)'
                                ),
                                yaxis='y2'
                            )
                        ]).update_layout(
                            title='Monthly Volume and Success Rate Trends',
                            yaxis=dict(
                                title='Volume (KES Millions)',
                                titlefont=dict(color='rgba(26, 118, 255, 0.8)'),
                                tickfont=dict(color='rgba(26, 118, 255, 0.8)')
                            ),
                            yaxis2=dict(
                                title='Success Rate (%)',
                                titlefont=dict(color='rgba(255, 128, 0, 0.8)'),
                                tickfont=dict(color='rgba(255, 128, 0, 0.8)'),
                                overlaying='y',
                                side='right',
                                range=[90, 100]
                            ),
                            height=400,
                            margin=dict(l=50, r=50, t=50, b=30),
                            legend=dict(
                                orientation="h",
                                y=1.1,
                                x=0.5,
                                xanchor='center'
                            )
                        )
                    )
                ])
            ], className="shadow-sm")
        ], width=12)
    ], className="mb-4"),

    # User Activity and Geographic Distribution
    dbc.Row([
        # User Activity
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Monthly User Activity"),
                dbc.CardBody([
                    dcc.Graph(
                        figure=go.Figure(data=[
                            go.Bar(
                                name='Remitters',
                                x=monthly_data['Month'],
                                y=monthly_data['Unique_Remitters'],
                                marker_color='rgba(26, 118, 255, 0.8)'
                            ),
                            go.Bar(
                                name='Recipients',
                                x=monthly_data['Month'],
                                y=monthly_data['Unique_Recipients'],
                                marker_color='rgba(255, 128, 0, 0.8)'
                            )
                        ]).update_layout(
                            title='Monthly Active Users',
                            barmode='group',
                            height=400,
                            margin=dict(l=50, r=50, t=50, b=30),
                            legend=dict(
                                orientation="h",
                                y=1.1,
                                x=0.5,
                                xanchor='center'
                            )
                        )
                    )
                ])
            ], className="shadow-sm")
        ], width=6),
        
        # Geographic Distribution
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Geographic Distribution"),
                dbc.CardBody([
                    dcc.Graph(
                        figure=go.Figure(
                            go.Pie(
                                labels=country_data['Country'],
                                values=country_data['Volume'],
                                textinfo='label+percent',
                                hole=0.3
                            )
                        ).update_layout(
                            title='Transaction Volume by Country',
                            height=400,
                            margin=dict(l=50, r=50, t=50, b=30)
                        )
                    )
                ])
            ], className="shadow-sm")
        ], width=6)
    ], className="mb-4"),

    # Daily Patterns and Failure Analysis
    dbc.Row([
        # Daily Transaction Pattern
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Daily Transaction Pattern"),
                dbc.CardBody([
                    dcc.Graph(
                        figure=go.Figure(data=[
                            go.Bar(
                                name='Volume',
                                x=daily_data['Day'],
                                y=daily_data['Volume']/1e6,
                                marker_color='rgba(26, 118, 255, 0.8)',
                                yaxis='y'
                            ),
                            go.Scatter(
                                name='Transactions',
                                x=daily_data['Day'],
                                y=daily_data['Count'],
                                mode='lines+markers',
                                marker=dict(
                                    size=8,
                                    color='rgba(255, 128, 0, 0.8)'
                                ),
                                line=dict(
                                    width=2,
                                    color='rgba(255, 128, 0, 0.8)'
                                ),
                                yaxis='y2'
                            )
                        ]).update_layout(
                            title='Daily Transaction Patterns',
                            yaxis=dict(
                                title='Volume (KES Millions)',
                                titlefont=dict(color='rgba(26, 118, 255, 0.8)'),
                                tickfont=dict(color='rgba(26, 118, 255, 0.8)')
                            ),
                            yaxis2=dict(
                                title='Number of Transactions',
                                titlefont=dict(color='rgba(255, 128, 0, 0.8)'),
                                tickfont=dict(color='rgba(255, 128, 0, 0.8)'),
                                overlaying='y',
                                side='right'
                            ),
                            height=400,
                            margin=dict(l=50, r=50, t=50, b=30),
                            legend=dict(
                                orientation="h",
                                y=1.1,
                                x=0.5,
                                xanchor='center'
                            )
                        )
                    ),
                    html.Div([
                        html.P([
                            "Peak Day: Friday ",
                            html.Span(
                                f"(KES {daily_data['Volume'].max()/1e6:.1f}M, {daily_data['Count'].max():,} transactions)",
                                className="text-muted"
                            )
                        ], className="mb-0 mt-3 regular-text")
                    ])
                ])
            ], className="shadow-sm")
        ], width=6),
        
        # Failure Analysis
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Failure Analysis"),
                dbc.CardBody([
                    dcc.Graph(
                        figure=go.Figure(
                            go.Treemap(
                                labels=failure_data['Reason'],
                                parents=[''] * len(failure_data),
                                values=failure_data['Total'],
                                textinfo='label+value+percent parent',
                                hovertemplate=(
                                    "<b>%{label}</b><br>" +
                                    "Count: %{value}<br>" +
                                    "Percentage: %{percentParent:.1%}<extra></extra>"
                                ),
                                marker=dict(
                                    colors=failure_data['Total'],
                                    colorscale=[[0, '#ffebee'], [1, '#c62828']],
                                    showscale=True
                                ),
                                textfont=dict(size=13)
                            )
                        ).update_layout(
                            title='Transaction Failure Distribution',
                            height=400,
                            margin=dict(l=20, r=20, t=50, b=20)
                        )
                    ),
                    html.Div([
                        html.P([
                            "Total Failed Transactions: ",
                            html.Span(
                                f"{failure_data['Total'].sum():,}",
                                className="text-muted"
                            )
                        ], className="mb-0 mt-3 regular-text text-center")
                    ])
                ])
            ], className="shadow-sm")
        ], width=6)
    ], className="mb-4"),

    # Client Market Share and Performance
    dbc.Row([
        # Client Market Share
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Client Market Share"),
                dbc.CardBody([
                    dcc.Graph(
                        figure=go.Figure(
                            data=[go.Pie(
                                labels=client_data['Client'],
                                values=client_data['Volume'],
                                textinfo='label+percent',
                                hole=0.3,
                                hovertemplate=(
                                    "<b>%{label}</b><br>" +
                                    "Volume: KES %{value:,.2f}<br>" +
                                    "Share: %{percent}<extra></extra>"
                                )
                            )]
                        ).update_layout(
                            title='Transaction Volume by Client',
                            height=400,
                            margin=dict(l=20, r=20, t=50, b=20),
                            showlegend=True,
                            legend=dict(
                                orientation="h",
                                yanchor="bottom",
                                y=-0.2,
                                xanchor="center",
                                x=0.5
                            )
                        )
                    ),
                    html.Div([
                        html.P([
                            "Top Client: Lemfi ",
                            html.Span(
                                f"({client_data['Market_Share'].max():.1f}% market share)",
                                className="text-muted"
                            )
                        ], className="mb-0 mt-3 regular-text text-center")
                    ])
                ])
            ], className="shadow-sm")
        ], width=6),
        
        # Client Performance
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Client Performance Metrics"),
                dbc.CardBody([
                    dcc.Graph(
                        figure=go.Figure(data=[
                            go.Bar(
                                name='Transactions',
                                x=client_data['Client'],
                                y=client_data['Transactions'],
                                marker_color='rgba(26, 118, 255, 0.8)',
                                yaxis='y'
                            ),
                            go.Scatter(
                                name='Market Share (%)',
                                x=client_data['Client'],
                                y=client_data['Market_Share'],
                                mode='lines+markers',
                                marker=dict(
                                    size=8,
                                    color='rgba(255, 128, 0, 0.8)'
                                ),
                                line=dict(
                                    width=2,
                                    color='rgba(255, 128, 0, 0.8)'
                                ),
                                yaxis='y2'
                            )
                        ]).update_layout(
                            title='Client Transaction Activity',
                            yaxis=dict(
                                title='Number of Transactions',
                                titlefont=dict(color='rgba(26, 118, 255, 0.8)'),
                                tickfont=dict(color='rgba(26, 118, 255, 0.8)')
                            ),
                            yaxis2=dict(
                                title='Market Share (%)',
                                titlefont=dict(color='rgba(255, 128, 0, 0.8)'),
                                tickfont=dict(color='rgba(255, 128, 0, 0.8)'),
                                overlaying='y',
                                side='right'
                            ),
                            height=400,
                            margin=dict(l=50, r=50, t=50, b=100),
                            legend=dict(
                                orientation="h",
                                y=1.1,
                                x=0.5,
                                xanchor='center'
                            ),
                            xaxis_tickangle=-45
                        )
                    )
                ])
            ], className="shadow-sm")
        ], width=6)
    ], className="mb-4")

], fluid=True, className="p-4")

# Run the app
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run_server(debug=False, host='0.0.0.0', port=port)
