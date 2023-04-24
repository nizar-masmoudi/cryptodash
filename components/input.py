from dash import html, callback, Output, Input, State, MATCH, ALL
import re
from dash import dcc
from dash_svg import Svg, Path
import uuid
from dotenv import load_dotenv
from api import APIClient
import os

load_dotenv() # Dev only
api = APIClient(api_key = os.getenv('RAPID_API_KEY'), api_host = os.getenv('RAPID_API_HOST'))

class AutoCompleteAIO(html.Div):
  class ids:
    input = lambda aio_id: {
      'component': 'AutoCompleteAIO',
      'subcomponent': 'input',
      'aio_id': aio_id
    }
    ul = lambda aio_id: {
      'component': 'AutoCompleteAIO',
      'subcomponent': 'ul',
      'aio_id': aio_id
    }
    parent = lambda aio_id: {
      'component': 'AutoCompleteAIO',
      'subcomponent': 'parent',
      'aio_id': aio_id
    }
  ids = ids
  
  def __init__(self, placeholder: str = None, aio_id = None):
    if aio_id is None:
      aio_id = str(uuid.uuid4())
    
    super().__init__(id = self.ids.parent(aio_id), children = [
      html.Div(children = [
        Svg([
          Path(d = 'M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z')
        ], className = 'w-6 h-6 stroke-white/75 fill-none'),
        dcc.Input(className = 'w-full bg-transparent font-light', placeholder = placeholder, id = self.ids.input(aio_id))
      ], className = 'absolute top-0 flex items-center space-x-4 h-12 w-full'),
      html.Ul(id = self.ids.ul(aio_id), children = [], className = 'absolute top-12 my-2 ml-4')
    ], className = 'transition-all duration-300 z-20 relative bg-[#21222D] rounded-lg px-4 h-12 min-h-12 w-1/3 overflow-hidden text-white/75 focus-within:border border-[#2595fd]')
  
  @callback(
    Output(ids.ul(MATCH), 'children'),
    Output(ids.input(MATCH), 'value'),
    Output(ids.parent(MATCH), 'className'),
    Input(ids.input(MATCH), 'value'),
    Input(ids.parent(MATCH), 'className'),
    Input({'type': 'option', 'index': ALL}, 'n_clicks'),
    State({'type': 'option', 'index': ALL}, 'children'),
    prevent_initial_call = True
  )
  def update_suggestions(value, className, n_clicks, options):
    # This section covers selection
    if n_clicks:
      for i, click in enumerate(n_clicks):
        if click is not None:
          return [], options[i], 'transition-all duration-300 z-20 relative bg-[#21222D] rounded-lg px-4 h-12 min-h-12 w-1/3 overflow-hidden text-white/75 focus-within:border border-[#2595fd]' # Default style
    # This section covers on input value change
    if value:
      coins, _ = api.get_coins(search = value) # limit = 5000
      children = []
      for i, coin in enumerate(coins):
        if value.lower() in coin['name'].lower():
          children.append(html.Li(id = {'type': 'option', 'index': f'{i}'}, value = coin['uuid'], children = coin['name'], className = 'h-9 cursor-pointer'))
      height = 48 + 36*min(len(children), 5) + 10 if children else 48
      className = re.sub('h-(\d{2,3}|\[\d{2,3}px\]) min-h-(\d{2,3}|\[\d{2,3}px\])', 'h-[{}px] min-h-[{}px]'.format(height, height), className)
      return children, value, className
    return [], value, 'transition-all duration-300 z-20 relative bg-[#21222D] rounded-lg px-4 h-12 min-h-12 w-1/3 overflow-hidden text-white/75 focus-within:border border-[#2595fd]' # Default style
