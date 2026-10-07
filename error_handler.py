"""
Централизованный модуль безопасной обработки системных исключений и валидации.
Разработан в рамках дисциплины УП.02 для группы 3ИП-1-24.
"""
from tkinter import messagebox


def safe_call(func, *args, **kwargs):
    """
    Безопасный вызов опасных функций (запросы к БД, файловые операции)
    с автоматическим перехватом критических ошибок и выводом диалоговых окон.
    
    :param func: Функция для выполнения
    :param args: Позиционные аргументы для функции
    :param kwargs: Именованные аргументы для функции
    :return: Результат функции или None при ошибке
    """
    try:
        return func(*args, **kwargs)
    except FileNotFoundError as e:
        messagebox.showerror("Ошибка файла", f"Критический файл ресурса не найден:\n{e}")
    except ConnectionError as e:
        messagebox.showerror("Ошибка базы данных", f"Сбой подключения к СУБД SQLite:\n{e}")
    except ValueError as e:
        messagebox.showwarning("Предупреждение данных", f"Обнаружен неверный формат параметров:\n{e}")
    except Exception as e:
        messagebox.showerror("Критический сбой приложения", f"Непредвиденное системное исключение:\n{e}")
    return None


def validate_positive_int(value, field_name="Значение"):
    """
    Проверяет, что введенное пользователем значение является 
    положительным целым числом.
    
    :param value: Строка, полученная из поля ввода (Entry)
    :param field_name: Название проверяемого поля для вывода в сообщении
    :return: Кортеж (True, число) при успехе или (False, сообщение об ошибке)
    """
    try:
        number = int(value)
        if number <= 0:
            return (False, f"Поле '{field_name}' должно быть больше нуля")
        return (True, number)
    except ValueError:
        return (False, f"Поле '{field_name}' должно быть целым числом")
