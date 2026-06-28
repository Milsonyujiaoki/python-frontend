"""Particle system for Kivy animations.

Provides particle effects for level-up celebrations and other visual feedback.
"""

from kivy.graphics import Canvas, Color, Ellipse, Rectangle
from kivy.properties import NumericProperty, ListProperty
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.vector import Vector
import random


class Particle(Widget):
    """Single particle with physics."""

    x = NumericProperty(0)
    y = NumericProperty(0)
    size = NumericProperty(10)
    color = ListProperty([1, 1, 1, 1])
    velocity = ListProperty([0, 0])
    life = NumericProperty(1.0)
    decay = NumericProperty(0.02)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            Color(*self.color)
            self._shape = Ellipse(pos=(self.x, self.y), size=(self.size, self.size))

    def update(self, dt):
        """Update particle physics."""
        # Update position
        self.x += self.velocity[0] * dt * 60
        self.y += self.velocity[1] * dt * 60

        # Apply gravity
        self.velocity[1] -= 50 * dt

        # Decay life
        self.life -= self.decay
        self.color[3] = self.life  # Alpha based on life

        # Update visual
        self._shape.pos = (self.x, self.y)
        self._shape.size = (self.size * self.life, self.size * self.life)

        # Mark for removal when dead
        return self.life > 0


class ParticleSystem(Widget):
    """Particle system emitter for effects like level-up."""

    particle_count = NumericProperty(50)
    particle_size = NumericProperty(15)
    particle_decay = NumericProperty(0.015)
    colors = ListProperty([
        [1, 0.84, 0, 1],   # Gold
        [1, 0.49, 0, 1],   # Orange
        [1, 0.2, 0.6, 1],  # Pink
        [0.2, 0.6, 1, 1],  # Blue
        [0.4, 1, 0.2, 1],  # Green
    ])
    spread = NumericProperty(100)
    gravity = NumericProperty(200)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.particles = []
        self._anim_bind = None
        Clock.schedule_interval(self.update_particles, 1/60)

    def update_particles(self, dt):
        """Update all particles and remove dead ones."""
        alive = []
        for p in self.particles:
            if p.update(dt):
                alive.append(p)
        self.particles = alive

    def emit(self, x=None, y=None):
        """Emit particles from a point.

        Args:
            x: X position (centers if None).
            y: Y position (centers if None).
        """
        target_x = x or self.center_x
        target_y = y or self.center_y

        for i in range(self.particle_count):
            angle = random.uniform(0, 2 * 3.14159)
            speed = random.uniform(50, 150)

            particle = Particle(
                x=target_x,
                y=target_y,
                size=self.particle_size,
                color=random.choice(self.colors),
                velocity=[
                    speed * (angle.__class__(0).__name__),  # random direction
                    speed * random.uniform(0.5, 1.5)
                ],
                decay=self.particle_decay,
            )
            # Correct velocity calculation
            particle.velocity = [
                speed * random.uniform(-1, 1),
                speed * random.uniform(0.5, 1.5)
            ]
            self.add_widget(particle)
            self.particles.append(particle)

    def emit_explosion(self, x=None, y=None):
        """Emit particles in explosion pattern (outward radial)."""
        target_x = x or self.center_x
        target_y = y or self.center_y

        for i in range(self.particle_count):
            angle = random.uniform(0, 2 * 3.14159)
            speed = random.uniform(100, 200)

            particle = Particle(
                x=target_x,
                y=target_y,
                size=self.particle_size,
                color=random.choice(self.colors),
                velocity=[
                    speed * 1.5 * (__import__('math').cos(angle)),
                    speed * 1.5 * (__import__('math').sin(angle))
                ],
                decay=self.particle_decay * 1.5,
            )
            self.add_widget(particle)
            self.particles.append(particle)

    def emit_confetti(self, x=None, y=None):
        """Emit confetti-style particles (upward with flutter)."""
        target_x = x or self.center_x
        target_y = y or self.center_y

        for i in range(self.particle_count):
            particle = Particle(
                x=target_x + random.uniform(-self.spread/2, self.spread/2),
                y=target_y,
                size=random.uniform(self.particle_size/2, self.particle_size),
                color=random.choice(self.colors),
                velocity=[
                    random.uniform(-30, 30),
                    random.uniform(150, 250)
                ],
                decay=self.particle_decay * 0.8,
            )
            self.add_widget(particle)
            self.particles.append(particle)

    def clear(self):
        """Remove all particles."""
        for p in self.particles[:]:
            self.remove_widget(p)
        self.particles.clear()

    def stop(self):
        """Stop the particle system."""
        if self._anim_bind:
            Clock.unschedule(self.update_particles)
        self.clear()


class LevelUpParticleSystem(ParticleSystem):
    """Specialized particle system for level-up effects."""

    def __init__(self, **kwargs):
        super().__init__(
            particle_count=80,
            particle_size=20,
            colors=[
                [1, 0.84, 0, 1],   # Gold
                [1, 0.7, 0, 1],    # Bronze
                [1, 0.9, 1, 1],    # Platinum
            ],
            **kwargs
        )

    def trigger_level_up(self, x=None, y=None):
        """Trigger level-up particle effect."""
        self.emit_confetti(x, y)

    def trigger_unlock(self, x=None, y=None):
        """Trigger unlock/explosion effect."""
        self.emit_explosion(x, y)


__all__ = ['Particle', 'ParticleSystem', 'LevelUpParticleSystem']