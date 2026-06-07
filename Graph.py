import plotly.express as px
import Database
from dash import Dash, html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
import plotly.io as pio
import Helpers
import Webscraper

# ---------------------------------------------------------------------#
# TODO:
#   Stop storing img in the sql Database, instead live scrape it
# ---------------------------------------------------------------------#
# Set table[0] as default
tables = Database.getTables()
tables.sort()
pdDF = Database.getPriceDateDF(tables[0])
qdDF = Database.getQuantityDateDF(tables[0])
app = Dash(external_stylesheets=[dbc.themes.SANDSTONE])

# Editing Dash app layout
app.layout = dbc.Container(
    [
        # FIRST ROW
        dbc.Row(
            children=[
                html.H1(
                    "Fragrance Buy Cologne Tracker",
                    className="my-3 bg-primary text-light text-decoration-underline py-1",
                ),
            ]
        ),
        # SECOND ROW
        dbc.Row(
            children=[
                # Left Side
                dbc.Col(
                    children=[
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.H2(
                                            "Tracked Fragrances",
                                            className="mt-3 mb-3 bg-primary bg-opacity-75 text-light py-1 text-decoration-underline",
                                        ),
                                        dbc.Input(
                                            placeholder="🔍︎ Search...",
                                            id="graphChoicesSearchBar",
                                        ),
                                        dcc.RadioItems(
                                            options=tables,
                                            value=tables[0],
                                            id="graphChoices",
                                            className="mb-4",
                                            labelStyle={
                                                "display": "block",
                                                "border-block-start": "solid",
                                                "width": "100%",
                                                "border-width": "0.5px",
                                                "border-color": "grey",
                                                "padding-top": "10px",
                                                "padding-bottom": "10px",
                                            },
                                            inputStyle={
                                                "display": "none",
                                            },
                                        ),
                                    ],
                                    className="border border-3 overflow-scroll ",
                                    style={"height": "1000px"},
                                )
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dcc.Input(
                                            id="addCologneInput",
                                            type="text",
                                            className="my-2",
                                            placeholder="Enter New Cologne URL Here...",
                                        )
                                    ],
                                    width="12",
                                ),  # Button Input
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                dbc.Button(
                                                    "Add Cologne",
                                                    id="addCologneButton",
                                                    className="w-auto",
                                                )
                                            ],
                                            width="auto",
                                        ),
                                        dbc.Col(
                                            [
                                                dbc.Button(
                                                    "Remove Cologne",
                                                    id="removeCologneButton",
                                                    color="danger",
                                                    className="w-auto",
                                                )
                                            ],
                                            width="auto",
                                        ),
                                        dbc.Col(
                                            [html.Div(id="addCologneMessage")],
                                            width="auto",
                                        ),
                                    ],
                                    className="justify-content-center",
                                ),
                            ],
                            className="justify-content-center",
                        ),
                    ],
                    width=3,
                ),
                # Right Side
                dbc.Col(
                    children=[
                        # Descriptor and image
                        dbc.Row(
                            children=[
                                # Rightish one
                                dbc.Col(
                                    children=[
                                        html.H2(
                                            "Description",
                                            className="bg-primary bg-opacity-75 text-light py-1 text-decoration-underline w-auto",
                                        ),
                                        html.H4(
                                            id="Description-ProductName",
                                        ),
                                        html.H5(id="description"),
                                        html.A(
                                            "Product Page",
                                            id="Description-URL",
                                            target="_blank",
                                            className="text-primary",
                                        ),
                                        # Live Price
                                        dbc.Row(
                                            children=[
                                                dbc.Col(
                                                    [
                                                        dbc.Card(
                                                            style={"width": "16rem"},
                                                            id="livePriceCard",
                                                        ),
                                                    ],
                                                    width="auto",
                                                ),
                                                # Live Quantity
                                                dbc.Col(
                                                    [
                                                        dbc.Card(
                                                            style={"width": "16rem"},
                                                            id="liveQuantityCard",
                                                        )
                                                    ],
                                                    width="auto",
                                                ),
                                            ],
                                            className="mt-3",
                                        ),
                                    ],
                                    width=7,
                                ),
                                # Leftish one
                                dbc.Col(
                                    children=[
                                        html.Img(
                                            id="productImage",
                                            style={
                                                "width": "100%",
                                                "height": "500px",
                                                "objectFit": "contain",
                                                "borderRadius": "8px",
                                            },
                                        )
                                    ],
                                    width=5,
                                ),
                            ],
                            className="align-items-center border border-3",
                        ),
                        dbc.Row(
                            [
                                dcc.Tabs(
                                    children=[
                                        dcc.Tab(
                                            label="Historical Price Data",
                                            value="priceTab",
                                            selected_className="fw-bold fs-5",
                                            className="fs-5",
                                        ),
                                        dcc.Tab(
                                            label="Historical Quantity Data",
                                            id="quantityTab",
                                            selected_className="fw-bold fs-5",
                                            className="fs-5",
                                        ),
                                    ],
                                    value="priceTab",
                                    id="graphTabs",
                                ),
                                dcc.Graph(id="graph", className="border-3"),
                            ],
                            className="mt-1",
                        ),
                    ],
                    width=9,
                    className="border border-3",
                ),
            ]
        ),
        dbc.Modal(
            [
                # Title
                dbc.ModalHeader(dbc.ModalTitle("⚠︎WARNING⚠︎"), close_button=True),
                # Mid
                dbc.ModalBody(id="areYouSureMessage"),
                # Lower Portion
                dbc.ModalFooter(
                    [
                        dbc.Button(
                            "Keep Cologne",
                            id="keepColognePopup",
                            className="w-auto",
                            color="success",
                        ),
                        dbc.Button(
                            "Remove Cologne",
                            id="removeColognePopup",
                            className="w-auto",
                            color="danger",
                        ),
                    ],
                    className="justify-content-center",
                ),
            ],
            id="confirmRemove",
            centered=True,
            is_open=False,
        ),
    ],
    fluid=True,
)


