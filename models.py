class User:
    def __init__(self, username, password, is_admin=False):
        self.username = username
        self.password = password
        self.is_admin = is_admin
        self.tickets = []

    def add_ticket(self, ticket):
        self.tickets.append(ticket)

    def remove_ticket(self, ticket_id):
        for ticket in self.tickets:
            if ticket.ticket_id == ticket_id:
                self.tickets.remove(ticket)
                return True
        return False


class Movie:
    def __init__(self, title, genre, duration, description, age_rating):
        self.title = title
        self.genre = genre
        self.duration = duration
        self.description = description
        self.age_rating = age_rating


class Ticket:
    def __init__(self, ticket_id, movie_title, time, row, seat, price, hall_name):
        self.ticket_id = ticket_id
        self.movie_title = movie_title
        self.time = time
        self.row = row
        self.seat = seat
        self.price = price
        self.hall_name = hall_name
        self.status = "Активний"


class Session:
    def __init__(self, session_id, movie, time, price, hall_name, rows=6, seats_per_row=8):
        self.session_id = session_id
        self.movie = movie
        self.time = time
        self.price = price
        self.hall_name = hall_name
        self.rows = rows
        self.seats_per_row = seats_per_row
        self.hall = [[False for _ in range(seats_per_row)] for _ in range(rows)]

    def show_hall_scheme(self):
        print(f"\n      === СХЕМА ЗАЛУ: {self.hall_name.upper()} ===")
        header = "      "
        for i in range(self.seats_per_row):
            header += f"[{i+1}] "
        print(header)
        print("   " + "-" * (self.seats_per_row * 5 + 5))

        for r_idx in range(self.rows):
            row_str = f"Ряд {r_idx+1} | "
            for seat in self.hall[r_idx]:
                if seat:
                    row_str += "[X]  "
                else:
                    row_str += "[0]  "
            print(row_str)
        print("\n* [0] - вільно, [X] - зайнято.")

    def book_place(self, row_num, seat_num):
        if row_num < 0 or row_num >= self.rows or seat_num < 0 or seat_num >= self.seats_per_row:
            print("[Помилка] Такого місця не існує!")
            return False
        if self.hall[row_num][seat_num]:
            print("[Помилка] Місце вже зайняте!")
            return False
        self.hall[row_num][seat_num] = True
        return True

    def release_place(self, row_num, seat_num):
        if 0 <= row_num < self.rows and 0 <= seat_num < self.seats_per_row:
            self.hall[row_num][seat_num] = False
            return True
        return False


class PromoCode:
    def __init__(self, code, discount_percent):
        self.code = code
        self.discount_percent = discount_percent