"""Проверить учебную структуру, локальные Markdown-ссылки и синтаксис Python."""
import ast
import re
from pathlib import Path
from urllib.parse import unquote
from update_reading_times import updated

root = Path(__file__).resolve().parents[1]
docs = root / "docs"
service_pages = {"index.md", "projects.md", "practice.md"}
lessons = 0
blocks = 0
errors = []
lesson_paths = set()
for path in sorted(docs.rglob("*.md")):
    text = path.read_text()
    if updated(text) != text:
        errors.append(f"{path}: stale reading estimate; run scripts/update_reading_times.py")
    if path.name not in service_pages:
        lessons += 1
        lesson_paths.add(path.relative_to(docs).as_posix())
        headings = ["## Теория", "## Частые ошибки", "## Разбор практических задач",
                    "## Самостоятельная практика", "## Проверьте себя",
                    "## Где пригодится и что повторить"]
        positions = [text.find(heading) for heading in headings]
        if -1 in positions or positions != sorted(positions):
            errors.append(f"{path}: missing/reordered lesson sections")
        if len(re.findall(r"^### Задача [123]\. ", text, re.M)) != 3:
            errors.append(f"{path}: expected three solved tasks")
    for match in re.finditer(r"^```python\n(.*?)^```", text, re.M | re.S):
        blocks += 1
        try:
            ast.parse(match[1])
        except SyntaxError as error:
            errors.append(f"{path}:{text[:match.start()].count(chr(10))+1}: {error}")
    for target in re.findall(r"\]\(([^)]+)\)", text):
        if "://" in target or target.startswith(("#", "mailto:")):
            continue
        target = unquote(target.split("#", 1)[0])
        if target and not (path.parent / target).exists():
            errors.append(f"{path}: broken local link {target}")
nav_paths = set(re.findall(r": ([\w/.-]+\.md)$", (root / "mkdocs.yml").read_text(), re.M))
expected_lessons = {name for name in nav_paths if Path(name).name not in service_pages}
if lesson_paths != expected_lessons:
    errors.append(f"Lesson/navigation mismatch: {sorted(lesson_paths ^ expected_lessons)}")
if errors:
    raise SystemExit("\n".join(errors))
print(f"{lessons} lessons, {lessons * 3} solved tasks, {blocks} Python blocks: checks passed")
