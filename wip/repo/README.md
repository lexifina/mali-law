# Mali: law history in git

The law of Mali as a git history: one file per article, one commit per law on the day it took effect, and the law that made each change as the commit's author. `git blame` names the law behind every paragraph; `git log` lists every change to an article; `tools/on.py` gives the text in force on any day.

It follows the shared design of [lexifina/global-law](https://github.com/lexifina/global-law), which places it at `ml/`. Every text is read from the *Journal officiel de la République du Mali* as the Secrétariat général du Gouvernement publishes it on [sgg-mali.ml](https://sgg-mali.ml): one PDF per issue, with a text layer. Mali publishes no consolidated texts with dated versions, so the history is rebuilt from the issues that printed each act and each amendment.

**What is in it**

| Folder | Act | Versions | History | Articles |
| --- | --- | ---: | --- | ---: |
| `constitution/` | Constitution de la République du Mali (2023) | 1 | 2023-07-22 | 191, plus the preamble |
| `donnees-personnelles/` | Loi n°2013-015 du 21 mai 2013 portant protection des données à caractère personnel | 2 | 2013-06-28 to 2017-12-29 | 69 |
| `code-penal/` | Code pénal (Loi n°2024-027 du 13 décembre 2024) | 1 | 2024-12-13 | 1,125 |

- **Constitution.** The Constitution adopted by the referendum of 18 June 2023 and promulgated on 22 July 2023, as printed in Journal officiel spécial n°13 of that day. No revision appears in any issue up to 20 October 2026.
- **Loi n°2013-015** (personal data). The law as printed in Journal officiel n°26 of 28 June 2013, then Loi n°2017-070 of 18 December 2017 (Journal officiel n°53, 29 December 2017), which replaces articles 21, 25, 36, 42 and 49 in full. It is the only amendment in any issue from 2013 to 20 October 2026.
- **Code pénal.** Loi n°2024-027 as printed in Journal officiel spécial n°21 of 13 December 2024. It replaced the Code pénal of 2001 (Loi n°01-079). No amendment appears in any issue up to 20 October 2026.

Each act's folder has a `plan.md` with its Livres, Titres, Chapitres and Sections, each followed by the first article under it. Each folder's `README.md` lists every article, how often it changed and when.

## A lawyer's questions as git commands

| Question | Command |
| --- | --- |
| What did art. 21 of the data law say on 2015-01-01? | `python tools/on.py 2015-01-01 donnees-personnelles art-021` |
| The same, with raw git (bash) | `git show $(git rev-list -1 --before="2015-01-01T23:59:59Z" main -- donnees-personnelles/art-021.md):donnees-personnelles/art-021.md` |
| The same, in PowerShell | `$r = git rev-list -1 --before="2015-01-01T23:59:59Z" main -- donnees-personnelles/art-021.md; git show "$($r):donnees-personnelles/art-021.md"` |
| Which law wrote each line? | `git blame donnees-personnelles/art-021.md` |
| Every change, word by word | `git log -p --word-diff donnees-personnelles/art-021.md` |
| Every law in the record, in order | `git log --reverse --format="%ad %an" --date=short main` |
| Everything one law changed | `git show law/loi-2017-070` (tags `law/<key>` mark each law's commit) |
| The whole act on a date | `python tools/on.py 2026-01-01 constitution` |

After a rebuild, refresh tags with `git fetch --force --tags`: a plain fetch keeps stale tags.

## Dates

- Each commit is dated at **noon, Africa/Bamako, on the day the change took effect**. The day is also in the `In-force:` trailer, which the tools read.
- No Malian text read for this build sets a general delay between publication and entry into force; the Constitution (art. 116) requires laws to be published in the Journal officiel. Each version is therefore **dated by the Journal officiel issue that printed it**, unless the law fixes its own date. None of these laws does.
- The Constitution is dated 22 July 2023: the day of its promulgation decree (Décret n°2023-0401/PT-RM) and of the Journal officiel spécial n°13 that printed it.
- `--before="YYYY-MM-DD"` alone uses your clock's time of day, so a law that took effect that day may be missed before noon. Use `T23:59:59Z` as above, or the tool.

## How it is checked

- **Every article, without gaps.** For each act, every paragraph of the text layer from the promulgation formula to the signature is in exactly one file, in the order printed, and every character of that text layer is there (spaces and line-end hyphens aside). Article numbers run without gaps in every series. `tools/parse.py --check` prints these results.
- **Second printings.** The Constitution was printed again in Journal officiel n°20 of 4 August 2023: the two give identical files. The Code pénal on the SGG's "Codes en vigueur" page (`codes/codepenal.pdf`) gives text identical to the Journal officiel.
- **Today's text.** Every Journal officiel issue listed on sgg-mali.ml up to 20 October 2026 was searched for amendments to the three acts (`tools/scan.py`); the only one found is Loi n°2017-070.
- Every version is read back from git on the day it took effect and on the day before (`tools/check_repo.py`); both must match `corpus.json`. Results are in `REPRODUCE.md`.
- The repository is rebuilt from the same data a second time and must give identical hashes.

## What "author" means

The author of a commit is the law that made the change, with an e-mail address that cannot exist, so `git blame` and `git log --author` name laws. The committer is always Lexifina.

- **Credits come only from the amending law itself.** Loi n°2017-070, art. 1er, names the five articles it replaces. Anything no law explains would be committed by the publisher and labelled "unexplained"; there is none.
- **The first commit** of each act is the act as enacted, credited to the act itself.
- Blame credits whole lines (one paragraph per line). Use `git log -p --word-diff` to see exactly which words each change made.

## What it does not show

- **Issues that could not be read.** Two issues in the sgg-mali.ml listing return 404: **JO n°2020-23 of 25 September 2020** (`mali-jo-2020-23.pdf`) and **JO n°2021-04 of 29 January 2021** (`mali-jo-2021-04-3.pdf`). Two files listed as **JO n°2024-32** (8 and 19 September 2024: `mali-jo-2024-32-php-2.pdf`, 517 bytes, and `mali-jo-2024-32-php00-2.pdf`, empty) are not valid PDFs. None could be searched, so an amendment to Loi n°2013-015 printed only in one of them, or to the Constitution printed only in the 2024 files, would be missed. All four predate the Code pénal.
- **Earlier law.** The Constitution of 25 February 1992 and the Code pénal of 2001 are not in the history: each act starts with the text as enacted.
- **Implied repeals.** Loi n°2017-070 and the Code pénal (art. 702-1) repeal "toutes dispositions antérieures contraires"; such repeals name no text and are not applied.
- **Scans.** Only text layers are read, and no OCR is used. All the issues used here have a text layer.
- **Signatures and promulgation formulas** are left out, and so is the table of contents annexed to the Code pénal.

## Notes on the Code pénal

- Its articles are numbered Livre-Titre-Chapitre, then article, so Livre V, Titres XI (activités pastorales) and XII (mines) print **511-1, 511-2 and 512-1 to 512-9**, numbers that Livre V, Titre I (cybercriminalité) also uses. Both are kept, each keyed and labelled with its Titre: `art-0511-001-titre-i.md` ("Article 511-1 (Titre I)") and `art-0511-001-titre-xi.md` ("Article 511-1 (Titre XI)").
- The code reproduces earlier laws and cites each in a bracketed note, such as "[Loi n°2019- 056 du 05 décembre 2019 portant répression de la cybercriminalité]". Notes under a heading are in `plan.md`, in place; notes printed inside an article stay in it. One unnumbered sentence opening Titre XII is in `plan.md` too.
- Some article headings are printed irregularly ("Articles 313-1", "Article : 551-7", "Article702-1"); their labels are normalised, the text is not.

## How it is built

`tools/fetch.py` downloads the Journal officiel listing and issues with curl, at no more than three requests a second, caching each by the sha256 of its URL; `tools/jo_index.py` reads the listing and `tools/scan.py` searches every cached issue. `tools/parse.py` reads only that cache: it rebuilds paragraphs from the PDF layout with PyMuPDF, splits each act into one file per article, normalises spacing, quotes and dashes, and writes `corpus.json`; the shared builder `tools/build.py` turns that into the commits. `REPRODUCE.md` lists every source, command, tool version and decision, and the result of the hash-for-hash rebuild.

## Sources

| Source | What it gives | Used for |
| --- | --- | --- |
| [Journal officiel de la République du Mali](https://sgg-mali.ml/fr/journal-officiel/le-journal-officiel.html) (Secrétariat général du Gouvernement) | Every issue from 1997 to 2026 as a PDF with a text layer; issues from May 2013 to October 2026 were read | Every text, and the search for amendments |
| ["Codes en vigueur"](https://sgg-mali.ml/fr/journal-officiel/les-codes-consolides.html) (the same site) | Current codes as PDFs, among them the Code pénal (the same Journal officiel issue) | Cross-check only |

Research guides that cover every country: [GlobaLex](https://www.nyulawglobal.org/globalex/) and the [Law Library of Congress Guide to Law Online](https://www.loc.gov/research-centers/law-library-of-congress/researcher-resources/guide-to-law-online/).

## Licence

See [LICENSE](LICENSE). sgg-mali.ml states no licence. Whether Malian copyright law excludes official legislative texts from protection has not been verified, so this repository is private. Lexifina's arrangement, messages, tables and tools are CC0.

This repository is not legal advice.

## En français

Ce dépôt retrace le droit malien dans git : un fichier par article, un commit par loi au jour de son entrée en vigueur, et la loi qui a fait chaque modification comme auteur du commit. Tous les textes viennent du *Journal officiel de la République du Mali* publié par le Secrétariat général du Gouvernement sur [sgg-mali.ml](https://sgg-mali.ml), lu dans la couche texte des PDF, sans OCR.

- **Constitution du 22 juillet 2023** (Journal officiel spécial n°13) : une version ; aucune révision dans les numéros parus jusqu'au 20 octobre 2026.
- **Loi n°2013-015 du 21 mai 2013** relative aux données à caractère personnel (Journal officiel n°26 du 28 juin 2013), puis la **Loi n°2017-070 du 18 décembre 2017** (Journal officiel n°53 du 29 décembre 2017), qui remplace les articles 21, 25, 36, 42 et 49.
- **Code pénal** (Loi n°2024-027 du 13 décembre 2024, Journal officiel spécial n°21) : une version ; aucune modification jusqu'au 20 octobre 2026.

Chaque version est datée du numéro du Journal officiel qui l'a publiée, faute de délai général d'entrée en vigueur. Les numéros JO n°2020-23 (25 septembre 2020) et JO n°2021-04 (29 janvier 2021) sont introuvables sur le site (erreur 404), et les deux fichiers du JO n°2024-32 (8 et 19 septembre 2024) ne sont pas des PDF valides : ils n'ont pas pu être examinés. Dans le Code pénal, les numéros 511-1, 511-2 et 512-1 à 512-9, employés à la fois au Titre I et aux Titres XI et XII du Livre V, sont conservés deux fois, chacun avec son Titre. Ce dépôt ne constitue pas un avis juridique.
