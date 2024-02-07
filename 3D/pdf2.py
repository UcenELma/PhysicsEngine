import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Potentiel d'interaction :
def g(r):
    return 1 / (r**2 + 1)

# Modèle de Cucker Smale en dimension 2 :
def Cucker_Smale2D(x, y, vx, vy, dt, lamda):
    N = len(x)

    # Xi−Xj
    xdiff = np.tile(x, (N, 1)) - np.tile(x, (N, 1)).T
    ydiff = np.tile(y, (N, 1)) - np.tile(y, (N, 1)).T
    normeXdiff = np.sqrt(xdiff**2 + ydiff**2)

    # Vj−Vi
    vxdiff = np.tile(vx, (N, 1)) - np.tile(vx, (N, 1)).T
    vydiff = np.tile(vy, (N, 1)) - np.tile(vy, (N, 1)).T

    # r évalué en Xi−Xj H = g(normeXdiff)
    H = g(normeXdiff)

    # x(t + dt)
    x += dt * vx
    y += dt * vy

    # Les particules restent dans la boîte x = x % lim
    y = y % lim

    # v(x + dt)
    vx += (np.sum(vxdiff * H, axis=1) / N) * dt * lamda
    vy += (np.sum(vydiff * H, axis=1) / N) * dt * lamda

    return x, y, vx, vy

# Nombre de particules
N = 100

# Limite de la boîte
lim = 100

# Positions initiales aléatoires
x = np.random.rand(N) * lim
y = np.random.rand(N) * lim

# Vitesses initiales aléatoires
vx = np.random.rand(N)
vy = np.random.rand(N)

# Pas de temps
dt = 0.1

# Facteur d'influence
lamda = 0.5

# Création de la figure
fig, ax = plt.subplots()
ax.set_xlim(0, lim)
ax.set_ylim(0, lim)

# Initialisation des éléments de la trame
quiver = ax.quiver(x, y, vx, vy, scale=20, color='blue', width=0.007)
scatter = ax.scatter(x, y, color='red')
annotations = [ax.annotate(f'{i+1}', (x[i], y[i]), textcoords="offset points", xytext=(0, 5), ha='center') for i in range(N)]
vitesse_annotation = ax.annotate('', xy=(0.5, 1.02), xycoords='axes fraction', ha='center')

# Fonction d'animation
def update(frame):
    global x, y, vx, vy, quiver, scatter, annotations, vitesse_annotation
    x, y, vx, vy = Cucker_Smale2D(x, y, vx, vy, dt, lamda)
    quiver.remove()
    scatter.remove()
    for annotation in annotations:
        annotation.remove()
    quiver = ax.quiver(x, y, vx, vy, scale=20, color='blue', width=0.007)
    scatter = ax.scatter(x, y, color='red')
    annotations = [ax.annotate(f'{i+1}', (x[i], y[i]), textcoords="offset points", xytext=(0, 5), ha='center') for i in range(N)]
    vitesse_moyenne = np.sqrt(np.mean(vx)**2 + np.mean(vy)**2)
    vitesse_annotation.set_text(f'Vitesse moyenne: {vitesse_moyenne:.2f}')

# Animation
ani = FuncAnimation(fig, update, frames=100, interval=50)

# Affichage de la vidéo
plt.show()
