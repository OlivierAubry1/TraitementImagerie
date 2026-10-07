import scipy.io
import numpy as np
import matplotlib.pyplot as plt

# Chargement des données
data = scipy.io.loadmat('BGM724_LABO3.mat')
S1 = np.array(data['SIG1'], dtype=np.float64).ravel()
S3 = np.array(data['SIG3'], dtype=np.float64).ravel()

# Paramètres
L = 30
d_valeurs = np.arange(0, 51)
indices = np.arange(0, 900)
N = len(S1)

u_z = []

for ind1 in indices:
    fenetre_s1 = S1[ind1 : ind1 + L]
    mean_s1 = np.mean(fenetre_s1)
    
    C_d = []
    
    for d in d_valeurs:
        fenetre_s3 = S3[ind1 + d : ind1 + L + d]
        
        if len(fenetre_s3) == L:
            mean_s3 = np.mean(fenetre_s3)
            numerateur = np.sum((fenetre_s1 - mean_s1) * (fenetre_s3 - mean_s3))
            denominateur = np.sqrt(np.sum((fenetre_s1 - mean_s1) ** 2) * np.sum((fenetre_s3 - mean_s3) ** 2))
            
            
            # Éviter la division par zéro
            if denominateur != 0:
                corr = numerateur / denominateur
            else:
                corr = 0
        else:
            corr = 0
            
        C_d.append(corr)
        
    meilleur_d_idx = np.argmax(C_d)
    u_z.append(d_valeurs[meilleur_d_idx])

# Affichage du graphique de uz en fonction de ind1
plt.figure(figsize=(10, 4))
plt.plot(indices, u_z, linewidth=1)
plt.title("Évolution du décalage optimal $u_z$ en fonction de $ind_1$")
plt.xlabel("ind$_1$")
plt.ylabel("$u_z$")
plt.xlim(0, 900)
plt.ylim(0, 50)
plt.grid(True)
plt.show()