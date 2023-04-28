import dash
from components import HeaderAIO, AutoCompleteAIO, IndicatorAIO, TableAIO, SparklineAIO, MenuAIO
from dash import html

dash.register_page(__name__, path = '/')

layout = html.Div([
  HeaderAIO([
    AutoCompleteAIO(placeholder = 'Search for coins'),
    MenuAIO()
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
  ], className = 'flex flex-wrap mt-12 gap-6'),
], className = 'w-4/5 h-screen p-10 ml-[20%]')