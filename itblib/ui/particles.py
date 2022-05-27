"""
Contains some Particle Spawners, used to create Particles that e.g.
have a colour, travel direction, spawn rate etc.
"""
from typing import TYPE_CHECKING

import pygame
from itblib.ui.widgets.ui_widget import Widget
import random

if TYPE_CHECKING:
    from typing import Generator

def get_color_from_gradients(lifetime:float, gradients:list[tuple[int,int,int,int]]):
    """
    Get the color at a certain time (>=0.0, <1.0), interpolated between the closest gradients.
    @lifetime: The amount of time that has passed for a particle
    @gradients: The gradients to use as interpolation points. Must be at least 2, with dim=4
    """
    assert lifetime >= 0 and lifetime <1
    gradient_dim = 4
    index_float = lifetime*(len(gradients)-1)
    start = int(index_float)
    end = int(index_float+1)
    g_1 = gradients[start]
    g_2 = gradients[end]
    timestep = 1/(len(gradients)-1)
    timestep_progress = (lifetime % timestep)
    timestep_progress_scaled = timestep_progress / timestep #scaled from 0-1
    #mix color a and b by weights from 0 to 1
    interp = tuple([
        int(g_1[x]*(1.0-timestep_progress_scaled) + g_2[x]*timestep_progress_scaled)
        for x in range(gradient_dim)])
    return interp


class ParticleSpawner(Widget):
    """
    Base Class for the other ParticleSpawners.
    A Widget capable of spawning particles, i.e. to produce some VFX.
    """
    #TODO: Add base class behviour
    def get_blits(self) -> "Generator[tuple[pygame.Surface, pygame.Rect, pygame.Rect]]":
        return super().get_blits()

    def update(self, delta_time:float):
        """Update the particles."""


class FireParticleSpawner(ParticleSpawner):
    """Creates fiery particles in a set area."""
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((64,64)).convert_alpha()
        self.image.fill(0)
        self.desired_particles = 40
        self.fire_left = 16
        self.fire_right = 48
        self.max_particle_lifetime = 5
        self.particle_xs        = [None] * self.desired_particles
        self.particle_ys        = [None] * self.desired_particles
        self.particle_lifetimes = [self.max_particle_lifetime+1] * self.desired_particles

    def update(self, delta_time:float):
        """Update the particles."""
        self.image.fill(0)
        for particle_index in range(self.desired_particles):
            self.particle_lifetimes[particle_index] += delta_time
            if self.particle_lifetimes[particle_index] > self.max_particle_lifetime:
                self.particle_lifetimes[particle_index] = random.random()*self.max_particle_lifetime
                x_pos = random.randint(self.fire_left,self.fire_right)
                ydiv = 16 - abs((self.fire_left + self.fire_right)/2 - x_pos)
                self.particle_xs[particle_index] = x_pos
                self.particle_ys[particle_index] = 28 - random.randint(-ydiv, ydiv)
                continue
            if random.random() < delta_time*3:
                self.particle_xs[particle_index] += (random.randint(-1,1)+random.randint(0,2))
            self.particle_ys[particle_index] -= 1 if random.random() < delta_time*self.max_particle_lifetime else 0
        for particle_index in range(self.desired_particles):
            self.image.fill(
                get_color_from_gradients(
                    self.particle_lifetimes[particle_index]/self.max_particle_lifetime,
                    [(255,255,000,255), (255,000,000,255), (100,0,0,255), (0,0,0,0)]
                ),
                (self.particle_xs[particle_index], self.particle_ys[particle_index], 3, 3)
            )

class TrailParticleSpawner(ParticleSpawner):
    """Creates tiny sparks in close proximity. Use as a trail for projectiles."""
    def __init__(self):
        super().__init__()
        self.desired_particles = 20
        self.max_particle_lifetime = .7
        self.particle_size = (1,1)
        self.particle_xs        = [None] * self.desired_particles
        self.particle_ys        = [None] * self.desired_particles
        self.particle_lifetimes = [self.max_particle_lifetime+1] * self.desired_particles
        self.particles:list[pygame.Surface] = [pygame.Surface(self.particle_size)] * self.desired_particles
        self.update(0)

    def update(self, delta_time:float):
        """Update the particles."""
        for particle_index in range(self.desired_particles):
            self.particle_lifetimes[particle_index] += delta_time
            if self.particle_lifetimes[particle_index] > self.max_particle_lifetime:
                self.particle_lifetimes[particle_index] = random.random()*self.max_particle_lifetime
                self.particle_xs[particle_index] = self.position.x
                self.particle_ys[particle_index] = self.position.y
                self.particles[particle_index].fill((155,255,255))
                continue
            if random.random() < delta_time*3:
                self.particle_xs[particle_index] += random.randint(-1,1)
                self.particle_ys[particle_index] += random.randint(-2,2)

    def get_blits(self) -> "Generator[tuple[pygame.Surface, pygame.Rect, pygame.Rect]]":
        for i, p_surf in enumerate(self.particles):
            x,y = self.particle_xs[i], self.particle_ys[i]
            yield (p_surf, pygame.Rect(x,y,*self.particle_size), pygame.Rect(0,0,*self.particle_size))
