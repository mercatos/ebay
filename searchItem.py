from distutils.log import error
import warnings
import requests
import getCredentials
import utils

prod_url_search = 'https://api.ebay.com/buy/browse/v1/item/'
sandbox_url_search = 'https://api.sandbox.ebay.com/buy/browse/v1/item'

def getItemDetails(search_string, limit=15, offset=0, condition=None, buyingOption=None, deliveryCountry=None, epid=None):
  credentials = getCredentials.fetchCredentials()
  headers = {
    'Authorization': f"Bearer {credentials['access_token']}"
  }
  params = {
    'q': search_string, 
    'limit': limit, 
    'offset': offset
  }

  filter = ''
  comma = ''
  if condition:
    fc = utils.getConditionId(condition)
    filter += 'conditionIds:{'+fc+'}'
    comma = ','

  if buyingOption:
    filter += comma + 'buyingOptions:{'+buyingOption+'}'
    comma = ','

  if deliveryCountry:
    filter += comma + 'deliveryCountry:'+deliveryCountry

  if filter != '':
    params['filter'] = filter

  if epid:
    params['epid'] = epid
    
  response = requests.get(f"{sandbox_url_search}", 
    params=params,
    headers=headers
  )
  response_json = response.json()

  required_data = []
  errors = []
  if 'itemSummaries' in response_json:
    for item in response_json['itemSummaries']:
      required_data.append({
        'Item ID': item['title'],
        'Item Title': item['itemId'],
        'Price': item['price'],
        'buyingOption': item['buyingOptions'],
        'condition': item['condition'],
        'URL': item['itemWebUrl']
      })
    return required_data, None
    
  elif 'warnings' in response_json:
    for warn in response_json['warnings']:
      errors.append(warn['message'])
    return None, errors
  else:
    return [], None

# --- Buying Options ---
# FIXED_PRICE
# AUCTION
# BEST_OFFER
# CLASSIFIED_AD


if __name__ == "__main__":
  items, errors = getItemDetails('laptop', 15, 0, 'Used|Excellent - Refurbished|Good|New', 'FIXED_PRICE', 'US')
  print(items, errors)
