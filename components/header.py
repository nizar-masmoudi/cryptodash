from dash import html

class HeaderAIO(html.Div):
  def __init__(self, children: list = None):
    super().__init__(children, className = 'w-full h-12')