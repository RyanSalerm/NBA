import dash
import dash_html_components as html
import dash_table
import pandas as pd
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

# Markdown format for image as a link: [![alt text](image link)](web link)
seattle = "[![Seattle](https://upload.wikimedia.org/wikipedia/commons/8/80/SeattleQueenAnne2021-2.png#thumbnail)](https://en.wikipedia.org/wiki/Seattle)"
montreal = "[![Montreal](https://upload.wikimedia.org/wikipedia/commons/d/d0/Montreal_August_2017_05.jpg#thumbnail)](https://en.wikipedia.org/wiki/Montreal)"
nyc = "[![New York City](https://upload.wikimedia.org/wikipedia/commons/f/f7/Lower_Manhattan_skyline_-_June_2017.jpg#thumbnail)](https://en.wikipedia.org/wiki/New_York_City)"

df = pd.DataFrame(
    dict(
        [
            ("temperature", [13, 43, 50]),
            ("city", ["NYC", "Montreal", "Seattle"]),
            ("image", [nyc, montreal, seattle]),
        ]
    )
)

# Função para renderizar o Markdown como HTML
def render_markdown(val):
    return html.Div(dash_html_components.Markdown(val))

app.layout = html.Div(
    [
        dash_table.DataTable(
            id="table-dropdown",
            data=df.to_dict("records"),
            columns=[
                {"id": "image", "name": "image", "presentation": "markdown"},
                {"id": "city", "name": "city"},
                {"id": "temperature", "name": "temperature"},
            ],
            style_cell_conditional=[{"if": {"column_id": "image"}, "width": "200px"},],
            # Use a função de renderização para a coluna "image"
            style_data_conditional=[
                {"if": {"column_id": "image"}, "width": "200px", "textAlign": "center"},
            ],
            style_table={"height": "300px", "overflowY": "auto"},
            style_header={"fontWeight": "bold"},
        )
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
