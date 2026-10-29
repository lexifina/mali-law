"""Builds scripts/mali-law/corpus.json from the cache only (no network).

    python -X utf8 scripts/mali-law/parse.py [--check]

Sources are Journal officiel issues published as PDFs with a text layer by the Secrétariat général du Gouvernement
(sgg-mali.ml). Text is read with PyMuPDF line by line; paragraphs are rebuilt from the justified layout (a line that
stops short of the column edge and ends a sentence closes a paragraph). --check also prints the comparisons this
corpus was verified with (second publications and the SGG "Codes en vigueur" copy).
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import unicodedata
from pathlib import Path

import fitz

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import fetch  # noqa: E402

SGG = 'https://sgg-mali.ml'
RETRIEVED = '2026-10-28'

# ---------------------------------------------------------------------------------------------------------------
# PDF to paragraphs


def norm(s: str) -> str:
    s = unicodedata.normalize('NFC', s)
    s = s.replace(' ', ' ').replace(' ', ' ').replace(' ', ' ').replace('\t', ' ')
    s = s.replace("'", '’').replace('‘', '’').replace('ʼ', '’')
    s = s.replace('“', '«').replace('”', '»').replace('—', '–').replace('‑', '-')
    s = s.replace('', '•').replace('●', '•').replace('', '-')
    s = re.sub(r'«\s*', '« ', s)
    s = re.sub(r'\s*»', ' »', s)
    s = re.sub(r' {2,}', ' ', s)
    return s.strip()


TERMINAL = tuple('.;:!?»')
ART_LINE = re.compile(r'^(?:Article|ARTICLE)\s*\d+(?:\s*-\s*\d+)?\s*(?:er|ER|ème)?\s*(?:bis|ter|quater)?\s*:')
HEAD_LINE = re.compile(r'^(?:LIVRE|TITRE|CHAPITRE|Chapitre|SECTION|Section|SOUS-SECTION|Sous-section|Paragraphe|'
                       r'PARAGRAPHE|Sous[- ]paragraphe)\s*(?:[IVXLC]+|\d+|unique|UNIQUE|premier|PREMIER|1er)')
HEADER_RX = re.compile(r'^(\d+\s*)?(\d{1,2}\s+\w+\s+\d{4}\s+)?JOURNAL\s+OFFICIEL DE LA REPUBLIQUE DU MALI(\s*\d+)?$')


def pdf_lines(data: bytes) -> list[dict]:
    """Every text line, in reading order, with its page, column edge and block id. Running heads are dropped."""
    doc = fitz.open(stream=data, filetype='pdf')
    out = []
    for pno, page in enumerate(doc):
        width = page.rect.width
        d = page.get_text('dict')
        lines = []
        for bi, b in enumerate(d['blocks']):
            if b.get('type') != 0:
                continue
            btext = ' '.join(''.join(s['text'] for s in ln['spans']) for ln in b['lines'])
            if b['bbox'][3] < 45 or HEADER_RX.match(norm(btext)) or re.fullmatch(r'\s*\d+\s*', btext):
                continue
            for ln in b['lines']:
                t = ''.join(s['text'] for s in ln['spans'])
                if not t.strip():
                    continue
                x0, y0, x1, y1 = ln['bbox']
                lines.append({'page': pno, 'block': (pno, bi), 'x0': x0, 'x1': x1, 'y0': y0, 'text': t,
                              'col': 0 if x0 < width / 2 - 10 else 1})
        edge = {}
        for ln in lines:
            edge[ln['col']] = max(edge.get(ln['col'], 0), ln['x1'])
        for ln in lines:
            ln['edge'] = edge[ln['col']]
        out.extend(lines)
    return out


def join_lines(parts: list[str], vocab: set[str]) -> str:
    s = ''
    for p in parts:
        p = p.strip()
        if not s:
            s = p
            continue
        m = re.search(r'(\w+)-$', s)
        if m and p[:1].isalpha():
            word = m.group(1) + re.match(r'\w*', p).group(0)
            # A hyphen at a line end is kept (sous-régionale, ci-dessus) unless the unhyphenated word occurs in the
            # same document and the hyphenated one does not.
            if word.lower() in vocab and (m.group(1) + '-' + re.match(r'\w*', p).group(0)).lower() not in vocab:
                s = s[:-1] + p
            else:
                s = s + p
        else:
            s = s + ' ' + p
    return s


def paragraphs(data: bytes) -> list[str]:
    lines = pdf_lines(data)
    vocab = set()
    for ln in lines:
        vocab.update(w.lower() for w in re.findall(r'\w+(?:-\w+)*', norm(ln['text'])))
    paras: list[list[str]] = []
    prev = None
    for ln in lines:
        t = norm(ln['text'])
        if not t:
            continue
        new = True
        if prev is not None:
            prev_full = prev['x1'] >= prev['edge'] - 12
            prev_t = paras[-1][-1]
            # An article ("Article N :"), a structural heading or a bracketed line always opens a paragraph, in the
            # same block or across blocks (a full-width heading line is otherwise read as running on).
            starts = bool(ART_LINE.match(t)) or bool(HEAD_LINE.match(t)) or t.startswith('[')
            if ln['block'] == prev['block']:
                new = (not prev_full and prev_t.endswith(TERMINAL)) or starts or bool(
                    HEAD_LINE.match(' '.join(paras[-1])) and not prev_full)
            else:
                new = starts or (not (prev_full and not prev_t.endswith(TERMINAL)) and not (
                    t[:1].islower() and not prev_t.endswith(('.', ':', '!', '?', '»'))))
            if paras[-1] == ['-'] or paras[-1] == ['•'] or paras[-1] == ['–']:
                new = False
        if new:
            paras.append([t])
        else:
            paras[-1].append(t)
        prev = ln
    out = []
    for p in paras:
        s = join_lines(p, vocab)
        s = re.sub(r'^([-–•])\s*', r'\1 ', s)
        out.append(norm(s))
    return out


def text_of(url: str) -> list[str]:
    return paragraphs(fetch.fetch(url, offline=True))


def sha(url: str) -> str:
    return hashlib.sha256(fetch.fetch(url, offline=True)).hexdigest()


def between(paras: list[str], start: str, end: str, after: str | None = None) -> list[str]:
    """Paragraphs strictly after the first one matching `start` (searched after `after`, if given), up to the first
    one matching `end`."""
    i = 0
    if after:
        i = next(k for k, p in enumerate(paras) if re.search(after, p))
    i = next(k for k in range(i, len(paras)) if re.search(start, paras[k]))
    j = next(k for k in range(i + 1, len(paras)) if re.search(end, paras[k]))
    return paras[i + 1:j]


# ---------------------------------------------------------------------------------------------------------------
# paragraphs to units

ART_RX = re.compile(r'^(?:Article|ARTICLE)\s*(\d+)(?:\s*-\s*(\d+))?\s*(er|ER|ème)?\s*(bis|ter|quater)?\s*:\s*(.*)$')
HEAD_RX = HEAD_LINE


def is_caps(p: str) -> bool:
    return len(p) < 200 and not re.search(r'[a-zà-ÿ]', p) and re.search(r'[A-Z]', p) is not None


def art_key(m: re.Match, pad1: int) -> tuple[str, str]:
    a, b, er, bis = m.group(1), m.group(2), m.group(3), m.group(4)
    if b is not None:
        key = f'art-{int(a):0{pad1}d}-{int(b):03d}'
        label = f'Article {int(a)}-{int(b)}'
    else:
        key = f'art-{int(a):03d}'
        label = f'Article {int(a)}' + ('er' if er and er.lower() == 'er' else '')
    if bis:
        key += '-' + bis.lower()
        label += ' ' + bis.lower()
    return key, label


def units_from(paras: list[str], *, pad1: int = 3, preamble: str | None = None) -> tuple[dict, list[str]]:
    """Articles become units; structural headings are collected into one 'plan' unit (heading, then the first
    article under it), so a change in the act's structure shows as a change there. Text before the first heading or
    article becomes `preamble` if given."""
    units: dict[str, dict] = {}
    plan: list[str] = []
    problems: list[str] = []
    cur = None
    pending_heads: list[str] = []
    pre: list[str] = []
    last_was_head = False
    for p in paras:
        m = ART_RX.match(p)
        if m:
            key, label = art_key(m, pad1)
            if key in units:
                problems.append(f'duplicate {key}')
                key += '-dup'
            cur = {'label': label, 'kind': 'art', 'lines': [f'# {label}'] + ([m.group(5)] if m.group(5) else [])}
            units[key] = cur
            for h in pending_heads:
                plan.append(f'{h} ({label})')
            pending_heads = []
            last_was_head = False
            continue
        if HEAD_RX.match(p) or p.upper().startswith('PREAMBULE') or (last_was_head and is_caps(p)) or (
                cur is None and is_caps(p)):
            if last_was_head and pending_heads and (is_caps(p) or not HEAD_RX.match(p)) and not p.upper().startswith(
                    'PREAMBULE'):
                pending_heads[-1] += ' : ' + p if not pending_heads[-1].rstrip().endswith(':') else ' ' + p
            else:
                pending_heads.append(p.rstrip(' :'))
            last_was_head = True
            cur = None if not p.upper().startswith('PREAMBULE') else cur
            if p.upper().startswith('PREAMBULE'):
                cur = 'pre'
            continue
        last_was_head = False
        if cur == 'pre' or cur is None:
            pre.append(p)
            if cur is None and units:
                problems.append(f'orphan paragraph after a heading: {p[:80]}')
            continue
        cur['lines'].append(p)
    out = {}
    if preamble and pre:
        out['preambule'] = {'label': preamble, 'kind': 'other', 'text': f'# {preamble}\n' + '\n'.join(pre) + '\n'}
    if plan:
        out['plan'] = {'label': 'Plan', 'kind': 'other', 'text': '# Plan\n' + '\n'.join(plan) + '\n'}
    for k, u in units.items():
        out[k] = {'label': u['label'], 'kind': u['kind'], 'text': '\n'.join(u['lines']) + '\n'}
    return out, problems


# ---------------------------------------------------------------------------------------------------------------
# the acts

def constitution() -> tuple[dict, dict, list[str]]:
    url = f'{SGG}/JO/2023/mali-jo-2023-13-sp-3.pdf'
    paras = text_of(url)
    body = between(paras, r'promulgue la\s*Constitution dont la teneur suit', r'^Bamako, le 22 juillet 2023')
    units, problems = units_from(body, preamble='Préambule')
    laws = {'constitution-2023': {
        'label': 'Constitution du 22 juillet 2023',
        'title': 'Constitution de la République du Mali, adoptée par le référendum du 18 juin 2023 et promulguée par '
                 'le Décret n°2023-0401/PT-RM du 22 juillet 2023',
        'kind': 'referendum', 'enacted': '2023-07-22', 'published': '2023-07-22', 'url': url,
        'temporary_until': None, 'restores': None, 'note': None}}
    act = {'slug': 'constitution', 'short': 'Constitution', 'title': 'Constitution de la République du Mali (2023)',
           'url': url, 'first_law': 'constitution-2023', 'earlier_laws': [],
           'versions': [{'from': '2023-07-22', 'source_url': url, 'sha256': sha(url), 'units': units,
                         'credits': {}, 'note': 'Journal officiel, spécial n°13 du 22 juillet 2023.'}]}
    return act, laws, problems


def code_penal() -> tuple[dict, dict, list[str]]:
    url = f'{SGG}/JO/2024/mali-jo-2024-21-sp.pdf'
    paras = text_of(url)
    body = between(paras, r'promulgue la\s*loi dont la teneur suit', r'^Bamako, le 13 décembre 2024')
    units, problems = units_from(body, pad1=4)
    laws = {'loi-2024-027': {
        'label': 'Loi n°2024-027', 'title': 'Loi n°2024-027 du 13 décembre 2024 portant Code pénal',
        'kind': 'law', 'enacted': '2024-12-13', 'published': '2024-12-13', 'url': url,
        'temporary_until': None, 'restores': None, 'note': None}}
    act = {'slug': 'code-penal', 'short': 'Code pénal', 'title': 'Code pénal (Loi n°2024-027 du 13 décembre 2024)',
           'url': url, 'first_law': 'loi-2024-027', 'earlier_laws': [],
           'versions': [{'from': '2024-12-13', 'source_url': url, 'sha256': sha(url), 'units': units,
                         'credits': {}, 'note': 'Journal officiel, spécial n°21 du 13 décembre 2024.'}]}
    return act, laws, problems


def donnees_personnelles() -> tuple[dict, dict, list[str]]:
    u1 = f'{SGG}/JO/2013/mali-jo-2013-26.pdf'
    paras = text_of(u1)
    body = between(paras, r'promulgue la\s*loi dont la\s*teneur suit', r'^Bamako, le 21 mai 2013',
                   after=r'^LOI N°\s*2013-015')
    units, problems = units_from(body)
    u2 = f'{SGG}/JO/2017/mali-jo-2017-53.pdf'
    p2 = text_of(u2)
    amend = between(p2, r'sont modifiés ainsi qu’il suit', r'^Article 2 : La présente loi abroge',
                    after=r'^LOI N°\s*2017-070')
    new, prob2 = units_from(amend)
    problems += prob2
    changed = {}
    for k, v in new.items():
        if k not in units:
            problems.append(f'2017-070 replaces {k}, which the 2013 text does not have')
        changed[k] = v
    want = {'art-021', 'art-025', 'art-036', 'art-042', 'art-049'}
    if set(changed) != want:
        problems.append(f'2017-070: expected {sorted(want)}, parsed {sorted(changed)}')
    laws = {
        'loi-2013-015': {'label': 'Loi n°2013-015',
                         'title': 'Loi n°2013-015 du 21 mai 2013 portant protection des données à caractère personnel '
                                  'en République du Mali',
                         'kind': 'law', 'enacted': '2013-05-21', 'published': '2013-06-28', 'url': u1,
                         'temporary_until': None, 'restores': None, 'note': None},
        'loi-2017-070': {'label': 'Loi n°2017-070',
                         'title': 'Loi n°2017-070 du 18 décembre 2017 portant modification de la Loi n°2013-015 du 21 '
                                  'mai 2013 portant protection des données à caractère personnel en République du Mali',
                         'kind': 'law', 'enacted': '2017-12-18', 'published': '2017-12-29', 'url': u2,
                         'temporary_until': None, 'restores': None, 'note': None}}
    act = {'slug': 'donnees-personnelles', 'short': 'Loi 2013-015',
           'title': 'Loi n°2013-015 du 21 mai 2013 portant protection des données à caractère personnel en République '
                    'du Mali', 'url': u1, 'first_law': 'loi-2013-015', 'earlier_laws': [],
           'versions': [
               {'from': '2013-06-28', 'source_url': u1, 'sha256': sha(u1), 'units': units, 'credits': {},
                'note': 'Journal officiel n°26 du 28 juin 2013, p. 1002.'},
               {'from': '2017-12-29', 'source_url': u2, 'sha256': sha(u2), 'changes': changed,
                'credits': {k: ['loi-2017-070'] for k in sorted(changed) if changed[k] != units.get(k)},
                'note': 'Journal officiel n°53 du 29 décembre 2017, p. 2115: Loi n°2017-070, art. 1er, replaces '
                        'articles 21, 25, 36, 42 and 49 in full.'}]}
    return act, laws, problems


# ---------------------------------------------------------------------------------------------------------------

DECISIONS = [
    'Source: the Journal officiel de la République du Mali as published by the Secrétariat général du Gouvernement '
    '(sgg-mali.ml), one PDF per issue with a text layer. No OCR was used; every text came from the text layer.',
    'Dates: no Malian text we read sets a general delay between publication and entry into force; the 2023 '
    'Constitution (art. 116) requires laws to be published in the Journal officiel. Each version is dated by the '
    'date printed on the Journal officiel issue that published it, unless the law fixes its own date. None of the '
    'three acts does.',
    'Constitution: dated 22 July 2023, the day the Décret n°2023-0401/PT-RM promulgated it and the day of the '
    'Journal officiel spécial n°13 that printed it (art. 191 ties promulgation to the referendum of 18 June 2023; '
    'Arrêt n°2023-08/CC-Réf of 21 July 2023 proclaimed the result). It was printed again in Journal officiel n°20 of '
    '4 August 2023 (p. 790); parse.py --check compares the two.',
    'Constitution and Code pénal: every Journal officiel issue from 22 July 2023 to 20 October 2026 listed on '
    'sgg-mali.ml (165 issues) was searched for a revision of the Constitution or an amendment of Loi n°2024-027; none '
    'was found. Two issues listed for September 2024 (mali-jo-2024-32-php-2.pdf, mali-jo-2024-32-php00-2.pdf) are '
    'not valid PDFs on the site, so they could not be searched; both predate the Code pénal.',
    'Code pénal: the SGG "Codes en vigueur" page (retrieved 2026-10-28) links codes/codepenal.pdf, which carries the '
    'same Journal officiel spécial n°21 of 13 December 2024; parse.py --check confirms the two give identical text, so '
    'today\'s text is the text as enacted.',
    'Code pénal: art. 702-1 repeals "toutes dispositions antérieures contraires" and Loi n°01-079 du 20 août 2001 '
    '(the former Code pénal). Implied repeals of other laws are not applied to any text in this repository.',
    'Loi n°2013-015: every Journal officiel issue listed on sgg-mali.ml from 28 June 2013 to 20 October 2026 was '
    'searched for laws modifying it. The only one is Loi n°2017-070 of 18 December 2017 (Journal officiel n°53, '
    '29 December 2017), which replaces articles 21, 25, 36, 42 and 49 in full; it is applied as printed. Two issues '
    'in the listing return 404 (mali-jo-2020-23.pdf, mali-jo-2021-04-3.pdf) and could not be searched.',
    'Loi n°2017-070 art. 2 also repeals "toutes dispositions antérieures contraires" of Loi n°2013-015 without naming '
    'any; no further change is made for it.',
    'Paragraphs are rebuilt from the PDF layout: a line that stops short of the column edge and ends with . ; : ! ? '
    'or » closes a paragraph; a block that starts after a full-width line without final punctuation continues it '
    '(page and column breaks). A hyphen at a line end is dropped only when the unhyphenated word occurs elsewhere in '
    'the same issue and the hyphenated form does not.',
    'Typesetting is normalised once: no-break spaces become spaces, straight and curly apostrophes become ’, '
    'guillemets get one inner space, em dashes become en dashes.',
    'Structural headings (Livre, Titre, Chapitre, Section, Paragraphe) are kept in one "plan" file per act, each '
    'followed by the first article under it; articles are one file each. Signatures and the promulgation formula are '
    'left out.',
    'Unit keys: art-NNN for single numbers; the Code pénal\'s two-part numbers (Livre-Titre-Chapitre, then article) '
    'become art-NNNN-NNN, zero-padded so files sort in code order.',
]

AI_USE = ['Claude Code (Claude Opus 5.5, claude-opus-5-5) wrote fetch.py, jo_index.py, scan.py and parse.py and chose '
          'the sources. No model wrote, translated or summarised legal text; all text is extracted by code from the '
          'official PDFs.']


def requests_count() -> int:
    p = HERE / '.cache' / 'requests.jsonl'
    return sum(1 for line in p.open(encoding='utf-8') if 'sgg-mali.ml' in line) if p.exists() else 0


def build() -> tuple[dict, list[str]]:
    acts, laws, problems = [], {}, []
    for fn in (constitution, donnees_personnelles):  # code_penal: duplicate numbers, see PROGRESS.md
        a, l, p = fn()
        acts.append(a)
        laws.update(l)
        problems += [f'{a["slug"]}: {x}' for x in p]
    corpus = {
        'country': {
            'code': 'ML', 'name': 'Mali', 'slug': 'mali', 'lang': 'fr', 'tz': 'Africa/Bamako', 'future_branch': 'futur',
            'publisher': {'name': 'Secrétariat général du Gouvernement (Journal officiel de la République du Mali)',
                          'email': 'sgg@sgg-mali.ml.invalid'},
            'default_in_force_rule': {
                'text': 'Constitution du 22 juillet 2023, art. 116: « Les lois et les règlements sont publiés au '
                        'Journal officiel. » No general delay is set; a law without its own commencement clause is '
                        'dated from its Journal officiel issue.',
                'source': f'{SGG}/JO/2023/mali-jo-2023-13-sp-3.pdf'},
            'licence_note': 'Texte officiel : Journal officiel de la République du Mali, Secrétariat général du '
                            'Gouvernement (sgg-mali.ml). Official legal texts; the site states no licence.'},
        'sources': [{
            'name': 'Journal officiel de la République du Mali (Secrétariat général du Gouvernement)',
            'url': f'{SGG}/fr/journal-officiel/le-journal-officiel.html', 'retrieved': RETRIEVED,
            'requests': requests_count(),
            'licence': 'Official legal texts published by the Government of Mali; sgg-mali.ml states no licence and '
                       'its robots.txt disallows nothing.',
            'notes': 'Issues used: JO spécial n°13 (22 July 2023), JO n°20 (4 August 2023, check only), JO spécial '
                     'n°21 (13 December 2024), JO n°26 (28 June 2013), JO n°53 (29 December 2017); the Codes en '
                     'vigueur copy codes/codepenal.pdf (check only). Every other issue fetched was read only to search '
                     'for amendments (scan.py).'}],
        'laws': dict(sorted(laws.items())),
        'acts': acts,
        'applies': [],
        'decisions': DECISIONS,
        'ai_use': AI_USE,
    }
    return corpus, problems


def check() -> None:
    a = text_of(f'{SGG}/JO/2024/mali-jo-2024-21-sp.pdf')
    b = text_of(f'{SGG}/codes/codepenal.pdf')
    print('Code pénal, JO spécial 21 vs Codes en vigueur copy:', 'identical' if a == b else 'DIFFERENT')
    c1 = between(text_of(f'{SGG}/JO/2023/mali-jo-2023-13-sp-3.pdf'),
                 r'promulgue la\s*Constitution dont la teneur suit', r'^Bamako, le 22 juillet 2023')
    c2 = between(text_of(f'{SGG}/JO/2023/mali-jo-2023-20-3.pdf'),
                 r'promulgue la\s*Constitution dont la teneur suit', r'^Bamako, le 22 juillet 2023')
    u1, _ = units_from(c1, preamble='Préambule')
    u2, _ = units_from(c2, preamble='Préambule')
    diff = [k for k in sorted(set(u1) | set(u2)) if u1.get(k) != u2.get(k)]
    print('Constitution, JO spécial 13 vs JO 20 (4 Aug 2023):', len(u1), 'units;', len(diff), 'differ', diff[:20])
    for k in diff[:5]:
        print('  ', k, '\n   A:', (u1.get(k) or {}).get('text', '')[:400], '\n   B:', (u2.get(k) or {}).get('text', '')[:400])


def main() -> None:
    if '--check' in sys.argv:
        check()
        return
    corpus, problems = build()
    for p in problems:
        print('PROBLEM', p)
    for a in corpus['acts']:
        print(a['slug'], [(v['from'], len(v.get('units') or v.get('changes') or {})) for v in a['versions']])
    tmp = HERE / 'corpus.json.tmp'
    tmp.write_text(json.dumps(corpus, ensure_ascii=False, indent=1, sort_keys=False) + '\n', encoding='utf-8',
                   newline='\n')
    if '--dry' not in sys.argv:
        os.replace(tmp, HERE / 'corpus.json')


if __name__ == '__main__':
    main()
