"""Builds scripts/mali-law/corpus.d/50-code-procedure-penale.json from the cache only (no network).

    python -X utf8 scripts/mali-law/parse_cpp.py [--check]

The Code de procédure pénale (Loi n°2024-028 du 13 décembre 2024), read from the Journal officiel spécial n°22 of
13 December 2024 (sgg-mali.ml) with the paragraph and unit rules of parse.py. --check compares it with the SGG "Codes
en vigueur" copy (codes/codeprocedurepenale.pdf), runs the coverage check (every character of the text layer from the
promulgation formula to the signature is in exactly one unit, in order) and lists numbering gaps.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import parse  # noqa: E402

SGG = parse.SGG
RETRIEVED = '2026-10-29'
CPP = (f'{SGG}/JO/2024/mali-jo-2024-22-sp.pdf', r'promulgue la\s*loi dont la teneur suit',
       r'^Bamako, le 13 décembre 2024')
CODES_COPY = f'{SGG}/codes/codeprocedurepenale.pdf'
PART = HERE / 'corpus.d' / '50-code-procedure-penale.json'

DECISIONS = [
    'Code de procédure pénale: Loi n°2024-028 du 13 décembre 2024, printed in the Journal officiel spécial n°22 of '
    '13 December 2024 (adopted by the Conseil national de Transition on 31 October 2024). It is dated 13 December '
    '2024, the day of promulgation and of that issue; the law sets no other date.',
    'Code de procédure pénale: the SGG "Codes en vigueur" page (retrieved 2026-10-29) links '
    'codes/codeprocedurepenale.pdf, which carries the same Journal officiel spécial n°22; the two give identical '
    'text, so today\'s text is the text as enacted.',
    'Code de procédure pénale: every Journal officiel issue listed on sgg-mali.ml from 13 December 2024 to the newest '
    'issue online was searched for an amendment of Loi n°2024-028; none was found (the issues that could not be '
    'read are named in the README).',
    'Code de procédure pénale: structural headings go to the act\'s "plan" file and the annexed table of contents '
    '(after the signature) is left out, as for the other acts.',
]


def build() -> tuple[dict, list[str]]:
    url = CPP[0]
    body = parse.between(parse.text_of(url), *CPP[1:])
    units, problems = parse.units_from(body)
    laws = {'loi-2024-028': {
        'label': 'Loi n°2024-028', 'title': 'Loi n°2024-028 du 13 décembre 2024 portant Code de procédure pénale',
        'kind': 'law', 'enacted': '2024-12-13', 'published': '2024-12-13', 'url': url,
        'temporary_until': None, 'restores': None, 'note': None}}
    act = {'slug': 'code-procedure-penale', 'short': 'Code de procédure pénale',
           'title': 'Code de procédure pénale (Loi n°2024-028 du 13 décembre 2024)',
           'url': url, 'first_law': 'loi-2024-028', 'earlier_laws': [],
           'versions': [{'from': '2024-12-13', 'source_url': url, 'sha256': parse.sha(url), 'units': units,
                         'credits': {}, 'note': 'Journal officiel, spécial n°22 du 13 décembre 2024.'}]}
    part = {
        'sources': [{
            'name': 'Journal officiel de la République du Mali (Secrétariat général du Gouvernement): Code de '
                    'procédure pénale',
            'url': f'{SGG}/fr/journal-officiel/les-codes-consolides.html', 'retrieved': RETRIEVED,
            'licence': 'Official legal texts published by the Government of Mali; sgg-mali.ml states no licence.',
            'notes': 'JO spécial n°22 (13 December 2024); the Codes en vigueur copy codes/codeprocedurepenale.pdf '
                     '(check only).'}],
        'laws': laws,
        'acts': [act],
        'decisions': DECISIONS,
        'ai_use': ["Claude Code (Claude Opus 5.5) wrote Lexifina's code. No model wrote, translated or summarised legal "
                   'text; all text is extracted by code from the official PDF.'],
    }
    return part, problems


def check() -> None:
    a = parse.between(parse.text_of(CPP[0]), *CPP[1:])
    b = parse.between(parse.text_of(CODES_COPY), *CPP[1:])
    print('CPP, JO spécial 22 vs Codes en vigueur copy (promulgation formula to signature):',
          'identical' if a == b else f'DIFFERENT ({len(a)} vs {len(b)} paragraphs)')
    if a != b:
        for x, y in zip(a, b):
            if x != y:
                print('  A:', x[:200], '\n  B:', y[:200])
                break
    parse.coverage('Code de procédure pénale', *CPP)
    part, _ = build()
    print('numbering gaps:', parse.numbering(part['acts'][0]['versions'][0]['units']) or 'none')


def main() -> None:
    if '--check' in sys.argv:
        check()
        return
    part, problems = build()
    for p in problems:
        print('PROBLEM', p)
    v = part['acts'][0]['versions'][0]
    print('units', len(v['units']), 'articles', sum(k.startswith('art-') for k in v['units']))
    PART.parent.mkdir(exist_ok=True)
    tmp = PART.with_suffix('.json.tmp')
    tmp.write_text(json.dumps(part, ensure_ascii=False, indent=1) + '\n', encoding='utf-8', newline='\n')
    if '--dry' not in sys.argv:
        os.replace(tmp, PART)


if __name__ == '__main__':
    main()