# ------------------------------CALLBACK FUNCTIONS------------------------#


# RadioItems - Change graph - Callback
@callback(
    # Graph
    Output("graph", "figure"),
    # Description Stuff
    Output("description", "children"),
    Output("productImage", "src"),
    Output("Description-ProductName", "children"),
    Output("Description-URL", "href"),
    # Live Info
    Output("livePriceCard", "children"),
    Output("liveQuantityCard", "children"),
    Input("graphChoices", "value"),
    Input("graphTabs", "value"),
)
def updateGraphDropDown(value, tab):
    # Get Dataframes (Price date & Quantity Date)

    if tab == "priceTab":
        df = Database.getPriceDateDF(value)
        graphFigure = px.line(
            df,
            x="DateScraped",
            y="Price",
            markers=True,
            labels={"Price": "Price of Cologne ($)", "DateScraped": "Time"},
            range_y=[-0.5, None],
        )

    else:
        df = Database.getQuantityDateDF(value)
        graphFigure = px.line(
            df,
            x="DateScraped",
            y="Quantity",
            markers=True,
            labels={"Quantity": "Inventory In Stock", "DateScraped": "Time"},
            range_y=[-0.5, None],
        )

    # Necessary items for product description
    url = Database.getURL(value)

    # Info Cards
    livePrice, liveQuantity, offSalePrice, description, img = Webscraper.scrapeLiveData(
        url
    )

    # Custom Price Cards (On Sale & Not On Sale)
    if offSalePrice is None:
        priceCard = dbc.CardBody(
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
                                    "Off sale",
                                    className="rounded-pill bg-danger bg-opacity-25 w-auto text-danger px-3 fs-6",
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
                            f"${livePrice}", className="opacity-100 fs-2 fw-bolder"
                        ),
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Div(
                                    "No active sale",
                                    className="opacity-50 fs-6 text-dark",
                                ),
                            ],
                            width="auto",
                        )
                    ],
                    justify="start",
                ),
            ],
            className="border-start border-danger border-5",
        )
    else:
        priceCard = dbc.CardBody(
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
                                    "On sale",
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
                            f"${livePrice}", className="opacity-100 fs-2 fw-bolder"
                        ),
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Div(
                                    f"Was ${offSalePrice}",
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
        )

    # Sold out
    if liveQuantity == 0:
        quantityCard = dbc.CardBody(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Div(
                                    "Stock",
                                    className="opacity-50 fs-6 text-decoration-underline fw-bold",
                                ),
                            ],
                            width="auto",
                        ),
                        dbc.Col(
                            [
                                html.Div(
                                    "Sold Out",
                                    className="rounded-pill bg-danger bg-opacity-25 w-auto text-danger px-3 fs-6",
                                ),
                            ],
                            width="auto",
                        ),
                    ],
                    justify="start",
                ),
                dbc.Row(
                    [
                        html.Div(liveQuantity, className="opacity-100 fs-2 fw-bolder"),
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Div(
                                    "Units available",
                                    className="opacity-50 fs-6 text-dark",
                                ),
                            ],
                            width="auto",
                        )
                    ],
                    justify="start",
                ),
            ],
            className="border-start border-danger border-5",
        )

    # One or a few left
    elif liveQuantity <= 10:
        quantityCard = dbc.CardBody(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Div(
                                    "Stock",
                                    className="opacity-50 fs-6 text-decoration-underline fw-bold",
                                ),
                            ],
                            width="auto",
                        ),
                        dbc.Col(
                            [
                                html.Div(
                                    "Few left",
                                    className="rounded-pill bg-warning bg-opacity-25 w-auto text-warning px-3 fs-6",
                                ),
                            ],
                            width="auto",
                        ),
                    ],
                    justify="start",
                ),
                dbc.Row(
                    [
                        html.Div(liveQuantity, className="opacity-100 fs-2 fw-bolder"),
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Div(
                                    "Units available",
                                    className="opacity-50 fs-6 text-dark",
                                ),
                            ],
                            width="auto",
                        )
                    ],
                    justify="start",
                ),
            ],
            className="border-start border-warning border-5",
        )

    # Lots left
    else:
        quantityCard = dbc.CardBody(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Div(
                                    "Stock",
                                    className="opacity-50 fs-6 text-decoration-underline fw-bold",
                                ),
                            ],
                            width="auto",
                        ),
                        dbc.Col(
                            [
                                html.Div(
                                    "In stock",
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
                        html.Div(liveQuantity, className="opacity-100 fs-2 fw-bolder"),
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Div(
                                    "Units available",
                                    className="opacity-50 fs-6 text-dark",
                                ),
                            ],
                            width="auto",
                        )
                    ],
                    justify="start",
                ),
            ],
            className="border-start border-success border-5",
        )

    return (graphFigure, description, img, value, url, priceCard, quantityCard)


