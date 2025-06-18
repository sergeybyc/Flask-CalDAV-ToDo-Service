# Flask CalDAV ToDo Service
___

Простой веб-сервис для работы с задачами (ToDo) через CalDAV-календарь на базе Flask. Проверена синхронизация с CalDAV-сервером Radicale и приложением Apple Напоминания на iOS.

A simple web service for managing tasks (ToDo) via a CalDAV calendar built with Flask. Synchronization tested with the Radicale CalDAV server and Apple Reminders on iOS.

<img width="1280" alt="image" src="https://github.com/user-attachments/assets/7b767ab4-de27-4e22-b5a9-b180a3eb46f6" />
<img width="1280" alt="image" src="https://github.com/user-attachments/assets/a786ef4f-4b21-4230-93d0-432687b4dcc3" />
<img width="1280" alt="image" src="https://github.com/user-attachments/assets/b44374f9-67fd-491a-a309-00d55732941e" />



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
