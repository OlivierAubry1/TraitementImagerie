import scipy.io
import numpy as np
import matplotlib.pyplot as plt

mat_data = scipy.io.loadmat('RF_SIGNALS.mat')

f0=3e6; # Transducer center frequency [Hz]
fs=50e6; # Sampling frequency [Hz]
c=1540; # Speed of sound [m/s]
spacing=0.1/1000; # Element spacing [m]
N_elements=128; # Number of physical elements
Nsamples = 4096; # Number of samples

rf = mat_data['RF_SIGNALS']

print(rf)

signal = np.squeeze(rf[:,63, 63])
time = np.arange(Nsamples)/fs

plt.figure()
plt.plot(time*1e6, signal)
plt.title('A scan Émetteur recepteur')
plt.xlabel('Temps')
plt.ylabel('Amplitude')
plt.show()

x_min = -15/1000
x_max = 15/1000
y_min = 0
y_max = 30/1000
step = 0.2/1000

Xv = np.arange(x_min, x_max, step)
Yv = np.arange(y_min, y_max, step)

X, Y = np.meshgrid(Xv, Yv)

#sonde
N_elements = 128
sonde_step = 0.1/1000

centre = (N_elements-1)*sonde_step/2

x_elements = np.linspace(-centre, centre, N_elements)
y_elements = np.zeros(N_elements)
plt.figure()
plt.plot(X, Y, 'k.')
plt.plot(x_elements, y_elements, 'o')
plt.title('Sonde')
plt.show()

#calcul
Xe = x_elements[63]
Xr = x_elements[63]
Ye = y_elements[63]
Yr = y_elements[63]

#temps de voll

d_e = np.sqrt((Xe-X)**2 + (Ye-Y)**2)
d_r = np.sqrt((Xr-X)**2 + (Yr-Y)**2)

temps_vol = (d_e + d_r)/c

indice = np.round(temps_vol*fs).astype(int)

A = np.zeros_like(X)

mask = (indice >= 0) & (indice < Nsamples)

A[mask] = signal[indice[mask]]

plt.figure()
plt.imshow(A, extent=[x_min, x_max, y_max, y_min], aspect='auto')
plt.colorbar()
plt.title('Image echo')
plt.show()

A_dB = 20*np.log10(np.abs(A) / np.max(np.abs(A)))
plt.figure()
plt.imshow(A_dB, extent=[x_min, x_max, y_max, y_min], aspect='auto')
plt.colorbar()
plt.show()

#image finale<

A_total = np.zeros_like(X)

for E in range(N_elements):
    Xe = x_elements[E]
    Ye = y_elements[E]
    for R in range(N_elements):
        Xr = x_elements[R]
        Yr = y_elements[R]

        d_e = np.sqrt((Xe-X)**2 + (Ye-Y)**2)
        d_r = np.sqrt((Xr-X)**2 + (Yr-Y)**2)

        temps_vol = (d_e + d_r)/c

        indice = np.round(temps_vol*fs).astype(int)

        mask = (indice >= 0) & (indice < Nsamples)

        A_total[mask] += signal[indice[mask]]

plt.figure()
plt.imshow(A_total, extent=[x_min, x_max, y_max, y_min], aspect='auto')
plt.colorbar()
plt.title('Image finale')
plt.show()

A_total_dB = 20*np.log10(np.abs(A_total) / np.max(np.abs(A_total)))
plt.figure()
plt.imshow(A_total_dB, extent=[x_min, x_max, y_max, y_min], aspect='auto')
plt.colorbar()
plt.title('Image finale en dB')
plt.show()