# How this repository was made (Mali)

This file is written by the build on 2026-10-29, the day the source data was retrieved.

## Sources

| Source | Address | Retrieved | Licence |
| --- | --- | --- | --- |
| Journal officiel de la République du Mali (Secrétariat général du Gouvernement) | <https://sgg-mali.ml/fr/journal-officiel/le-journal-officiel.html> | 2026-10-28 | Official legal texts published by the Government of Mali; sgg-mali.ml states no licence. |
| Journal officiel de la République du Mali (Secrétariat général du Gouvernement): Code de procédure pénale | <https://sgg-mali.ml/fr/journal-officiel/les-codes-consolides.html> | 2026-10-29 | Official legal texts published by the Government of Mali; sgg-mali.ml states no licence. |

Every word of law in this repository comes from these sources. Lexifina reads them and records each act's dated versions, and the laws that made each change, in one corpus file. This repository is built from that file.

## What is in it

| Act | Title | Versions | Span |
| --- | --- | ---: | --- |
| `constitution` | Constitution de la République du Mali (2023) | 1 | 2023-07-22 to 2023-07-22 |
| `donnees-personnelles` | Loi n°2013-015 du 21 mai 2013 portant protection des données à caractère personnel en République du Mali | 2 | 2013-06-28 to 2017-12-29 |
| `code-penal` | Code pénal (Loi n°2024-027 du 13 décembre 2024) | 1 | 2024-12-13 to 2024-12-13 |
| `code-procedure-penale` | Code de procédure pénale (Loi n°2024-028 du 13 décembre 2024) | 1 | 2024-12-13 to 2024-12-13 |

The build made 5 commits:

| Commits | Kind |
| ---: | --- |
| 4 | first version of an act |
| 1 | one law on its in-force day |
| 0 | changes no amendment note explains, credited to the publisher |

Other counts:
- 0 commits on the branch `futur`: laws not yet in force on 2026-10-29.
- 0 commits dated 1 January 1970: in force before 1970, with the real day in their `In-force` trailer.
- 5 laws in the record.
- 10 tags.

## Dates

Each commit is dated at noon (Africa/Bamako) on the day the change took effect. The other dates, enacted and published, are trailers.

When a law gives no date of its own, the default rule applies: Constitution du 22 juillet 2023, art. 116: « Les lois et les règlements sont publiés au Journal officiel. » No general delay is set; a law without its own commencement clause is dated from its Journal officiel issue. https://sgg-mali.ml/JO/2023/mali-jo-2023-13-sp-3.pdf

## How the history is built

`tools/build.py` turns the corpus into this history in one pass: one commit per law, on the day it took effect. The same corpus always gives the same commit hashes. `tools/check_repo.py` reads every version back from git and compares it with the corpus. `tools/on.py` shows the law as it stood on any date. The corpus format is described in `tools/SCHEMA.md`.

- Corpus: sha256 `0f8644f30f2b99d9d4b04cc72267d917f14e0c4cedf2299abaa316fd983c1650` (2035688 bytes).
- Builder blob hashes (`git hash-object`): `build.py` `a4faa25af85facb64b956b372f6b528aafdd7ec1`, `check.py` `3d00541d258745461ab52b1b0cb4e1716a27a95d`, `on.py` `644a6c0857fbcc72562032b58d57aa113fee0641`.
- Python 3.12.10; git version 2.46.0.windows.1.

## Checks

5 versions of 4 acts read back from git on the day each took effect and on the day before: 0 mismatches. Trailers: 0 commits whose trailers git cannot parse. Health: 0 merge commits on main, 0 commit dates that go backwards, 0 commits dated after the build.

No second build of this corpus has been compared yet.

## Decisions made by hand

- Source: the Journal officiel de la République du Mali as published by the Secrétariat général du Gouvernement (sgg-mali.ml), one PDF per issue with a text layer. No OCR was used; every text came from the text layer.
- Dates: no Malian text we read sets a general delay between publication and entry into force; the 2023 Constitution (art. 116) requires laws to be published in the Journal officiel. Each version is dated by the date printed on the Journal officiel issue that published it, unless the law fixes its own date. None of the three acts does.
- Constitution: dated 22 July 2023, the day the Décret n°2023-0401/PT-RM promulgated it and the day of the Journal officiel spécial n°13 that printed it (art. 191 ties promulgation to the referendum of 18 June 2023; Arrêt n°2023-08/CC-Réf of 21 July 2023 proclaimed the result). It was printed again in Journal officiel n°20 of 4 August 2023 (p. 790); the two printings are compared.
- Constitution and Code pénal: every Journal officiel issue from 22 July 2023 to 20 October 2026 listed on sgg-mali.ml (165 issues) was searched for a revision of the Constitution or an amendment of Loi n°2024-027; none was found. Two files listed as JO n°2024-32 (8 September 2024, mali-jo-2024-32-php-2.pdf, 517 bytes; 19 September 2024, mali-jo-2024-32-php00-2.pdf, empty) are not valid PDFs on the site, so they could not be searched; both predate the Code pénal, but a change to the Constitution or to Loi n°2013-015 printed only there would be missed.
- Code pénal: the SGG "Codes en vigueur" page (retrieved 2026-10-28) links codes/codepenal.pdf, which carries the same Journal officiel spécial n°21 of 13 December 2024; the two give identical text, so today's text is the text as enacted.
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
- Verification: for each act, every character of the text layer from the promulgation formula to the signature (spaces and line-end hyphens aside) is found in exactly one unit, in the order printed; the two printings of the Constitution give identical units; the Code pénal from the Journal officiel and from the Codes en vigueur copy give identical text.
- Code de procédure pénale: Loi n°2024-028 du 13 décembre 2024, printed in the Journal officiel spécial n°22 of 13 December 2024 (adopted by the Conseil national de Transition on 31 October 2024). It is dated 13 December 2024, the day of promulgation and of that issue; the law sets no other date.
- Code de procédure pénale: the SGG "Codes en vigueur" page (retrieved 2026-10-29) links codes/codeprocedurepenale.pdf, which carries the same Journal officiel spécial n°22; the two give identical text, so today's text is the text as enacted.
- Code de procédure pénale: every Journal officiel issue listed on sgg-mali.ml from 13 December 2024 to the newest issue online was searched for an amendment of Loi n°2024-028; none was found (the issues that could not be read are named in the README).
- Code de procédure pénale: structural headings go to the act's "plan" file and the annexed table of contents (after the signature) is left out, as for the other acts.

## What AI did and did not do

The scripts that read the sources and build this repository were written by Claude Code running Claude Opus 5.5 (`claude-opus-5-5`) under Lexifina's direction.

No model wrote, translated or corrected legal text. No model runs at build time. Every word of law in this repository comes from the official sources above.

The commit messages are written by `build.py` from the source data.

Model use at data-build time:
- Claude Code (Claude Opus 5.5, claude-opus-5-5) wrote Lexifina's code and chose the sources. No model wrote, translated or summarised legal text; all text is extracted by code from the official PDFs.
- Claude Code (Claude Opus 5.5) wrote Lexifina's code. No model wrote, translated or summarised legal text; all text is extracted by code from the official PDF.
