"""
Главная страница с обзорными показателями
"""

import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Генерация тестовых данных для демонстрации
def generate_sample_data():
    """Генерирует пример данных для демонстрации"""
    dates = pd.date_range(start='2020-01-01', end='2024-12-31', freq='ME')
    
    # Основные показатели
    data = {
        'date': dates,
        'unemployment': 4.5 - 0.3 * np.sin(np.linspace(0, 4*np.pi, len(dates))) + np.random.normal(0, 0.1, len(dates)),
        'salary': 35000 + 5000 * np.linspace(0, 1, len(dates)) + np.random.normal(0, 500, len(dates)),
        'population': 1.48e6 - 2000 * np.linspace(0, 1, len(dates)) + np.random.normal(0, 1000, len(dates)),
        'investment': 80e9 + 10e9 * np.linspace(0, 1, len(dates)) + np.random.normal(0, 2e9, len(dates)),
        'gdp': 500e9 + 30e9 * np.linspace(0, 1, len(dates)) + np.random.normal(0, 5e9, len(dates))
    }
    
    df = pd.DataFrame(data)
    return df

df_sample = generate_sample_data()

# Карточка KPI
def create_kpi_card(title, value, delta, icon, color="primary"):
    """Создание карточки с ключевым показателем"""
    return dbc.Card(
        dbc.CardBody([
            html.Div([
                html.I(className=f"fas fa-{icon} fa-2x text-{color}"),
                html.H6(title, className="card-subtitle mt-2 text-muted"),
                html.H3(f"{value:,.0f}".replace(',', ' '), className="card-title"),
                html.Small(
                    [
                        html.I(
                            className=f"fas fa-arrow-{'up' if delta > 0 else 'down'} me-1",
                            style={"color": "green" if delta > 0 else "red"}
                        ),
                        f"{abs(delta):.1f}% к прошлому году"
                    ],
                    className="text-muted"
                )
            ], className="text-center")
        ]),
        className="shadow-sm h-100"
    )

