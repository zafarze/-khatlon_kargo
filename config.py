# -*- coding: utf-8 -*-
# config.py
# (!!!) ПОЛНАЯ ИСПРАВЛЕННАЯ ВЕРСИЯ (С ПУТЯМИ К ПАПКЕ IMG) (!!!)

import logging
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# --- Настройка логирования ---
logger = logging.getLogger(__name__)

# --- Определение путей ---
BASE_DIR = Path(__file__).resolve().parent
env_path = BASE_DIR / '.env'

# --- Загрузка .env ---
BOT_TOKEN = os.environ.get("TELEGRAM_TOKEN")
if not BOT_TOKEN:
    logger.critical("❌ КРИТИЧЕСКАЯ ОШИБКА: TELEGRAM_TOKEN не найден в .env файле!")
    sys.exit(1)
else:
    logger.info("✅ TELEGRAM_TOKEN загружен успешно")

# --- База данных ---
DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    logger.critical("❌ КРИТИЧЕСКАЯ ОШИБКА: DATABASE_URL не найден в .env!")
    sys.exit(1)
else:
    logger.info("✅ DATABASE_URL загружен успешно")

# --- ID Администраторов ---
ADMIN_USER_IDS = [
    515809298,   # Zafar
    7990324820,  # uktam2222
]

logger.info(f"✅ Загружено {len(ADMIN_USER_IDS)} ID администраторов")

# --- Настройки Файлов ---
XLSX_FILENAME = "Khatlon.xlsx" # Изменено на Khatlon
BACKUP_DIR = "backups"
ACTIVE_USERS_STATS = "active_users"
CHANNEL_USERNAME = "@khatlon_cargo" # Изменено на новый канал

# --- Создание необходимых директорий ---
try:
    BACKUP_DIR_PATH = BASE_DIR / BACKUP_DIR
    BACKUP_DIR_PATH.mkdir(exist_ok=True)
    logger.info(f"✅ Директория бэкапов создана: {BACKUP_DIR_PATH}")
except Exception as e:
    logger.warning(f"⚠️ Не удалось создать директорию бэкапов: {e}")

# --- Пути к файлам (Фото и Видео в папке img) ---
IMG_DIR = BASE_DIR / 'img'

PHOTO_FILES = {
    "contacts_Bokhtar": "contacts_Bokhtar.png",
    "contacts_Qubodiyon": "contacts_Qubodiyon.png",
    "price_Bokhtar": "price_Bokhtar.png",
    "price_Qubodiyon": "price_Qubodiyon.png",
    "address_tajik_Bokhtar": "address_tajik_Bokhtar.png",
    "address_tajik_Qubodiyon": "address_tajik_Qubodiyon.png",
    "address_china": "address_china.png"
}

PHOTO_CONTACT_PATHS = {
    "Бохтар": IMG_DIR / PHOTO_FILES["contacts_Bokhtar"],
    "Кабодиён": IMG_DIR / PHOTO_FILES["contacts_Qubodiyon"]
}
PHOTO_PRICE_PATHS = {
    "Бохтар": IMG_DIR / PHOTO_FILES["price_Bokhtar"],
    "Кабодиён": IMG_DIR / PHOTO_FILES["price_Qubodiyon"]
}
PHOTO_ADDRESS_TAJIK_PATHS = {
    "Бохтар": IMG_DIR / PHOTO_FILES["address_tajik_Bokhtar"],
    "Кабодиён": IMG_DIR / PHOTO_FILES["address_tajik_Qubodiyon"]
}
PHOTO_ADDRESS_CHINA_PATH = IMG_DIR / PHOTO_FILES["address_china"]

VIDEO_FILES = {
    "address_tajik": "address_tajik.mov"  
}
VIDEO_ADDRESS_TAJIK_PATH = IMG_DIR / VIDEO_FILES["address_tajik"]

# Проверяем существование фото файлов
for region in ["Бохтар", "Кабодиён"]:
    for photo_name, photo_path in [
        (f"Контакты {region}", PHOTO_CONTACT_PATHS[region]),
        (f"Тарифы {region}", PHOTO_PRICE_PATHS[region]),
        (f"Адрес Таджикистан {region}", PHOTO_ADDRESS_TAJIK_PATHS[region])
    ]:
        if photo_path.exists():
            logger.info(f"✅ Фото {photo_name}: {photo_path.name} - найден")
        else:
            logger.warning(f"⚠️ Фото {photo_name}: {photo_path.name} - НЕ НАЙДЕН!")
            logger.warning(f"   Полный путь: {photo_path}")

if PHOTO_ADDRESS_CHINA_PATH.exists():
    logger.info(f"✅ Фото Адрес Китай: {PHOTO_ADDRESS_CHINA_PATH.name} - найден")
else:
    logger.warning(f"⚠️ Фото Адрес Китай: {PHOTO_ADDRESS_CHINA_PATH.name} - НЕ НАЙДЕН!")

