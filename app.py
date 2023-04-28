import dash
from dash import Dash, html
from components import SidebarAIO, HeaderAIO, AutoCompleteAIO, IndicatorAIO, TableAIO, SparklineAIO, MenuAIO
import argparse

parser = argparse.ArgumentParser(prog = 'CryptoDash', description = 'A dashboard for tracking cryptocurrency prices.')
parser.add_argument('--debug', action = 'store_true')
args = parser.parse_args()

app = Dash(__name__, external_scripts = ['https://cdn.tailwindcss.com'], use_pages = True)

app.layout = html.Div([
  # Sidebar
  SidebarAIO(),
  # Content
  dash.page_container
], className = 'w-screen min-h-screen')


if __name__ == '__main__':
    app.run_server(debug = args.debug)