def create_layout(app):
    """Создание лейаута главной страницы"""
    
    return html.Div([
        # Заголовок
        dbc.Row([
            dbc.Col([
                html.H1(
                    [
                        html.I(className="fas fa-chart-pie me-3 text-primary"),
                        "Обзор социально-экономического положения"
                    ],
                    className="display-4 mb-4"
                ),
                html.P(
                    "Ключевые показатели развития Тульской области в динамике",
                    className="lead text-muted mb-5"
                ),
            ])
        ]),
        
        # Строка с KPI
        dbc.Row([
            dbc.Col(create_kpi_card("ВРП", df_sample['gdp'].iloc[-1] / 1e9, 4.2, "chart-line"), md=3, className="mb-3"),
            dbc.Col(create_kpi_card("Население", df_sample['population'].iloc[-1] / 1e6, -0.3, "users"), md=3, className="mb-3"),
            dbc.Col(create_kpi_card("Ср. зарплата", df_sample['salary'].iloc[-1], 8.5, "ruble-sign"), md=3, className="mb-3"),
            dbc.Col(create_kpi_card("Безработица", df_sample['unemployment'].iloc[-1], -5.2, "briefcase"), md=3, className="mb-3"),
        ]),
        
        # Фильтры
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Фильтры", className="card-title mb-3"),
                        dbc.Row([
                            dbc.Col([
                                html.Label("Период:", className="fw-bold"),
                                dcc.DatePickerRange(
                                    id='date-range',
                                    start_date=df_sample['date'].min(),
                                    end_date=df_sample['date'].max(),
                                    display_format='DD.MM.YYYY',
                                    className="mb-2"
                                ),
                            ], md=4),
                            dbc.Col([
                                html.Label("Муниципалитет:", className="fw-bold"),
                                dcc.Dropdown(
                                    id='municipality-select',
                                    options=[
                                        {'label': 'Все муниципалитеты', 'value': 'all'},
                                        {'label': 'Тула', 'value': 'tula'},
                                        {'label': 'Новомосковск', 'value': 'novomoskovsk'},
                                        {'label': 'Алексин', 'value': 'aleksin'},
                                        {'label': 'Щекино', 'value': 'shchekino'},
                                    ],
                                    value='all',
                                    className="mb-2"
                                ),
                            ], md=4),
                            dbc.Col([
                                html.Label("Показатели:", className="fw-bold"),
                                dcc.Dropdown(
                                    id='indicators-select',
                                    options=[
                                        {'label': 'Все показатели', 'value': 'all'},
                                        {'label': 'ВРП', 'value': 'gdp'},
                                        {'label': 'Инвестиции', 'value': 'investment'},
                                        {'label': 'Зарплата', 'value': 'salary'},
                                    ],
                                    value='all',
                                    multi=True,
                                    className="mb-2"
                                ),
                            ], md=4),
                        ]),
                        dbc.Row([
                            dbc.Col([
                                dbc.Button(
                                    [html.I(className="fas fa-sync me-2"), "Применить"],
                                    color="primary",
                                    id="apply-filters",
                                    className="mt-3"
                                ),
                            ], className="text-end")
                        ])
                    ])
                ], className="shadow-sm mb-4")
            ])
        ]),
        
        # Графики
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5("Динамика ключевых показателей", className="mb-0"),
                    ]),
                    dbc.CardBody([
                        dcc.Graph(
                            id='main-trend-chart',
                            figure=create_trend_chart(df_sample),
                            config={'displayModeBar': True, 'scrollZoom': True}
                        )
                    ])
                ], className="shadow-sm mb-4")
            ], md=8),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5("Структура экономики", className="mb-0"),
                    ]),
                    dbc.CardBody([
                        dcc.Graph(
                            id='sector-pie-chart',
                            figure=create_sector_chart(),
                            config={'displayModeBar': False}
                        )
                    ])
                ], className="shadow-sm mb-4")
            ], md=4)
        ]),
        
        # Вторая строка графиков
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5("Сравнение с регионами ЦФО", className="mb-0"),
                    ]),
                    dbc.CardBody([
                        dcc.Graph(
                            id='region-comparison-chart',
                            figure=create_comparison_chart(),
                            config={'displayModeBar': True}
                        )
                    ])
                ], className="shadow-sm mb-4")
            ], md=6),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5("Тепловая карта показателей", className="mb-0"),
                    ]),
                    dbc.CardBody([
                        dcc.Graph(
                            id='heatmap-chart',
                            figure=create_heatmap(df_sample),
                            config={'displayModeBar': True}
                        )
                    ])
                ], className="shadow-sm mb-4")
            ], md=6)
        ]),
        
        # Таблица с данными
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5("Детальные данные", className="mb-0"),
                    ]),
                    dbc.CardBody([
                        dbc.Tabs([
                            dbc.Tab([
                                html.Div([
                                    html.H6("Основные показатели", className="mt-3"),
                                    dash.dash_table.DataTable(
                                        id='data-table',
                                        columns=[{"name": i, "id": i} for i in df_sample.columns],
                                        data=df_sample.tail(10).to_dict('records'),
                                        page_size=10,
                                        style_table={'overflowX': 'auto'},
                                        style_cell={
                                            'textAlign': 'left',
                                            'padding': '10px',
                                            'fontFamily': 'Arial'
                                        },
                                        style_header={
                                            'backgroundColor': 'rgb(230, 230, 230)',
                                            'fontWeight': 'bold'
                                        }
                                    )
                                ])
                            ], label="Таблица"),
                            
                            dbc.Tab([
                                html.Div([
                                    html.H6("Статистика", className="mt-3"),
                                    dash.dash_table.DataTable(
                                        id='stats-table',
                                        columns=[
                                            {"name": "Показатель", "id": "indicator"},
                                            {"name": "Среднее", "id": "mean"},
                                            {"name": "Мин", "id": "min"},
                                            {"name": "Макс", "id": "max"},
                                            {"name": "Тренд", "id": "trend"}
                                        ],
                                        data=calculate_stats(df_sample),
                                        style_table={'overflowX': 'auto'},
                                        style_cell={'textAlign': 'left', 'padding': '10px'}
                                    )
                                ])
                            ], label="Статистика"),
                        ])
                    ])
                ], className="shadow-sm")
            ])
        ])
    ])

