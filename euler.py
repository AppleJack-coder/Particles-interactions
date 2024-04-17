from particles import Particles
import math
from typing import NoReturn


class Euler:
    def __init__(self, dt: int):
        self.dt = dt
        self.particles = Particles()


    def calc(self) -> NoReturn:
        """
        Calculates next coordinates and velocities of particles using Euler method
        """

        self.calc_coords()
        self.calc_velocities()


    def calc_coords(self) -> NoReturn:
        """
        Calculates new coordinates
        """

        for particle_number in range(self.particles.particles_amount):
            x0, y0 = self.particles.get_coords(particle_number)
            vx0, vy0 = self.particles.get_v(particle_number)
            
            x = x0 + vx0*self.dt
            y = y0 + vy0*self.dt

            # Save results
            self.particles.x_list[particle_number].append(x)
            self.particles.y_list[particle_number].append(y)


    def calc_velocities(self) -> NoReturn:
        """
        Calculates new velocities for next step
        """

        A = k
        for particle_number in range(self.particles.particles_amount):
            A*=self.particles.get_q(particle_number)

        # Lenght between 2 particles
        particle_1 = 0
        particle_2 = 1
        x1, y1 = self.particles.get_coords(particle_1)
        x2, y2 = self.particles.get_coords(particle_2)
        
        L = math.sqrt((x2-x1)**2 + (y2-y1)**2)

        # Force between 2 particles
        F = A/(L**2)

        for particle_number in range(self.particles.particles_amount):
            m = self.particles.get_m(particle_number)

            # Force projection on each axis
            if particle_number == 0:
                cos = (x2-x1)/L
                sin = (y2-y1)/L
            else:
                cos = (x1-x2)/L
                sin = (y1-y2)/L
            
            Fx = F*cos
            Fy = F*sin

            # Velocity projections
            dvx = (Fx/m)*self.dt
            dvy = (Fy/m)*self.dt

            # Save results
            self.particles.vx_list[particle_number].append(dvx)
            self.particles.vy_list[particle_number].append(dvy)


if __name__ == '__main__':
    dt = 10**(-16)
    n = 1000

    k = 9*10**(9)

    # Init conditions
    L = 10*10**(-9)
    p = 2*10**(-9)
    mp = 1.673*10**(-27)
    e = 1.6*10**(-19)

    # Creating solution
    euler = Euler(dt)

    # Adding particles
    euler.particles.add(m=64*mp, q=29*e, x0=0, y0=p, vx0=10**6, vy0=0)
    euler.particles.add(m=28*mp, q=14*e, x0=math.sqrt(L**2 - p**2), y0=0, vx0=0, vy0=0)

    # Calculate step
    euler.calc()
