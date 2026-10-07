import scipy.io
import numpy as np
import matplotlib.pyplot as plt

data = scipy.io.loadmat('BGM724_LABO3.mat')

S1 = np.array(data['SIG1'], dtype=np.float64).ravel()
S2 = np.array(data['SIG2'], dtype=np.float64).ravel()
S3 = np.array(data['SIG3'], dtype=np.float64).ravel()

plt.plot(S1, label='Signal 1')
plt.plot(S2, label='Signal 2')  
plt.plot(S3, label='Signal 3')
plt.title('Signaux')
plt.xlabel('Échantillons')
plt.ylabel('Amplitude')
plt.legend()
plt.show(block=True)
#facteur de corrélation

decalage = range(-100, 101)
C_d = []
for d in decalage:
    somme = 0
    N = len(S1)
    for k in range(N):
        index_s2 = k + d
        if index_s2 < 0 or index_s2 >= N:
            continue
        somme += S1[k] * S2[index_s2]
    C_d.append(somme / N)
    print(f"Décalage d={d}: C(d)={C_d[-1]}")
    
plt.plot(decalage, C_d)
plt.title('Facteur de corrélation C(d)')
plt.xlabel('Décalage d (échantillons)')
plt.ylabel('C(d)')
plt.show(block=True)

#pour la formule corrélation non biaisée

n_S1 = np.mean(S1)
C_d_unbiased = []
for d in decalage:
    somme = 0
    n_S2 = np.mean(S2[max(0, -d):min(len(S2), len(S2)-d)])  # Moyenne de S2 pour les indices valides
    N = len(S1)
    for k in range(N):
        index_s2 = k + d
        if index_s2 < 0 or index_s2 >= N:
            continue
        somme += (S1[k] - n_S1) * (S2[index_s2] - n_S2)
    C_d_unbiased.append(somme / (N - abs(d)))
    print(f"Décalage d={d}: C(d) non biaisé={C_d_unbiased[-1]}")

plt.plot(decalage, C_d_unbiased)
plt.title('Facteur de corrélation C(d) non biaisé')
plt.xlabel('Décalage d (échantillons)')
plt.ylabel('C(d) non biaisé')
plt.show(block=True)

#corrélation fenétrée


ind1 = 0 
L = 64
d_valeurs = list(range(-100, 101))
C_fenetree_d = []

for d in d_valeurs:
    somme = 0  
    mean_s1 = np.mean(S1[ind1:ind1+L])
    
    debut_s2 = max(0, ind1+d)
    fin_s2 = min(N, ind1+L+d)
    mean_s2 = np.mean(S2[debut_s2:fin_s2]) if debut_s2 < fin_s2 else 0
    
    for k in range(L):
        idx_s1 = k + ind1
        idx_s2 = k + ind1 + d
            
        if 0 <= idx_s2 < N:
            somme += (S1[idx_s1] - mean_s1) * (S2[idx_s2] - mean_s2)
        else:
            continue
            
    C_fenetree_d.append(somme / L)
    
plt.plot(d_valeurs, C_fenetree_d)
plt.title('Facteur de corrélation C(d) fenêtré')
plt.xlabel('Décalage d (échantillons)')
plt.ylabel('C(d) fenêtré')
plt.show(block=True)

#corrélation fenétrée ind1 = 500


ind1 = 500 
L = 64
d_valeurs = list(range(-100, 101))
C_fenetree_d = []

for d in d_valeurs:
    somme = 0  
    mean_s1 = np.mean(S1[ind1:ind1+L])
    
    debut_s2 = max(0, ind1+d)
    fin_s2 = min(N, ind1+L+d)
    mean_s2 = np.mean(S2[debut_s2:fin_s2]) if debut_s2 < fin_s2 else 0
    
    for k in range(L):
        idx_s1 = k + ind1
        idx_s2 = k + ind1 + d
            
        if 0 <= idx_s2 < N:
            somme += (S1[idx_s1] - mean_s1) * (S2[idx_s2] - mean_s2)
        else:
            continue
            
    C_fenetree_d.append(somme / L)
    
plt.plot(d_valeurs, C_fenetree_d)
plt.title('Facteur de corrélation C(d) fenêtré')
plt.xlabel('Décalage d (échantillons)')
plt.ylabel('C(d) fenêtré')
plt.show(block=True)

#corrélation fenétrée multiple tailles de fenetre


ind1 = 500 
L = 64
d_valeurs = list(range(-100, 101))
C_fenetree_d = []

for L in (32, 64, 128, 256):
    C_fenetree_d = []
    for d in d_valeurs:
        somme = 0  
        mean_s1 = np.mean(S1[ind1:ind1+L])
        
        debut_s2 = max(0, ind1+d)
        fin_s2 = min(N, ind1+L+d)
        mean_s2 = np.mean(S2[debut_s2:fin_s2]) if debut_s2 < fin_s2 else 0
        
        for k in range(L):
            idx_s1 = k + ind1
            idx_s2 = k + ind1 + d
                
            if 0 <= idx_s2 < N:
                somme += (S1[idx_s1] - mean_s1) * (S2[idx_s2] - mean_s2)
            else:
                continue
                
        C_fenetree_d.append(somme / L)
        
    plt.plot(d_valeurs, C_fenetree_d, label=f'L={L}')

plt.title('Facteur de corrélation C(d) fenêtré pour différentes tailles de fenêtre')
plt.xlabel('Décalage d (échantillons)')
plt.ylabel('C(d) fenêtré')
plt.legend()
plt.show(block=True)

#corrélation fenétrée multiple normalisée


ind1 = 500 
L = 64
d_valeurs = list(range(-100, 101))
C_fenetree_d = []
for L in (32, 64, 128, 256):
    
    Cs1s1 = 1/L *np.sum((S1[ind1:ind1+L] - np.mean(S1[ind1:ind1+L]))**2)
    mean_s1 = np.mean(S1[ind1:ind1+L])

    C_fenetree_d = []
    for d in d_valeurs:
        somme = 0  
        debut_s2 = max(0, ind1+d)
        fin_s2 = min(N, ind1+L+d)
        mean_s2 = np.mean(S2[debut_s2:fin_s2]) if debut_s2 < fin_s2 else 0
        
        # 2. Cs2s2 dépend de L ET du décalage d (il va ici)
        if debut_s2 < fin_s2:
            fenetre_s2 = S2[debut_s2:fin_s2]
            mean_s2 = np.mean(fenetre_s2)
            # On utilise L pour être constant avec la formule de l'énoncé
            Cs2s2 = (1/L) * np.sum((fenetre_s2 - mean_s2)**2)
        else:
            mean_s2 = 0
            Cs2s2 = 0
        
        for k in range(L):
            idx_s1 = k + ind1
            idx_s2 = k + ind1 + d
                
            if 0 <= idx_s2 < N:
                somme += (S1[idx_s1] - mean_s1)/np.sqrt(Cs1s1) * (S2[idx_s2] - mean_s2)/np.sqrt(Cs2s2)
            else:
                continue
                
        C_fenetree_d.append(somme / L)
        
    plt.plot(d_valeurs, C_fenetree_d, label=f'L={L}')

plt.title('Facteur de corrélation C(d) fenêtré pour différentes tailles de fenêtre')
plt.xlabel('Décalage d (échantillons)')
plt.ylabel('C(d) fenêtré')
plt.legend()
plt.show(block=True)