# BUTTON - Add Cologne - Callback
@callback(
    Output("addCologneMessage", "children", allow_duplicate=True),
    Output("graphChoices", "options", allow_duplicate=True),
    Output("graph", "figure", allow_duplicate=True),
    # Description Stuff
    Output("description", "children", allow_duplicate=True),
    Output("productImage", "src", allow_duplicate=True),
    Output("Description-ProductName", "children", allow_duplicate=True),
    Output("Description-URL", "href", allow_duplicate=True),
    # Live Info
    Output("livePriceCard", "children", allow_duplicate=True),
    Output("liveQuantityCard", "children", allow_duplicate=True),
    Input("addCologneButton", "n_clicks"),
    State("addCologneInput", "value"),
    prevent_initial_call=True,
)
def addCologne(clicks, url):
    with open("fragranceBuy-Sites.txt", "a+") as file:
        isValid = Helpers.urlValidifier(url)
        file.seek(0)

        newtables = Database.getTables()

        if not isValid:
            return ("INVALID: Unreachable URL, Please Retry..."), newtables

        elif not (str(url).startswith("https://fragrancebuy.ca/products/")):
            return (
                "INVALID: The URL you have entered does not navigate to a fragrancebuy product..."
            ), newtables

        elif url in file:
            return ("INVALID: That product is already being tracked..."), newtables

        else:
            file.write("\n" + url)
            file.flush()
            Webscraper.scrapeOne(url)
            newtables = Database.getTables()

            graphFigure, description, img, value, url2, priceCard, quantityCard = (
                updateGraphDropDown(newtables[len(newtables) - 1], "priceTab")
            )

            newtables.sort()
            return (
                ("VALID: URL added to tracked products..."),
                newtables,
                graphFigure,
                description,
                img,
                value,
                url2,
                priceCard,
                quantityCard,
            )


@callback(
    Output("confirmRemove", "is_open", allow_duplicate=True),
    Output("areYouSureMessage", "children"),
    Input("removeCologneButton", "n_clicks"),
    State("graphChoices", "value"),
    prevent_initial_call=True,
)
def toggleRemovePopup(clicks, value):
    return (True, f"Are you sure you want to stop tracking: {value}?")


@callback(
    Output("confirmRemove", "is_open", allow_duplicate=True),
    Input("keepColognePopup", "n_clicks"),
    prevent_initial_call=True,
)
def keepsCologne(clicks):
    return False


@callback(
    Output("confirmRemove", "is_open", allow_duplicate=True),
    Output("graphChoices", "options"),
    # Graph
    Output("graph", "figure", allow_duplicate=True),
    # Description Stuff
    Output("description", "children", allow_duplicate=True),
    Output("productImage", "src", allow_duplicate=True),
    Output("Description-ProductName", "children", allow_duplicate=True),
    Output("Description-URL", "href", allow_duplicate=True),
    # Live Info
    Output("livePriceCard", "children", allow_duplicate=True),
    Output("liveQuantityCard", "children", allow_duplicate=True),
    Input("removeColognePopup", "n_clicks"),
    State("graphChoices", "value"),
    prevent_initial_call=True,
)
def deleteCologne(clicks, value):

    # Remove new tables from the file
    url = Database.getURL(value)

    with open("fragranceBuy-Sites.txt", "r") as file:
        lines = file.readlines()

    with open("fragranceBuy-Sites.txt", "w") as file:
        for line in lines:
            if not (line.strip() == url):
                file.write(line)

    # Remove Table "Value" from Database
    Database.removeTable(value)

    # Get new tables
    tables = Database.getTables()
    graphFigure, description, img, value2, url2, priceCard, quantityCard = (
        updateGraphDropDown(tables[len(tables) - 1], "priceTab")
    )
    tables.sort()

    return (
        False,
        tables,
        graphFigure,
        description,
        img,
        value2,
        url2,
        priceCard,
        quantityCard,
    )


# Search cologne
@callback(
    Output("graphChoices", "options", allow_duplicate=True),
    Input("graphChoicesSearchBar", "value"),
    prevent_initial_call=True,
)
def searchCologne(search):
    tables = Database.getTables()
    newChoices = []

    if search == "":
        newChoices = tables
    else:
        for table in tables:
            if str(search).lower() in str(table).lower():
                newChoices.append(table)

    return newChoices


if __name__ == "__main__":
    app.run(debug=True)
