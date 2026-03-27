import requests


def print_results(results):
    print("\n" + "=" * 80)
    print("РЕЗУЛЬТАТЫ ПРОВЕРКИ")
    print("=" * 80)

    for url, status, code in results:
        if code > 0:
            print(f"{url} – {status} – {code}")
        else:
            print(f"{url} – {status}")


class HTTPMonitor:
    def __init__(self):
        self.timeout = 10
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

    def check_url(self, url):
        headers = {'User-Agent': self.user_agent}

        try:
            response = requests.get(url, headers=headers, timeout=self.timeout, allow_redirects=True)

            if response.status_code == 200:
                status_text = "доступен"
            elif response.status_code == 403:
                status_text = "вход запрещен"
            elif response.status_code == 404:
                status_text = "не найден"
            elif 500 <= response.status_code < 600:
                status_text = "ошибка сервера"
            else:
                status_text = "доступен с кодом"

            return url, status_text, response.status_code

        except requests.exceptions.Timeout:
            return url, "не доступен", 0
        except requests.exceptions.ConnectionError:
            return url, "не доступен", 0
        except requests.exceptions.RequestException:
            return url, "не доступен", 0

    def check_multiple(self, urls):
        results = []
        for url in urls:
            print(f"Проверка {url}...")
            result = self.check_url(url)
            results.append(result)
        return results


def main():
    urls = [
        "https://github.com/",
        "https://www.binance.com/en",
        "https://tomtit.tomsk.ru/",
        "https://jsonplaceholder.typicode.com/",
        "https://moodle.tomtit-tomsk.ru/"
    ]

    monitor = HTTPMonitor()
    results = monitor.check_multiple(urls)
    print_results(results)


if __name__ == "__main__":
    main()