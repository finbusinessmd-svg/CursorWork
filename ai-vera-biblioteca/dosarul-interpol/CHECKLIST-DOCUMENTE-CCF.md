# Checklist documente — Dosar Interpol / Red Notice (draft din discuție)

> Status: **PROPUNERE** din masa rotundă (Tur 2). Nu e încă inventar pe documente reale.
> Forum: **CCF** (Commission for the Control of INTERPOL’s Files), portal online.
> Limbi: EN / FR / ES / AR (recomandat EN pentru dosarul Vera dacă echipa lucrează bilingv).

## Regula Bibliotecii (convenit în discuție)

Pentru fiecare act important:

```
PDF/  SENTINTA-XXX01-2014-05-12.pdf     ← scan / original, semnături vizibile
MD/   SENTINTA-XXX01-2014-05-12.md      ← text căutabil + metadate
```

Metadate minime în MD:

```yaml
id: SENTINTA-XXX01
tip: sentinta
data: YYYY-MM-DD
instanta: ...
dosar_nr: ...
limba: ro
pdf: ../PDF/SENTINTA-XXX01-....pdf
roluri: [Alexandru, Irina]   # cine îl folosește prioritar
pentru_ccf: da|nu|poate
status_ocr: ok|partial|lipsă
```

---

## A. Pachet formal CCF (obligatoriu pentru admisibilitate)

| # | Document | Format | Status | Note |
|---|----------|--------|--------|------|
| A1 | Pașaport / buletin Vera (copie) | PDF | LIPSĂ | identificare solicitant |
| A2 | Date contact + adresă corespondență | MD | LIPSĂ | |
| A3 | Împuternicire / power of attorney (dacă depune reprezentant) | PDF+MD | LIPSĂ | notarială dacă e cerută |
| A4 | Declarație semnată a solicitantului | PDF | LIPSĂ | |
| A5 | Cerere: access și/sau correction/deletion | EN (PDF/DOCX) | LIPSĂ | prin portal CCF |
| A6 | Summary of arguments (max ~10 pagini — verificare reguli curente) | EN | LIPSĂ | Alexandru |
| A7 | Listă anexe (numerotate, max ~20 — verificare reguli curente) | MD | LIPSĂ | |
| A8 | Identificatori Interpol (nr. Red Notice, Diffusion, țara sursă, date) | MD | PARȚIAL | Țară sursă: **Moldova** (spus de Robert). Nr. Red Notice: **necunoscut** → cerere access CCF + căutare în acte naționale |

## B. Acte naționale pe fond (prioritate maximă pentru Red Notice)

| # | Document | De ce | Status |
|---|----------|-------|--------|
| B1 | Ordonanță / demers prin care s-a cerut Red Notice / cooperare | legătură NCB–Interpol | LIPSĂ |
| B2 | Mandat de arestare / ordonanță de urmărire | baza notice | LIPSĂ |
| B3 | Învinuire / rechizitoriu / încadrare juridică | ce acuzație circulă | LIPSĂ |
| B4 | **Sentințe** (toate gradele) — ex. Sentința Nr. XXX01 | fond + procedură | LIPSĂ |
| B5 | Decizii apel / recurs / casare | stare finală | LIPSĂ |
| B6 | Dovezi că procedura e în curs / suspendată / închisă | actualitate date Interpol | LIPSĂ |
| B7 | Acte de citare / judecată în lipsă (dacă e cazul) | art. 2 / fair trial | LIPSĂ |
| B8 | Plângeri penale / civile depuse de Vera (dacă există) | context victimă vs. „făptuitor” | LIPSĂ |

## C. Linie „dispută privată / comercială / raider” (RPD)

| # | Document | De ce | Status |
|---|----------|-------|--------|
| C1 | Contracte, cesiuni, vânzări Ialtop | arată natură comercială | LIPSĂ |
| C2 | Transfer credite Ialtop → Energomigrup | operațiuni Movilă | LIPSĂ |
| C3 | Acte cu Mihailov Mihail / alți cumpărători | terți | LIPSĂ |
| C4 | Extrase registru companii (administratori, asociați) | cine controla | LIPSĂ |
| C5 | Litigii civile/patrimoniale paralele | „penalizarea” unui conflict privat | LIPSĂ |

## D. Linie contradicții / calitate date (Irina → Alexandru)

| # | Document | De ce | Status |
|---|----------|-------|--------|
| D1 | Toate declarațiile / audierile Movilă (datate) | contradicții în timp | LIPSĂ |
| D2 | Marturii Vera (datate, complete) | versiunea ei + coerență | LIPSĂ |
| D3 | Alte marturii / PV | coroborare | LIPSĂ |
| D4 | Acte medicale invocate de Movilă (dacă există în dosar) | „nu vedea” | LIPSĂ |

## E. Linie drepturile omului / politică / abuz (art. 2 / art. 3) — doar cu probe

| # | Document | De ce | Status |
|---|----------|-------|--------|
| E1 | Hotărâri care notează abuz / încălcări | individualizat | LIPSĂ |
| E2 | Refuzuri de extrădare (dacă există, orice țară) | foarte puternic la CCF | LIPSĂ |
| E3 | Rapoarte / decizii instituții (CEDO, ONU, etc.) **legate de caz**, nu generice | predominance | LIPSĂ |
| E4 | Dovezi de hărțuire procedurală, durata excesivă (~14 ani) | art. 2 / proporționalitate | LIPSĂ |

## F. Măsuri provizorii (opțional, urgent)

| # | Document | De ce | Status |
|---|----------|-------|--------|
| F1 | Cerere provisional measures (blocking) | blochează accesul la date pe durata examinării | LIPSĂ |
| F2 | Dovezi de urgență (risc arest la frontieră, călătorii, etc.) | justificare | LIPSĂ |

---

## Indexare Bibliotecă pe roluri (propunere)

```
biblioteca/
  00-index/
  01-identitate-vera/          → A*
  02-interpol-ccf/             → A*, F*
  03-penal-national/           → B*
  04-civil-comercial-raider/   → C*
  05-marturii-vera/            → D2
  06-marturii-movila/          → D1
  07-alti-martori/             → D3
  08-retele-actori/            → Mihai
  09-cedo-international/       → E*
  10-media-open-source/        → Nora (secundar)
  _pdf/                        → scanuri
  _md/                         → texte
```

Sau, alternativ, **același act** apare în index pe tag-uri: `tip:` `actor:` `pentru_ccf:` `rol:`.

## Ce cerem de la Robert acum (minim ca să începem lucrul)

1. Unde e corpusul real (alt repo / folder / Drive)?
2. Există număr Red Notice / țara sursă (Moldova NCB?) / copie a notice sau informare?
3. Top 10 acte pe care le poate încărca **prima** (PDF+MD), în ordine: B4, B2, B3, D1, D2, C1–C3, A1.
