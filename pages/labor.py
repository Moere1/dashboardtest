"""
Страница рынка труда
"""

from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

def create_layout(app):
    """Создание лейаута страницы рынка труда"""
    
    return html.Div([
        dbc.Row([
            dbc.Col([
                html.H1(
                    [
                        html.I(className="fas fa-briefcase me-3 text-primary"),
                        "Рынок труда"
                    ],
                    className="display-4 mb-4"
                ),
                html.P(
                    "Анализ занятости, безработицы и заработной платы в Тульской области",
                    className="lead text-muted mb-5"
                ),
            ])
        ]),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Уровень безработицы", className="card-title"),
                        html.H2("3.4%", className="text-primary"),
                        html.P("↓ 0.5% за год", className="text-success"),
                        dcc.Graph(
                            figure=create_unemployment_chart(),
                            config={'displayModeBar': False}
                        )
                    ])
                ], className="shadow-sm h-100")
            ], md=4),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Средняя зарплата", className="card-title"),
                        html.H2("54 280 ₽", className="text-primary"),
                        html.P("↑ 8.3% за год", className="text-success"),
                        dcc.Graph(
                            figure=create_salary_chart(),
                            config={'displayModeBar': False}
                        )
                    ])
                ], className="shadow-sm h-100")
            ], md=4),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Численность занятых", className="card-title"),
                        html.H2("745 тыс.", className="text-primary"),
                        html.P("↑ 2.1% за год", className="text-success"),
                        dcc.Graph(
                            figure=create_employment_chart(),
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
                        html.H5("Занятость по отраслям", className="mb-0"),
                    ]),
                    dbc.CardBody([
                        dcc.Graph(
                            figure=create_industry_employment_chart(),
                            config={'displayModeBar': True}
                        )
                    ])
                ], className="shadow-sm mb-4")
            ], md=8),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5("Вакансии по сферам", className="mb-0"),
                    ]),
                    dbc.CardBody([
                        dcc.Graph(
                            figure=create_vacancies_chart(),
                            config={'displayModeBar': True}
                        )
                    ])
                ], className="shadow-sm mb-4")
            ], md=4)
        ]),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5("Зарплаты по муниципалитетам", className="mb-0"),
                    ]),
                    dbc.CardBody([
                        dcc.Graph(
                            figure=create_municipality_salary_chart(),
                            config={'displayModeBar': True}
                        )
                    ])
                ], className="shadow-sm")
            ])
        ])
    ])

def create_unemployment_chart():
    """График безработицы"""
    months = ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн', 
              'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек']
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=months,
        y=[3.8, 3.7, 3.6, 3.5, 3.4, 3.3, 3.2, 3.1, 3.2, 3.3, 3.4, 3.4],
        mode='lines+markers',
        name='2024',
        line=dict(color='#1f77b4', width=3),
        fill='tozeroy',
        fillcolor='rgba(31, 119, 180, 0.1)'
    ))
    
    fig.add_trace(go.Scatter(
        x=months,
        y=[4.2, 4.1, 4.0, 3.9, 3.8, 3.7, 3.6, 3.5, 3.6, 3.7, 3.8, 3.9],
        mode='lines+markers',
        name='2023',
        line=dict(color='#ff7f0e', width=2, dash='dash')
    ))
    
    fig.update_layout(
        title='Динамика уровня безработицы (%)',
        xaxis_title='Месяц',
        yaxis_title='%',
        hovermode='x unified',
        template='plotly_white',
        height=300,
        margin=dict(l=40, r=40, t=50, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    return fig

def create_salary_chart():
    """График зарплат"""
    years = ['2020', '2021', '2022', '2023', '2024']
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=years,
        y=[42300, 45800, 49200, 52100, 54280],
        name='Средняя зарплата',
        marker_color='#1f77b4',
        text=[f"{v:,.0f} ₽".replace(',', ' ') for v in [42300, 45800, 49200, 52100, 54280]],
        textposition='outside',
        textfont=dict(size=10)
    ))
    
    fig.update_layout(
        title='Динамика средней зарплаты',
        xaxis_title='Год',
        yaxis_title='Рублей',
        template='plotly_white',
        height=300,
        margin=dict(l=40, r=40, t=50, b=40),
        showlegend=False
    )
    
    return fig

