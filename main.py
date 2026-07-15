from cinema_service import CinemaService
from menu import MenuController

def main():
    service = CinemaService()
    controller = MenuController(service)
    try:
        controller.run()
    except KeyboardInterrupt:
        print("\nПрограму завершено користувачем.")

if __name__ == "__main__":
    main()