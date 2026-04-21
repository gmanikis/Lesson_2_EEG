"""
Generate explainable diagrams for the ECG lab slides.
Run once: python generate_figs.py
All figures saved to current directory (slides/figs/).
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Circle, Rectangle, FancyBboxPatch
from scipy import signal

plt.rcParams.update({
    "font.size": 12,
    "axes.titlesize": 14,
    "axes.labelsize": 12,
    "savefig.dpi": 140,
    "savefig.bbox": "tight",
    "figure.facecolor": "white",
})


# ---------------------------------------------------------------
# 1) Heart conduction system — schematic
# ---------------------------------------------------------------
def fig_heart_conduction():
    fig, ax = plt.subplots(figsize=(11, 7))
    ax.set_xlim(0, 16); ax.set_ylim(0, 10)
    ax.set_aspect('equal'); ax.axis('off')

    # Heart outline (stylized) — placed on the LEFT half
    heart = FancyBboxPatch((1.0, 1.5), 7, 7, boxstyle="round,pad=0.1,rounding_size=1.5",
                            linewidth=2, edgecolor='darkred', facecolor='mistyrose')
    ax.add_patch(heart)

    # Septum
    ax.plot([4.5, 4.5], [1.7, 8.3], 'k--', alpha=0.4, lw=1)
    # Atria/Ventricles divider
    ax.plot([1.2, 7.8], [5.8, 5.8], 'k--', alpha=0.4, lw=1)

    ax.text(2.7, 7.0, "RA", ha='center', fontsize=11, fontweight='bold')
    ax.text(6.3, 7.0, "LA", ha='center', fontsize=11, fontweight='bold')
    ax.text(2.7, 3.6, "RV", ha='center', fontsize=11, fontweight='bold')
    ax.text(6.3, 3.6, "LV", ha='center', fontsize=11, fontweight='bold')

    # SA node
    sa = Circle((3.0, 7.6), 0.22, color='red', zorder=5)
    ax.add_patch(sa)
    # AV node
    av = Circle((4.5, 5.9), 0.20, color='orange', zorder=5)
    ax.add_patch(av)
    # His bundle + Purkinje
    ax.plot([4.5, 4.5], [5.7, 4.7], 'purple', lw=2)
    ax.plot([4.5, 3.0, 2.4], [4.7, 4.0, 2.3], 'purple', lw=1.5)
    ax.plot([4.5, 6.0, 6.6], [4.7, 4.0, 2.3], 'purple', lw=1.5)

    # Title
    ax.text(8, 9.5, "Ηλεκτρικό σύστημα αγωγής της καρδιάς",
            ha='center', fontsize=14, fontweight='bold')

    # Legend box on the RIGHT side — clean and non-overlapping
    legend_x = 9.5
    items = [
        ("red",       "1. SA node",
         "Βηματοδότης (60-100 bpm)\nαποπολώνει τους κόλπους\n→ P wave"),
        ("darkorange","2. AV node",
         "Καθυστέρηση 120-200 ms\n(κερδίζουμε χρόνο για\nπλήρωση κοιλιών)\n→ PR interval"),
        ("purple",    "3. His-Purkinje",
         "Πολύ γρήγορη αγωγή\nσε όλες τις κοιλίες\n→ QRS complex"),
        ("steelblue", "4. Επαναπόλωση",
         "Οι κοιλίες \"ξεφορτίζονται\"\nκαι ετοιμάζονται\nγια τον επόμενο παλμό\n→ T wave"),
    ]
    y = 8.4
    for col, head, body in items:
        ax.text(legend_x, y, head, fontsize=11, fontweight='bold', color=col)
        ax.text(legend_x, y - 0.35, body, fontsize=9, color='black', va='top')
        y -= 2.0

    # Arrows from legend to anatomical points
    ax.annotate("", xy=(3.0, 7.6), xytext=(legend_x - 0.1, 8.4),
                arrowprops=dict(arrowstyle='->', color='red', alpha=0.6))
    ax.annotate("", xy=(4.5, 5.9), xytext=(legend_x - 0.1, 6.4),
                arrowprops=dict(arrowstyle='->', color='darkorange', alpha=0.6))
    ax.annotate("", xy=(4.5, 4.7), xytext=(legend_x - 0.1, 4.4),
                arrowprops=dict(arrowstyle='->', color='purple', alpha=0.6))

    plt.savefig("01_heart_conduction.png")
    plt.close()


# ---------------------------------------------------------------
# 2) ECG wave labels — synthetic clean beat
# ---------------------------------------------------------------
def synthetic_beat(t):
    """Σύνθετος παλμός ECG με P, Q, R, S, T."""
    p   =  0.15 * np.exp(-((t - 0.10) / 0.025) ** 2)
    q   = -0.10 * np.exp(-((t - 0.23) / 0.010) ** 2)
    r   =  1.20 * np.exp(-((t - 0.26) / 0.010) ** 2)
    s   = -0.25 * np.exp(-((t - 0.29) / 0.012) ** 2)
    tw  =  0.30 * np.exp(-((t - 0.45) / 0.040) ** 2)
    return p + q + r + s + tw


def fig_ecg_wave_labels():
    t = np.linspace(0, 0.8, 2000)
    y = synthetic_beat(t)

    fig, ax = plt.subplots(figsize=(11, 5))
    ax.plot(t, y, color='darkblue', lw=2)
    ax.axhline(0, color='gray', lw=0.6, alpha=0.6)

    ann = [
        (0.10,  0.18, "P",   "↑ αποπόλωση κόλπων"),
        (0.23, -0.13, "Q",   ""),
        (0.26,  1.25, "R",   "↑ αποπόλωση κοιλιών (QRS)"),
        (0.29, -0.28, "S",   ""),
        (0.45,  0.33, "T",   "↑ επαναπόλωση κοιλιών"),
    ]
    for x, yv, lab, _ in ann:
        ax.annotate(lab, xy=(x, yv), xytext=(x, yv + 0.18),
                    ha='center', fontsize=14, fontweight='bold', color='darkred')

    # Intervals
    ax.annotate("", xy=(0.23, -0.45), xytext=(0.10, -0.45),
                arrowprops=dict(arrowstyle='<->', color='green'))
    ax.text(0.165, -0.55, "PR\ninterval", ha='center', color='green', fontsize=10)

    ax.annotate("", xy=(0.30, -0.45), xytext=(0.215, -0.45),
                arrowprops=dict(arrowstyle='<->', color='purple'))
    ax.text(0.26, -0.55, "QRS", ha='center', color='purple', fontsize=10)

    ax.annotate("", xy=(0.50, -0.45), xytext=(0.215, -0.45),
                arrowprops=dict(arrowstyle='<->', color='brown'))
    ax.text(0.36, -0.70, "QT interval", ha='center', color='brown', fontsize=10)

    ax.set_title("Τα κύματα του ECG — ένας παλμός")
    ax.set_xlabel("Χρόνος (sec)")
    ax.set_ylabel("Amplitude (mV)")
    ax.set_ylim(-0.85, 1.6)
    ax.grid(True, alpha=0.25)
    plt.savefig("02_ecg_wave_labels.png")
    plt.close()


# ---------------------------------------------------------------
# 3) RR interval / Heart Rate illustration
# ---------------------------------------------------------------
def fig_rr_intervals():
    fs = 500
    t = np.arange(0, 3.0, 1 / fs)
    # 3 beats at RR=0.8 sec  → HR = 75 bpm
    y = np.zeros_like(t)
    for r_t in [0.4, 1.2, 2.0, 2.8]:
        y += synthetic_beat(t - r_t + 0.26)

    fig, ax = plt.subplots(figsize=(11, 4.5))
    ax.plot(t, y, color='darkblue', lw=1.5)
    ax.axhline(0, color='gray', lw=0.5, alpha=0.5)

    r_times = [0.4, 1.2, 2.0, 2.8]
    for rt in r_times:
        ax.plot(rt, 1.2, 'rv', markersize=12)

    # RR brackets
    for i in range(len(r_times) - 1):
        x1, x2 = r_times[i], r_times[i + 1]
        ax.annotate("", xy=(x2, 1.45), xytext=(x1, 1.45),
                    arrowprops=dict(arrowstyle='<->', color='red', lw=1.5))
        ax.text((x1 + x2) / 2, 1.55, f"RR = {x2 - x1:.2f} s",
                ha='center', color='red', fontsize=11)

    ax.text(1.5, -0.6, "HR = 60 / RR  →  60 / 0.80 = 75 bpm",
            ha='center', fontsize=13, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='lightyellow', edgecolor='orange'))

    ax.set_title("RR interval & Heart Rate")
    ax.set_xlabel("Χρόνος (sec)")
    ax.set_ylabel("Amplitude (mV)")
    ax.set_ylim(-0.85, 1.85)
    ax.grid(True, alpha=0.25)
    plt.savefig("03_rr_intervals.png")
    plt.close()


# ---------------------------------------------------------------
# 4) Noise types — visual catalog
# ---------------------------------------------------------------
def fig_noise_types():
    fs = 500
    t = np.arange(0, 4.0, 1 / fs)
    clean = np.zeros_like(t)
    for r_t in np.arange(0.3, 4.0, 0.85):
        clean += synthetic_beat(t - r_t + 0.26)

    drift = 0.4 * np.sin(2 * np.pi * 0.2 * t)
    powerline = 0.15 * np.sin(2 * np.pi * 50 * t)
    emg = np.random.normal(0, 0.07, len(t))
    corrupted = clean + drift + powerline + emg

    fig, axes = plt.subplots(5, 1, figsize=(11, 9), sharex=True)
    titles = [
        ("Καθαρό ECG", clean, 'darkblue'),
        ("Baseline drift  (~0.2 Hz — αναπνοή/κίνηση)", drift, 'orange'),
        ("Powerline noise  (50 Hz — δίκτυο)", powerline, 'red'),
        ("Muscle / EMG noise  (>40 Hz — τυχαίο)", emg, 'green'),
        ("Corrupted = clean + όλα τα παραπάνω", corrupted, 'purple'),
    ]
    for ax, (title, sig, col) in zip(axes, titles):
        ax.plot(t, sig, color=col, lw=0.9)
        ax.set_title(title, loc='left', fontsize=11)
        ax.grid(True, alpha=0.2)
    axes[-1].set_xlabel("Χρόνος (sec)")
    fig.suptitle("Τύποι θορύβου στο ECG", fontsize=14, fontweight='bold', y=1.0)
    plt.tight_layout()
    plt.savefig("04_noise_types.png")
    plt.close()


# ---------------------------------------------------------------
# 5) Filter response curves — bandpass 0.5-40 Hz
# ---------------------------------------------------------------
def fig_filter_response():
    fs = 360
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))

    # Three bandpass options from the lab exercise
    configs = [("A: 1-20 Hz",   1.0, 20, 'orange'),
               ("B: 0.5-40 Hz", 0.5, 40, 'green'),
               ("C: 5-50 Hz",   5.0, 50, 'red')]

    for label, lo, hi, col in configs:
        b, a = signal.butter(4, [lo, hi], btype='bandpass', fs=fs)
        w, h = signal.freqz(b, a, worN=4096, fs=fs)
        axes[0].plot(w, 20 * np.log10(np.abs(h) + 1e-9), color=col, lw=2, label=label)

    axes[0].axvspan(0, 0.5, color='gray', alpha=0.15)
    axes[0].axvspan(50, fs / 2, color='gray', alpha=0.15)
    axes[0].axvline(50, color='red', ls=':', alpha=0.5)
    axes[0].text(50, -55, "50 Hz\npowerline", color='red', fontsize=9, ha='center')
    axes[0].set_xlim(0, 80)
    axes[0].set_ylim(-80, 5)
    axes[0].set_xlabel("Frequency (Hz)")
    axes[0].set_ylabel("Gain (dB)")
    axes[0].set_title("Butterworth bandpass — απόκριση συχνότητας")
    axes[0].legend(loc='lower center')
    axes[0].grid(True, alpha=0.3)

    # Useful ECG band annotation
    axes[1].axvspan(0.5, 40, color='lightgreen', alpha=0.4, label="χρήσιμο ECG\n0.5-40 Hz")
    axes[1].axvspan(0, 0.5, color='orange', alpha=0.3, label="baseline drift")
    axes[1].axvspan(40, 80, color='salmon', alpha=0.3, label="EMG / powerline")
    axes[1].axvline(50, color='red', ls='--', lw=2)
    axes[1].text(51, 0.8, "50 Hz", color='red', fontsize=11, fontweight='bold')
    axes[1].set_xlim(0, 80); axes[1].set_ylim(0, 1)
    axes[1].set_yticks([])
    axes[1].set_xlabel("Frequency (Hz)")
    axes[1].set_title("Πού ζει τι;  (χάρτης συχνοτήτων ECG)")
    axes[1].legend(loc='upper right', fontsize=9)
    axes[1].grid(True, alpha=0.3, axis='x')

    plt.tight_layout()
    plt.savefig("05_filter_response.png")
    plt.close()


# ---------------------------------------------------------------
# 6) R-peak detection — distance & height illustration
# ---------------------------------------------------------------
def fig_peak_detection():
    fs = 500
    t = np.arange(0, 4.0, 1 / fs)
    sig_clean = np.zeros_like(t)
    for r_t in np.arange(0.3, 4.0, 0.78):
        sig_clean += synthetic_beat(t - r_t + 0.26)
    np.random.seed(0)
    sig_noisy = sig_clean + 0.05 * np.random.randn(len(t))

    fig, axes = plt.subplots(3, 1, figsize=(11, 8), sharex=True)

    # Bad: too low height → catches noise
    pk_bad_h, _ = signal.find_peaks(sig_noisy, distance=int(fs * 0.6), height=0.05)
    axes[0].plot(t, sig_noisy, color='gray', lw=0.8)
    axes[0].plot(t[pk_bad_h], sig_noisy[pk_bad_h], 'rv', markersize=10)
    axes[0].axhline(0.05, color='red', ls='--', alpha=0.6, label='height = 0.05 (πολύ χαμηλό)')
    axes[0].set_title(f"[X] height πολύ χαμηλό → {len(pk_bad_h)} peaks (πολλά false)", loc='left', color='darkred')
    axes[0].legend(loc='upper right', fontsize=9)

    # Bad: too small distance → double counts
    pk_bad_d, _ = signal.find_peaks(sig_noisy, distance=int(fs * 0.05), height=0.5)
    axes[1].plot(t, sig_noisy, color='gray', lw=0.8)
    axes[1].plot(t[pk_bad_d], sig_noisy[pk_bad_d], 'rv', markersize=10)
    axes[1].set_title(f"[X] distance πολύ μικρό → {len(pk_bad_d)} peaks (διπλομέτρημα)", loc='left', color='darkred')

    # Good
    auto_h = np.mean(sig_noisy) + 0.5 * np.std(sig_noisy)
    pk_good, _ = signal.find_peaks(sig_noisy, distance=int(fs * 0.6), height=auto_h)
    axes[2].plot(t, sig_noisy, color='gray', lw=0.8)
    axes[2].plot(t[pk_good], sig_noisy[pk_good], 'gv', markersize=12)
    axes[2].axhline(auto_h, color='green', ls='--', alpha=0.6, label=f'height = mean+0.5·std')
    axes[2].set_title(f"[OK] καλός συνδυασμός → {len(pk_good)} peaks", loc='left', color='darkgreen')
    axes[2].legend(loc='upper right', fontsize=9)
    axes[2].set_xlabel("Χρόνος (sec)")

    for ax in axes:
        ax.grid(True, alpha=0.2)

    fig.suptitle("R-peak detection: ο ρόλος των distance και height",
                 fontsize=13, fontweight='bold', y=1.0)
    plt.tight_layout()
    plt.savefig("06_peak_detection.png")
    plt.close()


# ---------------------------------------------------------------
# 7) Normal vs PVC morphology
# ---------------------------------------------------------------
def fig_normal_vs_pvc():
    t = np.linspace(0, 0.8, 2000)

    normal = synthetic_beat(t)

    # PVC: wide QRS, no P, opposite polarity, larger amplitude
    pvc_q = -0.05 * np.exp(-((t - 0.20) / 0.020) ** 2)
    pvc_r =  0.40 * np.exp(-((t - 0.24) / 0.030) ** 2)
    pvc_s = -1.30 * np.exp(-((t - 0.30) / 0.045) ** 2)
    pvc_t =  0.50 * np.exp(-((t - 0.50) / 0.060) ** 2)
    pvc = pvc_q + pvc_r + pvc_s + pvc_t

    fig, axes = plt.subplots(1, 2, figsize=(13, 4.5), sharey=True)

    axes[0].plot(t, normal, color='blue', lw=2)
    axes[0].set_title("Normal beat (N)")
    axes[0].text(0.10, 0.25, "P", ha='center', fontsize=12, color='darkred', fontweight='bold')
    axes[0].text(0.26, 1.32, "R", ha='center', fontsize=12, color='darkred', fontweight='bold')
    axes[0].text(0.45, 0.40, "T", ha='center', fontsize=12, color='darkred', fontweight='bold')
    axes[0].annotate("στενό QRS\n(<120 ms)", xy=(0.27, 0.6), xytext=(0.55, 0.9),
                     fontsize=10, color='green',
                     arrowprops=dict(arrowstyle='->', color='green'))

    axes[1].plot(t, pvc, color='red', lw=2)
    axes[1].set_title("PVC beat (V)")
    axes[1].annotate("χωρίς P", xy=(0.10, 0.0), xytext=(0.0, 0.6),
                     fontsize=10, color='darkred',
                     arrowprops=dict(arrowstyle='->', color='darkred'))
    axes[1].annotate("πλατύ QRS\n(>120 ms)\n+ ανεστραμμένο",
                     xy=(0.30, -1.0), xytext=(0.45, -1.4),
                     fontsize=10, color='darkred',
                     arrowprops=dict(arrowstyle='->', color='darkred'))

    for ax in axes:
        ax.axhline(0, color='gray', lw=0.5, alpha=0.5)
        ax.set_xlabel("Χρόνος (sec)")
        ax.grid(True, alpha=0.25)
    axes[0].set_ylabel("Amplitude (mV)")

    fig.suptitle("Μορφολογία: Normal vs PVC", fontsize=13, fontweight='bold')
    plt.tight_layout()
    plt.savefig("07_normal_vs_pvc.png")
    plt.close()


# ---------------------------------------------------------------
# 8) HRV: Tachogram + ANS balance
# ---------------------------------------------------------------
def fig_hrv_concept():
    np.random.seed(2)
    n = 120
    rr_low_var = 0.85 + 0.02 * np.random.randn(n)
    rr_high_var = 0.85 + 0.10 * np.random.randn(n) + 0.05 * np.sin(np.linspace(0, 8 * np.pi, n))

    fig, axes = plt.subplots(1, 2, figsize=(13, 4.5))
    axes[0].plot(rr_low_var, marker='.', color='gray', lw=0.7, label=f"χαμηλό HRV (SDNN={np.std(rr_low_var)*1000:.0f} ms)")
    axes[0].plot(rr_high_var, marker='.', color='steelblue', lw=0.7, label=f"υψηλό HRV (SDNN={np.std(rr_high_var)*1000:.0f} ms)")
    axes[0].set_title("Tachogram — RR στον χρόνο")
    axes[0].set_xlabel("Beat number"); axes[0].set_ylabel("RR (sec)")
    axes[0].legend(fontsize=9); axes[0].grid(True, alpha=0.25)

    # ANS balance bar
    ax = axes[1]; ax.axis('off')
    ax.text(0.5, 0.95, "Αυτόνομο Νευρικό Σύστημα (ANS)", ha='center',
            fontsize=13, fontweight='bold', transform=ax.transAxes)
    ax.text(0.5, 0.85, "Ισορροπία = υγιής καρδιά", ha='center',
            fontsize=11, transform=ax.transAxes)

    ax.add_patch(Rectangle((0.05, 0.45), 0.4, 0.25, facecolor='salmon', edgecolor='darkred', lw=2,
                            transform=ax.transAxes))
    ax.text(0.25, 0.62, "Sympathetic", ha='center', fontsize=12, fontweight='bold',
            color='darkred', transform=ax.transAxes)
    ax.text(0.25, 0.52, "↑ HR  ↓ HRV\n(stress, exercise)", ha='center', fontsize=10,
            color='darkred', transform=ax.transAxes)

    ax.add_patch(Rectangle((0.55, 0.45), 0.4, 0.25, facecolor='lightgreen', edgecolor='darkgreen', lw=2,
                            transform=ax.transAxes))
    ax.text(0.75, 0.62, "Parasympathetic", ha='center', fontsize=12, fontweight='bold',
            color='darkgreen', transform=ax.transAxes)
    ax.text(0.75, 0.52, "↓ HR  ↑ HRV\n(rest, sleep)", ha='center', fontsize=10,
            color='darkgreen', transform=ax.transAxes)

    ax.text(0.5, 0.30, "SDNN ≈ συνολική μεταβλητότητα\nRMSSD ≈ βραχυπρόθεσμη (παρασυμπαθητικό)",
            ha='center', fontsize=10, transform=ax.transAxes,
            bbox=dict(boxstyle='round', facecolor='lightyellow', edgecolor='orange'))
    ax.text(0.5, 0.10,
            "Προσοχή: υψηλό SDNN λόγω αρρυθμιών ΔΕΝ είναι υγιές HRV",
            ha='center', fontsize=10, color='darkred', fontweight='bold',
            transform=ax.transAxes)

    plt.tight_layout()
    plt.savefig("08_hrv_concept.png")
    plt.close()


# ---------------------------------------------------------------
# 9) Rule-based detector schematic
# ---------------------------------------------------------------
def fig_rule_based():
    np.random.seed(3)
    n = 80
    rr = 0.80 + 0.04 * np.random.randn(n)
    # inject 3 PVCs
    pvc_idx = [20, 45, 65]
    for i in pvc_idx:
        rr[i] = 0.50
        if i + 1 < n:
            rr[i + 1] = 1.10  # compensatory pause

    mu, sd = np.mean(rr), np.std(rr)
    fig, ax = plt.subplots(figsize=(11, 5))
    ax.plot(rr, marker='o', lw=0.8, color='steelblue', label="RR")
    ax.axhline(mu, color='black', ls='-', alpha=0.7, label=f"mean = {mu:.2f}")
    for k, col in [(1.5, 'orange'), (2.0, 'red'), (2.5, 'purple')]:
        ax.axhline(mu + k * sd, color=col, ls='--', alpha=0.6, label=f"mean ± {k}·std")
        ax.axhline(mu - k * sd, color=col, ls='--', alpha=0.6)

    flagged = [i for i, r in enumerate(rr) if abs(r - mu) > 2 * sd]
    ax.plot(flagged, [rr[i] for i in flagged], 'rv', markersize=14,
            label=f"flagged (k=2): {len(flagged)} beats")

    ax.set_title("Rule-based arrhythmia detector:  |RR − mean| > k·std")
    ax.set_xlabel("Beat number"); ax.set_ylabel("RR (sec)")
    ax.legend(loc='upper right', fontsize=9, ncol=2); ax.grid(True, alpha=0.25)
    plt.tight_layout()
    plt.savefig("09_rule_based.png")
    plt.close()


if __name__ == "__main__":
    fig_heart_conduction()
    fig_ecg_wave_labels()
    fig_rr_intervals()
    fig_noise_types()
    fig_filter_response()
    fig_peak_detection()
    fig_normal_vs_pvc()
    fig_hrv_concept()
    fig_rule_based()
    print("All figures generated.")
