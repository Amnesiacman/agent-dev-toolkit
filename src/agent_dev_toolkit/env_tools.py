from pathlib import Path

def parse_template_keys(template_text: str) -> list[str]:
    keys = []
    for raw_line in template_text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key = line.split("=", 1)[0].strip()
        if key:
            keys.append(key)
    return keys

def init_env(template_path: Path, output_path: Path, force: bool = False):
    if not template_path.exists():
        return False, f"Template not found: {template_path}"
    if output_path.exists() and not force:
        return False, f"{output_path} already exists. Use --force to overwrite."
    output_path.write_text(template_path.read_text(encoding="utf-8"), encoding="utf-8")
    return True, f"Created {output_path} from {template_path}"

def doctor_env(template_path: Path, env_path: Path, allow_extra: bool = False):
    if not template_path.exists():
        return False, f"Template not found: {template_path}"
    if not env_path.exists():
        return False, f"Env file not found: {env_path}. Run env init first."
    template_keys = set(parse_template_keys(template_path.read_text(encoding="utf-8")))
    env_keys = set(parse_template_keys(env_path.read_text(encoding="utf-8")))
    missing = sorted(template_keys - env_keys)
    extra = sorted(env_keys - template_keys)
    if allow_extra:
        extra = []
    if not missing and not extra:
        if allow_extra:
            return True, "Environment looks good: no missing keys."
        return True, "Environment looks good: no missing or extra keys."
    lines = ["Environment differences detected:"]
    if missing:
        lines.append("- Missing keys: " + ", ".join(missing))
    if extra:
        lines.append("- Extra keys: " + ", ".join(extra))
    return False, "\n".join(lines)
