# Active-ready — the starting line

_Measured 2026-11-27 by `pipeline/readiness.py` (standard AR-1); no model calls. The goal: many thousands._

## 45 profiles are active-ready

Active-ready means the machine has gathered and source-checked everything an AI teaching service needs to write the lesson for that dance. It is not human-reviewed, rights-cleared or platform-tested: that comes after this line (ACTIVE_PROFILE_STANDARD.md).

Since 24 November 2026 a reference clip counts as the licensed picture only when its list was read, the clip shows the dance and it declares a licence (`pipeline/footage.py`). On that day the count went from 41 to 31: twelve profiles had been counted on a clip nobody had read, and they wait until a licensed picture is found (`pipeline/pictures.py` looks for one every night).

| Step | Profiles |
|---|---:|
| In the atlas | 1,415 |
| Researched from sources (in the atlas) | 838 |
| Published (passed every gate) | 697 |
| **Active-ready** | **45** |
| One item short | 73 |
| Two items short | 68 |
| Three to five short | 164 |
| Story-ready, teaching withheld (sacred or restricted) | 74 |

Video studied so far: 406 lessons, 442 performances.

Pace over the last two weeks: +25 active-ready a week.
Pace over the last two weeks: +215 published a week.

## What holds profiles back most

| Missing item | Profiles |
|---|---:|
| the steps with their counts | 394 |
| a lesson or performance the machine studied, with timestamps | 253 |
| what to avoid: common mistakes or safety | 232 |
| a hero video that passed the vision check | 200 |
| a licensed picture or licensed footage | 171 |
| two or more signature moves | 171 |
| tempo, meter or the teacher's count | 156 |
| posture | 147 |
| arms and hands | 114 |
| ordered basic steps or a lesson ladder | 113 |
| the instruments and what the music sounds like | 97 |
| origins, meaning and occasions, dress and setting — written from sources | 87 |
| formation and use of space | 56 |
| known to be living, revived or historical | 30 |

## Closest to the line

- **Abbots Bromley Horn Dance** — needs: the steps with their counts
- **Aerial dance** — needs: the steps with their counts
- **Agwara** — needs: the steps with their counts
- **Alegrías** — needs: the steps with their counts
- **Ballos** — needs: what to avoid: common mistakes or safety
- **Barn dance** — needs: what to avoid: common mistakes or safety
- **Bugg** — needs: ordered basic steps or a lesson ladder
- **Bump** — needs: a licensed picture or licensed footage
- **Bush dance** — needs: the steps with their counts
- **Cariñosa** — needs: what to avoid: common mistakes or safety
- **Carolina shag** — needs: a licensed picture or licensed footage
- **Charleston Stroll** — needs: a lesson or performance the machine studied, with timestamps
- **Chinese square dancing** — needs: the steps with their counts
- **Choobazi** — needs: the steps with their counts
- **Chunaengjeon** — needs: the steps with their counts
- **Condong** — needs: the steps with their counts
- **Courante** — needs: known to be living, revived or historical
- **Dance of Osman Taka** — needs: the steps with their counts
- **Dikir barat** — needs: the steps with their counts
- **Dutty Wine** — needs: a licensed picture or licensed footage
- **Eccentric dance** — needs: the steps with their counts
- **electric boogaloo** — needs: known to be living, revived or historical
- **Electric Slide** — needs: origins, meaning and occasions, dress and setting — written from sources
- **Fancy Shawl Dance** — needs: what to avoid: common mistakes or safety
- **Farruca** — needs: a licensed picture or licensed footage
- **Fouetté** — needs: the instruments and what the music sounds like
- **Fusion Dance** — needs: what to avoid: common mistakes or safety
- **Garrotín** — needs: what to avoid: common mistakes or safety
- **Geommu** — needs: the steps with their counts
- **Gloving** — needs: the steps with their counts
- **Gombey** — needs: the steps with their counts
- **Grotesque dance** — needs: the steps with their counts
- **Hiplet** — needs: the steps with their counts
- **Huaylas (Huaylarsh)** — needs: a licensed picture or licensed footage
- **Improv Tribal Style Belly Dance** — needs: the steps with their counts
- **J-Setting** — needs: the steps with their counts
- **Jacking** — needs: a licensed picture or licensed footage
- **Jota Aragonesa** — needs: known to be living, revived or historical
- **Kebyar duduk** — needs: the steps with their counts
- **Kikkli** — needs: the steps with their counts

## The fifteen items

1. passed every quality gate and the independent judge
2. origins, meaning and occasions, dress and setting — written from sources
3. known to be living, revived or historical
4. the steps with their counts
5. posture
6. arms and hands
7. formation and use of space
8. two or more signature moves
9. tempo, meter or the teacher's count
10. the instruments and what the music sounds like
11. ordered basic steps or a lesson ladder
12. what to avoid: common mistakes or safety
13. a hero video that passed the vision check
14. a lesson or performance the machine studied, with timestamps
15. a licensed picture or licensed footage

Evidence may come from quote-checked text, from a lesson the machine studied, or (never for counts) from the dance's own performance video. `pipeline_state/active_ready.json` records which, per profile.
