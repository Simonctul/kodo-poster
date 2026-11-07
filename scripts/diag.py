import os, json, requests
A="https://graph.facebook.com/v21.0"; T=os.environ["IG_TOKEN"]; I=os.environ["IG_USER_ID"]
def g(m,p,**k):
    k["access_token"]=T
    r=requests.request(m,f"{A}/{p}",**({"data":k} if m=="POST" else {"params":k}),timeout=60)
    print(m,p,k.get("media_type",""),r.status_code,r.text[:400].replace(T,"***"))
g("GET","me/permissions")
g("GET",f"{I}",fields="username,media_count,account_type")
g("GET",f"{I}/content_publishing_limit",fields="quota_usage,config")
g("POST",f"{I}/media",image_url="https://raw.githubusercontent.com/Simonctul/kodo-poster/main/media/victoria_1.jpg",caption="t")
g("POST",f"{I}/media",media_type="REELS",video_url="https://raw.githubusercontent.com/Simonctul/kodo-poster/main/media/kodor_reel.mp4",caption="t")
g("POST",f"{I}/media",media_type="REELS",upload_type="resumable",caption="t")
