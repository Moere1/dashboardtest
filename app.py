"""
Главный файл дашборда Тульской области
Запуск: python app.py
"""

import os
import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
from dotenv import load_dotenv
import logging
from datetime import datetime

# Загрузка переменных окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Константы
REGION_NAME = os.getenv('REGION_NAME', 'Тульская область')
REGION_CODE = os.getenv('REGION_CODE', '71')
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# Инициализация приложения
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        'https://use.fontawesome.com/releases/v6.0.0/css/all.css'
    ],
    suppress_callback_exceptions=True,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ],
    title=f'Социально-экономический дашборд {REGION_NAME}'
)

server = app.server
app.config.suppress_callback_exceptions = True

# Навигационная панель
navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                dbc.Row(
                    [
                        dbc.Col(html.I(className="fas fa-chart-line fa-2x")),
                        dbc.Col(dbc.NavbarBrand(
                            f"Социально-экономический дашборд {REGION_NAME}",
                            className="ms-2"
                        )),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="/",
                style={"textDecoration": "none"},
            ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            dbc.Collapse(
                dbc.Nav(
                    [
                        dbc.NavItem(dbc.NavLink("Главная", href="/", active="exact")),
                        dbc.NavItem(dbc.NavLink("Рынок труда", href="/labor", active="exact")),
                        dbc.NavItem(dbc.NavLink("Демография", href="/demographics", active="exact")),
                        dbc.NavItem(dbc.NavLink("Экономика", href="/economy", active="exact")),
                        dbc.DropdownMenu(
                            [
                                dbc.DropdownMenuItem("Социальная сфера", href="/social"),
                                dbc.DropdownMenuItem("Промышленность", href="/industry"),
                                dbc.DropdownMenuItem("Инвестиции", href="/investments"),
                                dbc.DropdownMenuItem(divider=True),
                                dbc.DropdownMenuItem("Все показатели", href="/all-indicators"),
                            ],
                            label="Ещё",
                            nav=True,
                        ),
                    ],
                    className="ms-auto",
                    navbar=True,
                ),
                id="navbar-collapse",
                navbar=True,
            ),
        ]
    ),
    color="primary",
    dark=True,
    className="mb-4",
)

# Футер
footer = html.Footer(
    dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.P(
                                [
                                    html.I(className="fas fa-calendar me-2"),
                                    f"Данные обновлены: {datetime.now().strftime('%d.%m.%Y')}"
                                ],
                                className="text-muted"
                            )
                        ],
                        md=6
                    ),
                    dbc.Col(
                        [
                            html.P(
                                [
                                    html.I(className="fas fa-database me-2"),
                                    "Источники: Росстат, Минфин, Банк России"
                                ],
                                className="text-muted text-end"
                            )
                        ],
                        md=6
                    ),
                ]
            )
        ],
        fluid=True,
        className="py-3 border-top mt-4"
    )
)

# Основной лейаут
app.layout = html.Div(
    [
        dcc.Location(id='url', refresh=False),
        navbar,
        dbc.Container(
            [
                dcc.Store(id='session-store', storage_type='session'),
                dcc.Interval(
                    id='interval-component',
                    interval=60*60*1000,  # обновление каждый час
                    n_intervals=0
                ),
                html.Div(id='page-content')
            ],
            fluid=True,
            className="px-4"
        ),
        footer
    ]
)

# Импорт страниц после создания app для избежания циклических импортов
from pages import overview, labor, demographics, economy

# Callback для навигации
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    """Отображение соответствующей страницы"""
    logger.info(f"Navigating to: {pathname}")
    
    if pathname == '/labor':
        return labor.create_layout(app)
    elif pathname == '/demographics':
        return demographics.create_layout(app)
    elif pathname == '/economy':
        return economy.create_layout(app)
    else:
        return overview.create_layout(app)

# Callback для сворачивания навбара на мобильных
@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [dash.dependencies.State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

if __name__ == '__main__':
    logger.info(f"Starting dashboard for {REGION_NAME}")
    app.run(
        debug=DEBUG,
        host=os.getenv('APP_HOST', '127.0.0.1'),
        port=int(os.getenv('APP_PORT', 8050))
    )