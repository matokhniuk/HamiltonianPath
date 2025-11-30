# HamiltonianPath

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
kde n je pocet vrcholu, m je pocet hran a kazdy radek `u v` (s 1 <= u, v <= n) popisuje jednu hranu grafu. Radky zacinajici znakem `#` a prazdne radky skript ignoruje.

Reseny rozhodovaci problem zni:

> Ma zadany graf G Hamiltonovskou cestu?

Vystupem systemu je:
- odpoved **ANO**, pokud existuje Hamiltonovska cesta,
- odpoved **NE**, pokud takova cesta neexistuje.

V pripade odpovedi ANO skript navic vypise jednu konkretni Hamiltonovskou cestu jako posloupnost vrcholu `v1 v2 ... vn`.
