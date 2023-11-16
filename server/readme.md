## Серверная часть 

### [en](./readmeeng.md)
### Примерный алгоритм работы 
#### 1) В *app.py* принять запрос с клиента, содержащий код, язык и название дерева и перенаправить в handler нужного модуля
#### 2) Получить вызов от *app.py* в методе *handler*. Вызов содержит код программы и название дерева
#### 3) Отправить код анализатору через handler (это не обязательно python программа, возможно использование *docker*)
#### 4) Вернуть клиенту представление графа в формате *dot*

## Код тестировался для python3.10
### Данные хранятся в базе данных
```bash
docker run --name pg_modelviewer -p 5432:5432 -e POSTGRES_PASSWORD=1234 -e POSTGRES_USER=USER -e POSTGRES_DB=modelviewer postgres
```
### Для работы авторизации VK [нужно создать приложение](https://vk.com/apps?act=manage) и установить адреса в настройках. Еще нужно передать ключи в качестве переменных среды
```bash
export client_id=<number>
export client_secret=<string>
export db_conn=postgresql+psycopg2://USER:1234@localhost:5432/modelviewer
```
## GUI запуск сервера в pycharm и т.п.
* Установка всех зависимостей (либо через pip install, либо через GUI среды и тд)
* Запуск метода main в /server/app.py
## Запуск сервера через pipenv
```bash
pip install pipenv
pipenv shell
pipenv install
python ./app.py
```
## Запуск через virtualenv
```bash
pip install virtualenv
virtualenv venv # создание среды
./venv/Scripts/activate.bat # windows
source venv/bin/activate # mac, linux
pip install -r requirements.txt 
python ./app.py
```
### По адресу `http://localhost:8000/docs` можно получить доcтуп к интерактивному api сервера.
### По адресу `http://localhost:8000/` основная страница *index.html*.
