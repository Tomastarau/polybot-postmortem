"""Reading order of the story.

Single source of truth for the sidebar and the end-of-page pager: a duplicated
reading order is an order that eventually desynchronises.
"""

CHAPTERS = [
    ("ch01_summary", {"fr": "Résumé", "en": "Summary"}),
    ("ch02_birth", {"fr": "Naissance", "en": "Birth"}),
    ("ch03_strategies", {"fr": "Stratégies", "en": "Strategies"}),
    ("ch04_weather", {"fr": "Météo", "en": "Weather"}),
    ("ch05_infra", {"fr": "Infra", "en": "Infra"}),
    ("ch06_real_money", {"fr": "Argent réel", "en": "Real money"}),
    ("ch07_overfitting", {"fr": "Overfitting", "en": "Overfitting"}),
    ("ch08_verdict", {"fr": "Verdict", "en": "Verdict"}),
    ("ch09_method", {"fr": "Méthode", "en": "Method"}),
]

KEYS = [key for key, _ in CHAPTERS]
LABELS = dict(CHAPTERS)


def path(key):
    return f"app/chapters/{key}.py"


def label(key, lang):
    return LABELS[key][lang]


def neighbours(key):
    index = KEYS.index(key)
    previous = KEYS[index - 1] if index > 0 else None
    following = KEYS[index + 1] if index < len(KEYS) - 1 else None
    return previous, following
