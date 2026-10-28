"""Публикация постов, каруселей, рилсов и сторис в Instagram по расписанию.

Читает queue/posts.json, публикует записи, у которых approved=true,
status="scheduled" и время публикации уже наступило. Результат пишет обратно
в queue/posts.json (workflow коммитит изменения).
"""
import json, os, sys, time, datetime as dt
import requests

API = "https://graph.facebook.com/v21.0"
TOKEN = os.environ["IG_TOKEN"]
IG_ID = os.environ["IG_USER_ID"]
REPO = os.environ.get("GITHUB_REPOSITORY", "Simonctul/kodo-poster")
BRANCH = os.environ.get("GITHUB_REF_NAME", "main")
RAW = f"https://raw.githubusercontent.com/{REPO}/{BRANCH}/"
QUEUE = "queue/posts.json"
MAX_ATTEMPTS = 3
DRY = "--dry-run" in sys.argv


def url(path):
    return RAW + path.lstrip("/")


def call(method, endpoint, **params):
    params["access_token"] = TOKEN
    r = requests.request(method, f"{API}/{endpoint}", data=params if method == "POST" else None,
                         params=params if method == "GET" else None, timeout=60)
    data = r.json()
    if r.status_code >= 400 or "error" in data:
        raise RuntimeError(json.dumps(data.get("error", data), ensure_ascii=False))
    return data


def wait_ready(container_id, tries=40):
    for _ in range(tries):
        st = call("GET", container_id, fields="status_code,status")
        code = st.get("status_code")
        if code == "FINISHED":
            return
        if code in ("ERROR", "EXPIRED"):
            raise RuntimeError(f"container {container_id}: {st}")
        time.sleep(8)
    raise RuntimeError(f"container {container_id}: timeout")


def publish_item(it):
    kind = it["type"]
    caption = it.get("caption", "")
    if kind == "image":
        c = call("POST", f"{IG_ID}/media", image_url=url(it["images"][0]), caption=caption)
    elif kind == "carousel":
        kids = []
        for img in it["images"]:
            k = call("POST", f"{IG_ID}/media", image_url=url(img), is_carousel_item="true")
            wait_ready(k["id"])
            kids.append(k["id"])
        c = call("POST", f"{IG_ID}/media", media_type="CAROUSEL", children=",".join(kids), caption=caption)
    elif kind == "reel":
        c = call("POST", f"{IG_ID}/media", media_type="REELS", video_url=url(it["video"]),
                 caption=caption, share_to_feed="true")
    elif kind == "story":
        c = call("POST", f"{IG_ID}/media", media_type="STORIES", image_url=url(it["images"][0]))
    else:
        raise RuntimeError(f"unknown type {kind}")
    wait_ready(c["id"])
    res = call("POST", f"{IG_ID}/media_publish", creation_id=c["id"])
    return res["id"]


def main():
    with open(QUEUE, encoding="utf-8") as f:
        items = json.load(f)
    now = dt.datetime.now(dt.timezone.utc)
    done = 0
    for it in items:
        if it.get("status") != "scheduled" or not it.get("approved"):
            continue
        when = dt.datetime.fromisoformat(it["when"])
        if when > now:
            continue
        print(f"-> {it['id']} ({it['type']})")
        if DRY:
            continue
        it["attempts"] = it.get("attempts", 0) + 1
        try:
            it["media_id"] = publish_item(it)
            it["status"] = "published"
            it["published_at"] = now.isoformat()
            it.pop("error", None)
            done += 1
        except Exception as e:  # noqa: BLE001
            it["error"] = str(e)[:500]
            if it["attempts"] >= MAX_ATTEMPTS:
                it["status"] = "failed"
            print("ошибка:", it["error"])
        break  # не больше одной публикации за запуск
    if not DRY:
        with open(QUEUE, "w", encoding="utf-8") as f:
            json.dump(items, f, ensure_ascii=False, indent=2)
    print("опубликовано:", done)


if __name__ == "__main__":
    main()
