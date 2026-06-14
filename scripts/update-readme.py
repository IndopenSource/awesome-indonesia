#!/usr/bin/env python3
import json
import os
import urllib.error
import urllib.request
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPOS_FILE = ROOT / "repos.json"
README_FILE = ROOT / "README.md"


def request_json(url, allow_not_found=False):
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "awesome-indonesia-readme-generator",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    request = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        if allow_not_found and error.code == 404:
            return None
        raise


def clean(value, fallback="N/A"):
    if value is None or value == "":
        return fallback
    return str(value)


def format_description(value):
    text = clean(value)
    text = re.sub(r"\bhttps?://[^\s\])>]+", lambda m: f"<{m.group(0)}>", text)
    text = re.sub(r"\bwww\.[^\s\])>]+\.[^\s\])>]+", lambda m: f"<https://{m.group(0)}>", text)
    return text.replace("|", "\\|")


def latest_release_metadata(full_name):
    data = request_json(
        f"https://api.github.com/repos/{full_name}/releases/latest",
        allow_not_found=True,
    )
    if not data:
        return {
            "latest_release": "N/A",
            "latest_release_url": "",
            "latest_release_date": "N/A",
        }

    return {
        "latest_release": clean(data.get("tag_name") or data.get("name")),
        "latest_release_url": clean(data.get("html_url"), ""),
        "latest_release_date": clean(
            (data.get("published_at") or data.get("created_at") or "")[:10]
        ),
    }


def repo_metadata(full_name):
    data = request_json(f"https://api.github.com/repos/{full_name}")
    license_data = data.get("license") or {}
    release_data = latest_release_metadata(data["full_name"])
    return {
        "full_name": data["full_name"],
        "name": data["name"],
        "owner": data["owner"]["login"],
        "url": data["html_url"],
        "description": clean(data.get("description")),
        "language": clean(data.get("language")),
        "stars": data.get("stargazers_count", 0),
        "forks": data.get("forks_count", 0),
        "open_issues": data.get("open_issues_count", 0),
        "watchers": data.get("watchers_count", 0),
        "updated_at": clean(data.get("pushed_at", "")[:10]),
        "license": clean(license_data.get("spdx_id")),
        "topics": data.get("topics") or [],
        **release_data,
    }


def tags_for(topics):
    if not topics:
        return "N/A"
    tags = " ".join(f"`{topic}`" for topic in topics[:6])
    if len(topics) > 6:
        tags += f" `+{len(topics) - 6}`"
    return tags


def project_cell(item):
    repo_link = f"[{item['name']}]({item['url']})"
    description = format_description(item["description"])
    anchor = f'<a id="{project_anchor(item["full_name"])}"></a>'
    return f"{anchor}{repo_link}<br>{description}"


def release_cell(item):
    release = clean(item.get("latest_release"))
    if release == "N/A":
        return "N/A"

    url = item.get("latest_release_url") or item["url"]
    release_label = release.replace("|", "\\|")
    release_link = f"[{release_label}]({url})"
    release_date = clean(item.get("latest_release_date"))
    if release_date == "N/A":
        return release_link
    return f"{release_link}<br>{release_date}"


def project_anchor(full_name):
    return full_name.lower().replace("/", "").replace(".", "").replace("_", "").replace(" ", "-")


