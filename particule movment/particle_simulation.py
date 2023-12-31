import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
PARTICLE_RADIUS = 8  # Change particle radius
NUM_PARTICLES = 100
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)  # Change color to blue

# Particle class
class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = PARTICLE_RADIUS
        self.color = BLUE  # Change color to blue
        self.velocity = [random.uniform(-2, 2), random.uniform(-2, 2)]

    def update(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]

        # Collisions with walls
        if self.x - self.radius < 0 or self.x + self.radius > WIDTH:
            self.velocity[0] *= -1
        if self.y - self.radius < 0 or self.y + self.radius > HEIGHT:
            self.velocity[1] *= -1

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Particle Simulation")

# Create particles
particles = [Particle(random.randint(PARTICLE_RADIUS, WIDTH - PARTICLE_RADIUS),
                      random.randint(PARTICLE_RADIUS, HEIGHT - PARTICLE_RADIUS))
             for _ in range(NUM_PARTICLES)]

# Main loop
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update particles
    for particle in particles:
        particle.update()

    # Draw background
    screen.fill(WHITE)  # Change background color to white

    # Draw particles
    for particle in particles:
        particle.draw(screen)

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
