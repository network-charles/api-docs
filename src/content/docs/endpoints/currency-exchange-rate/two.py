import http.client

conn = http.client.HTTPSConnection("real-time-finance-data.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "7c349ff51amsh15d8f29696cc225p1fe60fjsnca08a8eaed91",
    'x-rapidapi-host': "real-time-finance-data.p.rapidapi.com"
}

conn.request("GET", "/currency-news?from_symbol=USD&to_symbol=EUR&language=en", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))