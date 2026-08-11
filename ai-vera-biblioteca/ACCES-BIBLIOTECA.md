# ACCES Bibliotecă — unde sunt datele (clarificare pentru Robert)

## Răspuns scurt

**Nu am „furat” / mutat Biblioteca pe Cloud.**  
Agentul Cloud **nu vede** discul tău `D:\Vera 2026\Vera AI Biblioteca 2026`.

| Locație | Ce conține acum | Accesibil acestui agent Cloud? |
|---------|-----------------|--------------------------------|
| `D:\Vera 2026\Vera AI Biblioteca 2026` (PC Windows) | Baza ta reală (PDF/DOC/MD) | **NU** |
| GitHub `finbusinessmd-svg/CursorWork` | Doar `Start` + ce am creat noi (`ai-vera-biblioteca/` personaje, checklist) | **DA** |
| Agent anterior „Descriere atac raider” | Doar **narativă** din chat (fără PDF-uri Bibliotecă) | recuperat parțial aici |

## De ce s-a creat impresia că „s-au împărțit datele”

1. Tu lucrezi local pe `D:\...` (Cursor Desktop pe Windows).
2. Acest agent rulează pe un **server Linux** care clonează doar repo-ul GitHub `CursorWork`.
3. Folderul `D:\` **nu e montat** și **nu e în GitHub** → pentru noi e gol ca Bibliotecă de acte.
4. Un chat anterior pe web („Descriere atac raider”) a discutat cazul familiei, dar **nu a scris fișiere** și **nu a citit** `D:\`.

## Cum unim totul (alege 1 variantă)

### Varianta A — recomandată pentru discuție + acte (Desktop)
Deschide în Cursor Desktop folderul:
`D:\Vera 2026\Vera AI Biblioteca 2026`
și continuă chat-ul **local** (nu Cloud Agent), sau adaugă acest folder în workspace multi-root.

### Varianta B — pentru Cloud Agent
1. Creează un repo GitHub privat `Vera-AI-Biblioteca-2026` (sau similar).
2. Încarcă acolo Biblioteca (sau un subset prioritar: sentințe, mandate, marturii).
3. Adaugă repo-ul în Cloud Environment Cursor, **sau** cere unui agent să-l cloneze.
4. Abia atunci putem „verifica în Bibliotecă”.

### Varianta C — pachet minim acum
Copiază în `CursorWork/ai-vera-biblioteca/corpus/` (sau atașează în chat) doar Top 10 PDF-uri:
- mandat / ordonanță urmărire
- 2–3 sentințe
- 2 declarații Movilă
- 2 marturii Vera
- orice hârtie care menționează Interpol / urmărire internațională

## Ce am salvat local din Cloud (unificare parțială)

- Narativa din agentul „Descriere atac raider” → `dosarul-interpol/NARATIVA-RECUPERATA-RAIDER.md`
- Confirmări din Tur 3 → mai jos în discuții + checklist actualizat (Moldova = țara sursă; fără nr. Red Notice)
