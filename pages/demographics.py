"""
Страница демографии
"""

from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

def create_layout(app):
    """Создание лейаута страницы демографии"""
    
    return html.Div([
        dbc.Row([
            dbc.Col([
                html.H1(
                    [
                        html.I(className="fas fa-users me-3 text-primary"),
                        "Демография"
                    ],
                    className="display-4 mb-4"
                ),
                html.P(
                    "Анализ демографической ситуации в Тульской области",
                    className="lead text-muted mb-5"
                ),
            ])
        ]),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Численность населения", className="card-title"),
                        html.H2("1 456 200", className="text-primary"),
                        html.P("↓ 0.3% за год", className="text-danger"),
                        dcc.Graph(
                            figure=create_population_chart(),
                            config={'displayModeBar': False}
                        )
                    ])
                ], className="shadow-sm h-100")
            ], md=4),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Рождаемость", className="card-title"),
                        html.H2("8.2 ‰", className="text-primary"),
                        html.P("↓ 0.5‰ за год", className="text-danger"),
                        dcc.Graph(
                            figure=create_birth_rate_chart(),
                            config={'displayModeBar': False}
                        )
                    ])
                ], className="shadow-sm h-100")
            ], md=4),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Смертность", className="card-title"),
                        html.H2("15.6 ‰", className="text-primary"),
                        html.P("↑ 0.2‰ за год", className="text-danger"),
                        dcc.Graph(
                            figure=create_death_rate_chart(),
                            config={'displayModeBar': False}
                        )
                    ])
                ], className="shadow-sm h-100")
            ], md=4),
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5("Возрастно-половая пирамида", className="mb-0"),
                    ]),
                    dbc.CardBody([
                        dcc.Graph(
                            figure=create_age_pyramid(),
                            config={'displayModeBar': True}
                        )
                    ])
                ], className="shadow-sm mb-4")
            ], md=6),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5("Миграция", className="mb-0"),
                    ]),
                    dbc.CardBody([
                        dcc.Graph(
                            figure=create_migration_chart(),
                            config={'displayModeBar': True}
                        )
                    ])
                ], className="shadow-sm mb-4")
            ], md=6)
        ]),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5("Демографические показатели по годам", className="mb-0"),
                    ]),
                    dbc.CardBody([
                        dcc.Graph(
                            figure=create_demographic_trends(),
                            config={'displayModeBar': True}
                        )
                    ])
                ], className="shadow-sm")
            ])
        ])
    ])

def create_population_chart():
    """График численности населения"""
    years = ['2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024']
    population = [1515, 1506, 1497, 1488, 1479, 1470, 1462, 1455, 1450, 1445]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=years,
        y=population,
        mode='lines+markers',
        line=dict(color='#1f77b4', width=3),
        fill='tozeroy',
        fillcolor='rgba(31, 119, 180, 0.1)',
        hovertemplate='Год: %{x}<br>Население: %{y} тыс.<extra></extra>'
    ))
    
    # Добавим линию тренда
    z = np.polyfit(range(len(population)), population, 1)
    p = np.poly1d(z)
    fig.add_trace(go.Scatter(
        x=years,
        y=p(range(len(population))),
        mode='lines',
        line=dict(color='red', width=2, dash='dash'),
        name='Тренд',
        hovertemplate='Тренд: %{y:.0f} тыс.<extra></extra>'
    ))
    
    fig.update_layout(
        title='Динамика численности населения (тыс. чел.)',
        xaxis_title='Год',
        yaxis_title='Тыс. человек',
        template='plotly_white',
        height=300,
        margin=dict(l=40, r=40, t=50, b=40),
        showlegend=False
    )
    
    return fig

def create_birth_rate_chart():
    """График рождаемости"""
    years = ['2020', '2021', '2022', '2023', '2024']
    birth_rate = [9.2, 8.9, 8.5, 8.3, 8.2]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=years,
        y=birth_rate,
        marker_color='#2ca02c',
        text=[f"{v}‰" for v in birth_rate],
        textposition='outside',
        hovertemplate='Год: %{x}<br>Рождаемость: %{y}‰<extra></extra>'
    ))
    
    # Добавим среднюю линию
    avg_rate = np.mean(birth_rate)
    fig.add_hline(
        y=avg_rate,
        line_dash="dash",
        line_color="red",
        annotation_text=f"Средняя: {avg_rate:.1f}‰",
        annotation_position="bottom right"
    )
    
    fig.update_layout(
        title='Динамика рождаемости (на 1000 человек)',
        xaxis_title='Год',
        yaxis_title='Промилле (‰)',
        template='plotly_white',
        height=300,
        margin=dict(l=40, r=40, t=50, b=40),
        showlegend=False
    )
    
    return fig

def create_death_rate_chart():
    """График смертности"""
    years = ['2020', '2021', '2022', '2023', '2024']
    death_rate = [16.8, 18.2, 16.5, 15.8, 15.6]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=years,
        y=death_rate,
        marker_color='#d62728',
        text=[f"{v}‰" for v in death_rate],
        textposition='outside',
        hovertemplate='Год: %{x}<br>Смертность: %{y}‰<extra></extra>'
    ))
    
    fig.update_layout(
        title='Динамика смертности (на 1000 человек)',
        xaxis_title='Год',
        yaxis_title='Промилле (‰)',
        template='plotly_white',
        height=300,
        margin=dict(l=40, r=40, t=50, b=40),
        showlegend=False
    )
    
    return fig

