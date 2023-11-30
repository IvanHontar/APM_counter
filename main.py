import psycopg2
from pynput import mouse, keyboard
import threading
import time
from env import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD

class Counter:
    def __init__(self, db_host, db_name, db_user, db_password):
        self.action_count = 0
        self.is_running = True
        self.key_listener = None
        self.mouse_listener = None
        self.db_host = db_host
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password

    def on_action(self, key):
        self.action_count += 1

    def on_click(self, x, y, button, pressed):
        if pressed:
            self.action_count += 1

    def stop_listening(self, key):
        if key == keyboard.Key.esc:
            self.is_running = False
            return False
        return True

    def count_apm(self, username):
        print(f"Подсчет начался для пользователя {username}. Для остановки нажмите клавишу 'Esc'.")

       
        connection = psycopg2.connect(
            host=self.db_host,
            database=self.db_name,
            user=self.db_user,
            password=self.db_password
        )

        try:
            with connection.cursor() as cursor:
                cursor.execute('''CREATE TABLE IF NOT EXISTS results
                                (id SERIAL PRIMARY KEY, username TEXT, apm REAL)''')

            start_time = time.time()

            self.key_listener = keyboard.Listener(on_press=self.on_action)
            self.mouse_listener = mouse.Listener(on_click=self.on_click)

            self.key_listener.start()
            self.mouse_listener.start()

            while self.is_running:
                time.sleep(0.1)

            self.key_listener.stop()
            self.mouse_listener.stop()

            end_time = time.time()

            total_actions = self.action_count
            duration_seconds = end_time - start_time
            apm = total_actions / (duration_seconds / 60) if duration_seconds > 0 else 0

            print(f"\nAPM (действий в минуту): {apm:.2f}")

            
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO results (username, apm) VALUES (%s, %s)", (username, apm))

            
            connection.commit()
            connection.close()
        finally:
            connection.close()

        
        if apm < 100:
            print("Ну ты и уебище!")
            input('Новичок ')
        elif 100 <= apm < 150:
            print('Терпимо сынок терпимо')
            input(' ей лох! 5 евро на карту мне закинь')
        elif apm >= 150 and apm < 200:
            print('Неплохо, неплохо!')
            input('страж 4')
        elif apm >= 200:
            print('ХУя ты кабан')
            input('Поздравляю вы достигли ранга Властелин 5!!!')


        

    def run(self):
        username = input("Введите свое имя: ")
        input("Нажмите Enter для начала подсчета.")
        stop_listener = keyboard.Listener(on_press=self.stop_listening)
        stop_listener.start()

        self.thread = threading.Thread(target=self.count_apm, args=(username,))
        self.thread.start()

        while self.thread.is_alive():
            time.sleep(0.1)

        stop_listener.stop()

if __name__ == "__main__":
    try:
        db_host = DB_HOST
        db_name = DB_NAME
        db_user = DB_USER
        db_password = DB_PASSWORD

        counter = Counter(db_host, db_name, db_user, db_password)
        counter.run()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Произошла ошибка: {e}")
