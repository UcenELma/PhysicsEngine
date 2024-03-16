import pygame
import random
import math

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
PARTICLE_RADIUS = 10
NUM_PARTICLES = 40  # Change this to 40

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Particle class with wall collisions
class WallCollisionParticle:
    def __init__(self, x, y, mass, color):
        self.x = x
        self.y = y
        self.radius = PARTICLE_RADIUS
        self.mass = mass
        self.color = color
        self.velocity = [random.uniform(-2, 2), random.uniform(-2, 2)]

    def update(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]

        # Particle-wall collisions
        if self.x - self.radius < 0 or self.x + self.radius > WIDTH:
            self.velocity[0] *= -1

        if self.y - self.radius < 0 or self.y + self.radius > HEIGHT:
            self.velocity[1] *= -1

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

# Create particles with wall collisions
particles = [
    WallCollisionParticle(random.uniform(PARTICLE_RADIUS, WIDTH - PARTICLE_RADIUS),
                          random.uniform(PARTICLE_RADIUS, HEIGHT - PARTICLE_RADIUS),
                          random.uniform(1, 5), random.choice([RED, BLUE])) for _ in range(NUM_PARTICLES)
]

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Colorful Particle Collisions")

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

    # Check for collisions and create new particles
    for i in range(len(particles) - 1):
        for j in range(i + 1, len(particles)):
            dx = particles[j].x - particles[i].x
            dy = particles[j].y - particles[i].y
            distance = math.sqrt(dx**2 + dy**2)

            if distance < particles[i].radius + particles[j].radius:
                # Collision occurred, create a new particle with a different color
                new_particle_color = (particles[i].color[0] + particles[j].color[0]) // 2, \
                                     (particles[i].color[1] + particles[j].color[1]) // 2, \
                                     (particles[i].color[2] + particles[j].color[2]) // 2
                new_particle = WallCollisionParticle(particles[i].x, particles[i].y,
                                                     particles[i].mass + particles[j].mass,
                                                     new_particle_color)
                particles.append(new_particle)

                # Remove collided particles
                particles.remove(particles[i])
                particles.remove(particles[j - 1])
                break

    # Draw background
    screen.fill(WHITE)

    # Draw particles
    for particle in particles:
        particle.draw(screen)

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()