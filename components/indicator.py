from dash import html
from dotenv import load_dotenv
from dash_svg import Svg, Path
from api import APIClient
import os

load_dotenv() # Dev only
api = APIClient(api_key = os.getenv('RAPID_API_KEY'), api_host = os.getenv('RAPID_API_HOST'))

class IndicatorAIO(html.Div):
  def __init__(self, coin_id: str = 'Qwsogvtv82FCd'):
    coin = api.get_coin(coin_id)
    super().__init__([
      html.P(coin['name'], className = 'text-white/50 font-semibold'),
      html.H2('${:,.2f}'.format(float(coin['price'])), className = 'text-5xl my-4'),
      html.Span([
          html.Div([], className = 'w-0 h-0 border-l-8 border-l-transparent border-b-[14px] border-r-8 border-r-transparent -translate-y-px {}'.format('border-b-green-600 rotate-0' if float(coin['change']) > 0 else 'border-b-red-600 rotate-180')),
          html.P('{:.2f}%'.format(float(coin['change'])), className = '{} text-lg'.format('text-green-600' if float(coin['change']) > 0 else 'text-red-600')) 
      ], className = 'flex items-center space-x-2'),
      # Tooltip
      html.Div([
        Svg([
          Path(d = 'M256 512A256 256 0 1 0 256 0a256 256 0 1 0 0 512zm0-384c13.3 0 24 10.7 24 24V264c0 13.3-10.7 24-24 24s-24-10.7-24-24V152c0-13.3 10.7-24 24-24zM224 352a32 32 0 1 1 64 0 32 32 0 1 1 -64 0z')
        ], viewBox = '0 0 512 512', className = 'peer absolute right-8 top-8 w-5 h-5 fill-white/20 stroke-4 cursor-pointer'),
        html.Div([
          coin['description']
        ], className = 'transition-opacity duration-200 absolute right-14 top-14 p-2 max-w-sm bg-[#171821] opacity-0 peer-hover:opacity-100 text-sm')
      ])
    ])