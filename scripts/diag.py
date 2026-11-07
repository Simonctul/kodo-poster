import os, requests
A="https://graph.facebook.com/v21.0"; T=os.environ["IG_TOKEN"]; I=os.environ["IG_USER_ID"]
r=requests.get(f"{A}/{I}/media",params={"fields":"id,media_type,media_product_type,timestamp,permalink,caption","limit":12,"access_token":T})
print("MEDIA",r.text.replace(T,"***")[:3500])
r=requests.get(f"{A}/{I}/content_publishing_limit",params={"access_token":T,"fields":"quota_usage,config"})
print("LIMIT",r.text)
r=requests.get(f"{A}/debug_token",params={"input_token":T,"access_token":T})
print("DEBUG",r.text.replace(T,"***")[:800])
