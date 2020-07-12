#!/usr/bin/python3.5

#  General Librarie for matrix management and operation
import numpy as np 
from numpy import linalg as LA # LA to find eigen values and vectors
# General Librarie for math operations
from math import pi
import cmath

import matplotlib as mpl
import matplotlib.pyplot as plt

# Données d'inertie en rapport avec la dénomination choisie 
J11 = 7.37e-2 ; 
J12 = 2.67e-2 ;
J13 = 2.66e-2 ; 
J21 = 3.4 ; 
J22 = 4.3e-1 ; 
J23 = 2.08e-1 ; 
J31 = 9.25e-1 ; 
J32 = 1.09 ; 
J33 = 1.54e1 ; 
J41 = 9.17e1;
J42 = 8.59 ; 
J51 = 3.24 ;
J52 = 2.63e2 ; 
J53 = 4.74 ; 
J61 = 2.96 ; 
J62 = 1.49e2 ; 


# Données des raideurs en rapport avec la dénomincation choisie
K11 = 1.12e7 ; 
K12 = 1.12e7 ; 
K13 = 5.04e6 ; 
Ke1 = 9.22e6 ; 
K21 = 1.13e8 ; 
K22 = 1.13e8 ; 
Ke2 = 2.48e7 ; 
K31 = 5.42e8 ; 
K32 = 5.42e8 ;
Ke3 = 7.46e7 ; 
K41 = 6.95e9 ; 
Ke4 = 2.7e8 ; 
K51 = 3.63e8 ;
K52 = 2.73e8 ;
Ke5 = 1.25e9 ;  
K61 = 3.30e8 ; 
K62 = 1.04e6 ; 


# Définition des rapports de réduction en rapport avec la dénomination choisie
r1 = 0.317 ; 
r2 = 0.313 ; 
r3 = 0.295 ; 
r4 = 0.388 ; 
r5 = 1 ; 

# Définition des variables pour ramener les inerties/raideurs d'un arbre i sur arbre 1 (r21 --> arbre 2 vers 1) 
r21 = r1**2 ;
r31 =(r1*r2)**2 ; 
r41 =(r1*r2*r3)**2 ;
r51 =(r1*r2*r3*r4)**2 ; 
r61 =(r1*r2*r3*r4*r5)**2 ;

# Définition de la matrice [M]
inertie = [[0 for j in range(0, 16)] for i in range(0, 16)]
inertie[0][0] = J11 ; 
inertie[1][1] = J12 ; 
inertie[2][2] = r21*J21 ; 
inertie[3][3] = r21*J22 ; 
inertie[4][4] = r21*J23 ; 
inertie[5][5] = r31*J33 ; 
inertie[6][6] = r31*J32 ; 
inertie[7][7] = r31*J31 ; 
inertie[8][8] = r41*J41 ; 
inertie[9][9] = r41*J42 ; 
inertie[10][10] = r51*J52 ; 
inertie[11][11] = r61*J62 ; 
inertie[12][12] = J13 ; 
inertie[13][13] = r51*J51 ; 
inertie[14][14] = r51*J53 ; 
inertie[15][15] = r61*J61 ; 
M = np.matrix(inertie) ;

# Définition de la matrice [K]
# Saisie des termes diagonaux
K_d = [[0 for j in range(0, 16)] for i in range(0, 16)]
K_d[0][0] = K11 + K12 ;
K_d[1][1] = K12 + K13 + Ke1 ; 
K_d[2][2] = Ke1 + r21*K21 ; 
K_d[3][3] = r21*(K21+K22) ; 
K_d[4][4] = r21*(K22+Ke2) ; 
K_d[5][5] = r21*Ke2 + r31*K32 ; 
K_d[6][6] = r31*(K31+K32) ; 
K_d[7][7] = r31*(K31+Ke3) ; 
K_d[8][8] = r31*Ke3 + r41*K41 ; 
K_d[9][9] = r41*(K41+Ke4) ; 
K_d[10][10] = r41*Ke4 + r51*(K51+K52+Ke5) ; 
K_d[11][11] = r51*Ke5 + r61*(K61+K62) ; 
K_d[12][12] = K13 ; 
K_d[13][13] = r51*K51 ; 
K_d[14][14] = r51*K52 ; 
K_d[15][15] = r61*K62 ; 

# Saisie des données de la partie triangulaire supérieure (sans ramification) 
K_sup = [[0 for j in range(0, 16)] for i in range(0, 16)]
K_sup[0][1] = -K12 ; 
K_sup[1][2] = -Ke1 ; 
K_sup[2][3] = -r21*K21 ; 
K_sup[3][4] = -r21*K22 ; 
K_sup[4][5] = -r21*Ke2 ; 
K_sup[5][6] = -r31*K32 ; 
K_sup[6][7] = -r31*K31 ; 
K_sup[7][8] = -r31*Ke3 ; 
K_sup[8][9] = -r41*K41 ; 
K_sup[9][10] = -r41*Ke4 ; 
K_sup[10][11] = -r51*Ke5 ; 

# Saisue des termes pour les ramifications dans la partie triangulaire supérieure
K_sup[1][12] = -K13 ; 
K_sup[10][13] = -r51*K51 ; 
K_sup[10][14] = -r51*K52 ; 
K_sup[11][15] = -r61*K61 ; 

# Création de la matrice K par sommation des termes diagonaux, supérieurs et inférieurs
K=np.matrix(K_d)+np.matrix(K_sup)+np.matrix(K_sup).getT() ;
# print(K)

res_matrix = open('matrix.txt', 'w')
for i in range(0, 16):
    for j in range(0, 15):
        res_matrix.write(str(K.item(i,j))+';')
    res_matrix.write(str(K.item(i,15))+'\n')
