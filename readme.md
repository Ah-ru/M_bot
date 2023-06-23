# M_bot

**Подсказка:** Документация на русском ниже 

## English

### Description:
This bot can: save, read, send to a group/channel and delete messages, as well as ban users

### Instructions for deployment
1. Clone branch master.bot  from the M_bot repository:

  ```
    git clone https://github.com/Ah-ru/M_bot --branch master.bot
  ```

  2. Go to M_bot directory:

  ```
    cd M_bot
  ```

  3. Install libraries:

  ```
    pip install -r requirements.txt
  ```

  If was error, try:

  ```
    pip3 install -r requirements.txt
  ```

  4. Create an .env file according to the sample:
    
  TGAPI = "Your Telegram_api_token" \
  GID = "Group_ID_(integer)"
  NDB = "your_path_to_database"    


  **Hint:** To get the path to the working directory in linux:

  ```
    pwd
  ```
  You geted path to the working directory M_bot\
  Example : /home/test/M_bot\
  Create a name for your database (.db)  *For example: database.db\
  Example : /home/test/M_bot/database.db - This path to database

  5. Now, start 'main.py':

  ```
    python main.py
  ```

  If was error, try:

  ```
    python3 main.py
  ```
  *For stop CTRL+C*

## Русский

### Описание 
Бот позволяет записывать, читать, отправлять в группу/канал, и удалять сообщения полученные от пользователей, а так - же банить пользователей


### Инструкция по развертыванию
  1. Клонируйте ветку master.bot из репозитория M_bot:

  ```
    git clone https://github.com/Ah-ru/M_bot --branch master.bot
  ```

  2. Перейдите в директорию M_bot:

  ```
    cd M_bot
  ```

  3. Установите библиотеки:

  ```
    pip install -r requirements.txt
  ```

  Если у вас не получилось, попробуйте:

  ```
    pip3 install -r requirements.txt
  ```

  4. Создайте .env файл по шаблону:
    
  TGAPI = "Your Telegram_api_token" Ваш Api token telegram bot/ апи токен телеграм бота.\
  GID = "Group_ID_(integer)"        Ваш id группы / id - ай-ди.\
  NDB = "your_path_to_database"     Ваш путь к базе данных.


  **Подсказка:** Для получения пути до рабочей директорию Linux:

  ```
    pwd
  ```
  Вы получите путь по директории M_bot\
  Например : /home/test/M_bot\
  После этого добавьте в конец любой текст на английском с расширение .db\
  Например : /home/test/M_bot/tg.db - это и будет путь до базы данных

  5. После всех описанных выше шагов, запустите файл 'main.py':

  ```
    python main.py
  ```

  Если у вас не получилось, попробуйте:

  ```
    python3 main.py
  ```
  *Для остановки CTRL+C*