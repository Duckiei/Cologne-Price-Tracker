# This file is purely for testing designs & implementations of new dash ideas

from dash import Dash, html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
import plotly.io as pio

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container(
    [
        dbc.Card(
            [
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.Div(
                                            "Current Price",
                                            className="opacity-50 fs-6 text-decoration-underline fw-bold",
                                        ),
                                    ],
                                    width="auto",
                                ),
                                dbc.Col(
                                    [
                                        html.Div(
                                            "On Sale",
                                            className="rounded-pill bg-success bg-opacity-25 w-auto text-success px-3 fs-6",
                                        ),
                                    ],
                                    width="auto",
                                ),
                            ],
                            justify="start",
                        ),
                        dbc.Row(
                            [
                                html.Div(
                                    "$12.52",
                                    id="livePrice",
                                    className="opacity-100 fs-2 fw-bolder",
                                ),
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.Div(
                                            "was $52.39",
                                            className="opacity-50 fs-6 text-dark text-decoration-line-through",
                                        ),
                                    ],
                                    width="auto",
                                )
                            ],
                            justify="start",
                        ),
                    ],
                    className="border-start border-success border-5",
                ),
            ],
            style={"width": "16rem"},
        )
    ]
)

if __name__ == "__main__":
    app.run(debug=True)
