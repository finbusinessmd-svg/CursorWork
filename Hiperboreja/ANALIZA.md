# Analiza site-ului hiperboreja.ru

Data arhivei: 14 august 2026. Site-ul era încă online. Hostingul și domeniul expiră a doua zi.

## Ce este site-ul

Este site-ul editurii **Гиперборея** (Hiperboreja): catalog de cărți de yoga, ezoterism, meditație și poezie, plus blog și poezii.

Autori din catalog:

- **Георгий Бореев** (Georgii Boreev / Biazyrev) — autorul principal, yoghin și poet
- **Александр Бореев** / **Александр Волков** — redactor, compilator, autor (serie «Гита Просветления», articole)
- **Андрей Явный** — o carte: «Секреты управления судьбой»

Publicul: cititori de limbă rusă. Vânzare hârtie (Poșta Rusiei) + ebook după comandă.

## Tehnologie veche (nu merită păstrată ca platformă)

| Componentă | Detaliu |
|---|---|
| CMS | Joomla 2.5 (ieșit din suport din 2014) |
| Magazin | VirtueMart |
| Articole / poezii | K2 |
| Newsletter | AcyMailing |
| Șablon | JoomlArt JA Vintas + T3 |
| Analytics | Universal Analytics `UA-45185562-1` (mort din 2023) |
| Server | nginx, PHP vechi |

Joomla 2.5 + VirtueMart nu merită mutate pe hosting nou. Sunt nesigure, greoaie și costisitoare de întreținut. Pentru un catalog de ~23 de titluri, un site static modern este suficient.

## Ce am putut salva (fără Control Panel)

Fără parolă la cPanel/Joomla admin **nu există dump MySQL**. Am salvat tot ce era public:

| Conținut | Cantitate | Unde |
|---|---|---|
| Titluri unice de cărți | 23 | `content/books/`, `archive/extracted/catalog_clean.json` |
| SKU-uri magazin (hârtie + ebook) | 46 | același catalog |
| Coperți originale | 46 imagini | `content/covers/` |
| Anotații, ISBN, an, pagini, tiraj, preț | da | markdown + JSON |
| Articole de blog | ~13 eseuri | `content/blog/` |
| Poezii (СТИХИ) | ~22 | `content/blog/` |
| Pagini despre / plată | da | `content/pages/` |
| Imagini homepage / slider | da | `content/site-images/` |
| HTML brut al paginilor publice | arhivă | `archive/raw-html.tar.gz` |
| Previzualizare catalog | 23 coperți | `preview/index.html` |

Contacte salvate:

- Telefon: `+7 903-148-53-56`
- Email: `giperboreja8@rambler.ru`
- VK: https://vk.com/club3484987

## Ce NU s-a putut salva (fără admin)

Acestea dispar odată cu hostingul, dacă firma nu le dă:

1. **Baza de date MySQL** — comenzi, clienți, parole, stoc
2. **Lista AcyMailing** — abonați la newsletter
3. **Fișierele ebook** (PDF/EPUB) — nu sunt publice; se trimiteau pe email după plată. **Nu există niciun `.pdf` pe site.**
4. **Media din `/administrator/`** — fișiere nelegate în pagini publice
5. **Logouri / șablon sursă** — doar CSS compilat T3

Dacă mai poți vorbi cu firma astăzi: cere **doar dump-ul bazei + folderul `images/` + orice PDF din `media/`**. Nu e nevoie de Joomla-ul întreg. Fără ebook-uri, noul site poate arăta catalogul, dar nu poate revinde versiunea electronică.

## Ce merită luat pe site-ul nou

**Da, nucleul noului site:**

- Identitatea editurii (nume Гиперборея, textul de bun venit, articolul «Издательство, которого нет»)
- Catalogul de 23 de titluri, cu anotații, ISBN și coperți
- Autorii (3 persoane) și seriile: Азбука йоги, За пределами пределов, Гита Просветления
- Eseurile din blog (voce editorială, nu doar vânzare)
- Poeziile — arhivă literară, pagină «Стихи»
- Contactele

**Nu merită copiat 1:1:**

- Magazinul VirtueMart (coș, TVA, variante SKU duplicate)
- Prețurile în ruble din 2014 — trebuie actualizate sau înlocuite cu «scrie-ne»
- Pagina de plată (Sberbank, ramburs Poșta Rusiei, date de card publicate pe site — risc; datele nu le repet aici)
- Șablonul JA Vintas, jQuery 1.8, MooTools, Google Analytics UA
- Newsletter-ul vechi (lista e în baza de date, pierdută)

## Propunere pentru site modern

Un site static (HTML sau Astro), 5–6 pagini:

1. Acasă — misiunea editurii + 4–6 cărți evidențiate
2. Catalog — cele 23 de titluri
3. Autori
4. Blog / eseuri
5. Poezii
6. Contact

Vânzare: la început **fără magazin**. Un formular sau email/Telegram. Magazin (Stripe, YooKassa, etc.) doar dacă încă vinzi hârtie sau ebook-uri pe care le ai pe disc.

Cost față de 120–130 €/an:

- Domeniu nou (`.org` / `.com` / `.ru`): circa 10–20 €/an
- Hosting static: **0 €** (Cloudflare Pages, Netlify, GitHub Pages)
- Dacă vrei să păstrezi `hiperboreja.ru`: mută doar domeniul la un registrar ieftin, fără pachetul lor de hosting Joomla

120–130 €/an pentru Joomla 2.5 pe un catalog mic **nu se justifică**.

## Structura arhivei (echivalentul `D:\Hiperboreja`)

În acest mediu Linux arhiva este folderul `Hiperboreja/` din repository. Descarcă ZIP-ul branch-ului și extrage-l în `D:\Hiperboreja`.

```
Hiperboreja/
  ANALIZA.md                 ← acest document
  README.md
  preview/index.html         ← deschide în browser, vezi catalogul
  content/
    books/                   ← câte un .md per SKU
    blog/                    ← eseuri + poezii
    pages/                   ← despre, contacte, plată (redactat)
    covers/                  ← coperți originale
    site-images/             ← imagini de pe homepage
  archive/extracted/         ← JSON (catalog_clean.json = cel mai util)
  archive/raw-html.tar.gz    ← HTML-ul public brut
```
