import requests


def print_profile(profile):
    if "error" in profile:
        print(f"\nОшибка: {profile['error']}")
        return

    print("\n" + "=" * 60)
    print(f"ПРОФИЛЬ: {profile['name']} (@{profile['login']})")
    print("=" * 60)
    print(f"Ссылка: {profile['profile_url']}")
    print(f"Репозитории: {profile['repos_count']}")
    print(f"Подписчики: {profile['followers']}")
    print(f"Подписки: {profile['following']}")
    print(f"Дата регистрации: {profile['created_at']}")
    print("=" * 60)


def print_repos(repos):
    if not repos:
        print("\nНет репозиториев")
        return

    if "error" in repos[0]:
        print(f"\nОшибка: {repos[0]['error']}")
        return

    print("\n" + "=" * 70)
    print("РЕПОЗИТОРИИ")
    print("=" * 70)

    for i, repo in enumerate(repos, 1):
        print(f"\n{i}. {repo['name']}")
        print(f"   Ссылка: {repo['url']}")
        print(f"   Язык: {repo['language']}")
        print(f"   Видимость: {repo['visibility']}")
        print(f"   Ветка по умолчанию: {repo['default_branch']}")
        print(f"   Звезды: {repo['stars']} | Форки: {repo['forks']}")
    print("=" * 70)


def print_search_results(repos, query):
    if not repos:
        print(f"\nПо запросу '{query}' ничего не найдено")
        return

    if "error" in repos[0]:
        print(f"\nОшибка: {repos[0]['error']}")
        return

    print(f"\nРЕЗУЛЬТАТЫ ПОИСКА: '{query}'")
    print("=" * 70)

    for i, repo in enumerate(repos, 1):
        print(f"\n{i}. {repo['full_name']}")
        print(f"   Ссылка: {repo['url']}")
        print(f"   Описание: {repo['description'][:100]}")
        print(f"   Язык: {repo['language']}")
        print(f"   Звезды: {repo['stars']} | Форки: {repo['forks']}")
    print("=" * 70)


class GitHubClient:
    def __init__(self, token=None):
        self.base_url = "https://api.github.com"
        self.headers = {"Accept": "application/vnd.github.v3+json"}
        if token:
            self.headers["Authorization"] = f"token {token}"

    def get_user_profile(self, username):
        try:
            response = requests.get(
                f"{self.base_url}/users/{username}",
                headers=self.headers
            )

            if response.status_code == 200:
                data = response.json()
                return {
                    "name": data.get("name", username),
                    "login": data["login"],
                    "profile_url": data["html_url"],
                    "repos_count": data["public_repos"],
                    "followers": data["followers"],
                    "following": data["following"],
                    "created_at": data["created_at"][:10]
                }
            elif response.status_code == 404:
                return {"error": f"Пользователь {username} не найден"}
            else:
                return {"error": f"Ошибка: {response.status_code}"}

        except Exception as e:
            return {"error": str(e)}

    def get_user_repos(self, username):
        try:
            response = requests.get(
                f"{self.base_url}/users/{username}/repos",
                headers=self.headers,
                params={"sort": "updated", "per_page": 100}
            )

            if response.status_code == 200:
                repos = []
                for repo in response.json():
                    repos.append({
                        "name": repo["name"],
                        "url": repo["html_url"],
                        "language": repo.get("language", "Не указан"),
                        "visibility": "Приватный" if repo["private"] else "Публичный",
                        "default_branch": repo["default_branch"],
                        "stars": repo["stargazers_count"],
                        "forks": repo["forks_count"]
                    })
                return repos
            else:
                return [{"error": f"Ошибка: {response.status_code}"}]

        except Exception as e:
            return [{"error": str(e)}]

    def search_repos(self, query):
        try:
            response = requests.get(
                f"{self.base_url}/search/repositories",
                headers=self.headers,
                params={"q": query, "per_page": 10}
            )

            if response.status_code == 200:
                repos = []
                for repo in response.json()["items"]:
                    repos.append({
                        "name": repo["name"],
                        "full_name": repo["full_name"],
                        "url": repo["html_url"],
                        "description": repo.get("description", "Нет описания"),
                        "language": repo.get("language", "Не указан"),
                        "stars": repo["stargazers_count"],
                        "forks": repo["forks_count"]
                    })
                return repos
            else:
                return [{"error": f"Ошибка: {response.status_code}"}]

        except Exception as e:
            return [{"error": str(e)}]


def main():
    client = GitHubClient()

    while True:
        print("\n" + "=" * 50)
        print("GITHUB API КЛИЕНТ")
        print("=" * 50)
        print("1. Просмотр профиля пользователя")
        print("2. Репозитории пользователя")
        print("3. Поиск репозиториев")
        print("4. Выход")
        print("=" * 50)

        choice = input("Выберите действие (1-4): ")

        if choice == '1':
            username = input("Введите имя пользователя GitHub: ")
            profile = client.get_user_profile(username)
            print_profile(profile)

        elif choice == '2':
            username = input("Введите имя пользователя GitHub: ")
            repos = client.get_user_repos(username)
            print_repos(repos)

        elif choice == '3':
            query = input("Введите название для поиска: ")
            repos = client.search_repos(query)
            print_search_results(repos, query)

        elif choice == '4':
            print("\nДо свидания!")
            break

        else:
            print("Неверный выбор")


if __name__ == "__main__":
    main()