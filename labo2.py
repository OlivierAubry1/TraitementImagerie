import scipy.io
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

data = scipy.io.loadmat('IMAGE_DATA.mat')
image = data['IMAGE']
image_dB = data['IMAGE_dB']
x = data['x'].flatten()
y = data['y'].flatten()

#largeur du pic a 3dB
def largeur(signal, axe, idx_pic):
    niveau = signal[idx_pic] - 3
    i = idx_pic
    while i > 0 and signal[i] > niveau:
        i -= 1
    gauche = np.interp(niveau, [signal[i], signal[i + 1]], [axe[i], axe[i + 1]])
    j = idx_pic
    while j < len(signal) - 1 and signal[j] > niveau:
        j += 1
    droite = np.interp(niveau, [signal[j - 1], signal[j]], [axe[j - 1], axe[j]])
    return droite - gauche

#num1

idx_x = np.argmin(np.abs(x - (-15)))
col_fil = image_dB[:, idx_x]

plt.figure()
plt.plot(y, col_fil)
plt.xlabel('y (mm)')
plt.ylabel(r'IMAGE$_{dB}$')
plt.title('Coupe axiale à $x_c$ = -15 mm')
plt.show()

pics_idx, _ = find_peaks(col_fil, height=-20, distance=65)

for p in pics_idx:
    width = largeur(col_fil, y, p)
    print(f"Fil à y={y[p]:.1f} mm — résolution axiale = {width:.3f} mm")

#num2

profondeurs =  [40, 50, 60, 70, 80]

plt.figure()
for profondeur in profondeurs:
    idx_y = np.argmin(np.abs(y - profondeur))
    ligne_fil = image_dB[idx_y, :]
    plt.plot(x, ligne_fil, label=f'Coupe à y={profondeur} mm')
    idx_pic = idx_x
    width = largeur(ligne_fil, x, idx_pic)
    print(f"Coupe à y={profondeur} mm — résolution latérale = {width:.3f} mm")
    
plt.xlabel('x (mm)')
plt.ylabel(r'IMAGE$_{dB}$')
plt.title('Coupes latérales à différentes profondeurs')
plt.legend()
plt.xlim(-20, -10)
plt.show()

#partie 2
X, Y = np.meshgrid(x, y)


def masque_circulaire(xc, yc, rayon):
    return (X - xc)**2 + (Y - yc)**2 <= rayon**2


def afficher_masque(mask, titre='Masque'):
    plt.figure()
    plt.imshow(
        mask.astype(int),
        extent=[x.min(), x.max(), y.max(), y.min()],
        aspect='auto',
        cmap='viridis',
        vmin=0, vmax=1
    )
    plt.colorbar()
    plt.xlabel('Lateral distance [mm]')
    plt.ylabel('Axial distance [mm]')
    plt.title(titre)
    plt.show()


def snr_cnr(mask, mu_bg, sigma_bg):
    region = image[mask]
    mu = region.mean()
    sigma = region.std()
    snr = mu / sigma
    cnr = abs(mu - mu_bg) / np.sqrt(sigma**2 + sigma_bg**2)
    snr_dB = 20 * np.log10(snr)
    cnr_dB = 20 * np.log10(cnr) if cnr > 0 else -np.inf
    return mu, sigma, snr_dB, cnr_dB


# --- Plus grosse zone hyper-échoïque (exemple) ---
xc, yc, rayon = -5, 80, 3
mask_inclusion = masque_circulaire(xc, yc, rayon)
afficher_masque(mask_inclusion, titre='Masque - plus grosse inclusion hyper-échoïque')

mu_i = image[mask_inclusion].mean()
sigma_i = image[mask_inclusion].std()
print(f"\nInclusion: mu={mu_i:.4f}, sigma={sigma_i:.4f}")

# --- Zone de fond (background) — teste 2-3 positions/tailles ---
mask_bg = masque_circulaire(0, 45, 3)
afficher_masque(mask_bg, titre='Masque - zone de fond')

mu_bg = image[mask_bg].mean()
sigma_bg = image[mask_bg].std()
print(f"Background: mu={mu_bg:.4f}, sigma={sigma_bg:.4f}")

# --- SNR / CNR pour la plus grosse inclusion ---
_, _, snr_dB, cnr_dB = snr_cnr(mask_inclusion, mu_bg, sigma_bg)
print(f"SNR = {snr_dB:.1f} dB, CNR = {cnr_dB:.1f} dB")

# --- Boucle sur les inclusions hyper-échoïques (x_c = -5 mm) ---
inclusions_hyper = [
    (-5, 40, 1), (-5, 50, 1.5), (-5, 60, 2), (-5, 70, 2.5), (-5, 80, 3),
]  # (xc, yc, rayon) — ajuste selon les vraies positions/diamètres

print("\n--- Hyper-échoïques ---")
for xc, yc, r in inclusions_hyper:
    mask = masque_circulaire(xc, yc, r)
    _, _, snr_dB, cnr_dB = snr_cnr(mask, mu_bg, sigma_bg)
    print(f"y={yc} mm, d={2*r}mm — SNR={snr_dB:.1f} dB, CNR={cnr_dB:.1f} dB")

# --- Boucle sur les inclusions hypo-échoïques (x_c = 10 mm) ---
inclusions_hypo = [
    (10, 40, 1), (10, 50, 1.5), (10, 60, 2), (10, 70, 2.5), (10, 80, 3),
]

print("\n--- Hypo-échoïques ---")
for xc, yc, r in inclusions_hypo:
    mask = masque_circulaire(xc, yc, r)
    _, _, snr_dB, cnr_dB = snr_cnr(mask, mu_bg, sigma_bg)
    print(f"y={yc} mm, d={2*r}mm — SNR={snr_dB:.1f} dB, CNR={cnr_dB:.1f} dB")