from dash import html

class SidebarAIO(html.Div):
  def __init__(self):
    super().__init__([
      html.H1('CryptoDash', className = 'text-4xl font-semibold text-center mb-16')
    ], className = 'fixed inset-0 bg-[#13151B] w-1/5 h-screen text-white font-light py-10')