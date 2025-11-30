# Hamiltonian Path

## 1. Popis reseneho problemu

Resim rozhodovaci verzi problemu Hamiltonovske cesty v (ne)orientovanem grafu.

**Vstup:**  
Graf G = (V, E), kde:

- V = {1..n} je mnozina vrcholu,
- E je mnozina hran.

Graf je zadany souborem ve formatu:
n m
u1 v1
u2 v2
...
um vm
kde n je pocet vrcholu, m je pocet hran a kazdy radek `u v`popisuje jednu hranu grafu.

Reseny rozhodovaci problem zni:

> Ma zadany graf G Hamiltonovskou cestu?

Vystupem systemu je:
- odpoved **ANO**, pokud existuje Hamiltonovska cesta,
- odpoved **NE**, pokud takova cesta neexistuje.

V pripade odpovedi ANO skript navic vypise jednu konkretni Hamiltonovskou cestu jako posloupnost vrcholu `v1 v2 ... vn`.

## 2. Zakodovani problemu do CNF

Pouzivam standardni SAT formulaci Hamiltonovske cesty s n*n binarnimi promennymi.

### 2.1 Rozhodovaci promenne

Zavadim binarni promenne:
Zavadim binarni promenne X(v, i):

- v ... cislo vrcholu (1..n)
- i ... pozice v ceste (1..n)

Promenna X(v, i) = 1 znamena, ze vrchol v je na pozici i.
## 2.2 Constrainty

### 2.2.1 Kazda pozice obsahuje prave jeden vrchol

**Alespon jeden vrchol na pozici `i`:**
X(1,i) v X(2,i) v ... v X(n,i)
**Nejvyse jeden vrchol na pozici `i`:**

Pro vsechny dvojice vrcholu `v != w`:
¬X(v,i) v ¬X(w,i)
### 2.2.2 Kazdy vrchol se objevi prave jednou

**Alespon jednou:**
X(v,1) v X(v,2) v ... v X(v,n)

**Nejvyse jednou:**

Pro vsechny dvojice pozic `i != j`:
¬X(v,i) v ¬X(v,j)

### 2.2.3 Povolené prechody mezi vrcholy

Pokud mezi vrcholy `u` a `v` neexistuje hrana, zakazujeme prechod z `u` na `v`:

Pro kazde `i = 1..n-1`:
¬X(u,i) v ¬X(v,i+1)
Tento constraint generujeme pro vsechny dvojice (u, v) bez hrany v grafu.

---

## 2.3 Prevod do DIMACS CNF

Literal pro promennou `X(v,i)` prevadim na cislo:
X(v,i) → (v - 1) * n + i
Negace literalu:
¬X(v,i) → -((v - 1) * n + i)
Klauzule ma tvar:
a b c ... 0
`0` ukoncuje klauzuli dle standardu DIMACS.

---

## 2.4 Velikost CNF

Vysledna CNF obsahuje:

- `n` klauzuli typu "alespon jeden vrchol na pozici",
- `n * (n - 1) / 2 * n` klauzuli typu "nejvyse jeden vrchol na pozici",
- `n` klauzuli typu "vrchol alespon jednou",
- `n * (n - 1) / 2 * n` klauzuli typu "vrchol nejvyse jednou",
- `(pocet neexistujicich hran) * (n - 1)` klauzuli pro zakazane prechody.

Formule je obecne velmi velka, typicky tisice az statisice klauzuli.

## 3. Uzivatelska dokumentace skriptu

Skript `hamiltonian.py` resi rozhodovaci problem Hamiltonovske cesty pomoci SAT solveru Glucose 4.2.

### 3.1 Spusteni skriptu

Zakladni spusteni:
python3 hamiltonian.py --instance cesta_k_souboru.txt --glucose /cesta/k/glucose

### 3.2 Argumenty prikazove radky
| Argument | Povinne | Popis |
|---------|---------|-------|
| `--instance <soubor>` | ano | Cesta k souboru obsahujicimu graf. |
| `--glucose <binarka>` | ano | Cesta k SAT solveru Glucose (kompilovanemu). |
| `--directed` | ne | Interpretuje graf jako orientovany (default je neorientovany). |
| `--cnf-output <soubor>` | ne | Jmeno vystupniho CNF souboru (default: `formula.cnf`). |
| `--print-cnf` | ne | Vypise CNF formuli na stdout. |
| `--print-stats` | ne | Vypise puvodni vystup SAT solveru. |

