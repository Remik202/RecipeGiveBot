# Инструкция по подключению subscription_stats.py

- Скопировать файл subscription_stats.py в проект бота (рядом с основным кодом).

## Импортировать функции:
```bash
from subscription_stats import add_subscription, get_total_revenue
```

- Вызывать add_subscription() при каждой покупке.

- Вызывать get_total_revenue() для получения текущего дохода.

- Убедиться, что рядом с проектом есть права на запись — файл subscription_stats.json создаётся автоматически.

- При необходимости изменить цену подписки — изменить значение переменной ```SUBSCRIPTION_PRICE``` в скрипте.