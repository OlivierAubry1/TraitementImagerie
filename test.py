import numpy as np
import matplotlib.pyplot as plt

# Chargement fictif des signaux S1 et S2 (à remplacer par le chargement réel des fichiers du cours)
# S1 = np.loadtxt('S1.txt') 
# S2 = np.loadtxt('S2.txt')
N = len(S1)

# Définition de la plage des décalages d de -100 à +100 inclus
d_valeurs = range(-100, 101) 
C_d = []

for d in d_valeurs:
    somme = 0
    # k varie de 0 à N-1 en Python
    for k in range(N):
        index_s2 = k + d
        
        # Distinction des 3 cas demandés par l'énoncé
        if index_s2 < 0:
            # Correspond à k+d < 1 : on ignore
            continue 
        elif index_s2 >= N:
            # Correspond à k+d > N : on ignore
            continue 
        else:
            # Correspond à 1 < k+d < N : l'index est valide
            somme += S1[k] * S2[index_s2]
            
    # Application du facteur 1/N à la somme
    C_d.append(somme / N)

# Représentation de la courbe C(d)
plt.figure(figsize=(10, 4))
plt.plot(d_valeurs, C_d, color='cadetblue')
plt.xlabel("d (échantillons)")
plt.ylabel("C(d)")
plt.title("Facteur de corrélation C(d)")
plt.xlim(-100, 100)
plt.grid(True, linestyle='--', alpha=0.6)
plt.show()

# On suppose que S1, S2 et N sont déjà définis
# N = len(S1)

# 1. Calcul des moyennes globales des signaux
mean_S1 = np.mean(S1)
mean_S2 = np.mean(S2)

d_valeurs = list(range(-100, 101))
C_prime_d = []

# 2. Calcul itératif de la corrélation non biaisée
for d in d_valeurs:
    somme = 0
    for k in range(N):
        index_s2 = k + d
        
        # Gestion des indices valides (1 < k+d < N)
        if index_s2 < 0 or index_s2 >= N:
            continue 
        else:
            # Application de la formule : (S1[k] - moy(S1)) * (S2[k+d] - moy(S2))
            somme += (S1[k] - mean_S1) * (S2[index_s2] - mean_S2)
            
    # Division par (N - |d|) pour retirer le biais
    facteur = 1 / (N - abs(d))
    C_prime_d.append(facteur * somme)

# 3. Vérification du décalage (recherche du pic maximum)
max_index = np.argmax(C_prime_d)
decalage_optimal = d_valeurs[max_index]
print(f"Décalage trouvé : {decalage_optimal} échantillons.") # Devrait afficher 60

# 4. Affichage de la courbe C'(d)
plt.figure(figsize=(10, 4))
plt.plot(d_valeurs, C_prime_d, color='cadetblue')
plt.xlabel("d (échantillons)")
plt.ylabel("C'(d)")
plt.title("Facteur de corrélation non biaisée C'(d)")
plt.xlim(-100, 100)
plt.grid(True, linestyle='--', alpha=0.6)
plt.show()



# S1, S2 et N sont supposés déjà chargés
# N = len(S1)

ind1 = 0  # Équivalent de ind1 = 1 en indexation Python
L = 64
d_valeurs = list(range(-100, 101))
C_fenetree_d = []

for d in d_valeurs:
    # Initialisation des fenêtres locales
    fenetre_s1 = np.zeros(L)
    fenetre_s2 = np.zeros(L)
    
    # Remplissage des fenêtres échantillon par échantillon pour gérer les bords
    for k in range(L):
        idx_s1 = k + ind1
        idx_s2 = k + ind1 + d
        
        # S1 est garanti d'être dans les limites pour ce ind1
        fenetre_s1[k] = S1[idx_s1]
        
        # Vérification des limites pour S2 (remplissage par 0 si hors limites)
        if 0 <= idx_s2 < N:
            fenetre_s2[k] = S2[idx_s2]
        else:
            fenetre_s2[k] = 0
            
    # Calcul des moyennes locales (spécifique à l'intervalle de travail)
    mean_s1_locale = np.mean(fenetre_s1)
    mean_s2_locale = np.mean(fenetre_s2)
    
    # Application de la formule de corrélation fenêtrée
    somme = np.sum((fenetre_s1 - mean_s1_locale) * (fenetre_s2 - mean_s2_locale))
    C_fenetree_d.append(somme / L)

# Représentation graphique
plt.figure(figsize=(10, 4))
plt.plot(d_valeurs, C_fenetree_d, color='cadetblue')
plt.xlabel("d (échantillons)")
plt.ylabel("C'(d)")
plt.title(f"Corrélation fenêtrée (ind1={ind1 + 1}, L={L})")
plt.xlim(-100, 100)
plt.grid(True, linestyle='--', alpha=0.6)
plt.show()

#3 fenetrage 1
ind1 = 1    #depar
L1 = 64      # tialle fenetre
C_fen1 = np.zeros(k.shape[0])
for i in range(k.shape[0]):
    #calcul de corrélation
    mean_S1 = np.mean(S1[ind1:ind1+L1])
    # S2 peut se déplacer avant 0 aussi
    mean_S2 = np.mean(S2[max(0, ind1+k[i]):min(N, ind1+L1+k[i])])
    # prise en charge des cas ou k+d<1
    for n in range(ind1, ind1+L1):
        if n+k[i] >= 0 and n+k[i] < N:
            C_fen1[i] += (S1[n]-mean_S1)*(S2[n+k[i]]-mean_S2)


    C_fen1[i]= C_fen1[i]/L1
    
    import numpy as np
import matplotlib.pyplot as plt

# S1, S2 et N sont supposés déjà chargés
ind1 = 0  # On utilise le premier indice pour l'exemple
valeurs_L = [32, 64, 128, 256]
d_valeurs = list(range(-100, 101))

plt.figure(figsize=(10, 5))

for L in valeurs_L:
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
                
        C_fenetree_d.append(somme / L)
        
    # Tracer la courbe pour la valeur de L courante
    plt.plot(d_valeurs, C_fenetree_d, label=f'L = {L}')

plt.xlabel("d (échantillons)")
plt.ylabel("C'(d)")
plt.title(f"Influence de la taille de la fenêtre L (ind1 = {ind1 + 1})")
plt.xlim(-100, 100)
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.show()