def create_employment_chart():
    """График занятости"""
    years = ['2020', '2021', '2022', '2023', '2024']
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=years,
        y=[710, 720, 730, 738, 745],
        mode='lines+markers',
        line=dict(color='#2ca02c', width=3),
        fill='tozeroy',
        fillcolor='rgba(44, 160, 44, 0.1)',
        hovertemplate='Год: %{x}<br>Занятых: %{y} тыс.<extra></extra>'
    ))
    
    fig.update_layout(
        title='Численность занятых (тыс. чел.)',
        xaxis_title='Год',
        yaxis_title='Тыс. человек',
        template='plotly_white',
        height=300,
        margin=dict(l=40, r=40, t=50, b=40),
        showlegend=False
    )
    
    return fig

def create_industry_employment_chart():
    """Занятость по отраслям"""
    industries = [
        'Обрабатывающие производства',
        'Торговля',
        'Образование',
        'Здравоохранение',
        'Строительство',
        'Транспорт',
        'Сельское хозяйство',
        'Гостиницы и общепит',
        'IT и связь',
        'Финансы'
    ]
    
    employment = [142, 98, 76, 68, 52, 48, 42, 35, 18, 12]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=employment,
        y=industries,
        orientation='h',
        marker=dict(
            color=employment,
            colorscale='Blues',
            showscale=True,
            colorbar=dict(title="Тыс. чел.")
        ),
        text=employment,
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Занято: %{x} тыс.<extra></extra>'
    ))
    
    fig.update_layout(
        title='Распределение занятых по отраслям',
        xaxis_title='Тыс. человек',
        yaxis_title='',
        template='plotly_white',
        height=500,
        margin=dict(l=150, r=50, t=50, b=40)
    )
    
    return fig

def create_vacancies_chart():
    """Вакансии по сферам"""
    sectors = ['Продажи', 'Рабочие', 'IT', 'Производство', 'Строительство', 
               'Транспорт', 'Медицина', 'Образование']
    vacancies = [2450, 2100, 1850, 1650, 1200, 980, 750, 620]
    
    fig = go.Figure(data=[go.Pie(
        labels=sectors,
        values=vacancies,
        hole=.3,
        marker=dict(colors=px.colors.qualitative.Set3),
        textinfo='label+percent',
        textposition='auto',
        hovertemplate='<b>%{label}</b><br>Вакансий: %{value}<br>Доля: %{percent}<extra></extra>'
    )])
    
    fig.update_layout(
        title='Структура вакансий',
        height=500,
        showlegend=False,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    
    return fig

def create_municipality_salary_chart():
    """Зарплаты по муниципалитетам"""
    cities = ['Тула', 'Новомосковск', 'Алексин', 'Щекино', 'Ефремов', 
              'Узловая', 'Донской', 'Кимовск', 'Богородицк', 'Суворов']
    salaries = [58900, 51200, 47800, 49500, 44200, 45800, 42100, 43500, 44800, 41200]
    
    # Сортируем по убыванию
    sorted_data = sorted(zip(cities, salaries), key=lambda x: x[1], reverse=True)
    cities_sorted, salaries_sorted = zip(*sorted_data)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=cities_sorted,
        y=salaries_sorted,
        marker_color=salaries_sorted,
        marker_colorscale='Viridis',
        text=[f"{s:,.0f} ₽".replace(',', ' ') for s in salaries_sorted],
        textposition='outside',
        textangle=0,
        hovertemplate='<b>%{x}</b><br>Средняя зарплата: %{y:,.0f} ₽<extra></extra>'
    ))
    
    fig.update_layout(
        title='Среднемесячная зарплата по муниципалитетам',
        xaxis_title='',
        yaxis_title='Рублей',
        template='plotly_white',
        height=400,
        xaxis_tickangle=-45,
        margin=dict(l=50, r=50, t=50, b=100)
    )
    
    return fig