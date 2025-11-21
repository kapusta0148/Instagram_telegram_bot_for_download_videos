import os
from dotenv import load_dotenv


def dotenv(name):
    key = os.environ.get(name)

    if key is None:
        for file in os.listdir("."):
            if file.endswith(".env"):
                load_dotenv(file)

        key = os.environ.get(name)

    return key
