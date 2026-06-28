import os
import re
import tempfile
import uuid

import requests

# Обычный Telegram-бот может отправлять файлы не больше 50 МБ.
TELEGRAM_FILE_LIMIT = 50 * 1024 * 1024

RAPIDAPI_HOST = 'social-media-video-downloader.p.rapidapi.com'
RAPIDAPI_URL = (
    'https://social-media-video-downloader.p.rapidapi.com'
    '/instagram/v3/media/post/details'
)


def escape_md(text: str) -> str:
    return re.sub(r'([_*\[\]()~`>#+\-=|{}.!\\])', r'\\\1', text)


def extract_shortcode(url: str) -> str:
    """Достаёт shortcode из ссылки Instagram (/reel/<code>/, /p/<code>/ и т.п.)."""
    match = re.search(
        r'instagram\.com/(?:reel|reels|p|tv)/([A-Za-z0-9_-]+)', url
    )
    if not match:
        raise ValueError('Не удалось извлечь shortcode из ссылки')
    return match.group(1)


def get_video_url_via_rapidapi(url: str, api_key: str) -> str:
    """Получает прямую ссылку на видео через RapidAPI."""
    shortcode = extract_shortcode(url)
    response = requests.get(
        RAPIDAPI_URL,
        headers={
            'x-rapidapi-host': RAPIDAPI_HOST,
            'x-rapidapi-key': api_key,
        },
        params={'shortcode': shortcode, 'renderableFormats': '720p,highres'},
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()

    if data.get('error'):
        raise ValueError(f"API вернул ошибку: {data['error']}")

    for content in data.get('contents', []):
        videos = content.get('videos', [])
        if videos:
            return videos[0]['url']

    raise ValueError('Видео не найдено в ответе API')


def download_video(video_url: str) -> str:
    """Скачивает видео по прямой ссылке во временный файл.

    Возвращает путь к файлу. Вызывающая сторона обязана удалить файл.
    """
    tmp_path = os.path.join(tempfile.gettempdir(), f'{uuid.uuid4().hex}.mp4')
    with requests.get(video_url, stream=True, timeout=60) as r:
        r.raise_for_status()
        with open(tmp_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return tmp_path