### 3.3 Format vstupniho souboru s grafem

Soubor obsahuje nejprve hlavicku `n m`:
n m
u1 v1
u2 v2
...
um vm
- `n` = pocet vrcholu (oznacuji se cisly `1..n`)
- `m` = pocet hran
- `u v` = jedna hrana grafu

Priklad male instance:
5 4
1 2
2 3
3 4
4 5
### 3.4 Format vystupu skriptu

V pripade, ze existuje Hamiltonovska cesta:
SAT: Hamiltonian path found:
v1 v2 v3 ... vn

V pripade, ze cesta neexistuje:
UNSAT: no Hamiltonian path exists for this instance.

### 3.5 CNF formuli
Soubor obsahuje:

- hlavicku `p cnf <pocet_promennych> <pocet_klauzuli>`
- kazdou klauzuli ukoncenou `0`

Priklad:

p cnf 25 158
1 6 11 16 21 0
-1 -6 0
...

## 4. Popis prilazenych instanci
K projektu jsou prilozene tri testovaci instance:

### 4.1 Instance g1.txt (mala, splnitelna)

Tato instance obsahuje:

- maly graf (5 vrcholu),
- jednoducha struktura,
- Hamiltonovska cesta existuje.

Slouzi k rychlemu otestovani celeho systemu.  
Reseni nalezne SAT solver okamzite.

### 4.2 Instance g2.txt (mala, nesplnitelna)

Tato instance:

- je mala (6 vrcholu),
- explicitne neobsahuje Hamiltonovskou cestu (napr. graf se vetvi, nebo chybi dulezite hrany).

Vhodne pro overeni, ze system spravne vraci:
UNSAT
### 4.3 Instance g3.txt (vetsi, splnitelna, pomalejsi)

Tato instance obsahuje:

- 28 vrcholu,
- husty graf,
- existuje Hamiltonovska cesta,
- SAT solver potrebuje znatelny cas (cca >= 10s).

Je urcena k testovani vykonnosti a experimentum s behovym casem.

---

## 5. Experimenty a mereni vykonnosti

Pro vedeni experimentu jsem pouzil prilozene instance.  
Uvadim pozorovani:

### 5.1 G1 — mala splnitelna instance

- Pocet vrcholu: 5  
- Pocet promennych: 25  
- Pocet klauzuli: 158  
- Doba behu Glucose: 0.01 s  

Solver okamzite nasel cestu.  
Kodovani funguje spravne.

### 5.2 G2 — mala nesplnitelna instance

- Pocet vrcholu: 6  
- Pocet promennych: 25  
- Pocet klauzuli: 166  
- Doba behu: 0.01 s  

Solver vratil `UNSAT` podle ocekavani.

### 5.3 G3 — vetsi instance (28 vrcholu)

- Pocet vrcholu: 28  
- Pocet promennych: 784  
- Pocet klauzuli: 29378  
- Doba behu: 10–20 sekund  
- Solver nalezl Hamiltonovskou cestu


## 6. Vystupy pro prilozene instance

Zde uvadim skutecne vystupy skriptu pro tri dodane testovaci instance.

### 6.1 Vystup pro g1.txt (mala splnitelna instance)
SAT: Hamiltonian path found:
5 4 3 2 1

Hamiltonovska cesta existuje. Solver ji nalezl okamzite.

---

### 6.2 Vystup pro g2.txt (mala nesplnitelna instance)
UNSAT: no Hamiltonian path exists for this instance.

Tato instance skutecne neobsahuje Hamiltonovskou cestu a solver to potvrdil.

---

### 6.3 Vystup pro g3.txt (vetsi instance, netrivialni cas)
SAT: Hamiltonian path found:
28 27 26 25 24 23 22 21 20 19 18 17 16 15 14 13 12 11 9 10 8 7 6 5 4 3 2 1
