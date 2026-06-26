import os
import re
import tempfile
import uuid

import yt_dlp

# Обычный Telegram-бот может отправлять файлы не больше 50 МБ.
TELEGRAM_FILE_LIMIT = 50 * 1024 * 1024


def escape_md(text: str) -> str:
    return re.sub(r'([_*\[\]()~`>#+\-=|{}.!\\])', r'\\\1', text)


def mirror_link(url: str) -> str:
    """Ссылка на стороннее зеркало для больших видео (фолбэк)."""
    return url.replace('instagram', 'kksav', 1)


def download_instagram_video(url: str) -> str:
    """Скачивает видео во временный файл и возвращает путь к нему.

    Вызывающая сторона обязана удалить файл после использования.
    """
    out_template = os.path.join(
        tempfile.gettempdir(), f'{uuid.uuid4().hex}.%(ext)s'
    )
    cookies_path = os.path.join(os.path.dirname(__file__), 'cookies.txt')
    ydl_opts = {
        'format': 'mp4/bestvideo+bestaudio/best',
        'outtmpl': out_template,
        'quiet': True,
        'no_warnings': True,
        'noplaylist': True,
    }
    if os.path.exists(cookies_path):
        ydl_opts['cookiefile'] = cookies_path
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)
