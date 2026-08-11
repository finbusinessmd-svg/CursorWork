# Cum se creează un personaj AI (corect)

Un personaj bun **nu e un CV inventat**. E un **contract de lucru**: ce știe, cum gândește, ce nu are voie să facă, cum livrează.

## 1. O singură misiune

Întreabă: *„Dacă scoatem acest personaj, ce lipsește din echipă?”*

- Dacă răspunsul e vag → personajul e prea general.
- Dacă răspunsul e clar („nimeni nu mai verifică contradicțiile în timp”) → e bun.

## 2. Cele 7 câmpuri obligatorii

| Câmp | Întrebare |
|------|-----------|
| **Nume + rol** | Cum îl chemi în conversație |
| **Misiune** | 1–2 propoziții |
| **Expertiză** | Domenii + limite geografice/juridice |
| **Metodă** | Pașii pe care îi urmează mereu |
| **Interdicții** | Ce nu inventează, ce nu amestecă |
| **Instrumente** | Ce i se dă (dosare, web, legi) |
| **Format output** | Cum arată răspunsul (tabele, etichete FAPT/INFERENȚĂ) |

## 3. Separă fapte de opinie

Personajele juridice **nu „știu” ce s-a întâmplat**. Ele:

1. citesc documente / declarații;
2. marchează contradicții;
3. propun întrebări și linii de atac;
4. lasă verdictul umanului (Vera / echipa).

## 4. Nu supraîncărca un rol

Exemplu greșit: un singur agent care e avocat + detectiv + expert corupție + researcher.

Exemplu bun: 4 roluri mici care se apelează pe rând.

## 5. Memorie pe caz, nu pe personaj

Personajul e **stabil**.  
Dosarul se schimbă.  

Pune faptele în `dosarul-interpol/`, nu în promptul personajului. Altfel, la fiecare update de dosar trebuie să rescrii personajul.

## 6. Testul de calitate (5 minute)

Dă același task la 2 personaje. Dacă răspund la fel → rolurile se suprapun. Restrânge misiunile.

### Test rapid pe Dosarul Interpol

**Task:** „Analizează schimbarea declarațiilor Movilă despre relația cu Vera.”

- **Detectivul** → timeline contradicții, citate, impact probatoriu.
- **Avocatul** → ce înseamnă juridic (credibilitate martor, art. relevante, strategie).
- **Cartograful** → cine a beneficiat / cine a semnat / ce rețele apar *dacă* există probe.
- **Scout** → cazuri similare (schimbare de narativă, „doamnă de companie”, raider MD/UE).

Dacă toți patru scriu același eseu → ai eșuat la separare.

## 7. Cum „iese din limite” Scout-ul (fără haos)

Agentul de idei **nu** trebuie să inventeze probe. El trebuie:

1. să propună **unghiuri** pe care nu le-ai cerut;
2. să caute **analogii** (alte țări, alte dosare, cărți, documentare);
3. să întoarcă **3–7 idei** + surse + „de ce merită”;
4. să marcheze ce e **speculativ**.

„Dincolo de task” = *explorare controlată*, nu delir.

## 8. Ce să eviți

- Personaje cu biografii de roman (soție, copii, hobby) fără utilitate.
- „30 de ani experiență” fără metodă concretă.
- Amestec FAPT + acuzație de corupție în aceeași propoziție.
- Citarea de articole de lege inventate. Dacă nu e sigur → spune „de verificat în Codul … art. …”.