def create_trend_chart(df):
    """Создание графика трендов"""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['gdp'] / 1e9,
        name='ВРП (млрд ₽)',
        line=dict(color='#1f77b4', width=3),
        hovertemplate='Дата: %{x|%d.%m.%Y}<br>ВРП: %{y:.1f} млрд ₽<extra></extra>'
    ))
    
    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['investment'] / 1e9,
        name='Инвестиции (млрд ₽)',
        line=dict(color='#ff7f0e', width=3),
        yaxis='y2',
        hovertemplate='Дата: %{x|%d.%m.%Y}<br>Инвестиции: %{y:.1f} млрд ₽<extra></extra>'
    ))
    
    fig.update_layout(
        title='Динамика ВРП и инвестиций',
        xaxis_title='Дата',
        yaxis_title='ВРП (млрд ₽)',
        yaxis2=dict(
            title='Инвестиции (млрд ₽)',
            overlaying='y',
            side='right'
        ),
        hovermode='x unified',
        template='plotly_white',
        height=400
    )
    
    return fig

def create_sector_chart():
    """Создание круговой диаграммы секторов экономики"""
    sectors = {
        'Промышленность': 42,
        'Торговля': 18,
        'Транспорт': 12,
        'Строительство': 10,
        'Сельское хозяйство': 8,
        'Услуги': 10
    }
    
    fig = go.Figure(data=[go.Pie(
        labels=list(sectors.keys()),
        values=list(sectors.values()),
        hole=.3,
        marker=dict(colors=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b'])
    )])
    
    fig.update_layout(
        title='Структура ВРП по секторам',
        height=400,
        showlegend=True
    )
    
    return fig

def create_comparison_chart():
    """Создание графика сравнения с регионами"""
    regions = ['Тульская', 'Московская', 'Калужская', 'Рязанская', 'Владимирская']
    values = [542, 1250, 380, 295, 268]
    
    fig = go.Figure(data=[
        go.Bar(
            x=regions,
            y=values,
            marker_color=['#1f77b4' if r == 'Тульская' else '#a9a9a9' for r in regions],
            text=values,
            textposition='outside',
            hovertemplate='<b>%{x} область</b><br>ВРП: %{y} млрд ₽<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title='Сравнение ВРП с регионами ЦФО (2023)',
        xaxis_title='Регион',
        yaxis_title='ВРП (млрд ₽)',
        height=400,
        template='plotly_white'
    )
    
    return fig

def create_heatmap(df):
    """Создание тепловой карты корреляций"""
    # Выбираем только числовые колонки
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    corr_matrix = df[numeric_cols].corr()
    
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.columns,
        colorscale='RdBu',
        zmin=-1, zmax=1,
        text=np.round(corr_matrix.values, 2),
        texttemplate='%{text}',
        textfont={"size": 10},
        hovertemplate='<b>%{x}</b> и <b>%{y}</b><br>Корреляция: %{z:.2f}<extra></extra>'
    ))
    
    fig.update_layout(
        title='Корреляция показателей',
        height=400,
        xaxis_title='',
        yaxis_title=''
    )
    
    return fig

def calculate_stats(df):
    """Расчет статистики для таблицы"""
    stats = []
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    for col in numeric_cols:
        # Простой расчет тренда (положительный/отрицательный)
        trend = df[col].iloc[-1] - df[col].iloc[0]
        trend_icon = "↑" if trend > 0 else "↓"
        
        stats.append({
            'indicator': col,
            'mean': f"{df[col].mean():,.0f}".replace(',', ' '),
            'min': f"{df[col].min():,.0f}".replace(',', ' '),
            'max': f"{df[col].max():,.0f}".replace(',', ' '),
            'trend': trend_icon
        })
    
    return stats

# Callbacks для интерактивности
@callback(
    [Output('main-trend-chart', 'figure'),
     Output('sector-pie-chart', 'figure')],
    [Input('date-range', 'start_date'),
     Input('date-range', 'end_date'),
     Input('municipality-select', 'value'),
     Input('apply-filters', 'n_clicks')]
)
def update_charts(start_date, end_date, municipality, n_clicks):
    """Обновление графиков при изменении фильтров"""
    # Фильтруем данные по датам
    mask = (df_sample['date'] >= start_date) & (df_sample['date'] <= end_date)
    filtered_df = df_sample[mask]
    
    # Обновляем графики
    trend_fig = create_trend_chart(filtered_df)
    sector_fig = create_sector_chart()
    
    # Добавляем информацию о фильтрах в заголовки
    if municipality != 'all':
        trend_fig.update_layout(
            title=f"Динамика показателей - {municipality}"
        )
    
    return trend_fig, sector_fig