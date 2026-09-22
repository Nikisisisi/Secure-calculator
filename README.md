# Secure Calculator API

Учебный проект по дисциплине **«Безопасная разработка»**.

**Авторы:** Nikita Obukhov & Daria Lapshina

## О проекте

Secure Calculator — API-калькулятор, разработанный на Python с использованием FastAPI.

Приложение поддерживает:

- сложение;
- вычитание;
- умножение;
- деление;
- обработку деления на ноль;
- проверку входных данных;
- веб-интерфейс;
- автоматическую документацию Swagger;
- автоматические тесты;
- запуск в Docker-контейнере.

## Используемые технологии

- Python 3.13
- FastAPI
- Uvicorn
- Pydantic
- Pytest
- Docker
- Git / GitHub

---

# Быстрый запуск через Docker

Это рекомендуемый способ запуска проекта.

## 1. Клонировать репозиторий

```bash
git clone https://github.com/Nikisisisi/Secure-calculator.git
```

Перейти в папку проекта:

```bash
cd Secure-calculator
```

## 2. Собрать Docker-образ

```bash
docker build -t secure-calculator:1.0 .
```

## 3. Запустить контейнер

```bash
docker run -d --name secure-calculator -p 8000:8000 secure-calculator:1.0
```

## 4. Открыть приложение

Веб-интерфейс:

```text
http://127.0.0.1:8000/web
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

Проверка состояния API:

```text
http://127.0.0.1:8000/health
```

## 5. Остановить контейнер

```bash
docker stop secure-calculator
```

Удалить контейнер:

```bash
docker rm secure-calculator
```

---

# API

Калькулятор предоставляет следующие API-методы:

| Метод | Endpoint | Описание |
|---|---|---|
| GET | `/` | Информация о работе API |
| GET | `/health` | Проверка состояния приложения |
| GET | `/web` | Веб-интерфейс калькулятора |
| POST | `/calculate/add` | Сложение |
| POST | `/calculate/subtract` | Вычитание |
| POST | `/calculate/multiply` | Умножение |
| POST | `/calculate/divide` | Деление |

Пример запроса:

```json
{
  "a": 10,
  "b": 5
}
```

Пример ответа:

```json
{
  "result": 15
}
```

При попытке деления на ноль API возвращает ошибку HTTP 400.

---

# Автоматические тесты

Для проекта реализованы тесты с использованием `pytest`.

Проверяются:

- корневой endpoint;
- health-check;
- сложение;
- вычитание;
- умножение;
- деление;
- деление на ноль;
- некорректные входные данные;
- работа веб-интерфейса.

Всего:

```text
9 tests
```

Для запуска тестов локально:

```bash
python -m pytest
```

---

# Локальный запуск без Docker

Создать виртуальное окружение:

```bash
python -m venv .venv
```

### Windows PowerShell

Активировать окружение:

```powershell
.\.venv\Scripts\Activate.ps1
```

Установить зависимости:

```bash
pip install -r requirements.txt
```

Запустить приложение:

```bash
uvicorn app.main:app --reload
```

После запуска приложение будет доступно по адресу:

```text
http://127.0.0.1:8000
```

---

# 📁 Структура проекта

```text
secure-calculator/
├── app/
│   ├── __init__.py
│   ├── main.py
│   └── index.html
│
├── tests/
│   └── test_calculator.py
│
├── .dockerignore
├── .gitignore
├── Dockerfile
├── README.md
└── requirements.txt
```

---

# 🐳 Docker

Проект использует базовый образ:

```text
python:3.13-slim
```

Приложение внутри контейнера запускается через Uvicorn и использует порт:

```text
8000
```

---

# Версия

Текущая версия приложения:

```text
1.0.0
```

Проект будет развиваться в рамках следующих этапов работы:

- настройка CI/CD;
- автоматическое обновление версии;
- внедрение Semgrep;
- внедрение Trivy;
- анализ найденных уязвимостей;
- улучшение безопасности приложения.