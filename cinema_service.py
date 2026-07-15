from models import User, Movie, Ticket, Session, PromoCode

class CinemaService:
    def __init__(self):
        self.users = {
            "admin": User("admin", "admin111", is_admin=True),
            "student": User("student", "stud2026"),
            "guest": User("guest", "guest999")
        }
        
        self.movies = [
            Movie("Дюна: Частина друга", "Фантастика", 166, "Історія Пола Атріда на пустельній планеті Арракіс.", "16+"),
            Movie("Бетмен", "Детектив", 176, "Темний лицар Готема розслідує серію жорстоких злочинів.", "16+"),
            Movie("Льодовиковий період", "Мультфільм", 81, "Пригоди доісторичних друзів під час глобального похолодання.", "0+")
        ]
        
        self.sessions = [
            Session(101, self.movies[0], "12:00", 150.0, "Синій зал", 5, 6),
            Session(102, self.movies[0], "18:30", 200.0, "Синій зал", 5, 6),
            Session(201, self.movies[1], "15:00", 160.0, "Червоний зал", 6, 8),
            Session(202, self.movies[1], "21:00", 190.0, "Червоний зал", 6, 8),
            Session(301, self.movies[2], "10:30", 110.0, "Дитячий зал", 4, 6)
        ]
        
        self.promocodes = {
            "STUDENT20": PromoCode("STUDENT20", 20),
            "CINEMA10": PromoCode("CINEMA10", 10),
            "FREE50": PromoCode("FREE50", 50)
        }
        
        self.current_user = None
        self.ticket_counter = 1000

    def register(self, username, password):
        if not username or not password:
            print("[Помилка] Дані не можуть бути порожніми!")
            return False
        if username in self.users:
            print("[Помилка] Цей логін вже зайнятий!")
            return False
        self.users[username] = User(username, password)
        print(f"[Успіх] Користувача {username} успішно створено!")
        return True

    def login(self, username, password):
        if username in self.users and self.users[username].password == password:
            self.current_user = self.users[username]
            print(f"[Успіх] Авторизація успішна. Вітаємо, {username}!")
            return True
        print("[Помилка] Неправильний логін або пароль!")
        return False

    def logout(self):
        if self.current_user:
            print(f"[Успіх] Користувач {self.current_user.username} вийшов.")
            self.current_user = None

    def search_movies(self, text):
        results = []
        search_text = text.lower()
        for movie in self.movies:
            if search_text in movie.title.lower() or search_text in movie.genre.lower():
                results.append(movie)
        return results

    def validate_promo(self, code_str):
        if code_str in self.promocodes:
            return self.promocodes[code_str].discount_percent
        return 0

    def generate_ticket_id(self):
        self.ticket_counter += 1
        return self.ticket_counter

    def refund_ticket(self, ticket_id):
        if not self.current_user:
            return False
        
        target_ticket = None
        for ticket in self.current_user.tickets:
            if ticket.ticket_id == ticket_id:
                target_ticket = ticket
                break
                
        if not target_ticket:
            print("[Помилка] Квиток із таким ID не знайдено у вашому профілі!")
            return False

        for session in self.sessions:
            if session.movie.title == target_ticket.movie_title and session.time == target_ticket.time:
                session.release_place(target_ticket.row - 1, target_ticket.seat - 1)
                self.current_user.remove_ticket(ticket_id)
                print(f"[Успіх] Квиток №{ticket_id} скасовано. Гроші повернуто на картку.")
                return True
                
        print("[Помилка] Не вдалося знайти відповідний сеанс для скасування.")
        return False

    def admin_add_movie(self, title, genre, duration, description, age_rating):
        for movie in self.movies:
            if movie.title.lower() == title.lower():
                print("[Помилка] Цей фільм вже є в базі!")
                return False
        new_movie = Movie(title, genre, duration, description, age_rating)
        self.movies.append(new_movie)
        print(f"[Адмін] Фільм '{title}' додано.")
        return True

    def admin_add_session(self, movie_idx, time, price, hall_name, rows, seats):
        if movie_idx < 0 or movie_idx >= len(self.movies):
            print("[Помилка] Невірний вибір фільму!")
            return False
        new_id = self.sessions[-1].session_id + 1 if self.sessions else 101
        new_session = Session(new_id, self.movies[movie_idx], time, price, hall_name, rows, seats)
        self.sessions.append(new_session)
        print(f"[Адмін] Сеанс ID {new_id} створено.")
        return True

    def admin_delete_session(self, session_id):
        for session in self.sessions:
            if session.session_id == session_id:
                self.sessions.remove(session)
                print(f"[Адмін] Сеанс {session_id} видалено.")
                return True
        print("[Помилка] Сеанс не знайдено.")
        return False