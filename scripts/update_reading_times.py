"""Пересчитать время чтения всего текста и кода статей; --check проверяет актуальность.

Ориентиры: 110–160 слов/мин и 10–18 непустых строк кода/мин.
Это расчётные диапазоны для повторения, а не замеры на учениках.
Время практики сохраняется: его оценивают по содержанию заданий.
"""
import argparse
import html
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TIME = re.compile(r'<p class="reading-time">Примерное время[^<]*</p>\n*')

def reading_range(markdown):
    content = re.sub(r'<div class="topic-nav" markdown>.*?</div>', '', markdown, flags=re.S)
    content = re.sub(r'<p class="reading-time">.*?</p>', '', content)
    blocks = re.findall(r'^```[^\n]*\n(.*?)^```', content, re.M | re.S)
    lines = sum(sum(bool(line.strip()) for line in code.splitlines()) for code in blocks)
    prose = re.sub(r'^```[^\n]*\n.*?^```', '', content, flags=re.M | re.S)
    prose = re.sub(r'!?\[([^\]]*)\]\([^)]*\)', r'\1', prose)
    prose = re.sub(r'<[^>]+>', ' ', prose)
    prose = re.sub(r'\{[^}\n]*\}', '', prose)
    words = len(re.findall(r'\w+', html.unescape(prose)))
    low = max(1, math.ceil(words / 160 + lines / 18))
    high = max(low + 1, math.ceil(words / 110 + lines / 10))
    return low, high

def updated(markdown):
    practical = re.search(r'Практика: (\d+–\d+) (?:минут|мин)', markdown)
    body = TIME.sub('', markdown)
    low, high = reading_range(body)
    label = f'<p class="reading-time">Примерное время · Чтение: {low}–{high} мин'
    if practical:
        label += f' · Практика: {practical[1]} мин'
    label += '</p>'
    title, rest = body.split('\n', 1)
    return title + '\n\n' + label + '\n\n' + rest.lstrip('\n')

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    changed = []
    paths = sorted((ROOT / 'docs').rglob('*.md'))
    for path in paths:
        before = path.read_text()
        after = updated(before)
        if before != after:
            changed.append(path.relative_to(ROOT).as_posix())
            if not args.check:
                path.write_text(after)
    if args.check and changed:
        raise SystemExit('Устаревшие оценки чтения:\n' + '\n'.join(changed))
    print(f'Статей: {len(paths)}; ' + (f'обновлено: {len(changed)}' if not args.check else 'все оценки чтения актуальны'))

if __name__ == '__main__':
    main()
