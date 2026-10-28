# How this repository was made (Mali)

This file is written by the build on 2026-10-28, the day the source data was retrieved. Everything below is enough to rebuild this repository hash for hash.

## Sources

| Source | Address | Retrieved | Requests | Licence |
| --- | --- | --- | ---: | --- |
| Journal officiel de la République du Mali (Secrétariat général du Gouvernement) | <https://sgg-mali.ml/fr/journal-officiel/le-journal-officiel.html> | 2026-10-28 | 809 | Official legal texts published by the Government of Mali; sgg-mali.ml states no licence and its robots.txt disallows nothing. |

Every response is cached by the sha256 of its URL, and the table above lists every source with its retrieval date. Lexifina keeps its fetch scripts privately; `tools/parse.py` reads only the cache and writes `corpus.json`, so the same cache always gives the same corpus.

## What is in it

| Act | Title | Versions | Span |
| --- | --- | ---: | --- |
| `constitution` | Constitution de la République du Mali (2023) | 1 | 2023-07-22 to 2023-07-22 |
| `donnees-personnelles` | Loi n°2013-015 du 21 mai 2013 portant protection des données à caractère personnel en République du Mali | 2 | 2013-06-28 to 2017-12-29 |
| `code-penal` | Code pénal (Loi n°2024-027 du 13 décembre 2024) | 1 | 2024-12-13 to 2024-12-13 |

The build made 4 commits:

| Commits | Kind |
| ---: | --- |
| 3 | first version of an act |
| 1 | one law on its in-force day |
| 0 | changes no amendment note explains, credited to the publisher |

Other counts:
- 0 commits on the branch `futur`: laws not yet in force on 2026-10-28.
- 0 commits dated 1 January 1970: in force before 1970, with the real day in their `In-force` trailer.
- 4 laws in the record.
- 8 tags.

## Dates

Each commit is dated at noon (Africa/Bamako) on the day the change took effect. The other dates, enacted and published, are trailers.

When a law gives no date of its own, the default rule applies: Constitution du 22 juillet 2023, art. 116: « Les lois et les règlements sont publiés au Journal officiel. » No general delay is set; a law without its own commencement clause is dated from its Journal officiel issue. https://sgg-mali.ml/JO/2023/mali-jo-2023-13-sp-3.pdf

## Commands, in order

```sh
# fill the cache from the sources listed above (network; Lexifina's fetch scripts are kept privately)
python -X utf8 tools/parse.py                  # cache -> corpus.json (no network)
python -X utf8 tools/build.py <folder> --repo <empty folder> --docs-date 2026-10-28
python -X utf8 tools/check_repo.py <repo> --corpus <folder>/corpus.json --write
python -X utf8 tools/build.py <folder> --repo <another empty folder> --docs-date 2026-10-28 --compare <repo>
```

In the main Lexifina repository these files live as follows:
- `fetch.py`, `parse.py` and `repo/`: in `scripts/mali-law/`.
- `build.py`, `check_repo.py` (`check.py` there) and `on.py`: in `scripts/gitlaw_common/`, with the corpus format in `SCHEMA.md`.

## Exact inputs

- `corpus.json` sha256 `691c6dac639f49499251ca0fdd9852149836cfcc2221ae8c8aeca6d43981692b` (1052170 bytes)
- Script blob hashes (`git hash-object`):

| Script | Blob |
| --- | --- |
| build.py | `2bfc4ac9df193a7be844556d7f69cdb9d93ec3f2` |
| check.py | `cd346c7ff9996d450240e3bab52bcae03b2bc865` |
| on.py | `644a6c0857fbcc72562032b58d57aa113fee0641` |
| fetch.py | `307ccf7c81bbd847179fa72ebbdc0c5cb38e55a3` |
| parse.py | `a1d2c3b8045f46f2d39fe6dcfaca5aa6fe35024c` |

- Tools:
  - Python 3.14.0
  - git version 2.52.0.windows.1
  - curl 8.21.0 (Windows) libcurl/8.21.0 Schannel zlib/1.3.2 WinIDN WinLDAP

## Checks

4 versions of 3 acts read back from git on the day each took effect and on the day before: 0 mismatches. Trailers: 0 commits whose trailers git cannot parse. Health: 0 merge commits on main, 0 commit dates that go backwards, 0 commits dated after the build.

Not yet run for this build.

These results are from the check run on the build before this one, from the same corpus.

## Decisions made by hand