res_matrix.close()

'''
# Résolution du problème pour avoir valeur et vecteur propre
# [mode_propre, omega_carre]=eig(inv(M)*K) ;

# Calcul des pulsation propres 
# pulsation_propre = zeros(length(inertie), 1) ; 
# for i = 1:length(inertie)
#   pulsation_propre(i, 1) = abs(sqrt(omega_carre(i,i))) ; 
# end 

# %Conversion en frequence (passage de rad/s en Hz) 
# frequence_propre = 1/(2*pi) * pulsation_propre ;

# %Pseudo normalisation des vecteurs propres 
# for i = 1:length(inertie)
#   normalisateur = mode_propre(1, i) ;
#   for h = 1:length(inertie) 
#     mode_propre(h, i) = mode_propre(h, i) / normalisateur ; 
#   end 
# end 

# %Tri dans l'ordre des fréquences propres et mode propre 
# p=2 ; 
# while p>=1
#   p=0;
#   for i=1:size(frequence_propre)-1
#     if frequence_propre(i)>frequence_propre(i+1)
#       aux_vect = frequence_propre(i);
#       aux_mat = mode_propre( : , i) ; 
#       frequence_propre(i)= frequence_propre(i+1);
#       mode_propre(:, i) = mode_propre(:, i+1) ;
#       frequence_propre(i+1)= aux_vect;
#       mode_propre(:, i+1) = aux_mat ; 
#       p = p+1;
#     end 
#   end 
# end

# %Affichage des fréquences propres dans la fenêtre de commande
# fprintf('\n')
# for i=1:length(inertie)
#   fprintf('La frequence propre %d est : %f Hz\n', i, frequence_propre(i))
# end 

# %Affichage des modes propres dans la fenêtre de commande
# fprintf('\n')
# for i=1:length(inertie)
#   fprintf('Le mode propre %d est : (%4.2f, %4.2f, %4.2f, %4.2f, %4.2f, %4.2f, %4.2f, %4.2f, %4.2f, %4.2f, %4.2f, %4.2f, %4.2f, %4.2f, %4.2f, %4.2f)\n', i, mode_propre(1,i),mode_propre(2,i),mode_propre(3,i),mode_propre(4,i),mode_propre(5,i),mode_propre(6,i),mode_propre(7,i),mode_propre(8,i),mode_propre(9,i),mode_propre(10,i),mode_propre(11,i),mode_propre(12,i),mode_propre(13,i),mode_propre(14,i),mode_propre(15,i),mode_propre(16,i))
# end 
'''

# Calcul de la réponse en frequence avec amortissement
Mat_Fe = [0 for i in range(0, 16)] ; 
Mat_Fe[0] = 1 ; 
fmax = int(1.1*6800) ;
d = 0; 

Y = {}
for i in range(0,16):
    Y['{}'.format(i)] = []

for f in range(1,fmax):
  omega =2*3.1415*f ;
  B = K - omega*omega*M + 1j*K*d; 
  X = np.matmul(LA.inv(B),  Mat_Fe) ; 
  for i in range(0,16):
    Y['{}'.format(i)].append(abs(X.item(0,i))) ; 


figure = plt.figure(figsize=(10,5)) 
axes = figure.add_subplot(111)
axes.set_yscale('log')
axes.set_ylabel('Responce [rad]')
axes.set_xlabel('Pulsating [rad/s]')
for i in range(0,9):
    y = Y['{}'.format(i)]
    axes.plot(y, label=str(i))
        
# figure.legend()
figure.savefig('test.png')

'''
# Creation du vecteur abscisse
abscisse=zeros(fmax,1) ;
for f = 1:1:fmax
  abscisse(f) = f;
end 

%Affichage de la réponse en frequence dans deux figures pour ne surchager 
%le graphique
figure(1)
semilogy(abscisse, Yf(1,:), 'y') ; 
hold on ;
semilogy(abscisse, Yf(2,:), 'm') ; 
hold on ;
semilogy(abscisse, Yf(3,:), 'c') ; 
hold on ;
semilogy(abscisse, Yf(4,:), 'r') ; 
hold on ;
semilogy(abscisse, Yf(5,:), 'g') ; 
hold on ;
semilogy(abscisse, Yf(6,:), 'b') ; 
hold on ;
semilogy(abscisse, Yf(7,:), 'k') ; 
hold on ;
semilogy(abscisse, Yf(8,:), 'b--') ; 
hold on ; 

xlabel('Frequence[Hz]') ; 
ylabel('Amplitude[rad]'); 
title('Réponse en frequence avec amortissement') ; 
legend('X1', 'X2','X3','X4','X5','X6','X7','X8') ; 

figure(2)
semilogy(abscisse, Yf(9,:), 'y') ; 
hold on ;
semilogy(abscisse, Yf(10,:), 'm') ; 
hold on ;
semilogy(abscisse, Yf(11,:), 'c') ; 
hold on ;
semilogy(abscisse, Yf(12,:), 'r') ; 
hold on ;
semilogy(abscisse, Yf(13,:), 'g') ; 
hold on ;
semilogy(abscisse, Yf(14,:), 'b') ; 
hold on ;
semilogy(abscisse, Yf(15,:), 'k') ; 
hold on ;
semilogy(abscisse, Yf(16,:), 'b..') ; 

xlabel('Frequence[Hz]') ; 
ylabel('Amplitude[rad]'); 
title('Réponse en frequence avec amortissement') ; 
legend('X9', 'X10','X11','X12','X13','X14','X15','X16') ; 

%Affichage des amplitude max pour chaque inertie dans la fenêtre de commande
fprintf('\n')
for i=1:length(inertie)
    fprintf('Amplitude max pour %d est : %f rad\n', i, max(Yf(i, :)))
end 
'''