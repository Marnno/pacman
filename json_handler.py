import json
from error_models import ConfigError


def pre_read(config_file: str) -> str:
    try:
        with open(config_file, "r", encoding='utf-8') as file:
            lines = [
                line for line in file
                if not line.lstrip().startswith("#")
            ]

            content = "".join(lines)

            return json.loads(content)

    except PermissionError as e:
        raise ConfigError(f"[ERROR]: {e}") from e

    except json.JSONDecodeError as e:
        raise ConfigError(f"[ERROR]: {e}") from e

    except OSError as e:
        raise ConfigError(f"[ERROR]: {e}") from e
