import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

# Load the data
df = pd.read_csv('country_wise_latest.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout
app.layout = html.Div([
    html.H1('COVID-19 Global Dashboard'),
    
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='country-dropdown',
                options=[{'label': country, 'value': country} for country in df['Country/Region'].unique()],
                value=['US', 'India', 'Brazil'],
                multi=True
            )
        ], style={'width': '48%', 'display': 'inline-block'}),
        
        html.Div([
            dcc.RadioItems(
                id='metric-radio',
                options=[
                    {'label': 'Confirmed Cases', 'value': 'Confirmed'},
                    {'label': 'Deaths', 'value': 'Deaths'},
                    {'label': 'Recovered', 'value': 'Recovered'}
                ],
                value='Confirmed',
                labelStyle={'display': 'inline-block', 'marginRight': 10}
            )
        ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),
    
    dcc.Graph(id='bar-chart'),
    
    dcc.Graph(id='scatter-plot'),
    
    dcc.Graph(id='choropleth-map'),
    
    html.Div([
        html.H3('Summary and Conclusions'),
        html.P(id='summary-text')
    ])
])

# Callback for updating bar chart
@app.callback(
    Output('bar-chart', 'figure'),
    [Input('country-dropdown', 'value'),
     Input('metric-radio', 'value')]
)
def update_bar_chart(countries, metric):
    filtered_df = df[df['Country/Region'].isin(countries)]
    fig = px.bar(filtered_df, x='Country/Region', y=metric,
                 title=f'{metric} by Country')
    return fig

# Callback for updating scatter plot
@app.callback(
    Output('scatter-plot', 'figure'),
    [Input('country-dropdown', 'value')]
)
def update_scatter_plot(countries):
    filtered_df = df[df['Country/Region'].isin(countries)]
    fig = px.scatter(filtered_df, x='Confirmed', y='Deaths',
                     size='Recovered', color='Country/Region',
                     hover_name='Country/Region', log_x=True, log_y=True,
                     title='Confirmed Cases vs Deaths (log scale)')
    return fig

# Callback for updating choropleth map
@app.callback(
    Output('choropleth-map', 'figure'),
    [Input('metric-radio', 'value')]
)
def update_choropleth_map(metric):
    fig = px.choropleth(df, locations='Country/Region',
                        locationmode='country names',
                        color=metric,
                        hover_name='Country/Region',
                        projection='natural earth',
                        title=f'Global {metric} Distribution')
    return fig

# Callback for updating summary text
@app.callback(
    Output('summary-text', 'children'),
    [Input('country-dropdown', 'value'),
     Input('metric-radio', 'value')]
)
def update_summary(countries, metric):
    filtered_df = df[df['Country/Region'].isin(countries)]
    total = filtered_df[metric].sum()
    avg = filtered_df[metric].mean()
    max_country = filtered_df.loc[filtered_df[metric].idxmax(), 'Country/Region']
    
    summary = f"For the selected countries, the total {metric.lower()} is {total:,.0f}. "
    summary += f"The average {metric.lower()} per country is {avg:,.0f}. "
    summary += f"{max_country} has the highest number of {metric.lower()} among the selected countries."
    
    return summary

if __name__ == '__main__':
    app.run_server(debug=True)
