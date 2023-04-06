# test_google
# Тестовое задание группы компаний Каналсервис

### Что необходимо на локальной машине:
1. установленный python 3.8 и выше.
2. установленный postgres.

### Подготовительный этап
1. Клонировать репозиторий командой ```git clone https://github.com/Aleksey-Surnov/test_google.git```.
2. Создать сервисный аккаунт Google Cloud Platform. Инструкция создания [здесь](https://support.google.com/a/answer/7378726?hl=ru).
3. Получить доступ к Google API, для этого ознакомьтесь со [статьей](https://habr.com/ru/articles/575160/).
4. Cкачать файл <имя файла>.json сервисного аккаунта и поместить его в папку проекта **test_google**.
5. Назвать файл <имя файла>.json сервисного аккаунта: *gs_my_credentials.json.*
6. Сгенерировать API key в Google Cloud Platform.
7. Создать (перенести) таблицу в googlesheets.
8. Дать название листу в таблице с данными googlesheets **data_list**. 

![изображение](https://user-images.githubusercontent.com/55957778/230509788-3891ccab-d530-4de6-9d52-f730b0910712.png)

9. Предоставить доступ в таблице googlesheets сервисному аккаунту c правами редактора. 
10. В папке проекта **test_google** создать файл *.env* заполнив его следующим образом:  

![изображение](https://user-images.githubusercontent.com/55957778/230509062-e4322b89-ccb8-4ffc-b77f-2deac9bf6d93.png)


Например: POSTGRES_HOST=localhost. \
SPREADSHEET_ID берем из адресной строки в googlesheets.

### Установка зависимостей и запуск скрипта
1. Войти в папку ```cd test_google```.
2. Создать вирутальное окружение ```python3 -m venv venv```.
3. Активировать виртуальное окружение ```source ./venv/bin/activate```.
4. Установить зависимости и пакеты ```pip install -r requirements.txt```.
5. Запустить скрипт ```flask run --host=0.0.0.0```

### Просмотр результатов
-Для просмотра результата работы откройте браузер и введите адрес http://127.0.0.1:5000/

Браузер:
![изображение](https://user-images.githubusercontent.com/55957778/230505491-208f4b87-7f76-4149-9c40-9f73eef730d7.png)

Таблица:
![изображение](https://user-images.githubusercontent.com/55957778/230505750-4571b796-f4f1-483b-9fdd-c3730f2d4afa.png)


-Изменим в таблице на строке _№10_ значение номера заказа на _1111111_

Браузер:
![изображение](https://user-images.githubusercontent.com/55957778/230506278-1cb65d63-6176-4786-85b6-6f17d6a83417.png)

Таблица:
![изображение](https://user-images.githubusercontent.com/55957778/230506122-77ea21f5-3627-49d0-84b1-143fdc5f9b10.png)


-Изменим в таблице на строке №1 значение номера заказа на _1111777_ и стоимость$ на _300_

Браузер:
![изображение](https://user-images.githubusercontent.com/55957778/230507030-dd38fb75-2047-40c9-962b-c88ffbbfbded.png)

Таблица:
![изображение](https://user-images.githubusercontent.com/55957778/230507085-d0f73d9a-e218-4cf3-93c9-8242bdc7c679.png)




Для остановки работы программы используйте команду ```kill -9 $(lsof -t -i:"5000")```