def create_age_pyramid():
    """Возрастно-половая пирамида"""
    age_groups = ['0-4', '5-9', '10-14', '15-19', '20-24', '25-29', '30-34', 
                  '35-39', '40-44', '45-49', '50-54', '55-59', '60-64', 
                  '65-69', '70-74', '75-79', '80-84', '85+']
    
    male = [35, 38, 40, 42, 45, 48, 52, 55, 58, 60, 58, 55, 50, 45, 38, 30, 20, 12]
    female = [33, 36, 38, 41, 44, 47, 51, 54, 57, 62, 62, 62, 60, 58, 55, 50, 45, 38]
    
    # Создаем пирамиду (мужчины - отрицательные значения)
    y = age_groups
    x_male = [-m for m in male]
    x_female = female
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=y,
        x=x_male,
        name='Мужчины',
        orientation='h',
        marker=dict(color='#1f77b4'),
        hovertemplate='Возраст: %{y}<br>Мужчины: %{customdata} тыс.<extra></extra>',
        customdata=male,
        text=[f"{m} тыс." for m in male],
        textposition='inside',
        textangle=0,
        insidetextanchor='middle'
    ))
    
    fig.add_trace(go.Bar(
        y=y,
        x=x_female,
        name='Женщины',
        orientation='h',
        marker=dict(color='#ff7f0e'),
        hovertemplate='Возраст: %{y}<br>Женщины: %{customdata} тыс.<extra></extra>',
        customdata=female,
        text=[f"{f} тыс." for f in female],
        textposition='inside',
        textangle=0,
        insidetextanchor='middle'
    ))
    
    fig.update_layout(
        title='Возрастно-половая структура населения',
        xaxis_title='Тыс. человек',
        yaxis_title='Возрастные группы',
        barmode='overlay',
        template='plotly_white',
        height=500,
        bargap=0.1,
        xaxis=dict(
            tickvals=[-80, -60, -40, -20, 0, 20, 40, 60, 80],
            ticktext=['80', '60', '40', '20', '0', '20', '40', '60', '80']
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5
        )
    )
    
    return fig

def create_migration_chart():
    """График миграции"""
    years = ['2019', '2020', '2021', '2022', '2023', '2024']
    arrival = [28.5, 24.2, 26.8, 29.4, 31.2, 32.5]
    departure = [26.8, 23.5, 25.2, 27.8, 29.5, 30.8]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=years,
        y=arrival,
        name='Прибывшие',
        marker_color='#2ca02c',
        text=[f"{v} тыс." for v in arrival],
        textposition='inside'
    ))
    
    fig.add_trace(go.Bar(
        x=years,
        y=departure,
        name='Выбывшие',
        marker_color='#d62728',
        text=[f"{v} тыс." for v in departure],
        textposition='inside'
    ))
    
    # Добавим линию миграционного прироста
    net_migration = [a - d for a, d in zip(arrival, departure)]
    fig.add_trace(go.Scatter(
        x=years,
        y=net_migration,
        name='Миграционный прирост',
        mode='lines+markers',
        line=dict(color='gold', width=3),
        yaxis='y2',
        text=[f"{v:.1f} тыс." for v in net_migration],
        textposition='top center'
    ))
    
    fig.update_layout(
        title='Миграционные потоки',
        xaxis_title='Год',
        yaxis_title='Тыс. человек',
        yaxis2=dict(
            title='Миграционный прирост (тыс.)',
            overlaying='y',
            side='right'
        ),
        template='plotly_white',
        height=400,
        barmode='group',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5
        )
    )
    
    return fig

def create_demographic_trends():
    """Демографические тренды"""
    years = ['2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023']
    
    # Данные
    birth_rate = [10.2, 10.5, 9.8, 9.5, 9.2, 8.9, 8.5, 8.3, 8.2]
    death_rate = [16.5, 16.2, 15.9, 15.8, 16.2, 16.8, 18.2, 16.5, 15.8]
    natural_increase = [b - d for b, d in zip(birth_rate, death_rate)]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=years,
        y=birth_rate,
        name='Рождаемость',
        mode='lines+markers',
        line=dict(color='#2ca02c', width=2),
        fill='tozeroy',
        fillcolor='rgba(44, 160, 44, 0.1)'
    ))
    
    fig.add_trace(go.Scatter(
        x=years,
        y=death_rate,
        name='Смертность',
        mode='lines+markers',
        line=dict(color='#d62728', width=2),
        fill='tonexty',
        fillcolor='rgba(214, 39, 40, 0.1)'
    ))
    
    fig.add_trace(go.Bar(
        x=years,
        y=natural_increase,
        name='Естественный прирост',
        marker_color=['#2ca02c' if x > 0 else '#d62728' for x in natural_increase],
        yaxis='y2',
        text=[f"{v:.1f}‰" for v in natural_increase],
        textposition='outside'
    ))
    
    fig.update_layout(
        title='Демографические показатели в динамике',
        xaxis_title='Год',
        yaxis_title='Промилле (‰)',
        yaxis2=dict(
            title='Естественный прирост (‰)',
            overlaying='y',
            side='right'
        ),
        template='plotly_white',
        height=400,
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5
        )
    )
    
    return fig