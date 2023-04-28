from dash import html, dcc, callback, Input, Output, MATCH
import plotly.graph_objects as go
import uuid
from api import APIClient
from dotenv import load_dotenv
import os
from math import floor, ceil
import re
from datetime import datetime, timedelta

load_dotenv() # Dev only
api = APIClient(api_key = os.getenv('RAPID_API_KEY'), api_host = os.getenv('RAPID_API_HOST'))

class DashLayout(go.Layout):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    # Set transparent background
    self.paper_bgcolor = 'rgba(0, 0, 0, 0)'
    self.plot_bgcolor = 'rgba(0, 0, 0, 0)'
    self.font = dict(
      family = 'Poppins, sans-serif'
    )
    self.margin = dict(l = 0, r = 0, t = 0, b = 0)
    self.xaxis = dict(
      gridcolor = 'rgba(255, 255, 255, 0.1)',
      color = 'rgba(255, 255, 255, .7)',
      linecolor = 'rgba(255, 255, 255, 0.2)',
      zeroline = False,
      fixedrange = True,
      mirror = True,
      showspikes = False,
    )
    self.yaxis = dict(
      gridcolor = 'rgba(255, 255, 255, 0.1)',
      color = 'rgba(255, 255, 255, .7)',
      linecolor = 'rgba(255, 255, 255, 0.2)',
      zeroline = False,
      fixedrange = True,
      mirror = True,
    )
    self.hoverlabel = dict(
      bgcolor = '#1a2226',
      bordercolor = '#1a2226',
      font_family = 'Poppins, sans-serif',
      font_color = 'white',
      font_size = 15,
    )
    self.hovermode = 'x unified'

class Sparkline(go.Figure):
  def __init__(self, x = None, y = None, layout = None, **kwargs):
    data = go.Scatter(
      x = x, 
      y = y, 
      mode = 'markers+lines',
      line = dict(color = '#26c564'),
      marker = dict(
        size = 10,
        line = dict(color = 'rgba(38, 197, 100, .2)', width = 12)
      ),
      hovertemplate = '$%{y}<extra></extra>',
      # fill = 'tozeroy'
      
    )
    super().__init__(data, layout, **kwargs)

class SparklineAIO(html.Span):
  class ids:
    period = lambda aio_id: {
      'component': 'SparklineAIO',
      'subcomponent': 'period',
      'aio_id': aio_id
    }
    graph = lambda aio_id: {
      'component': 'SparklineAIO',
      'subcomponent': 'graph',
      'aio_id': aio_id
    }
  ids = ids
  
  def __init__(self, coin_id = 'Qwsogvtv82FCd', aio_id = None):
    if aio_id is None:
      aio_id = str(uuid.uuid4())
      
    coin = api.get_coin(coin_id)
    sparkline = coin['sparkline']
    sparkline = [float(price) for price in sparkline]
    datetimes = list(reversed([f'{t+1}h' for t in range(len(sparkline))]))

    super().__init__([
      html.Span([
        html.Img(src = coin['iconUrl'], className = 'w-14 h-14'),
        html.Span([
          html.P(coin['symbol'], className = 'text-white/30'),
          html.H3(coin['name'], className = 'text-2xl font-semibold'),
        ], className = 'flex flex-col justify-between w-56 h-16'),
        html.Div(className = 'w-0.5 h-full bg-white/20'),
        html.Span([
          html.P('LIVE PRICE', className = 'text-white/30'),
          html.Span([
            html.H3('${:,.2f}'.format(float(coin['price'])), className = 'text-2xl font-semibold'),
            html.Div([
              html.Div([], className = 'w-0 h-0 border-l-[6px] border-l-transparent border-b-[10px] border-r-[6px] border-r-transparent -translate-y-px border-b-white {}'.format('rotate-0' if float(coin['change']) > 0 else 'rotate-180')),
              html.P('{}%'.format(abs(float(coin['change'])))),
            ], className = 'flex items-center justify-around w-20 h-8 rounded-md p-2 {}'.format('bg-[#26c363]' if float(coin['change']) > 0 else 'bg-red-600'))
          ], className = 'flex items-center space-x-4'),
        ], className = 'flex flex-col justify-between w-56 h-16'),
        html.Span([
          html.Span([
            html.P('Period', className = 'text-lg'),
            dcc.Dropdown(
              id = self.ids.period(aio_id),
              options = ['1 hour' ,'3 hours' ,'12 hours' ,'24 hours' ,'7 days' ,'30 days' ,'3 months' ,'1 year' ,'3 years' ,'5 years'], 
              value = '24 hours', 
              clearable = False, 
              searchable = False,
            ),
          ], className = 'flex items-center space-x-4'),
        ], className = 'flex flex-col justify-center items-end w-full h-16')
      ], className = 'flex items-center space-x-4 h-14'),
      html.Div([
        dcc.Graph(
          id = self.ids.graph(aio_id), 
          figure = Sparkline(x = datetimes, y = sparkline, layout = DashLayout(), layout_yaxis_range = [floor(min(sparkline) / 100)*100, ceil(max(sparkline) / 100)*100])
        )
      ], className = 'bg-[#171821] rounded-lg p-6 mt-12 border-[1px] border-white/20'),
    ], className = 'w-full h-full')
  
  @callback(
    Output(ids.graph(MATCH), 'figure'),
    Input(ids.period(MATCH), 'value'),
    prevent_initial_call = True,
  )
  def update_graph(period):
    today = datetime.today()
    
    period = re.sub(r'(\d{1,2})\s([a-z]{1})[a-z]*', r'\1\2', period)
    coin = api.get_coin('Qwsogvtv82FCd', period = period)
    sparkline = coin['sparkline']
    sparkline = [float(price) for price in sparkline]
    
    # datetimes = []
    # today = datetime.today() - timedelta(hours = 1)
    # print(d.strftime('%H:%M %p'))
    if period.endswith('m') or period.endswith('y'):
      xs = list(reversed([f'{t+1}' for t in range(len(sparkline))]))
    else:
      days = int(period[:-1]) if period.endswith('d') else 0
      hours = int(period[:-1]) if period.endswith('h') else 0
      delta = timedelta(days = days, hours = hours)
      
      xs = []
      for i in range(1, len(sparkline) + 1):
        digits = []
        d = delta*i/len(sparkline)
        if d.days: digits.append(str(d.days) + 'd')
        if d.seconds//3600: digits.append(str(d.seconds//3600) + 'h')
        if d.seconds%3600: digits.append(str((d.seconds%3600)//60) + 'min')
        xs.append(', '.join(digits))
      xs = xs[::-1]
    
    # if period in ['1h', '3h']:
    #   datetimes = list(reversed([f'{(t+1)*5}min' for t in range(len(sparkline))]))
    # elif period in ['12h', '24h']:
    #   datetimes = list(reversed([f'{t+1}h' for t in range(len(sparkline))]))
    # # elif period in ['']
    # elif period in ['30d']:
    #   datetimes = list(reversed([f'{t+1}d' for t in range(len(sparkline))]))
    # else:
    #   datetimes = list(reversed([f'{t+1}' for t in range(len(sparkline))]))
    
    return Sparkline(x = xs, y = sparkline, layout = DashLayout(), layout_yaxis_range = [floor(min(sparkline) / 100)*100, ceil(max(sparkline) / 100)*100])