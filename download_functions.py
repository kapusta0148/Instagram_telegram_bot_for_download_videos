import re


def escape_md(text: str) -> str:
    return re.sub(r'([_*\[\]()~`>#+\-=|{}.!\\])', r'\\\1', text)


def download_mp4_from_instagram(url):
    return url.replace('instagram', 'kksav', 1)
