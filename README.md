# Flask CalDAV ToDo Service

Простой веб-сервис для работы с задачами (ToDo) в CalDAV календаре через Flask.
Протестирована синхронизация с CalDAV Radicale с подключенным к нему Apple Напоминания iOS
---
<img width="1280" alt="image" src="https://github.com/user-attachments/assets/62c289ea-e61c-4aac-976c-950b15a8413f" />
<img width="1280" alt="image" src="https://github.com/user-attachments/assets/bda6f09a-3d45-483e-8a90-b400dee63bbb" />
<img width="1280" alt="image" src="https://github.com/user-attachments/assets/5feddac8-ff7b-490b-9e15-8882cd63aeaf" />


## Требования

- Python 3.9+
- CalDAV сервер с поддержкой задач (например, Radicale)
- Пакеты Python из `requirements.txt`

---

## Установка

1. Клонируйте репозиторий или скачайте файлы.

2. Создайте и активируйте виртуальное окружение (рекомендуется):

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```
3. Установите зависимости:
```bash
pip install -r requirements.txt
```
4. Настройте параметры подключения к CalDAV серверу и для входа в приложение в файле config.py:
```
# CalDAV-сервер
CALDAV_URL = 'https://your-caldav-server-url/'
CALDAV_USERNAME = 'your-caldav-username'
CALDAV_PASSWORD = 'your-caldav-password'
# App
LOGIN = 'admin' # Придумайте логин
PASSWORD = 'admin' # Придумайте пароль
```

5. Запустите приложение:
```bash
python app.py
```

# Использование
Откройте браузер и перейдите по адресу: http://localhost:5030
Войдите под пользователем из config.py
Выберите календарь из списка
Просматривайте задачи, добавляйте, редактируйте и отмечайте как выполненные

# Маршруты:
```
/ — страница входа
/logout — выход
/index — список календарей
/calendar?calendar_url=... — просмотр задач выбранного календаря
/add_task?calendar_url=... — добавление задачи
/edit_task?task_url=...&calendar_url=... — редактирование задачи
/delete_task — удаление задачи (через POST)
```
