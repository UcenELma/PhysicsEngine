import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

# Potentiel d'interaction :
def g(r):
    return 1 / (r ** 2 + 1)

# Modèle de Cucker Smale en dimension 3 :
def Cucker_Smale3D(x, y, z, vx, vy, vz, dt, lamda):
    N = len(x)

    # Xi−Xj
    xdiff = np.tile(x, (N, 1)) - np.tile(x, (N, 1)).T
    ydiff = np.tile(y, (N, 1)) - np.tile(y, (N, 1)).T
    zdiff = np.tile(z, (N, 1)) - np.tile(z, (N, 1)).T
    normeXdiff = np.sqrt(xdiff ** 2 + ydiff ** 2 + zdiff ** 2)

    # Vj−Vi
    vxdiff = np.tile(vx, (N, 1)) - np.tile(vx, (N, 1)).T
    vydiff = np.tile(vy, (N, 1)) - np.tile(vy, (N, 1)).T
    vzdiff = np.tile(vz, (N, 1)) - np.tile(vz, (N, 1)).T

    # r évalué en Xi−Xj H = g(normeXdiff)
    H = g(normeXdiff)

    # x(t + dt)
    x += dt * vx
    y += dt * vy
    z += dt * vz

    # Les particules restent dans la boîte x = x % lim
    y = y % lim
    z = z % lim

    # v(t + dt)
    vx += (np.sum(vxdiff * H, axis=1) / N) * dt * lamda
    vy += (np.sum(vydiff * H, axis=1) / N) * dt * lamda
    vz += (np.sum(vzdiff * H, axis=1) / N) * dt * lamda

    return x, y, z, vx, vy, vz

# Nombre de particules
N = 100
lim = 100
x = np.random.rand(N) * lim
y = np.random.rand(N) * lim
z = np.random.rand(N) * lim
vx = np.random.rand(N)
vy = np.random.rand(N)
vz = np.random.rand(N)
dt = 0.1
lamda = 0.5

# Création de la figure 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Ajouter des flèches dans les points qui indiquent la direction (avec une taille triplée)
quiver = ax.quiver(x, y, z, vx, vy, vz, color='blue', length=4.5, normalize=True, arrow_length_ratio=0.5)

# Ajout d'une annotation pour la vitesse moyenne
text_annotation = ax.text2D(0.5, 0.95, '', transform=ax.transAxes, ha='center')

# Fonction d'animation
def update(frame):
    global x, y, z, vx, vy, vz, quiver
    x, y, z, vx, vy, vz = Cucker_Smale3D(x, y, z, vx, vy, vz, dt, lamda)

    # Mettre à jour les données des flèches
    quiver.remove()
    quiver = ax.quiver(x, y, z, vx, vy, vz, color='blue', length=4.5, normalize=True, arrow_length_ratio=0.5)

    vitesse_moyenne = np.sqrt(np.mean(vx)**2 + np.mean(vy)**2 + np.mean(vz)**2)
    text_annotation.set_text(f'Vitesse moyenne: {vitesse_moyenne:.2f}')

# Animation
ani = FuncAnimation(fig, update, frames=100, interval=50)

# Affichage de l'animation
plt.show()



