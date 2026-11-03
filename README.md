# BULDO web

Statický web BULDO (HTML, CSS, JavaScript bez knihoven) podle návrhu ve Figmě. Běží na GitHub Pages bez buildu.

## Stránky
- `index.html` – homepage (hero video, loga, čísla, animace papírky → telefon, hlavní funkce s videi, Proč BULDO, ceník, články, FAQ)
- `clanky.html` – výpis článků
- `clanek.html` – detail článku
- `kontakt.html` – kontakty a formulář
- `poradna.html` – nápověda s hledáním

## Úpravy
Sdílená hlavička, patička, FAQ a CTA jsou v `tools/build.py`. Po úpravě spusť:

```
python3 tools/build.py
```

Styly jsou v `assets/css/style.css`, interakce v `assets/js/main.js`.

## Nasazení na GitHub Pages
Settings → Pages → Source: *Deploy from a branch* → větev `main`, složka `/ (root)`.

## Co zbývá doplnit
- Kontaktní formulář zatím nic neodesílá (jen ukázka). Na ostrý provoz napojit např. Formspree nebo backend webu.
- Texty návodů v Poradně a odpovědi FAQ jsou zástupné, je potřeba je převzít z aktuální nápovědy.
- Odkazy na sociální sítě, obchodní podmínky a ochranu osobních údajů.