def build_readme(items):
    rows = [
        "# Awesome Indonesia",
        "",
        "[![Awesome](https://awesome.re/badge.svg)](https://github.com/sindresorhus/awesome)",
        "[![GitHub stars](https://img.shields.io/github/stars/indopensource/awesome-indonesia?style=social)](https://github.com/indopensource/awesome-indonesia)",
        "[![Markdown Lint](https://github.com/IndopenSource/awesome-indonesia/actions/workflows/markdown-lint.yml/badge.svg)](https://github.com/IndopenSource/awesome-indonesia/actions/workflows/markdown-lint.yml)",
        "[![Contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](CONTRIBUTING.md)",
        "[![Made in Indonesia](https://img.shields.io/badge/made%20in-Indonesia-red.svg)](https://github.com/IndopenSource/awesome-indonesia)",
        "",
        '<meta name="description" content="Awesome Indonesia adalah katalog proyek open source Indonesia yang disusun berdasarkan jumlah stars GitHub untuk menilai popularitas komunitas.">',
        '<meta name="keywords" content="awesome indonesia, awesome-list indonesia, proyek open source indonesia, repository indonesia, komunitas open source indonesia">',
        "",
        "Kumpulan proyek open source Indonesia yang aktif dan bisa langsung dijadikan referensi belajar, integrasi, atau kontribusi.",
        "",
        "## Daftar Isi",
        "",
        "- [Tentang Daftar](#tentang-daftar)",
        "- [Urutan & Sumber Data](#urutan--sumber-data)",
        "- [Indeks Proyek](#indeks-proyek)",
        "- [Daftar Proyek](#daftar-proyek)",
        "- [Cara Berkontribusi](#cara-berkontribusi)",
        "- [Lisensi](#lisensi)",
        "- [Kontributor](#kontributor)",
        "- [Star History](#star-history)",
        "",
        "## Tentang Daftar",
        "",
        "Awesome List ini berisi koleksi proyek open source Indonesia yang dapat diakses publik dan tetap dirawat oleh komunitas.",
        "",
        "Daftar ini juga tersedia dalam versi UI di [tokengratis.id/opensource](https://www.tokengratis.id/opensource) dan [indopensource.org/projects](https://indopensource.org/projects/).",
        "",
        "## Urutan & Sumber Data",
        "",
        "Urutan proyek berdasarkan jumlah **GitHub stars** (descending).",
        f"Data terakhir disinkronkan: **{date.today().isoformat()}**.",
        "",
        "## Indeks Proyek",
        "",
        *[f"- [{item['full_name']}](#{project_anchor(item['full_name'])})" for item in items],
        "",
        "## Daftar Proyek",
        "",
        "| No | Project | Pembuat | Bahasa | Stars | Forks | Issue | Lisensi | Terakhir Update | Tags | Latest Release |",
        "| - | - | - | - | - | - | - | - | - | - | - |",
    ]

    for index, item in enumerate(items, 1):
        owner = f"[@{item['owner']}](https://github.com/{item['owner']})"
        rows.append(
            f"| {index} | {project_cell(item)} | {owner} | {item['language']} | "
            f"{item['stars']} | {item['forks']} | {item['open_issues']} | {item['license']} | "
            f"{item['updated_at']} | {tags_for(item['topics'])} | {release_cell(item)} |"
        )

    rows.extend(
        [
            "",
            "## Cara Berkontribusi",
            "",
            "Lihat [CONTRIBUTING.md](CONTRIBUTING.md).",
            "",
            "## Lisensi",
            "",
            "Dokumen dan struktur daftar ini menggunakan MIT License, sedangkan tiap proyek tetap mengikuti lisensi asli masing-masing repositori.",
            "",
            "## Kontributor",
            "",
            "[![Kontributor](https://contrib.rocks/image?repo=IndopenSource/awesome-indonesia)](https://github.com/IndopenSource/awesome-indonesia/graphs/contributors)",
            "",
            "## Star History",
            "",
            "[![Star History Chart](https://api.star-history.com/svg?repos=IndopenSource/awesome-indonesia&type=Date)](https://www.star-history.com/#IndopenSource/awesome-indonesia&Date)",
        ]
    )
    return "\n".join(rows)


def main():
    repos = json.loads(REPOS_FILE.read_text(encoding="utf-8"))
    items = [repo_metadata(repo) for repo in repos]
    items.sort(key=lambda item: (item["stars"], item["watchers"], item["forks"]), reverse=True)
    README_FILE.write_text(build_readme(items) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
