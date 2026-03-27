import requests
import json
import os


class CurrencyMonitor:
    def __init__(self, save_file="save.json"):
        self.url = "https://www.cbr-xml-daily.ru/daily_json.js"
        self.save_file = save_file
        self.rates = {}
        self.groups = {}
        self.load_groups()

    def fetch_rates(self):
        try:
            response = requests.get(self.url, timeout=10)
            data = response.json()
            self.rates = data['Valute']
            return True
        except Exception as e:
            print(f"Ошибка получения курсов: {e}")
            return False

    def show_all_currencies(self):
        if not self.fetch_rates():
            return

        print("\n" + "=" * 70)
        print("КУРСЫ ВАЛЮТ")
        print("=" * 70)

        for code, info in self.rates.items():
            print(f"{code:5} | {info['Name']:30} | {info['Value']:10.2f} руб.")
        print("=" * 70)

    def show_currency_by_code(self, code):
        if not self.fetch_rates():
            return

        code = code.upper()
        if code in self.rates:
            info = self.rates[code]
            print(f"\n{code} - {info['Name']}")
            print(f"Курс: {info['Value']:.2f} руб.")
            print(f"Номинал: {info['Nominal']}")
        else:
            print(f"\nВалюта с кодом '{code}' не найдена")

    def create_group(self, group_name):
        if group_name in self.groups:
            print(f"Группа '{group_name}' уже существует")
            return

        self.groups[group_name] = []
        self.save_groups()
        print(f"Группа '{group_name}' создана")

    def add_to_group(self, group_name, currency_code):
        if group_name not in self.groups:
            print(f"Группа '{group_name}' не найдена")
            return

        currency_code = currency_code.upper()
        if currency_code not in self.rates:
            print(f"Валюта '{currency_code}' не найдена в курсах")
            return

        if currency_code in self.groups[group_name]:
            print(f"Валюта '{currency_code}' уже в группе")
            return

        self.groups[group_name].append(currency_code)
        self.save_groups()
        print(f"Валюта '{currency_code}' добавлена в группу '{group_name}'")

    def remove_from_group(self, group_name, currency_code):
        if group_name not in self.groups:
            print(f"Группа '{group_name}' не найдена")
            return

        currency_code = currency_code.upper()
        if currency_code not in self.groups[group_name]:
            print(f"Валюта '{currency_code}' не найдена в группе")
            return

        self.groups[group_name].remove(currency_code)
        self.save_groups()
        print(f"Валюта '{currency_code}' удалена из группы '{group_name}'")

    def show_groups(self):
        if not self.groups:
            print("\nНет созданных групп")
            return

        print("\n" + "=" * 50)
        print("ГРУППЫ ВАЛЮТ")
        print("=" * 50)

        for group_name, currencies in self.groups.items():
            print(f"\n{group_name}:")
            if currencies:
                for code in currencies:
                    if code in self.rates:
                        info = self.rates[code]
                        print(f"  {code} - {info['Name']}: {info['Value']:.2f} руб.")
                    else:
                        print(f"  {code} - данные недоступны")
            else:
                print("  (пусто)")
        print("=" * 50)

    def show_group_rates(self, group_name):
        if group_name not in self.groups:
            print(f"Группа '{group_name}' не найдена")
            return

        if not self.fetch_rates():
            return

        currencies = self.groups[group_name]
        if not currencies:
            print(f"Группа '{group_name}' пуста")
            return

        print(f"\nГРУППА: {group_name}")
        print("=" * 50)
        for code in currencies:
            if code in self.rates:
                info = self.rates[code]
                print(f"{code:5} | {info['Name']:30} | {info['Value']:10.2f} руб.")
        print("=" * 50)

    def save_groups(self):
        try:
            with open(self.save_file, 'w', encoding='utf-8') as f:
                json.dump(self.groups, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Ошибка сохранения: {e}")

    def load_groups(self):
        if os.path.exists(self.save_file):
            try:
                with open(self.save_file, 'r', encoding='utf-8') as f:
                    self.groups = json.load(f)
            except Exception as e:
                print(f"Ошибка загрузки: {e}")
                self.groups = {}


def main():
    monitor = CurrencyMonitor()

    while True:
        print("\n" + "=" * 50)
        print("МОНИТОРИНГ КУРСА ВАЛЮТ")
        print("=" * 50)
        print("1. Все валюты")
        print("2. Найти валюту по коду")
        print("3. Создать группу")
        print("4. Добавить валюту в группу")
        print("5. Удалить валюту из группы")
        print("6. Показать все группы")
        print("7. Показать курсы группы")
        print("8. Выход")
        print("=" * 50)

        choice = input("Выберите действие (1-8): ")

        if choice == '1':
            monitor.show_all_currencies()

        elif choice == '2':
            code = input("Введите код валюты (например, USD, EUR): ")
            monitor.show_currency_by_code(code)

        elif choice == '3':
            name = input("Введите название группы: ")
            monitor.create_group(name)

        elif choice == '4':
            group = input("Название группы: ")
            code = input("Код валюты: ")
            monitor.add_to_group(group, code)

        elif choice == '5':
            group = input("Название группы: ")
            code = input("Код валюты: ")
            monitor.remove_from_group(group, code)

        elif choice == '6':
            monitor.show_groups()

        elif choice == '7':
            group = input("Название группы: ")
            monitor.show_group_rates(group)

        elif choice == '8':
            print("\nДо свидания!")
            break

        else:
            print("Неверный выбор")


if __name__ == "__main__":
    main()