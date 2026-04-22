# agent-dev-toolkit

Полезный CLI-проект для dev-задач.

## Команды
- `agent-toolkit env init`
- `agent-toolkit env doctor`

### Проверка `.env` с разрешёнными extra-ключами
Если в локальном `.env` есть дополнительные переменные (например, для отладки), можно игнорировать их:

`agent-toolkit env doctor --allow-extra`

### JSON-вывод для CI и скриптов
Для машинной обработки результата используйте JSON-формат:

`agent-toolkit env doctor --format json`
