from dash import html, dcc

class SidebarAIO(html.Div):
  def __init__(self):
    super().__init__([
      dcc.Link('CryptoDash', className = 'block text-4xl font-semibold text-center mb-16', href = '/')
    ], className = 'fixed inset-0 bg-[#13151B] w-1/5 h-screen text-white font-light py-10')