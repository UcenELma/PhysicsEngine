import pygame
import random
import math
import sys

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
CUBE_SIZE = 300
PARTICLE_RADIUS = 20  # Increase the particle radius
NEUTRON_RADIUS = 5
NEUTRON_SPEED = 3

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Particle class
class Particle:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed = random.uniform(1, 2)
        self.angle = random.uniform(0, 2 * math.pi)

    def move(self):
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)
        self.confine_to_cube()

    def confine_to_cube(self):
        min_x = (WIDTH - CUBE_SIZE) // 2 + self.radius
        max_x = (WIDTH + CUBE_SIZE) // 2 - self.radius
        min_y = (HEIGHT - CUBE_SIZE) // 2 + self.radius
        max_y = (HEIGHT + CUBE_SIZE) // 2 - self.radius

        if self.x < min_x:
            self.x = min_x
            self.angle = math.pi - self.angle
        elif self.x > max_x:
            self.x = max_x
            self.angle = math.pi - self.angle

        if self.y < min_y:
            self.y = min_y
            self.angle = -self.angle
        elif self.y > max_y:
            self.y = max_y
            self.angle = -self.angle

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

# Neutron class
class Neutron:
    def __init__(self):
        self.x = random.randint((WIDTH - CUBE_SIZE) // 2, (WIDTH + CUBE_SIZE) // 2)
        self.y = random.randint((HEIGHT - CUBE_SIZE) // 2, (HEIGHT + CUBE_SIZE) // 2)
        self.radius = NEUTRON_RADIUS
        self.color = GREEN
        self.angle = random.uniform(0, 2 * math.pi)

    def move(self):
        self.x += NEUTRON_SPEED * math.cos(self.angle)
        self.y += NEUTRON_SPEED * math.sin(self.angle)
        self.confine_to_cube()

    def confine_to_cube(self):
        min_x = (WIDTH - CUBE_SIZE) // 2 + self.radius
        max_x = (WIDTH + CUBE_SIZE) // 2 - self.radius
        min_y = (HEIGHT - CUBE_SIZE) // 2 + self.radius
        max_y = (HEIGHT + CUBE_SIZE) // 2 - self.radius

        if self.x < min_x:
            self.x = min_x
            self.angle = math.pi - self.angle
        elif self.x > max_x:
            self.x = max_x
            self.angle = math.pi - self.angle

        if self.y < min_y:
            self.y = min_y
            self.angle = -self.angle
        elif self.y > max_y:
            self.y = max_y
            self.angle = -self.angle

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3D Cube Fission Simulation")
clock = pygame.time.Clock()

# Create a particle and a neutron
particle = Particle(WIDTH // 2, HEIGHT // 2, PARTICLE_RADIUS, RED)
neutron = Neutron()

# Function to handle fission
def fission(particle):
    if particle.radius > 5:
        for _ in range(2):
            new_particle = Particle(particle.x, particle.y, particle.radius // 2, BLUE)
            particles.append(new_particle)
        particles.remove(particle)

# Main loop
particles = [particle]
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)

    # Draw cube
    cube_top_left = (WIDTH - CUBE_SIZE) // 2, (HEIGHT - CUBE_SIZE) // 2
    pygame.draw.rect(screen, RED, (*cube_top_left, CUBE_SIZE, CUBE_SIZE), 1)

    # Update and draw particles
    for particle in particles:
        particle.move()
        particle.draw(screen)

    # Move and draw neutron
    neutron.move()
    neutron.draw(screen)

    # Check for collision and fission
    for particle in particles:
        distance = math.hypot(neutron.x - particle.x, neutron.y - particle.y)
        if distance < neutron.radius + particle.radius:
            fission(particle)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
