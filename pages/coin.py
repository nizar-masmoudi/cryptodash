import dash
from dash import html
from components import HeaderAIO, AutoCompleteAIO, MenuAIO

dash.register_page(__name__, path_template = '/coin/<uuid>')


def layout(uuid = None):
  return html.Div([
    HeaderAIO([
      AutoCompleteAIO(placeholder = 'Search for coins'),
      MenuAIO()
    ]),
    html.Span([
      html.P(f'The user requested coin uuid: {uuid}')
    ], className = 'flex mt-12')
  ], className = 'w-4/5 h-screen p-10 ml-[20%]')