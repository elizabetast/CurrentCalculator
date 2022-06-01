import requests
dataEUR = requests.get('https://free.currconv.com/api/v7/convert?apiKey=d84cf1bb0ece1d1a78a5&q=EUR_RUB&compact=ultra').json()
resEUR = dataEUR['EUR_RUB']
dataUSD = requests.get('https://free.currconv.com/api/v7/convert?apiKey=d84cf1bb0ece1d1a78a5&q=USD_RUB&compact=ultra').json()
resUSD = dataUSD['USD_RUB']