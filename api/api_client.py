# https://developers.coinranking.com/api/documentation

import requests
from urllib.parse import urljoin

class APIClient:
  def __init__(self, api_key: str, api_host: str) -> None:
    self.api_key = api_key
    self.api_host = api_host
    self.base_url = 'https://coinranking1.p.rapidapi.com'
  
  def get_coins(
    self, 
    currency: str = 'yhjMzLPhuIDl', 
    time_period: str = '24h', 
    order_by: str = 'marketCap', 
    desc: bool = True, 
    limit: int = 50,
    offset: int = 0,
    search: str = ''
  ):
    endpoint = urljoin(self.base_url, '/coins')
    params = {
      'referenceCurrencyUuid': currency,
      'timePeriod': time_period,
      'orderBy': order_by,
      'orderDirection': 'desc' if desc else 'asc',
      'limit': str(limit),
      'offset': offset,
      'search': search
    }
    headers = {
      'X-RapidAPI-Key': self.api_key,
      'X-RapidAPI-Host': self.api_host
    }
    
    try:
      response = requests.get(endpoint, headers = headers, params = params)
    except requests.exceptions.RequestException as e:
      raise SystemExit(e)
    json = response.json()
    return json['data']['coins'], json['data']['stats']
  
  def get_coin(self, uuid: str = 'Qwsogvtv82FCd', currency: str = 'yhjMzLPhuIDl', period: str = '24h'):
    endpoint = urljoin(self.base_url, f'/coin/{uuid}')
    params = {
      'referenceCurrencyUuid': currency,
      'timePeriod': period
    }
    headers = {
      'X-RapidAPI-Key': self.api_key,
      'X-RapidAPI-Host': self.api_host
    }
    
    try:
      response = requests.get(endpoint, headers = headers, params = params)
    except requests.exceptions.RequestException as e:
      raise SystemExit(e)
    json = response.json()
    return json['data']['coin']