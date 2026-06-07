# ------------------- IMPORT STATEMENTS -------------------#
import plotly.express as px
import Database
from dash import Dash, html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
import plotly.io as pio
import Helpers
import Webscraper

# ------------------- INITIALIZING VARIABLES -------------------#
# Set table[0] as default
tables = Database.getTables()
tables.sort()
pdDF = Database.getPriceDateDF(tables[0])
qdDF = Database.getQuantityDateDF(tables[0])
app = Dash(external_stylesheets=[dbc.themes.SANDSTONE])


# ------------------- EDITING THE DASHBOARD LAYOUT -------------------#

app.layout = dbc.Container(
    [
        # Title
        dbc.Row(
            children=[
                html.H1(
                    "Fragrance Buy Cologne Tracker",
                    className="my-3 bg-primary text-light text-decoration-underline py-1",
                ),
            ]
        ),
        # Second Row (Everything under the title)
        dbc.Row(
            children=[
                # Everything on the left side
                dbc.Col(
                    children=[
                        # Above
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        # Left side column title
                                        html.H2(
                                            "Tracked Fragrances",
                                            className="mt-3 mb-3 bg-primary bg-opacity-75 text-light py-1 text-decoration-underline",
                                        ),
                                        # Search bar
                                        dbc.Input(
                                            placeholder="🔍︎ Search...",
                                            id="graphChoicesSearchBar",
                                        ),
                                        # Colognes scrolldown selection menu
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
                                        # Add cologne URL input box
                                        dcc.Input(
                                            id="addCologneInput",
                                            type="text",
                                            className="my-2",
                                            placeholder="Enter New Cologne URL Here...",
                                        )
                                    ],
                                    width="12",
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                # Add new cologne button
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
                                                # Remove currently viewed cologne button
                                                dbc.Button(
                                                    "Remove Cologne",
                                                    id="removeCologneButton",
                                                    color="danger",
                                                    className="w-auto",
                                                )
                                            ],
                                            width="auto",
                                        ),
                                        #!!Might Remove
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
                # Everything on the right side
                dbc.Col(
                    children=[
                        dbc.Row(
                            children=[
                                dbc.Col(
                                    children=[
                                        # Title of this section (large font)
                                        html.H2(
                                            "Description",
                                            className="bg-primary bg-opacity-75 text-light py-1 text-decoration-underline w-auto",
                                        ),
                                        # Name of product (smaller font)
                                        html.H4(
                                            id="Description-ProductName",
                                        ),
                                        # Actual description of the product
                                        html.H5(id="description"),
                                        # Anchor link to product page
                                        html.A(
                                            "Product Page",
                                            id="Description-URL",
                                            target="_blank",
                                            className="text-primary",
                                        ),
                                        dbc.Row(
                                            children=[
                                                dbc.Col(
                                                    [
                                                        # Card to display live price of product
                                                        dbc.Card(
                                                            style={"width": "16rem"},
                                                            id="livePriceCard",
                                                        ),
                                                    ],
                                                    width="auto",
                                                ),
                                                dbc.Col(
                                                    [
                                                        # Card to display live quantity of product
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
                                # Right side of the description box
                                dbc.Col(
                                    children=[
                                        # Image of the selected cologne
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
                        # Bottom of the right side of the page
                        dbc.Row(
                            [
                                # Tabs section to choose price or quantity for the graph
                                dcc.Tabs(
                                    children=[
                                        # Price tab
                                        dcc.Tab(
                                            label="Historical Price Data",
                                            value="priceTab",
                                            selected_className="fw-bold fs-5",
                                            className="fs-5",
                                        ),
                                        # Quantity tab
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
                                # Display the graph (whatever is selected + price/quantity)
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
        # Popup notification that comes up when attempting to remove a cologne
        dbc.Modal(
            [
                # Title
                dbc.ModalHeader(dbc.ModalTitle("⚠︎WARNING⚠︎"), close_button=True),
                # Mid
                dbc.ModalBody(id="areYouSureMessage"),
                # Lower Portion
                dbc.ModalFooter(
                    [
                        # Button to keep cologne (close modal)
                        dbc.Button(
                            "Keep Cologne",
                            id="keepColognePopup",
                            className="w-auto",
                            color="success",
                        ),
                        # Button to remove cologne (stop tracking cologne, then close modal)
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


# Update everything (description and graphs) when a different cologne is pressed from the side bar
@callback(
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
def viewNewCologne(selectedCologneName, tab):
    # Update the graph, depending on which tab was selected
    if tab == "priceTab":
        df = Database.getPriceDateDF(selectedCologneName)
        graphFigure = px.line(
            df,
            x="DateScraped",
            y="Price",
            markers=True,
            labels={"Price": "Price of Cologne ($)", "DateScraped": "Time"},
            range_y=[-0.5, None],
        )

    else:
        df = Database.getQuantityDateDF(selectedCologneName)
        graphFigure = px.line(
            df,
            x="DateScraped",
            y="Quantity",
            markers=True,
            labels={"Quantity": "Inventory In Stock", "DateScraped": "Time"},
            range_y=[-0.5, None],
        )

    # Get all necessary data for the description section
    url = Database.getURL(selectedCologneName)

    # Get all necessary data for the description section
    livePrice, liveQuantity, offSalePrice, description, img = Webscraper.scrapeLiveData(
        fragBuyURL=url
    )

    # Live price cards
    # Not on sale
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
    # Is on sale
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

    # Live quantity cards
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

    return (
        graphFigure,
        description,
        img,
        selectedCologneName,
        url,
        priceCard,
        quantityCard,
    )


# Takes url from textbox, and when button is pressed, attempts to start tracking that product
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
    State("graphChoices", "value"),
    State("graphTabs", "value"),
    State("addCologneInput", "value"),
    prevent_initial_call=True,
)
def addCologne(clicks, currentlyViewedCologne, tab, url):
    with open("fragranceBuy-Sites.txt", "a+") as file:
        # See if we can even access that url
        isValid = Helpers.urlValidifier(url)

        # Go to top of file so we can read everything
        file.seek(0)

        newtables = Database.getTables()

        # Currently selected data (To change nothing if error occurs)
        graphFigure, description, img, value, url2, priceCard, quantityCard = (
            viewNewCologne(currentlyViewedCologne, tab)
        )

        if not isValid:
            return (
                ("INVALID: Unreachable URL, Please Retry..."),
                newtables,
                graphFigure,
                description,
                img,
                value,
                url2,
                priceCard,
                quantityCard,
            )

        elif not (str(url).startswith("https://fragrancebuy.ca/products/")):
            return (
                (
                    "INVALID: The URL you have entered does not navigate to a fragrancebuy product..."
                ),
                newtables,
                graphFigure,
                description,
                img,
                value,
                url2,
                priceCard,
                quantityCard,
            )

        elif url in file:
            return (
                ("INVALID: That product is already being tracked..."),
                newtables,
                graphFigure,
                description,
                img,
                value,
                url2,
                priceCard,
                quantityCard,
            )

        else:
            file.write("\n" + url)
            file.flush()

            # Scrape the newly added link, so we have a starting datapoint for it
            Webscraper.scrapeOne(fragBuyURL=url)
            # Get all the tables that are being tracked (now that a new one has been added)
            newtables = Database.getTables()

            # Get all the information we need to update the page to view the newly added cologne (indexed at the last element, since its ordered by add-by date)
            graphFigure, description, img, value, url2, priceCard, quantityCard = (
                viewNewCologne(newtables[len(newtables) - 1], "priceTab")
            )

            # Sort side list alphabetically
            newtables.sort()

            # Update everything
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


# Popup that is shown when trying to remove a cologne
@callback(
    Output("confirmRemove", "is_open", allow_duplicate=True),
    Output("areYouSureMessage", "children"),
    Input("removeCologneButton", "n_clicks"),
    State("graphChoices", "value"),
    prevent_initial_call=True,
)
def toggleRemovePopup(clicks, value):
    return (True, f"Are you sure you want to stop tracking: {value}?")


# Popup closed when user chooses to keep the cologne
@callback(
    Output("confirmRemove", "is_open", allow_duplicate=True),
    Input("keepColognePopup", "n_clicks"),
    prevent_initial_call=True,
)
def keepsCologne(clicks):
    return False


# Cologne is removed from .txt file and from database if user chooses to remove the cologne
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
def deleteCologne(clicks, selectedCologneTitle):

    url = Database.getURL(selectedCologneTitle)

    with open("fragranceBuy-Sites.txt", "r") as file:
        lines = file.readlines()

    with open("fragranceBuy-Sites.txt", "w") as file:
        # Iterate through all the lines and remove the line that matches the desired colognes URL
        for line in lines:
            if not (line.strip() == url):
                file.write(line)

    # Remove that cologne from database
    Database.removeTable(selectedCologneTitle)

    # Get new tables
    tables = Database.getTables()
    graphFigure, description, img, value2, url2, priceCard, quantityCard = (
        viewNewCologne(tables[len(tables) - 1], "priceTab")
    )
    tables.sort()

    # Update everything, defaulting to last added cologne in database
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


# Search bar implementation
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
            # If the searched thing is in the name of any cologne we are tracking, then show those tables
            if str(search).lower() in str(table).lower():
                newChoices.append(table)

    # Send these new choices to update the side bar
    return newChoices


# ------------------- RUNNING THE PROGRAM -------------------#

if __name__ == "__main__":
    app.run(debug=True)
