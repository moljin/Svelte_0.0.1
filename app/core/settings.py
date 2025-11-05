import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

APP_ENV = "development"
# APP_ENV = "production"
APP_NAME = "Svelte_FastAPI"
APP_VERSION = "0.0.1"
APP_DESCRIPTION = "FastAPI_Svelte을 이용한 프로젝트"

""" DEBUG MODE
개발 과정: true
배포 시: false
"""

PRESENT_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = Path(__file__).resolve().parent.parent
ROOT_DIR = Path(__file__).resolve().parent.parent.parent  ## root폴더
print("APP_DIR: ", APP_DIR)
print("ROOT_DIR: ", ROOT_DIR)

ENV_PATH = os.path.join(ROOT_DIR, ".env")

ORIGINS = [
    # 프론트엔드 개발에 사용되는 포트: 아래 두개(127.0.0.1, localhost)는 별개로 인식한다. 둘다 필요하다.
    "http://localhost:5173",
    "http://localhost:5100",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5100",
]