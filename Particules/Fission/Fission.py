import pygame
import random
import math
import sys

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
PARTICLE_RADIUS = 8
SQUARE_SIZE = 300  # Size of the square in which particles are confined

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Particle class for fission simulation
class Particle:
    def __init__(self, x, y, radius, color, speed):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.angle = random.uniform(0, 2 * math.pi)
        self.speed = speed

    def update(self):
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)

        # Collision with square boundaries
        left_boundary = (WIDTH - SQUARE_SIZE) // 2 + self.radius
        right_boundary = (WIDTH + SQUARE_SIZE) // 2 - self.radius
        top_boundary = (HEIGHT - SQUARE_SIZE) // 2 + self.radius
        bottom_boundary = (HEIGHT + SQUARE_SIZE) // 2 - self.radius

        if self.x < left_boundary or self.x > right_boundary:
            self.angle = math.pi - self.angle
        if self.y < top_boundary or self.y > bottom_boundary:
            self.angle = -self.angle

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fission Particle Simulation")

# Create initial particle
particles = [Particle(WIDTH // 2, HEIGHT // 2, PARTICLE_RADIUS, GREEN, 3)]

# Main loop
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update particles
    new_particles = []
    for particle in particles:
        particle.update()

        # Create new particles (simplified fission)
        if random.random() < 0.01:
            new_particle = Particle(particle.x, particle.y, particle.radius, GREEN, particle.speed)
            new_particle.angle = particle.angle + math.pi / 2
            new_particles.append(new_particle)

    particles.extend(new_particles)

    # Draw background
    screen.fill(WHITE)

    # Draw square
    square_top_left = ((WIDTH - SQUARE_SIZE) // 2, (HEIGHT - SQUARE_SIZE) // 2)
    pygame.draw.rect(screen, GREEN, (*square_top_left, SQUARE_SIZE, SQUARE_SIZE), 1)

    # Draw particles
    for particle in particles:
        particle.draw(screen)

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

pygame.quit()
sys.exit()