- Source: the Journal officiel de la République du Mali as published by the Secrétariat général du Gouvernement (sgg-mali.ml), one PDF per issue with a text layer. No OCR was used; every text came from the text layer.
- Dates: no Malian text we read sets a general delay between publication and entry into force; the 2023 Constitution (art. 116) requires laws to be published in the Journal officiel. Each version is dated by the date printed on the Journal officiel issue that published it, unless the law fixes its own date. None of the three acts does.
- Constitution: dated 22 July 2023, the day the Décret n°2023-0401/PT-RM promulgated it and the day of the Journal officiel spécial n°13 that printed it (art. 191 ties promulgation to the referendum of 18 June 2023; Arrêt n°2023-08/CC-Réf of 21 July 2023 proclaimed the result). It was printed again in Journal officiel n°20 of 4 August 2023 (p. 790); parse.py --check compares the two.
- Constitution and Code pénal: every Journal officiel issue from 22 July 2023 to 20 October 2026 listed on sgg-mali.ml (165 issues) was searched for a revision of the Constitution or an amendment of Loi n°2024-027; none was found. Two files listed as JO n°2024-32 (8 September 2024, mali-jo-2024-32-php-2.pdf, 517 bytes; 19 September 2024, mali-jo-2024-32-php00-2.pdf, empty) are not valid PDFs on the site, so they could not be searched; both predate the Code pénal, but a change to the Constitution or to Loi n°2013-015 printed only there would be missed.
- Code pénal: the SGG "Codes en vigueur" page (retrieved 2026-10-28) links codes/codepenal.pdf, which carries the same Journal officiel spécial n°21 of 13 December 2024; parse.py --check confirms the two give identical text, so today's text is the text as enacted.
- Code pénal: art. 702-1 repeals "toutes dispositions antérieures contraires" and Loi n°01-079 du 20 août 2001 (the former Code pénal). Implied repeals of other laws are not applied to any text in this repository.
- Code pénal: the official text numbers articles Livre-Titre-Chapitre, then article, so Livre V Titre XI (activités pastorales) and Titre XII (mines) print 511-1, 511-2 and 512-1 to 512-9, numbers that Livre V Titre I (cybercriminalité), Chapitres 1 and 2, also uses. Both are kept: each such article is keyed and labelled with its Titre (art-0511-001-titre-i, "Article 511-1 (Titre I)"; art-0511-001-titre-xi, "Article 511-1 (Titre XI)").
- Code pénal: some article headings are printed irregularly and are read as articles: "Articles" (plural) for arts. 313-1, 314-1, 314-2, 314-5, 314-6, 315-1 and 315-2, "Article : 551-7", "Article702-1", and a space after the hyphen in arts. 321-54, 423-16, 512-9, 552-17 and 561-1. Their labels are normalised to "Article N-M"; the text is unchanged.
- Code pénal: the code reproduces earlier laws and cites each one in a bracketed note ("[Loi n°… ]") under the heading it concerns. Notes standing alone are kept in the plan file, in place; a note printed inside an article (arts. 131-5, 242-11, 242-28, 242-29, 242-31 to 242-33) stays in that article. One unnumbered paragraph (the opening sentence of Titre XII, Chapitre unique) is kept in the plan file too. The annexed table of contents ("ANNEXE, TABLE DES MATIERES", after the signature) is left out.
- Loi n°2013-015: every Journal officiel issue listed on sgg-mali.ml from 28 June 2013 to 20 October 2026 was searched for laws modifying it. The only one is Loi n°2017-070 of 18 December 2017 (Journal officiel n°53, 29 December 2017), which replaces articles 21, 25, 36, 42 and 49 in full; it is applied as printed. Two issues in the listing return 404 (JO n°2020-23 of 25 September 2020, mali-jo-2020-23.pdf; JO n°2021-04 of 29 January 2021, mali-jo-2021-04-3.pdf) and could not be searched, nor could the two invalid September 2024 files.
- Loi n°2017-070 art. 2 also repeals "toutes dispositions antérieures contraires" of Loi n°2013-015 without naming any; no further change is made for it.
- Paragraphs are rebuilt from the PDF layout: a line that stops short of the column edge and ends with . ; : ! ? » or ] closes a paragraph; a line beginning "Article N :", a structural heading or "[" always opens one, and so does an enumerated item ("1°)", "a)", "-") after a line ending ; : or .; a block more than 1.5 line spacings below the previous line in the same column opens one (table rows); otherwise a block that starts after a full-width line without final punctuation continues it (page and column breaks). A hyphen at a line end is dropped only when the unhyphenated word occurs elsewhere in the same issue and the hyphenated form does not.
- Typesetting is normalised once: no-break spaces become spaces, straight and curly apostrophes become ’, guillemets get one inner space, em dashes become en dashes.
- Structural headings (Livre, Titre, Chapitre, Section, Paragraphe, and the Code pénal's numbered sub-headings such as "1°) Des résultats du test de dépistage") are kept in one "plan" file per act, each followed by the first article under it; articles are one file each. Signatures and the promulgation formula are left out. A heading misprinted in the text layer (Loi n°2013-015: "SECTIQN 3") is kept as printed.
- Unit keys: art-NNN for single numbers; the Code pénal's two-part numbers (Livre-Titre-Chapitre, then article) become art-NNNN-NNN, zero-padded.
- Verification (parse.py --check): for each act, every character of the text layer from the promulgation formula to the signature (spaces and line-end hyphens aside) is found in exactly one unit, in the order printed; the two printings of the Constitution give identical units; the Code pénal from the Journal officiel and from the Codes en vigueur copy give identical text.

## What AI did and did not do

The fetch, parse and check scripts were written by Claude Code running Claude Opus 5.5 (`claude-opus-5-5`) under Lexifina's direction.

No model wrote, translated or corrected legal text. No model runs at build time. Every word of law in this repository comes from the official sources above, through code that anyone can rerun.

The commit messages are written by `build.py` from the source data.

Model use at data-build time:
- Claude Code (Claude Opus 5.5, claude-opus-5-5) wrote fetch.py, jo_index.py, scan.py and parse.py and chose the sources. No model wrote, translated or summarised legal text; all text is extracted by code from the official PDFs.
