from dash import Dash, html
from components import SidebarAIO, HeaderAIO, AutoCompleteAIO, IndicatorAIO, TableAIO, SparklineAIO

app = Dash(__name__, external_scripts = ['https://cdn.tailwindcss.com'])

app.layout = html.Div([
  # Sidebar
  SidebarAIO(),
  # Content
  html.Div([
    HeaderAIO([
      AutoCompleteAIO(placeholder = 'Search for coins')
    ]),
    html.Span([
      html.Div([IndicatorAIO(coin_id = 'Qwsogvtv82FCd')], className = 'relative w-[calc(50%-12px)] h-48 bg-[#21222D] rounded-xl p-8'),
      html.Div([IndicatorAIO(coin_id = 'razxDUgYGNAdQ')], className = 'relative w-[calc(50%-12px)] h-48 bg-[#21222D] rounded-xl p-8'),
      html.Div([
        SparklineAIO(coin_id = 'Qwsogvtv82FCd')
      ], className = 'w-full bg-[#21222D] rounded-xl p-8 text-white'),
      html.Div([
        TableAIO()
      ], className = 'w-full bg-[#21222D] rounded-xl p-8 text-white')
    ], className = 'flex flex-wrap mt-12 gap-6')
  ], className = 'w-4/5 h-screen p-10 ml-[20%]')
], className = 'w-screen min-h-screen')


if __name__ == '__main__':
    app.run_server()