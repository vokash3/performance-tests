# QA Performance Engineer
<img src="https://cdn.stepik.net/media/cache/images/courses/242935/cover_cE4uVIf/46ed8cc5a9b8982bd8e91ff34374a376.png" alt="Course cover" height="230" width="230">

Проект для взаимодействие с тестовой банковской системой в рамках [курса Никиты Филонова на Stepik](https://stepik.org/242935).

_Проверено на Python3.12._

__Отдельный тестовый стенд развёрнут на виртуальном сервере.__

### Ссылки

- [OpenAPI](http://155.212.171.137:8003/docs)
- [pgAdmin](http://155.212.171.137:5050/)
- [Grafana](http://155.212.171.137:3002/d/23673d3b-5bd8-4027-88e4-31eb65880e72/docker-and-system-monitoring/)
- [MinIO](http://155.212.171.137:3001/)
- [Kafka](http://155.212.171.137:8081/)

## Task 7.1
Работаем в рабочей директории **performance-tests**
- Создаём среду
  ```bash
  python3 -m venv venv
  ```
- Активируем venv
  ```bash
  source venv/bin/activate
  ```
- Устанавливаем зависимости
  ```bash
  pip install -r requirements.txt
  ```
- Запускаем **httpx_open_deposit_account.py**
  ```bash
  python httpx_open_deposit_account.py
  ```