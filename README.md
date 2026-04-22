# agent-dev-toolkit

`agent-dev-toolkit` - минималистичный CLI для автоматизации повседневных dev-задач.
Сейчас фокус на работе с `.env`-файлами: быстро создать локальный `.env` из шаблона и проверить конфигурацию в CI или локально.

## Что умеет

- `agent-toolkit env init` - создает `.env` из `.env.example`
- `agent-toolkit env doctor` - сверяет ключи шаблона и реального env-файла
- человекочитаемый (`text`) и машинный (`json`) формат вывода
- управление строгостью проверок (`--allow-extra`, `--strict`)
- запись отчета в файл (`--output`)

## Установка и запуск

Требования: Python `>=3.10`.

Локальный запуск без установки:

`python3 -m agent_dev_toolkit.cli --help`

После установки пакета доступна команда:

`agent-toolkit --help`

## Команда `env init`

Создает env-файл по шаблону.

Пример:

`agent-toolkit env init --template .env.example --output .env`

Полезные флаги:

- `--force` - перезаписать существующий output-файл

## Команда `env doctor`

Проверяет соответствие ключей в `--template` и `--env-file`.
Ключ определяется как часть строки до `=`.
Пустые строки и комментарии (`# ...`) игнорируются.

Базовый пример:

`agent-toolkit env doctor --template .env.example --env-file .env`

### Режимы валидации

- по умолчанию: ошибка, если есть missing **или** extra ключи
- `--allow-extra`: extra-ключи игнорируются, но missing остаются ошибкой
- `--strict`: строгий режим, ошибка на любые отличия (включая extra), даже если указан `--allow-extra`

Примеры:

- Локальная разработка с дополнительными переменными:
  `agent-toolkit env doctor --allow-extra`
- Строгий CI-гейт:
  `agent-toolkit env doctor --strict`

### Формат вывода

- `--format text` (по умолчанию) - читаемое сообщение для человека
- `--format json` - структурированный вывод для скриптов и CI

Пример:

`agent-toolkit env doctor --format json`

Пример JSON-ответа:

```json
{
  "ok": false,
  "missing": ["DB_HOST"],
  "extra": ["LOCAL_DEBUG"],
  "allow_extra": false,
  "strict": false,
  "message": "Environment differences detected:\n- Missing keys: DB_HOST\n- Extra keys: LOCAL_DEBUG"
}
```

### Запись результата в файл

`--output <path>` пишет тот же вывод, который печатается в stdout, в указанный файл.

Пример:

`agent-toolkit env doctor --format json --output .artifacts/env-doctor.json`

## Код возврата (exit code)

- `0` - проверка успешна (`ok=true`)
- `1` - найдены проблемы или ошибка входных файлов

Это удобно использовать в CI как шаг-валидатор.
