# AI VERA Biblioteca — personaje & agenți

Sistem de **personaje AI** (roluri specializate) pentru Biblioteca VERA, cu focus pe **Dosarul Interpol** și pe analiza documentară a cazurilor.

## Recomandarea pe scurt

Nu pune totul într-un singur „avocat magic”. Creează **o echipă mică**, cu misiuni separate:

| # | Personaj | Ce face | De ce e separat |
|---|----------|---------|-----------------|
| 1 | **Alexandru Codreanu** — avocat senior | Strategie juridică MD + UE, drepturi omului, raider, civil/penal | Expertiză de drept, nu de investigație |
| 2 | **Irina Valeanu** — avocat-detectiv | Contradicții, minciuni în timp, timeline, probe vs. declarații | Fapte din dosar; fără teorii politice |
| 3 | **Mihai Răutu** — cartograf rețele | Judecători, procurori, avocati, scheme, legături dubioase | Risc mare de speulație — trebuie izolat |
| 4 | **Scout Nora** — agent de idei | Caută singură analogii, strategii din alte cazuri, surse | Explorare, nu verdict juridic |

**Da: personajul 3 trebuie separat de 2.**  
Detectivul de contradicții lucrează pe **probe și declarații**. Cartograful de rețele lucrează pe **legături și pattern-uri** (inclusiv politice/corupție). Amestecate, se contaminează: o contradicție reală din 2011 poate fi „împinsă” greșit spre o teorie de corupție fără dovezi.

## Cum se face corect (metoda)

1. **Rol-card** (fișier Markdown) cu: misiune, expertiză, metodă, interdicții, format de output.
2. **Bază de fapte** separată de **interpretare** (vezi `dosarul-interpol/`).
3. **Orchestrator** care decide cine răspunde (vezi `orchestrare/`).
4. **Regula de aur:** fiecare afirmație = `FAPT` / `INFERENȚĂ` / `ÎNTREBARE DESCHISĂ`, cu sursă.

## Cum le folosești în Cursor (sau alt AI)

- Copiezi conținutul din `personaje/<nume>/SYSTEM.md` în **Custom Instructions** / Agent prompt.
- Atașezi fișierele din `dosarul-interpol/` ca context.
- Pentru task-uri mixte, începi cu `orchestrare/ROUTER.md`.

## Structură

```
ai-vera-biblioteca/
  README.md                 ← acest fișier
  CUM-SE-CREEAZA.md         ← metodă pas cu pas
  personaje/
    01-avocat-senior/
    02-avocat-detectiv/
    03-cartograf-retele/
    04-scout-idei/
  dosarul-interpol/
  orchestrare/
```
