from dash import html, dcc
import plotly.graph_objects as go
import uuid
from api import APIClient
from dotenv import load_dotenv
import os
from math import floor, ceil

load_dotenv() # Dev only
api = APIClient(api_key = os.getenv('RAPID_API_KEY'), api_host = os.getenv('RAPID_API_HOST'))

class DashLayout(go.Layout):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    # Set transparent background
    self.paper_bgcolor = 'rgba(0, 0, 0, 0)'
    self.plot_bgcolor = 'rgba(0, 0, 0, 0)'
    self.margin = dict(l = 0, r = 0, t = 0, b = 0)
    self.xaxis = dict(
      gridcolor = 'rgba(255, 255, 255, 0.2)',
      griddash = 'dash',
      color = 'rgba(255, 255, 255, 0.2)',
      linecolor = 'rgba(255, 255, 255, 0.2)',
      zeroline = False,
      fixedrange = True,
      mirror = True,
      showspikes = False,
      # spikemode = 'across',
      # spikesnap = 'data',
      # spikethickness = 1,
      # spikecolor = 'rgba(255, 255, 255, 0.2)',
      # showline = True,
    )
    self.yaxis = dict(
      gridcolor = 'rgba(255, 255, 255, 0.2)',
      griddash = 'dash',
      color = 'rgba(255, 255, 255, 0.2)',
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
      
    )
    super().__init__(data, layout, **kwargs)

class SparklineAIO(html.Span):
  class ids:
    pass
  ids = ids
  
  def __init__(self, coin_id = 'Qwsogvtv82FCd', aio_id = None):
    if aio_id is None:
      aio_id = str(uuid.uuid4())
      
    coin = api.get_coin(coin_id)
    sparkline = coin['sparkline']
    sparkline = [float(price) for price in sparkline]
    datetimes = list(reversed([f'{t+1}h' for t in range(len(sparkline))]))

    super().__init__([
      html.H2('Sparkline', className = 'text-2xl'),
      html.Div(className = 'w-full h-px bg-white/10 my-6'),
      dcc.Graph(figure = Sparkline(x = datetimes, y = sparkline, layout = DashLayout(), layout_yaxis_range = [floor(min(sparkline) / 100)*100, ceil(max(sparkline) / 100)*100]))
    ], className = 'w-full h-full')