from dash import html

class HeaderAIO(html.Div):
  def __init__(self, children: list = None):
    super().__init__(children, className = 'flex items-start justify-between w-full h-12')