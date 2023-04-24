from dash import html, callback, Output, Input, State, MATCH
from dotenv import load_dotenv
from dash_svg import Svg, Path
from api import APIClient
import os
from dash import dcc
import uuid
from dash import callback_context
import json

load_dotenv() # Dev only
api = APIClient(api_key = os.getenv('RAPID_API_KEY'), api_host = os.getenv('RAPID_API_HOST'))

def generate_rows(coins: list[dict], stats: dict):
  for i in range(len(coins)):
    yield html.Span([
      html.Img(src = coins[i]['iconUrl'], className = 'w-6 h-6'), 
      html.P(coins[i]['name'])
    ], className = 'flex items-center space-x-3')
    yield html.P(coins[i]['symbol'])
    yield html.P('${:,.2f}'.format(float(coins[i]['price'])))
    yield html.Span([
      html.Div([], className = 'w-0 h-0 border-l-8 border-l-transparent border-b-[14px] border-r-8 border-r-transparent -translate-y-px {}'.format('border-b-green-600 rotate-0' if float(coins[i]['change']) > 0 else 'border-b-red-600 rotate-180')),
      html.P('{:.2f}%'.format(float(coins[i]['change'])), className = '{} text-lg'.format('text-green-600' if float(coins[i]['change']) > 0 else 'text-red-600')) 
    ], className = 'flex items-center space-x-2')
    yield html.P('{:.2%}'.format(float(coins[i]['marketCap'])/float(stats['totalMarketCap'])))
    yield html.Div(className = 'w-full h-px bg-white/5 col-span-5 rounded-full')

class TableAIO(html.Div):
  class ids:
    button_prev = lambda aio_id: {
      'component': 'TableAIO',
      'subcomponent': 'button_prev',
      'aio_id': aio_id
    }
    button_next = lambda aio_id: {
      'component': 'TableAIO',
      'subcomponent': 'button_next',
      'aio_id': aio_id
    }
    button_first = lambda aio_id: {
      'component': 'TableAIO',
      'subcomponent': 'button_first',
      'aio_id': aio_id
    }
    button_last = lambda aio_id: {
      'component': 'TableAIO',
      'subcomponent': 'button_last',
      'aio_id': aio_id
    }
    page_counter = lambda aio_id: {
      'component': 'TableAIO',
      'subcomponent': 'page_counter',
      'aio_id': aio_id
    }
    p = lambda aio_id: {
      'component': 'TableAIO',
      'subcomponent': 'p',
      'aio_id': aio_id
    }
    table = lambda aio_id: {
      'component': 'TableAIO',
      'subcomponent': 'table',
      'aio_id': aio_id
    }
    
  ids = ids
    
  def __init__(self, aio_id = None):
    if aio_id is None:
      aio_id = str(uuid.uuid4())
    coins, stats = api.get_coins(limit = 10)
    header = ['CURRENCY', 'SYMBOL', 'PRICE', 'CHANGE', 'MARKET CAP']
    
    super().__init__([
      dcc.Store(data = 1, id = self.ids.page_counter(aio_id)),
      html.Span(id = self.ids.table(aio_id), children = [
        # Header
        *[html.P(title.upper(), className = 'text-white/50') for title in header],
        html.Div(className = 'w-full h-px col-span-5 rounded-full'),
        # Rows
        *list(generate_rows(coins, stats))
      ], className = 'grid grid-cols-5 auto-cols-max gap-y-4'),
      html.Span([
        html.Span([
          Svg(id = self.ids.button_first(aio_id), children = [
            Path(d = 'M11.25 4.5l7.5 7.5-7.5 7.5m-6-15l7.5 7.5-7.5 7.5', strokeLinecap = 'round', strokeLinejoin = 'round')
          ], viewBox = '0 0 24 24', className = 'fill-none stroke-white/50 w-6 h-6 rotate-180 cursor-pointer'),
          Svg(id = self.ids.button_prev(aio_id), children = [
            Path(d = 'M8.25 4.5l7.5 7.5-7.5 7.5', strokeLinecap = 'round', strokeLinejoin = 'round')
          ], viewBox = '0 0 24 24', className = 'fill-none stroke-white/50 w-6 h-6 rotate-180 cursor-pointer'),
          html.P(id = self.ids.p(aio_id), className = 'text-white/50 font-light mx-4'),
          Svg(id = self.ids.button_next(aio_id), children = [
            Path(d = 'M8.25 4.5l7.5 7.5-7.5 7.5', strokeLinecap = 'round', strokeLinejoin = 'round')
          ], viewBox = '0 0 24 24', className = 'fill-none stroke-white/50 w-6 h-6 cursor-pointer'),
          Svg(id = self.ids.button_last(aio_id), children = [
            Path(d = 'M11.25 4.5l7.5 7.5-7.5 7.5m-6-15l7.5 7.5-7.5 7.5', strokeLinecap = 'round', strokeLinejoin = 'round')
          ], viewBox = '0 0 24 24', className = 'fill-none stroke-white/50 w-6 h-6 cursor-pointer'),
        ], className = 'flex items-center justify-center'),
      ], className = 'flex w-full justify-center mt-6')
    ])
  
  @callback(
   Output(ids.page_counter(MATCH), 'data'),
   Input(ids.button_prev(MATCH), 'n_clicks'),
   Input(ids.button_next(MATCH), 'n_clicks'),
   Input(ids.button_first(MATCH), 'n_clicks'),
   Input(ids.button_last(MATCH), 'n_clicks'),
   State(ids.page_counter(MATCH), 'data'),
   prevent_initial_call = True,
  )
  def update_page(n_clicks_prev, n_clicks_next, n_clicks_first, n_clicks_last, page):
    trigger = callback_context.triggered[0]
    button = json.loads(trigger['prop_id'].split('.')[0])['subcomponent']
    if button == 'button_prev':
      if page == 1:
        return page
      page -= 1
    elif button == 'button_next':
      # Only show 100 coins (no need to go through 2500 pages)
      if page == 10:
        return page
      page += 1
    elif button == 'button_first':
      return 1
    else:
      return 10
    return page
  
  @callback(
    Output(ids.p(MATCH), 'children'),
    Output(ids.table(MATCH), 'children'),
    Input(ids.page_counter(MATCH), 'data'),
  )
  def on_page_change(page):
    coins, stats = api.get_coins(offset = 10*(page - 1), limit = 10)
    header = ['CURRENCY', 'SYMBOL', 'PRICE', 'CHANGE', 'MARKET CAP']
    return (
      f'Page {page} of 10',
      # Header
      [*[html.P(title.upper(), className = 'text-white/50') for title in header],
      html.Div(className = 'w-full h-px col-span-5 rounded-full'),
      # Rows
      *list(generate_rows(coins, stats))]
    )