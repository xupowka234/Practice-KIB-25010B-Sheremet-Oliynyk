import time

class MenuController:
    def __init__(self, service):
        self.service = service

    def run(self):
        while True:
            if self.service.current_user is None:
                self.show_auth_menu()
            else:
                if self.service.current_user.is_admin:
                    self.show_admin_menu()
                else:
                    self.show_user_menu()

    def show_auth_menu(self):
        print("\n==================================")
        print("     КІНОТЕАТР: СИСТЕМА КВИТКІВ   ")
        print("==================================")
        print("1. Вхід в систему")
        print("2. Реєстрація")
        print("3. Перегляд фільмів без входу")
        print("0. Вихід з програми")
        print("----------------------------------")
        
        choice = input("Ваш вибір: ").strip()
        
        if choice == "1":
            username = input("Логін: ").strip()
            password = input("Пароль: ").strip()
            self.service.login(username, password)
        elif choice == "2":
            username = input("Новий логін: ").strip()
            password = input("Новий пароль: ").strip()
            self.service.register(username, password)
        elif choice == "3":
            query = input("Введіть назву фільму або жанр: ")
            results = self.service.search_movies(query)
            if not results:
                print("Нічого не знайдено.")
            else:
                for m in results:
                    print(f"-> {m.title} [{m.age_rating}] | Жанр: {m.genre} | {m.duration} хв.")
        elif choice == "0":
            print("Програма завершена.")
            exit()
        else:
            print("Невірна команда.")

    def show_user_menu(self):
        user = self.service.current_user
        print(f"\n==================================")
        print(f"   МЕНЮ КОРИСТУВАЧА: {user.username}")
        print("==================================")
        print("1. Афіша фільмів")
        print("2. Розклад усіх сеансів")
        print("3. Купити квиток")
        print("4. Мої квитки (Перегляд та повернення)")
        print("5. Пошук фільму")
        print("0. Вийти з акаунту")
        print("----------------------------------")
        
        choice = input("Ваш вибір: ").strip()
        
        if choice == "1":
            print("\n--- АФІША ---")
            for idx, m in enumerate(self.service.movies):
                print(f"{idx + 1}. '{m.title}' [{m.age_rating}]")
                print(f"   Жанр: {m.genre} | Тривалість: {m.duration} хв.")
                print(f"   Опис: {m.description}\n")
        elif choice == "2":
            print("\n--- РОЗКЛАД СЕАНСІВ ---")
            for s in self.service.sessions:
                print(f"ID: {s.session_id} | Фільм: '{s.movie.title}' [{s.movie.age_rating}]")
                print(f"Зал: {s.hall_name} | Час: {s.time} | Ціна: {s.price} грн.")
                print("-" * 40)
        elif choice == "3":
            print("\n--- ОФОРМЛЕННЯ КВИТКА ---")
            try:
                s_id = int(input("Введіть ID сеансу: "))
            except ValueError:
                print("[Помилка] Невірний формат ID.")
                return
                
            selected_session = None
            for s in self.service.sessions:
                if s.session_id == s_id:
                    selected_session = s
                    break
            
            if not selected_session:
                print("[Помилка] Сеанс не знайдено.")
                return
                
            selected_session.show_hall_scheme()
            
            try:
                row = int(input("Ряд: ")) - 1
                seat = int(input("Місце: ")) - 1
            except ValueError:
                print("[Помилка] Вводьте тільки числа.")
                return
                
            if selected_session.book_place(row, seat):
                final_price = selected_session.price
                print(f"Базова вартість: {final_price} грн.")
                
                promo_reply = input("Маєте промокод? (y/n): ").strip().lower()
                if promo_reply == "y":
                    code_str = input("Введіть промокод: ").strip()
                    discount = self.service.validate_promo(code_str)
                    if discount > 0:
                        final_price = final_price * (100 - discount) / 100
                        print(f"[Успіх] Промокод застосовано! Знижка {discount}%. Нова ціна: {final_price} грн.")
                    else:
                        print("[Помилка] Недійсний промокод.")
                
                print(f"Сума до сплати: {final_price} грн.")
                card = input("Введіть 16 цифр картки: ").strip()
                if len(card) == 16 and card.isdigit():
                    print("Обробка платежу...")
                    time.sleep(1)
                    
                    from models import Ticket
                    t_id = self.service.generate_ticket_id()
                    new_ticket = Ticket(t_id, selected_session.movie.title, selected_session.time, row + 1, seat + 1, final_price, selected_session.hall_name)
                    user.add_ticket(new_ticket)
                    print(f"[Успіх] Квиток №{t_id} успішно куплено!")
                else:
                    print("[Помилка] Невірні дані картки. Бронювання скасовано.")
                    selected_session.hall[row][seat] = False
        elif choice == "4":
            print("\n--- ВАШІ КВИТКИ ---")
            if not user.tickets:
                print("У вас немає придбаних квитків.")
                return
            for t in user.tickets:
                print(f"Квиток №{t.ticket_id} | Фільм: '{t.movie_title}'")
                print(f"Зал: {t.hall_name} | Час: {t.time} | Ряд: {t.row} | Місце: {t.seat}")
                print(f"Ціна: {t.price} грн. | Статус: {t.status}")
                print("-" * 40)
                
            refund_reply = input("Бажаєте повернути квиток? (y/n): ").strip().lower()
            if refund_reply == "y":
                try:
                    t_id_ref = int(input("Введіть номер квитка для повернення: "))
                    self.service.refund_ticket(t_id_ref)
                except ValueError:
                    print("[Помилка] Невірний формат номера.")
        elif choice == "5":
            query = input("Введіть назву чи жанр: ")
            results = self.service.search_movies(query)
            for m in results:
                print(f"-> {m.title} ({m.genre})")
        elif choice == "0":
            self.service.logout()

    def show_admin_menu(self):
        print(f"\n==================================")
        print("       АДМІНІСТРАТИВНА ПАНЕЛЬ     ")
        print("==================================")
        print("1. Додати новий фільм")
        print("2. Створити сеанс")
        print("3. Видалити сеанс")
        print("4. Фінансовий звіт кінотеатру")
        print("0. Вийти з акаонуту")
        print("----------------------------------")
        
        choice = input("Дія адміна: ").strip()
        
        if choice == "1":
            title = input("Назва фільму: ").strip()
            genre = input("Жанр: ").strip()
            try:
                duration = int(input("Тривалість (хв): "))
            except ValueError:
                print("[Помилка] Має бути числом.")
                return
            description = input("Опис: ").strip()
            age = input("Віковий ценз (напр. 12+, 16+): ").strip()
            self.service.admin_add_movie(title, genre, duration, description, age)
        elif choice == "2":
            print("Список фільмів:")
            for idx, m in enumerate(self.service.movies):
                print(f"[{idx}] - {m.title}")
            try:
                m_idx = int(input("Індекс фільму: "))
                time_str = input("Час (напр. 18:00): ").strip()
                price = float(input("Ціна: "))
                hall = input("Назва залу: ").strip()
                rows = int(input("Рядів у залі: "))
                seats = int(input("Місць у ряду: "))
                self.service.admin_add_session(m_idx, time_str, price, hall, rows, seats)
            except ValueError:
                print("[Помилка] Невірний формат числових даних.")
        elif choice == "3":
            try:
                s_id = int(input("Введіть ID сеансу для видалення: "))
                self.service.admin_delete_session(s_id)
            except ValueError:
                print("[Помилка] Має бути числом.")
        elif choice == "4":
            total_money = 0
            total_tickets = 0
            for u in self.service.users.values():
                for t in u.tickets:
                    total_money += t.price
                    total_tickets += 1
            print(f"\n--- ЗВІТ ПРО ПУБЛІЧНУ АКТИВНІСТЬ ---")
            print(f"Зареєстровано користувачів: {len(self.service.users)}")
            print(f"Усього продано квитків: {total_tickets}")
            print(f"Загальний виторг: {total_money} грн.")
        elif choice == "0":
            self.service.logout()