# Проверка наличия видео (для логов)
if VIDEO_ADDRESS_TAJIK_PATH.exists():
    logger.info(f"✅ Видео адреса: {VIDEO_ADDRESS_TAJIK_PATH.name} - найдено")
else:
    logger.warning(f"⚠️ Видео адреса: {VIDEO_ADDRESS_TAJIK_PATH.name} - НЕ НАЙДЕНО!")


# --- Настройки JobQueue (Фоновые задачи) ---
JOBS = {
    'reload_codes': {
        'enabled': True,  
        'interval': 300,  # Каждые 300 сек = 5 минут
        'first': 10       # Запустить через 10 сек после старта бота
    },
    'notify_dushanbe': {
        'enabled': True,
        'interval': 300,  # Каждые 300 сек = 5 минут
        'first': 15       # Запустить через 15 сек после старта бота
    }
}

logger.info("✅ Настройки фоновых задач загружены")

# --- Состояния для ConversationHandler (Логика диалогов) ---
(
    START_ROUTES,          # 0
    AWAITING_SUBSCRIPTION, # 1

    # --- ГЛАВНЫЕ СОСТОЯНИЯ ---
    MAIN_MENU,             # 2
    LK_MENU,               # 3
    ADMIN_MENU,            # 4

    # --- РЕГИСТРАЦИЯ ---
    AWAITING_FULL_NAME,    # 5
    AWAITING_PHONE,        # 6
    AWAITING_ADDRESS,      # 7
    AWAITING_LANG_CHOICE,  # 8
    AWAITING_REGION_CHOICE, # 9

    # --- ОТСЛЕЖИВАНИЕ ЗАКАЗА ---
    AWAITING_TRACK_CODE,   # 10

    # --- ЛИЧНЫЙ КАБИНЕТ (ЛК) ---
    LK_AWAIT_DELIVERY_ADDRESS, # 11
    LK_AWAIT_PROFILE_ADDRESS,  # 12
    LK_AWAIT_PHONE,            # 13

    # --- АДМИН-ПАНЕЛЬ ---
    AWAITING_BROADCAST_MESSAGE, # 14
    CONFIRM_BROADCAST,          # 15
    ADMIN_AWAIT_SEARCH_CODE,    # 16

    # --- АДМИНСКОЕ ДОБАВЛЕНИЕ ЗАКАЗА ---
    ADMIN_AWAIT_ORDER_CODE,     # 17
    ADMIN_AWAIT_ORDER_STATUS,   # 18
    ADMIN_AWAIT_ORDER_DATE_YIWU, # 19
    ADMIN_AWAIT_ORDER_DATE_DUSH  # 20

) = range(21)

logger.info(f"✅ Загружено 21 состояний ConversationHandler")

# --- Функция для проверки конфигурации ---
def check_config():
    """Проверяет всю конфигурацию и возвращает результат."""
    issues = []

    if not BOT_TOKEN:
        issues.append("❌ TELEGRAM_TOKEN не установлен")

    if not DATABASE_URL:
        issues.append("❌ DATABASE_URL не установлен")

    missing_photos = []
    for region in ["Бохтар", "Кабодиён"]:
        for name, path in [
            (f"Контакты {region}", PHOTO_CONTACT_PATHS[region]),
            (f"Тарифы {region}", PHOTO_PRICE_PATHS[region]),
            (f"Адрес Таджикистан {region}", PHOTO_ADDRESS_TAJIK_PATHS[region]),
        ]:
            if not path.exists():
                missing_photos.append(f"❌ {name}: {path.name}")
    
    if not PHOTO_ADDRESS_CHINA_PATH.exists():
        missing_photos.append(f"❌ Адрес Китай: {PHOTO_ADDRESS_CHINA_PATH.name}")

    if missing_photos:
        issues.append("Отсутствуют файлы изображений:")
        issues.extend(missing_photos)

    xlsx_path = BASE_DIR / XLSX_FILENAME
    if not xlsx_path.exists():
        issues.append(f"⚠️ Excel файл не найден: {XLSX_FILENAME}")

    return issues

# --- Автопроверка при импорте ---
if __name__ != "__main__":
    config_issues = check_config()
    if config_issues:
        logger.warning("⚠️ Обнаружены проблемы в конфигурации:")
        for issue in config_issues:
            logger.warning(f"   {issue}")
    else:
        logger.info("✅ Конфигурация проверена - все критически важные параметры установлены")

# --- Информация о конфигурации ---
logger.info("=" * 50)
logger.info("🎯 КОНФИГУРАЦИЯ ЗАГРУЖЕНА")
logger.info(f"📁 Рабочая директория: {BASE_DIR}")
logger.info(f"🤖 Токен бота: {'✅ Установлен' if BOT_TOKEN else '❌ Отсутствует'}")
logger.info(f"🗄️  База данных: {'✅ PostgreSQL' if DATABASE_URL else '❌ Не настроена'}")
logger.info(f"👑 Админы: {len(ADMIN_USER_IDS)} пользователей")
logger.info(f"📊 Фоновые задачи: {sum(1 for job in JOBS.values() if job['enabled'])} активны")
logger.info("=" * 50)