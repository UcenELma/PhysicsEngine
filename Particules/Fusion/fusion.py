import pygame
import random
import math
import sys

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
SQUARE_SIZE = 300  # Size of the square in which particles are confined

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Particle class for fusion simulation
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
pygame.display.set_caption("Fusion Particle Simulation")

# Create initial particles within the square
square_left = (WIDTH - SQUARE_SIZE) // 2
square_top = (HEIGHT - SQUARE_SIZE) // 2
particles = [Particle(random.randint(square_left + 50, square_left + SQUARE_SIZE - 50), random.randint(square_top + 50, square_top + SQUARE_SIZE - 50), 8, BLUE, 3),
             Particle(random.randint(square_left + 50, square_left + SQUARE_SIZE - 50), random.randint(square_top + 50, square_top + SQUARE_SIZE - 50), 8, BLUE, 3)]

# Main loop
clock = pygame.time.Clock()
running = True
fusion_triggered = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update particles
    for particle in particles:
        particle.update()

    # Draw background
    screen.fill(WHITE)

    # Draw square
    pygame.draw.rect(screen, BLUE, (square_left, square_top, SQUARE_SIZE, SQUARE_SIZE), 1)

    # Draw particles
    for particle in particles:
        particle.draw(screen)

    # Check for fusion when particles collide
    if not fusion_triggered and pygame.Rect.colliderect(pygame.Rect(particles[0].x - particles[0].radius, particles[0].y - particles[0].radius, particles[0].radius*2, particles[0].radius*2),
                                                        pygame.Rect(particles[1].x - particles[1].radius, particles[1].y - particles[1].radius, particles[1].radius*2, particles[1].radius*2)):
        # Fusion event (combine particles)
        particles[0].color = RED  # Change color to indicate fusion
        particles[0].radius += particles[1].radius
        particles.pop(1)
        fusion_triggered = True  # Set the flag to avoid repeated fusion events

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

pygame.quit()
sys.exit()
