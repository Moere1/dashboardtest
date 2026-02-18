"""
Страница экономики
"""

from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

def create_layout(app):
    """Создание лейаута страницы экономики"""
    
    return html.Div([
        dbc.Row([
            dbc.Col([
                html.H1(
                    [
                        html.I(className="fas fa-chart-line me-3 text-primary"),
                        "Экономика"
                    ],
                    className="display-4 mb-4"
                ),
                html.P(
                    "Анализ экономических показателей и развития Тульской области",
                    className="lead text-muted mb-5"
                ),
            ])
        ]),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("ВРП", className="card-title"),
                        html.H2("542.3 млрд ₽", className="text-primary"),
                        html.P("↑ 4.2% за год", className="text-success"),
                        dcc.Graph(
                            figure=create_gdp_chart(),
                            config={'displayModeBar': False}
                        )
                    ])
                ], className="shadow-sm h-100")
            ], md=4),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Инвестиции", className="card-title"),
                        html.H2("98.5 млрд ₽", className="text-primary"),
                        html.P("↑ 12.5% за год", className="text-success"),
                        dcc.Graph(
                            figure=create_investment_chart(),
                            config={'displayModeBar': False}
                        )
                    ])
                ], className="shadow-sm h-100")
            ], md=4),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Промпроизводство", className="card-title"),
                        html.H2("105.3%", className="text-primary"),
                        html.P("↑ 2.1% за год", className="text-success"),
                        dcc.Graph(
                            figure=create_industry_chart(),
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
                        html.H5("Структура экономики", className="mb-0"),
                    ]),
                    dbc.CardBody([
                        dcc.Graph(
                            figure=create_economy_structure(),
                            config={'displayModeBar': True}
                        )
                    ])
                ], className="shadow-sm mb-4")
            ], md=6),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5("Ключевые предприятия", className="mb-0"),
                    ]),
                    dbc.CardBody([
                        dcc.Graph(
                            figure=create_top_enterprises(),
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
                        html.H5("Динамика промышленного производства", className="mb-0"),
                    ]),
                    dbc.CardBody([
                        dcc.Graph(
                            figure=create_industry_dynamics(),
                            config={'displayModeBar': True}
                        )
                    ])
                ], className="shadow-sm mb-4")
            ])
        ]),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5("Инвестиции по отраслям", className="mb-0"),
                    ]),
                    dbc.CardBody([
                        dcc.Graph(
                            figure=create_investment_by_sector(),
                            config={'displayModeBar': True}
                        )
                    ])
                ], className="shadow-sm")
            ])
        ])
    ])

def create_gdp_chart():
    """График ВРП"""
    years = ['2019', '2020', '2021', '2022', '2023', '2024']
    gdp = [485, 468, 502, 521, 542, 560]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=years,
        y=gdp,
        mode='lines+markers',
        line=dict(color='#1f77b4', width=3),
        fill='tozeroy',
        fillcolor='rgba(31, 119, 180, 0.1)',
        hovertemplate='Год: %{x}<br>ВРП: %{y} млрд ₽<extra></extra>'
    ))
    
    # Добавим столбцы темпов роста
    growth = [gdp[i] / gdp[i-1] * 100 - 100 for i in range(1, len(gdp))]
    
    fig.update_layout(
        title='Динамика ВРП (млрд ₽)',
        xaxis_title='Год',
        yaxis_title='Млрд рублей',
        template='plotly_white',
        height=300,
        margin=dict(l=40, r=40, t=50, b=40),
        showlegend=False
    )
    
    # Добавим аннотации с темпами роста
    for i, (year, value, gr) in enumerate(zip(years[1:], gdp[1:], growth)):
        fig.add_annotation(
            x=year,
            y=value,
            text=f"+{gr:.1f}%",
            showarrow=True,
            arrowhead=1,
            ax=0,
            ay=-40,
            font=dict(color='green' if gr > 0 else 'red')
        )
    
    return fig

def create_investment_chart():
    """График инвестиций"""
    years = ['2019', '2020', '2021', '2022', '2023', '2024']
    investment = [82, 78, 85, 91, 98, 105]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=years,
        y=investment,
        marker_color='#ff7f0e',
        text=[f"{v} млрд ₽" for v in investment],
        textposition='outside',
        hovertemplate='Год: %{x}<br>Инвестиции: %{y} млрд ₽<extra></extra>'
    ))
    
    fig.update_layout(
        title='Инвестиции в основной капитал',
        xaxis_title='Год',
        yaxis_title='Млрд рублей',
        template='plotly_white',
        height=300,
        margin=dict(l=40, r=40, t=50, b=40),
        showlegend=False
    )
    
    return fig

def create_industry_chart():
    """График промпроизводства"""
    years = ['2019', '2020', '2021', '2022', '2023', '2024']
    index = [102.5, 98.2, 104.8, 103.2, 105.3, 106.1]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=years,
        y=index,
        mode='lines+markers',
        line=dict(color='#2ca02c', width=3),
        hovertemplate='Год: %{x}<br>Индекс: %{y}%<extra></extra>'
    ))
    
    # Добавим линию 100%
    fig.add_hline(
        y=100,
        line_dash="dash",
        line_color="red",
        annotation_text="100%",
        annotation_position="bottom right"
    )
    
    fig.update_layout(
        title='Индекс промышленного производства (%)',
        xaxis_title='Год',
        yaxis_title='% к предыдущему году',
        template='plotly_white',
        height=300,
        margin=dict(l=40, r=40, t=50, b=40),
        showlegend=False
    )
    
    return fig

