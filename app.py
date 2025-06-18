from flask import Flask, render_template, request, redirect, url_for, session
import caldav
from caldav.elements import dav
from icalendar import Todo
from datetime import datetime
import uuid
import vobject
import os
import config

app = Flask(__name__)
app.secret_key = os.urandom(24)

CALDAV_URL = config.CALDAV_URL
CALDAV_USERNAME = config.CALDAV_USERNAME
CALDAV_PASSWORD = config.CALDAV_PASSWORD

LOGIN = config.LOGIN
PASSWORD = config.PASSWORD

def get_client():
    return caldav.DAVClient(url=CALDAV_URL, username=CALDAV_USERNAME, password=CALDAV_PASSWORD)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == LOGIN and request.form['password'] == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="Неверный логин или пароль")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/index')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    try:
        client = get_client()
        principal = client.principal()
        calendars = principal.calendars()

        calendar_list = []
        for cal in calendars:
            props = cal.get_properties([dav.DisplayName()])
            displayname = props.get('{DAV:}displayname')

            if displayname is not None:
                displayname = str(displayname)
            else:
                displayname = 'Без названия'

            # Считаем количество задач в календаре
            tasks = cal.todos()
            task_count = len(tasks)

            # Здесь можно потом добавить уникальный emoji для каждого календаря
            calendar_list.append({
                'name': displayname,
                'url': cal.url,
                'emoji': '🗒️',  # Пока заглушка, можно потом хранить в БД
                'task_count': task_count
            })

        return render_template('index.html', calendars=calendar_list)
    except Exception as e:
        return f"Ошибка подключения: {e}"

@app.route('/edit_task', methods=['GET', 'POST'])


def edit_task():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    task_url = request.args.get('task_url')
    calendar_url = request.args.get('calendar_url')

    if not task_url or not calendar_url:
        return "Ошибка: отсутствуют обязательные параметры"

    client = get_client()
    calendar = client.calendar(url=calendar_url)

    # Попытка найти задачу в календаре по URL
    task = None
    try:
        todos = calendar.todos()
        for t in todos:
            if t.url == task_url:
                task = t
                break
    except Exception as e:
        return f"Ошибка получения задач календаря: {e}"

    if task is None:
        return "Задача не найдена"

    task_data = getattr(task, 'data', None)
    if task_data is None:
        # Пробуем получить через get_data()
        try:
            task_data = task.get_data()
        except Exception as e:
            return f"Ошибка получения данных задачи: {e}"

    if not task_data:
        return "Ошибка: задача не содержит данных или недоступна"

    # Парсим ICS
    import vobject
    try:
        component = vobject.readOne(task_data)
    except Exception as e:
        return f"Ошибка парсинга ICS: {e}"

    # Ищем VTODO
    vtodo = None
    if component.name == "VTODO":
        vtodo = component
    else:
        for comp in component.components():
            if comp.name == "VTODO":
                vtodo = comp
                break

    if vtodo is None:
        return "Ошибка: задача не найдена или имеет неверный формат"

    if request.method == 'POST':
        new_summary = request.form.get('summary', '').strip()
        if not new_summary:
            return "Ошибка: поле summary не может быть пустым"

        vtodo.summary.value = new_summary

        # Сохраняем
        try:
            task.data = component.serialize()
            task.save()
        except Exception as e:
            return f"Ошибка сохранения задачи: {e}"

        return redirect(url_for('view_calendar', calendar_url=calendar_url))

    summary = getattr(vtodo.summary, 'value', '')

    return render_template('edit_task.html', summary=summary, task_url=task_url, calendar_url=calendar_url)










@app.route('/calendar')
def view_calendar():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    calendar_url = request.args.get('calendar_url')
    try:
        client = get_client()
        calendar = caldav.Calendar(client, url=calendar_url)

        # Получаем имя календаря
        props = calendar.get_properties([dav.DisplayName()])
        displayname = props.get('{DAV:}displayname')
        if displayname is not None:
            calendar_name = str(displayname)
        else:
            calendar_name = 'Без названия'

        tasks = calendar.todos()

        parsed_tasks = []
        for task in tasks:
            component = task.vobject_instance
            summary = component.vtodo.summary.value
            uid = component.vtodo.uid.value
            parsed_tasks.append({'summary': summary, 'uid': uid, 'href': task.url})

        return render_template('calendar.html', tasks=parsed_tasks, calendar_url=calendar_url, calendar_name=calendar_name)
    except Exception as e:
        return f"Ошибка: {e}"


@app.route('/add_task', methods=['GET', 'POST'])
def add_task():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    calendar_url = request.args.get('calendar_url')
    if request.method == 'POST':
        summary = request.form['summary']

        client = get_client()
        calendar = caldav.Calendar(client, url=calendar_url)

        todo = Todo()
        todo.add('uid', str(uuid.uuid4()))
        todo.add('summary', summary)
        todo.add('dtstamp', datetime.now())

        calendar.add_todo(todo.to_ical().decode('utf-8'))
        return redirect(url_for('view_calendar', calendar_url=calendar_url))

    return render_template('add_task.html', calendar_url=calendar_url)

@app.route('/delete_task', methods=['GET', 'POST'])
def delete_task():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        task_url = request.form.get('task_url') or request.args.get('task_url')
        calendar_url = request.form.get('calendar_url') or request.args.get('calendar_url')

        try:
            client = get_client()
            task = caldav.Todo(client, url=task_url)
            task.delete()
            return redirect(url_for('view_calendar', calendar_url=calendar_url))
        except Exception as e:
            return f"Ошибка при удалении: {e}"
    else:
        # Например, если GET, можно просто показать ошибку или редирект
        return redirect(url_for('view_calendar', calendar_url=request.args.get('calendar_url')))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5030, debug=True)
