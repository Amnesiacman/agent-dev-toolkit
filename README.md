# agent-dev-toolkit

Полезный CLI-проект для dev-задач.

## Команды
- `agent-toolkit env init`
- `agent-toolkit env doctor`

### Проверка `.env` с разрешёнными extra-ключами
Если в локальном `.env` есть дополнительные переменные (например, для отладки), можно игнорировать их:

`agent-toolkit env doctor --allow-extra`
