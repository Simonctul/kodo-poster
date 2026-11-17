import os, requests
A="https://graph.facebook.com/v21.0"; T=os.environ["IG_TOKEN"]; I=os.environ["IG_USER_ID"]
r=requests.get(f"{A}/{I}/media",params={"fields":"id,media_product_type,timestamp,caption","limit":6,"access_token":T})
for m in r.json().get("data",[]): print("MEDIA",m["timestamp"],m.get("media_product_type"),(m.get("caption") or "")[:50].replace("\n"," "))
r=requests.get(f"{A}/{I}",params={"fields":"username,account_type","access_token":T}); print("ACC",r.text)
