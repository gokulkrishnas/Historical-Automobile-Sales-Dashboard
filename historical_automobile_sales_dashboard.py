import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

# Load the data using pandas
data = pd.read_csv(r'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)

server = app.server

# Set the title of the dashboard
app.title = "Automobile Statistics Dashboard"

# Define colors for dark theme
colors = {
    'background': '#121212',
    'secondary_background': '#1e1e1e',
    'card_background': '#252525',
    'text': '#FFFFFF',
    'secondary_text': '#AAAAAA',
    'accent': '#3d85c6',  # Blue accent color
    'accent_secondary': '#ff7b00',  # Orange accent color
    'border': '#333333',
    'grid': '#333333',
}

# Add custom CSS for dark theme components
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            body {
                background-color: #121212;
                color: white;
                font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
                margin: 0;
                padding: 0;
            }
            
            /* Dark dropdown styles */
            .Select-control, .Select-menu-outer, .Select-menu, .Select-option, .Select-value {
                background-color: #252525 !important;
                color: white !important;
                border-color: #333333 !important;
            }
            .Select-arrow {
                border-color: #3d85c6 transparent transparent !important;
            }
            .Select-arrow-zone:hover > .Select-arrow {
                border-top-color: #3d85c6 !important;
            }
            .Select-control:hover {
                box-shadow: 0 0 0 1px #3d85c6 !important;
                border-color: #3d85c6 !important;
            }
            .Select.is-focused > .Select-control {
                background-color: #1e1e1e !important;
                border-color: #3d85c6 !important;
                box-shadow: 0 0 0 1px #3d85c6 !important;
            }
            .Select.is-open > .Select-control {
                background-color: #1e1e1e !important;
                border-color: #3d85c6 !important;
            }
            .Select-option.is-focused {
                background-color: #333333 !important;
            }
            .Select-option.is-selected {
                background-color: #3d85c6 !important;
                color: white !important;
            }
            .Select-option:hover {
                background-color: #333333 !important;
            }
            .Select-value-label {
                color: white !important;
            }
            .Select-placeholder, .Select--single > .Select-control .Select-value {
                color: #AAAAAA !important;
            }
            
            /* Dashboard container */
            .dashboard-container {
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
            }
            
            /* Header styling */
            .dashboard-header {
                margin-bottom: 30px;
                padding-bottom: 15px;
                border-bottom: 1px solid #333333;
                text-align: center;
            }
            
            /* Controls container */
            .controls-container {
                display: flex;
                flex-wrap: wrap;
                gap: 20px;
                margin-bottom: 30px;
                padding: 20px;
                background-color: #1e1e1e;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
            
            .control-item {
                flex: 1;
                min-width: 200px;
            }
            
            /* Charts grid */
            .chart-grid {
                display: flex;
                flex-wrap: wrap;
                gap: 20px;
                margin-bottom: 20px;
            }
            
            .chart-row {
                display: flex;
                flex-wrap: wrap;
                width: 100%;
                gap: 20px;
                margin-bottom: 20px;
            }
            
            .chart-item {
                flex: 1;
                min-width: 45%;
                background-color: #252525;
                border-radius: 10px;
                padding: 15px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                margin-bottom: 20px;
            }
            
            /* Label styling */
            label {
                display: block;
                margin-bottom: 8px;
                font-weight: bold;
                color: #FFFFFF;
            }
            
            /* Responsive adjustments */
            @media (max-width: 768px) {
                .chart-item {
                    min-width: 100%;
                }
                
                .control-item {
                    min-width: 100%;
                }
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
</html>
'''

# Create the dropdown menu options
dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]

# List of years 
year_list = [i for i in range(1980, 2024, 1)]

# Create the layout of the app
app.layout = html.Div(
    className='dashboard-container',
    children=[
        # Dashboard Header
        html.Div(
            className='dashboard-header',
            children=[
                html.H1(
                    "Automobile Sales Statistics Dashboard",
                    style={
                        'textAlign': 'center',
                        'color': colors['accent'],
                        'fontSize': '32px',
                        'fontWeight': 'bold',
                        'marginBottom': '5px',
                    }
                ),
                html.P(
                    "Analyze historical automobile sales trends and patterns",
                    style={
                        'textAlign': 'center',
                        'color': colors['secondary_text'],
                        'fontSize': '16px',
                        'marginTop': '0',
                    }
                ),
            ]
        ),
        
        # Controls Container
        html.Div(
            className='controls-container',
            children=[
                # Report Type Dropdown
                html.Div(
                    className='control-item',
                    children=[
                        html.Label(
                            "Select Statistics:",
                            style={
                                'marginBottom': '10px',
                                'fontSize': '16px',
                                'fontWeight': 'normal',
                                'color': colors['text'],
                            }
                        ),
                        dcc.Dropdown(
                            id='dropdown-statistics',
                            options=dropdown_options,
                            value='Select Statistics',
                            placeholder='Select a report type',
                            clearable=False,
                        )
                    ]
                ),
                
                # Year Selection Dropdown
                html.Div(
                    className='control-item',
                    children=[
                        html.Label(
                            "Select Year:",
                            style={
                                'marginBottom': '10px',
                                'fontSize': '16px',
                                'fontWeight': 'normal',
                                'color': colors['text'],
                            }
                        ),
                        dcc.Dropdown(
                            id='select-year',
                            options=[{'label': i, 'value': i} for i in year_list],
                            value='Select Year',
                            clearable=False,
                        )
                    ]
                ),
            ]
        ),
        
        # Output Container
        html.Div(
            id='output-container',
            className='chart-grid',
        )
    ]
)

# Define the callback function to update the input container based on the selected statistics
@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics', component_property='value')
)
def update_input_container(selected_statistics):
    if selected_statistics == 'Yearly Statistics': 
        return False
    else: 
        return True

# Callback for plotting
@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='select-year', component_property='value'), 
     Input(component_id='dropdown-statistics', component_property='value')]
)
def update_output_container(input_year, selected_statistics):
    # Clear the output container on new selections
    if not selected_statistics or (selected_statistics == 'Yearly Statistics' and not input_year):
        # Return default/welcome message
        return html.Div(
            style={
                'textAlign': 'center',
                'padding': '50px 20px',
                'backgroundColor': colors['secondary_background'],
                'borderRadius': '10px',
                'marginTop': '20px',
                'position': 'relative',  # Add positioning context
                'zIndex': 1,  # Base z-index
            },
            children=[
                html.H3(
                    "Welcome to the Automobile Sales Dashboard",
                    style={'color': colors['text'], 'marginBottom': '15px'}
                ),
                html.P(
                    "Please select a report type and year (if applicable) to view the statistics.",
                    style={'color': colors['secondary_text']}
                ),
                html.Div(
                    style={
                        'marginTop': '30px',
                        'display': 'flex',
                        'justifyContent': 'center',
                        'gap': '20px',
                    },
                    children=[
                        html.Div(
                            style={
                                'backgroundColor': colors['card_background'],
                                'padding': '15px 25px',
                                'borderRadius': '5px',
                                'textAlign': 'center',
                                'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
                            },
                            children=[
                                html.P("Yearly Statistics", style={'color': colors['accent'], 'fontWeight': 'bold'}),
                                html.P("View sales data for a specific year", style={'color': colors['secondary_text']})
                            ]
                        ),
                        html.Div(
                            style={
                                'backgroundColor': colors['card_background'],
                                'padding': '15px 25px',
                                'borderRadius': '5px',
                                'textAlign': 'center',
                                'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
                            },
                            children=[
                                html.P("Recession Statistics", style={'color': colors['accent_secondary'], 'fontWeight': 'bold'}),
                                html.P("Analyze sales during recession periods", style={'color': colors['secondary_text']})
                            ]
                        )
                    ]
                )
            ]
        )
    
    # Common graph layout settings
    graph_layout = {
        'paper_bgcolor': colors['card_background'],
        'plot_bgcolor': colors['card_background'],
        'font': {'color': colors['text']},
        'title_font': {'color': colors['text'], 'size': 16},
        'legend_font': {'color': colors['text']},
        'xaxis': {
            'gridcolor': colors['grid'],
            'title_font': {'color': colors['text']},
            'tickfont': {'color': colors['text']},
        },
        'yaxis': {
            'gridcolor': colors['grid'],
            'title_font': {'color': colors['text']},
            'tickfont': {'color': colors['text']},
        },
        'margin': {'t': 50, 'b': 50, 'l': 50, 'r': 30},
    }
    
    if selected_statistics == 'Recession Period Statistics':
        # Filter the data for recession periods
        recession_data = data[data['Recession'] == 1]
        
        # Plot 1: Automobile sales fluctuate over Recession Period (year wise)
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            id='recession-chart1',  # Add unique ID
            config={'displayModeBar': False, 'responsive': True},
            figure=px.line(
                yearly_rec, 
                x='Year',
                y='Automobile_Sales',
                title="Average Automobile Sales During Recession Periods",
                template="plotly_dark",
                line_shape='spline',  # Smooth line
                color_discrete_sequence=[colors['accent']]
            ).update_layout(
                **graph_layout,
                xaxis_title='Year',
                yaxis_title='Average Sales',
                title_x=0.5
            )
        )

        # Plot 2: Calculate the average number of vehicles sold by vehicle type
        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(
            id='recession-chart2',  # Add unique ID
            config={'displayModeBar': False, 'responsive': True},
            figure=px.bar(
                average_sales, 
                x='Vehicle_Type',
                y='Automobile_Sales',
                title="Average Sales by Vehicle Type During Recessions",
                template="plotly_dark",
                color_discrete_sequence=[colors['accent_secondary']]
            ).update_layout(
                **graph_layout,
                xaxis_title='Vehicle Type',
                yaxis_title='Average Sales',
                title_x=0.5
            )
        )
        
        # Plot 3: Pie chart for total expenditure share by vehicle type during recessions
        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(
            id='recession-chart3',  # Add unique ID
            config={'displayModeBar': False, 'responsive': True},
            figure=px.pie(
                exp_rec,
                values='Advertising_Expenditure',
                names='Vehicle_Type',
                title="Ad Expenditure by Vehicle Type During Recessions",
                template="plotly_dark",
                color_discrete_sequence=px.colors.sequential.Blues_r,
                hole=0.4  # Create a donut chart for better appearance
            ).update_layout(
                **graph_layout,
                title_x=0.5,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.15,
                    xanchor="center",
                    x=0.5
                )
            )
        )

        # Plot 4: Bar chart for the effect of unemployment rate on vehicle type and sales
        unemp = recession_data.groupby(['Vehicle_Type', 'unemployment_rate'])['Automobile_Sales'].mean().reset_index()
        R_chart4 = dcc.Graph(
            id='recession-chart4',  # Add unique ID
            config={'displayModeBar': False, 'responsive': True},
            figure=px.bar(
                unemp,
                x='unemployment_rate',
                y='Automobile_Sales',
                color="Vehicle_Type",
                title="Effect of Unemployment Rate on Vehicle Sales",
                template="plotly_dark",
                color_discrete_sequence=px.colors.sequential.Blues_r,
                barmode='group'
            ).update_layout(
                **graph_layout,
                xaxis_title='Unemployment Rate',
                yaxis_title='Average Sales',
                title_x=0.5,
                legend_title_text='Vehicle Type'
            )
        )

        return [
            html.Div(
                id='recession-row1',  # Add unique ID
                className='chart-row',
                style={'position': 'relative', 'zIndex': 10},  # Add positioning and z-index
                children=[
                    html.Div(className='chart-item', children=[R_chart1]),
                    html.Div(className='chart-item', children=[R_chart2])
                ]
            ),
            html.Div(
                id='recession-row2',  # Add unique ID
                className='chart-row',
                style={'position': 'relative', 'zIndex': 10},  # Add positioning and z-index
                children=[
                    html.Div(className='chart-item', children=[R_chart3]),
                    html.Div(className='chart-item', children=[R_chart4])
                ]
            )
        ]

    # Yearly Statistic Report Plots                             
    elif (input_year and selected_statistics == 'Yearly Statistics'):
        yearly_data = data[data['Year'] == input_year]
                              
        # Plot 1: Yearly Automobile sales using line chart for the whole period
        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(
            id=f'yearly-chart1-{input_year}',  # Add unique ID with year
            config={'displayModeBar': False, 'responsive': True},
            figure=px.line(
                yas, 
                x='Year',
                y='Automobile_Sales',
                title="Average Automobile Sales (1980-2023)",
                template="plotly_dark",
                line_shape='spline',  # Smooth line
                color_discrete_sequence=[colors['accent']]
            ).update_layout(
                **graph_layout,
                xaxis_title='Year',
                yaxis_title='Average Sales',
                title_x=0.5
            ).add_shape(  # Highlight selected year
                type="line",
                x0=input_year,
                y0=0,
                x1=input_year,
                y1=yas['Automobile_Sales'].max() * 1.1,
                line=dict(color=colors['accent_secondary'], width=2, dash="dot")
            )
        )

        # Plot 2: Total Monthly Automobile sales using line chart
        mas = data.groupby('Month')['Automobile_Sales'].mean().reset_index()
        # Convert month to proper order
        month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        mas['Month'] = pd.Categorical(mas['Month'], categories=month_order, ordered=True)
        mas = mas.sort_values('Month')
        
        Y_chart2 = dcc.Graph(
            id=f'yearly-chart2-{input_year}',  # Add unique ID with year
            config={'displayModeBar': False, 'responsive': True},
            figure=px.line(
                mas, 
                x='Month',
                y='Automobile_Sales',
                title="Average Monthly Automobile Sales",
                template="plotly_dark",
                line_shape='spline',  # Smooth line
                markers=True,  # Show markers on the line
                color_discrete_sequence=[colors['accent']]
            ).update_layout(
                **graph_layout,
                xaxis_title='Month',
                yaxis_title='Average Sales',
                title_x=0.5
            )
        )

        # Plot 3: Bar chart for average number of vehicles sold during the given year
        avr_vdata = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(
            id=f'yearly-chart3-{input_year}',  # Add unique ID with year
            config={'displayModeBar': False, 'responsive': True},
            figure=px.bar(
                avr_vdata, 
                x='Vehicle_Type',
                y='Automobile_Sales',
                title=f'Average Sales by Vehicle Type in {input_year}',
                template="plotly_dark",
                color_discrete_sequence=[colors['accent_secondary']]
            ).update_layout(
                **graph_layout,
                xaxis_title='Vehicle Type',
                yaxis_title='Average Sales',
                title_x=0.5
            )
        )
            
        # Plot 4: Total Advertisement Expenditure for each vehicle using pie chart
        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(
            id=f'yearly-chart4-{input_year}',  # Add unique ID with year
            config={'displayModeBar': False, 'responsive': True},
            figure=px.pie(
                exp_data,
                values='Advertising_Expenditure',
                names='Vehicle_Type',
                title=f"Ad Expenditure by Vehicle Type in {input_year}",
                template="plotly_dark",
                color_discrete_sequence=px.colors.sequential.Blues_r,
                hole=0.4  # Create a donut chart for better appearance
            ).update_layout(
                **graph_layout,
                title_x=0.5,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.15,
                    xanchor="center",
                    x=0.5
                )
            )
        )

        return [
            # Use a container div with clear identifier
            html.Div(
                id=f'yearly-stats-container-{input_year}',  # Add unique ID with year
                style={'width': '100%', 'position': 'relative', 'zIndex': 20},  # Add positioning and higher z-index
                children=[
                    html.Div(
                        id=f'yearly-row1-{input_year}',  # Add unique ID with year
                        className='chart-row',
                        children=[
                            html.Div(className='chart-item', children=[Y_chart1]),
                            html.Div(className='chart-item', children=[Y_chart2])
                        ]
                    ),
                    html.Div(
                        id=f'yearly-row2-{input_year}',  # Add unique ID with year
                        className='chart-row',
                        children=[
                            html.Div(className='chart-item', children=[Y_chart3]),
                            html.Div(className='chart-item', children=[Y_chart4])
                        ]
                    )
                ]
            )
        ]
        
    else:
        # If no selection is made yet, show a welcome message
        return html.Div(
            style={
                'textAlign': 'center',
                'padding': '50px 20px',
                'backgroundColor': colors['secondary_background'],
                'borderRadius': '10px',
                'marginTop': '20px',
                'position': 'relative',  # Add positioning context
                'zIndex': 1,  # Base z-index
            },
            children=[
                html.H3(
                    "Welcome to the Automobile Sales Dashboard",
                    style={'color': colors['text'], 'marginBottom': '15px'}
                ),
                html.P(
                    "Please select a report type and year (if applicable) to view the statistics.",
                    style={'color': colors['secondary_text']}
                ),
                html.Div(
                    style={
                        'marginTop': '30px',
                        'display': 'flex',
                        'justifyContent': 'center',
                        'gap': '20px',
                    },
                    children=[
                        html.Div(
                            style={
                                'backgroundColor': colors['card_background'],
                                'padding': '15px 25px',
                                'borderRadius': '5px',
                                'textAlign': 'center',
                                'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
                            },
                            children=[
                                html.P("Yearly Statistics", style={'color': colors['accent'], 'fontWeight': 'bold'}),
                                html.P("View sales data for a specific year", style={'color': colors['secondary_text']})
                            ]
                        ),
                        html.Div(
                            style={
                                'backgroundColor': colors['card_background'],
                                'padding': '15px 25px',
                                'borderRadius': '5px',
                                'textAlign': 'center',
                                'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
                            },
                            children=[
                                html.P("Recession Statistics", style={'color': colors['accent_secondary'], 'fontWeight': 'bold'}),
                                html.P("Analyze sales during recession periods", style={'color': colors['secondary_text']})
                            ]
                        )
                    ]
                )
            ]
        )

# Run the Dash app
if __name__ == '__main__':
    app.run()
