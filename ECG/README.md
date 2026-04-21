# ECG Lab Slides

Marp-based slide deck που συνοδεύει το `ECG.ipynb`.
Σχεδιασμένο για **side-by-side** χρήση: slides αριστερά, notebook δεξιά.

## Δομή

- `ECG_slides.md` — η παρουσίαση (Marp markdown)
- `figs/` — όλα τα διαγράμματα
  - `generate_figs.py` — αναπαράγει τα PNGs (αν χρειαστεί)
  - `01..09_*.png` — διαγράμματα

## Preview & Export

### Επιλογή 1: VS Code (απλούστερο)

1. Εγκατάσταση extension **"Marp for VS Code"**.
2. Άνοιγμα `ECG_slides.md`.
3. `Ctrl+Shift+V` → live preview δίπλα.
4. Από το command palette: **"Marp: Export slide deck"** → PDF / HTML / PPTX.

### Επιλογή 2: CLI (για αυτοματισμό)

```bash
npm install -g @marp-team/marp-cli
marp ECG_slides.md -o ECG_slides.pdf
marp ECG_slides.md -o ECG_slides.html
marp ECG_slides.md -o ECG_slides.pptx --pptx
```

### Επιλογή 3: Παρουσίαση απευθείας από browser

```bash
marp ECG_slides.md --preview
```
Ή export σε HTML και άνοιγμα στον browser σε full-screen (`F11`).

## Setup για παρουσίαση 2 οθονών

**Συνιστώμενη διάταξη:**
- **Οθόνη 1 (projector):** `ECG_slides.html` σε full-screen
- **Οθόνη 2 (laptop):** Jupyter notebook με το `ECG.ipynb`

Κάθε φορά που ένα slide έχει το πορτοκαλί box `▶ Τρέξτε: ...`, στρέφετε στο notebook και τρέχετε το αντίστοιχο κελί.

## Αναπαραγωγή των διαγραμμάτων

Αν θέλετε να αλλάξετε χρώματα / μέγεθος / κείμενο σε κάποιο διάγραμμα:

```bash
cd figs
py generate_figs.py
```

Απαιτεί: `numpy`, `scipy`, `matplotlib`.

## Δομή deck (40 slides)

1. Title + overview + πρόγραμμα (3)
2. Ενότητα 1 — Καρδιά ως ηλεκτρικό όργανο (4)
3. Ενότητα 2 — Κύματα ECG (3)
4. Ενότητα 3 — MIT-BIH data (3)
5. Ενότητα 4 — Θόρυβος (4)
6. Ενότητα 5 — Filtering (4)
7. Ενότητα 6 — R-peak detection (4)
8. Ενότητα 7 — HR & RR (3)
9. Ενότητα 8 — HRV (4)
10. Ενότητα 9 — Αρρυθμίες (6)
11. Ενότητα 10 — Σύγκριση ομάδων (2)
12. Bonus — Spectral + ML (2)
13. Σύνοψη (1)
