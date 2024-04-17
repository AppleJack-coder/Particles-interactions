from typing import NoReturn, Tuple


class Particles:
    def __init__() -> NoReturn:
        self.m_list = []
        self.q_list = []
        self.x_list = []
        self.y_list = []
        self.vx_list = []
        self.vy_list = []
        
        self.particles_amount = 0


    def add(m: float, q: float, x0: float, y0: float, vx0: float, vy0: float) -> NoReturn:
        """
        Adds new particle to equation

        Parameters
        ----------
        m: float
            The mass of particle
        q: float
            Particle charge
        x0: float
            Start x coordinate
        y0: float
            Start y coordinate
        vx0: float
            Start x velocity
        vy0: float
            Start y velocity
        """

        self.m_list.append([m])
        self.q_list.append([q])
        self.x_list.append([x0])
        self.y_list.append([y0])
        self.vx_list.append([vx0])
        self.vy_list.append([vy0])

        self.particles_amount+=1


    def get_m(particle_number: int) -> float:
        """
        Returns mass of particle

        Parameters
        ----------
        particle_number: int
            Particle number
        
        Returns
        -------
        m: float
            Mass of particle
        """

        m = self.m_list[particle_number]
        return m


    def get_q(particle_number: int) -> float:
        """
        Returns charge of particle

        Parameters
        ----------
        particle_number: int
            Particle number

        Returns
        -------
        q: float
            Charge of particle
        """

        q = self.q_list[particle_number]
        return q

    
    def get_coords(particle_number: int) -> Tuple[float, float]:
        """
        Returns particle's last coordinates

        Parameters
        ----------
        particle_number: int
            Particle number

        Returns
        -------
        coords: Tuple[float, float]
            Particle's last coords
        """

        coords = (self.x_list[particle_number][-1], self.y_list[particle_number][-1])
        return coords

    
    def get_v(particle_number: int) -> Tuple[float, float]:
        """
        Returns particle's last velocity projections on each axis

        Parameters
        ----------
        particle_number: int
            Particle number

        Returns
        -------
        v: Tuple[float, float]
            Particle's last velocity projections
        """

        v = (self.vx_list[particle_number][-1], self.xy_list[particle_number][-1])
        return v
