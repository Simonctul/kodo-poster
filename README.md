# kodo-poster

Автопубликация в Instagram `kodo_web_studio`.

- `queue/posts.json` — очередь публикаций (`type`: image / carousel / reel / story, `when` — время с часовым поясом, `approved` — разрешение публиковать).
- `media/` — картинки (только JPEG) и видео (MP4), на которые ссылается очередь.
- `scripts/publish.py` — публикация через Instagram Graph API.
- `.github/workflows/publish.yml` — запуск каждые 30 минут.

Секреты репозитория: `IG_TOKEN`, `IG_USER_ID`.
