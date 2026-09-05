#!/usr/bin/env python3
"""Regenerate the README's ROUTING-LINKS block from the current DEEPLINK
files. Run after the JSON/DEEPLINK files themselves have been regenerated.
Replaces only the block between the two marker comments, leaving the rest
of README.md untouched.
"""
import re
from datetime import datetime, timezone
from pathlib import Path


def read(path):
    return Path(path).read_text(encoding="utf-8").strip()


def main():
    happ_default = read("HAPP/DEFAULT.DEEPLINK")
    incy_default = read("INCY/DEFAULT.DEEPLINK")
    happ_whitelist = read("HAPP/WHITELIST.DEEPLINK")
    incy_whitelist = read("INCY/WHITELIST.DEEPLINK")
    happ_jsonsub = read("HAPP/JSONSUB.DEEPLINK")
    incy_jsonsub = read("INCY/JSONSUB.DEEPLINK")

    happ_default_b64 = happ_default.split("/onadd/", 1)[1]
    incy_default_b64 = incy_default.split("/onadd/", 1)[1]

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    block = f"""<!-- ROUTING-LINKS:START -->
> Обновлено автоматически: **{now}**. Ссылки и payload ниже регенерируются
> каждым запуском [Actions](../../actions) — всегда актуальны, ничего
> вручную собирать не нужно.

#### 📱 Happ — основной профиль (DEFAULT, RU+CN direct)

```
{happ_default}
```

<details>
<summary>Base64 payload (то, что внутри диплинка)</summary>

```
{happ_default_b64}
```
</details>

#### 📱 INCY — основной профиль (DEFAULT, RU+CN direct)

```
{incy_default}
```

<details>
<summary>Base64 payload (то, что внутри диплинка)</summary>

```
{incy_default_b64}
```
</details>

<details>
<summary>WHITELIST и JSONSUB диплинки (Happ / INCY)</summary>

| Вариант | Happ | INCY |
|---|---|---|
| WHITELIST | `{happ_whitelist}` | `{incy_whitelist}` |
| JSONSUB | `{happ_jsonsub}` | `{incy_jsonsub}` |

</details>
<!-- ROUTING-LINKS:END -->"""

    readme_path = Path("README.md")
    readme = readme_path.read_text(encoding="utf-8")

    pattern = re.compile(
        r"<!-- ROUTING-LINKS:START -->.*?<!-- ROUTING-LINKS:END -->",
        re.DOTALL,
    )
    if not pattern.search(readme):
        raise SystemExit("README.md is missing the ROUTING-LINKS markers")

    readme_path.write_text(pattern.sub(block, readme), encoding="utf-8")


if __name__ == "__main__":
    main()
