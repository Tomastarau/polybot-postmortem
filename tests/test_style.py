"""The narrative voice is a project rule, so a machine checks it.

Three habits made the story read as machine-written: the em dash, the colon
that announces a moral, and the "not X, but Y" antithesis. A rule no machine
checks is a rule that eventually gets violated.
"""
import pathlib
import re
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app import i18n  # noqa: E402

LANGS = ["fr", "en"]
EM_DASH = "—"

ANTITHESIS = {
    "fr": re.compile(
        r"\b(n['’]|ne\s)[^.!?]{0,20}\b(pas|rien|plus|jamais)\b[^.!?]{0,80}[,;:]"
        r"\s*(c['’](est|était)|il\s+(a|avait|est|était)\b)"
    ),
    "en": re.compile(
        r"\b((is|was|had|did)\s*n[o']t|never|nothing)\b[^.!?]{0,80}[,;:]"
        r"\s*(it['’]?s|it\s+(was|had|is)|the\s+real)\b"
    ),
}


def ui_texts(lang):
    return [(key, value) for key, value in i18n.UI[lang].items()
            if key.endswith("_takeaway") or key.endswith("_method")]


@pytest.mark.parametrize("lang", LANGS)
def test_ui_texts_have_no_em_dash(lang):
    guilty = [key for key, value in ui_texts(lang) if EM_DASH in value]
    assert not guilty, f"em dash in {lang}: {guilty}"


@pytest.mark.parametrize("lang", LANGS)
def test_ui_texts_have_no_antithesis(lang):
    guilty = [key for key, value in ui_texts(lang)
              if ANTITHESIS[lang].search(value)]
    assert not guilty, f"antithesis in {lang}: {guilty}"


@pytest.mark.parametrize("lang", LANGS)
def test_takeaways_have_no_colon(lang):
    """The colon that announces a moral is the loudest tic of the three."""
    guilty = [key for key, value in i18n.UI[lang].items()
              if key.endswith("_takeaway") and ":" in value]
    assert not guilty, f"colon in {lang} takeaway: {guilty}"


PROSE_LANGS = ["fr", "en"]


def prose_files(lang):
    return sorted((i18n.CONTENT / lang).glob("*.md"))


@pytest.mark.parametrize("lang", PROSE_LANGS)
def test_prose_has_no_em_dash(lang):
    guilty = [f.name for f in prose_files(lang)
              if EM_DASH in f.read_text(encoding="utf-8")]
    assert not guilty, f"em dash in {lang}: {guilty}"


@pytest.mark.parametrize("lang", PROSE_LANGS)
def test_prose_has_no_antithesis(lang):
    guilty = [f.name for f in prose_files(lang)
              if ANTITHESIS[lang].search(f.read_text(encoding="utf-8"))]
    assert not guilty, f"antithesis in {lang}: {guilty}"