def create_economy_structure():
    """Структура экономики"""
    sectors = ['Обрабатывающие производства', 'Торговля', 'Транспорт', 
               'Строительство', 'Сельское хозяйство', 'Добыча полезных',
               'Энергетика', 'Образование', 'Здравоохранение', 'Прочее']
    
    shares = [32.5, 15.2, 8.8, 7.5, 6.2, 5.8, 5.5, 4.8, 4.2, 9.5]
    
    # Создадим treemap для лучшей визуализации структуры
    fig = go.Figure(go.Treemap(
        labels=sectors,
        parents=[''] * len(sectors),
        values=shares,
        textinfo="label+percent entry",
        hovertemplate='<b>%{label}</b><br>Доля: %{percentRoot:.1%}<br>ВРП: %{value}%<extra></extra>',
        marker=dict(
            colors=shares,
            colorscale='Blues',
            showscale=True,
            colorbar=dict(title="Доля, %")
        )
    ))
    
    fig.update_layout(
        title='Структура ВРП по видам деятельности',
        height=500,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    
    return fig

def create_top_enterprises():
    """Топ предприятий"""
    enterprises = ['Тулачермет', 'Щекиноазот', 'АК ТУЛАМАШЗАВОД', 
                   'Новомосковская ГРЭС', 'ЕВРАЗ Ванадий Тула',
                   'Тульский патронный завод', 'Полипласт', 
                   'Косогорский металлургический завод']
    
    revenue = [85.2, 72.5, 45.8, 38.2, 32.5, 28.9, 25.4, 22.1]
    
    # Сортируем по убыванию
    sorted_data = sorted(zip(enterprises, revenue), key=lambda x: x[1], reverse=True)
    ent_sorted, rev_sorted = zip(*sorted_data)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=rev_sorted,
        y=ent_sorted,
        orientation='h',
        marker=dict(
            color=rev_sorted,
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title="Млрд ₽")
        ),
        text=[f"{r:.1f} млрд ₽" for r in rev_sorted],
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Выручка: %{x:.1f} млрд ₽<extra></extra>'
    ))
    
    fig.update_layout(
        title='Крупнейшие предприятия области по выручке',
        xaxis_title='Выручка (млрд ₽)',
        yaxis_title='',
        template='plotly_white',
        height=400,
        margin=dict(l=200, r=50, t=50, b=40)
    )
    
    return fig

def create_industry_dynamics():
    """Динамика промышленности по отраслям"""
    quarters = ['Q1 2023', 'Q2 2023', 'Q3 2023', 'Q4 2023', 'Q1 2024', 'Q2 2024']
    
    sectors = {
        'Металлургия': [102.5, 103.2, 104.1, 105.5, 106.2, 107.1],
        'Химическая': [104.2, 105.1, 106.5, 107.2, 108.5, 109.8],
        'Машиностроение': [98.5, 99.2, 100.5, 101.8, 103.2, 104.5],
        'Пищевая': [101.2, 101.8, 102.5, 103.1, 103.8, 104.2],
        'Легкая': [95.2, 96.5, 97.8, 98.5, 99.2, 100.1]
    }
    
    fig = go.Figure()
    
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    
    for (sector, values), color in zip(sectors.items(), colors):
        fig.add_trace(go.Scatter(
            x=quarters,
            y=values,
            name=sector,
            mode='lines+markers',
            line=dict(color=color, width=2),
            hovertemplate='<b>%{x}</b><br>' + sector + ': %{y}%<extra></extra>'
        ))
    
    fig.add_hline(
        y=100,
        line_dash="dash",
        line_color="gray",
        annotation_text="100%",
        annotation_position="bottom right"
    )
    
    fig.update_layout(
        title='Индексы производства по отраслям (%, к аналогичному периоду прошлого года)',
        xaxis_title='Период',
        yaxis_title='%',
        template='plotly_white',
        height=500,
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

def create_investment_by_sector():
    """Инвестиции по отраслям"""
    sectors = ['Промышленность', 'Транспорт', 'Строительство', 
               'Сельское хозяйство', 'Энергетика', 'Торговля',
               'IT и связь', 'Социальная сфера']
    
    investments = [45.2, 12.8, 8.5, 6.2, 5.8, 4.5, 3.2, 2.8]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=sectors,
        y=investments,
        marker=dict(
            color=investments,
            colorscale='Greens',
            showscale=True,
            colorbar=dict(title="Млрд ₽")
        ),
        text=[f"{v:.1f} млрд ₽" for v in investments],
        textposition='outside',
        textangle=0,
        hovertemplate='<b>%{x}</b><br>Инвестиции: %{y:.1f} млрд ₽<extra></extra>'
    ))
    
    fig.update_layout(
        title='Инвестиции по отраслям экономики',
        xaxis_title='',
        yaxis_title='Млрд рублей',
        template='plotly_white',
        height=400,
        xaxis_tickangle=-45,
        margin=dict(l=50, r=50, t=50, b=100)
    )
    
    return fig