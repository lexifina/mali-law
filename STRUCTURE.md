# Structure du dépôt / Repository layout

Un dossier par texte, un fichier par article. / One folder per text, one file per article.

| Dossier | Contenu |
| --- | --- |
| `constitution/` | La Constitution du 22 juillet 2023 : `preambule.md`, `plan.md` (intitulés), `art-NNN.md` |
| `codes/<code>/` | Les codes : `codes/code-penal/`, `codes/code-de-procedure-penale/` (2024), `codes/code-des-personnes-et-de-la-famille/` (2011), `codes/code-du-travail/`, `codes/code-de-procedure-civile-commerciale-et-sociale/` (versions consolidées des « Codes en vigueur ») … Une nouvelle loi instituant le même code est une nouvelle version du même dossier. Un code de plus de 990 articles est rangé par Livre (`livre-1/`, `livre-preliminaire/` …), `plan.md` et `README.md` restant à la racine du code. |
| `lois/<année>/<numéro>-<objet>/` | Les autres lois, l’année étant celle de la signature (`lois/2017/2017-061-portant-creation-de-la-direction-nationale-de-l/`) |
| `ordonnances/<année>/<numéro>-<objet>/` | Les ordonnances |
| `decrets/<année>/<numéro>-<objet>/` | Les décrets réglementaires (sans les actes individuels : nominations, promotions, permis, agréments, approbations de marchés) ; les décrets du Premier ministre (`/PM-RM`), numérotés à part, portent `-pm` après leur numéro |
| `arretes/<année>/<numéro>-<autorité>-<objet>/` | Les arrêtés réglementaires publiés au Journal officiel |
| `corpus.json` | La liste des textes ajoutés depuis le Journal officiel (`ml/national/acts`) |

Dans chaque dossier de texte / In each text folder:

- `README.md` : intitulé, numéro du Journal officiel et URL du PDF, date de signature, date d’entrée en vigueur et sa justification ;
- `visas.md` : l’en-tête, les visas et la formule de promulgation ;
- `art-NNN.md` (`art-012-bis.md`, `art-unique.md`) : un article ; `# Article N` puis le texte, un alinéa par ligne ;
- `plan.md` : les intitulés (Livre, Titre, Chapitre, Section), chacun suivi du premier article qu’il contient ;
- `signatures.md` : la formule finale et les signatures ; `annexes.md` : les annexes imprimées après les signatures ;
- `texte-integral.md` : le texte entier, quand aucun article n’a pu être repéré.

Numéros / Numbers: `<année sur quatre chiffres>-<n sur trois chiffres au moins>` (`2005-215`, `2026-026`).

Dates : chaque commit est daté à midi (Africa/Bamako, UTC) du jour d’entrée en vigueur : le jour du numéro du Journal
officiel qui a publié le texte, sauf si le texte fixe lui-même sa date (dès sa signature, ou une date donnée) ;
trailers `Law`, `Kind`, `Enacted`, `Published`, `In-force`, `In-force-basis`, `Source`, `Text-layer`, `Version`, et
`Source-status: secondary copy (…)` pour une copie qui n’est pas celle du Journal officiel.

Each commit is dated at noon (Africa/Bamako, UTC) on the day the text took effect: the day of the Journal officiel issue
that printed it, unless the text sets its own date (on signature, or a stated day).
