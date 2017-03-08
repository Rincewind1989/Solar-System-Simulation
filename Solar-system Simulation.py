import random
import time
import numpy as np
import pygame

# WIDTH and HEIGHT of the Solarsystem
WIDTH = 900
HEIGHT = 600

# Gravitational Constant
G = 1.e2

# Time-Step
delta_time = 0.01

# Seed the Random engine with time
random.seed(time.time())

# List of all Planets
list_of_planets = []

# Defining the Planet Class
class Planet():

    # Initiliazing the Position, Velocity, Density and Radius of the Planet
    # The first Index-Entry is the actual Position and Velocity
    # The other Index-Entries are for the Runge-Kutta Solution
    def __init__(self):
        self._x_position = [random.randrange(0, WIDTH), 0, 0, 0]
        self._x_velocity = [random.randrange(-40, 40, 1), 0, 0, 0]
        self._x_acceleration = [0, 0, 0, 0]
        self._y_position = [random.randrange(0, HEIGHT), 0, 0, 0]
        self._y_velocity = [random.randrange(-40, 40, 1), 0, 0, 0]
        self._y_acceleration = [0, 0, 0, 0]
        self._mass = random.randrange(1, 3)
        self._density = random.randrange(1, 10)/10
        self.setRadiusFromMass()

    # Prints the Properties of this Planet
    def __repr__(self):
        print('Properties of Planet: (x-coordinate=%s, y-coordinate=%s, x-velocity=%s, y-velocity=%s, density=%s, radius=%s)' % (self._x_position, self._y_position, self._x_velocity, self._y_velocity, self._density, self._radius))

    # Defining the mass from the radius and the density
    def setMassFromRadius(self):
        self._mass = 4/3 * np.pi * self._radius**3 * self._density

    # Defining the radius from the mass and the density
    def setRadiusFromMass(self):
        self._radius = (3.*self._mass/(self._density*4.*np.pi))**0.33333

    # Defining the Initial Acceleration of this time-step by accumulating all forces on this Planet by other Objects
    def acceleration(self, step):
        for planet in list_of_planets:
            if planet == self:  #Planet doesn´t have force on itself
                continue
            else:
                x_distance = planet._x_position[0] - self._x_position[step]
                y_distance = planet._y_position[0] - self._y_position[step]
                sq_distance = abs(x_distance**2 + y_distance**2)
                distance = abs(np.sqrt(sq_distance))
                gravitational_force = G * planet._mass/sq_distance
                self._x_acceleration[step] += gravitational_force * x_distance/distance
                self._y_acceleration[step] += gravitational_force * y_distance/distance
        return (self._x_acceleration[step], self._y_acceleration[step])

    # Total Velocity after Runge-Kutta
    def velocity_after_runge_step(self):
        self._x_velocity[0] += delta_time / 6 * ( self._x_acceleration[0] + 2 * (self._x_acceleration[1] + (self._x_acceleration[2])) + self._x_acceleration[3])
        self._y_velocity[0] += delta_time / 6 * ( self._y_acceleration[0] + 2 * (self._y_acceleration[1] + (self._y_acceleration[2])) + self._y_acceleration[3])

    # Total Position after Runge-Kutta
    def position_after_runge_step(self):
        self._x_position[0] += delta_time/6 * (self._x_velocity[0] + 2 * (self._x_velocity[1] + self._x_velocity[2]) + self._x_velocity[3])
        self._y_position[0] += delta_time/6 * (self._y_velocity[0] + 2 * (self._y_velocity[1] + self._y_velocity[2]) + self._y_velocity[3])

    # Runge-Kutta-4th-Order Method to calculate the velocity and position of the next time-step
    def update_planet(self):

        # Sets the acceleration to 0 for the start of the calulation. Must be done,
        # because the Function "acceleration" adds to the acceleration to add every force from every object
        # So the acceleration is never reset inside its calculation
        self._x_acceleration[0], self._y_acceleration[0] = 0, 0

        # Initial Conditions (Initial Velocities and Positions are safed in the first Index of the Lists)
        self._x_acceleration[0], self._y_acceleration[0] = self.acceleration(0)

        # Runge-Kutta-Step
        for step in range(0, 3):
            if step != 2:
                delta_delta_time = 0.5
            else:
                delta_delta_time = 1.0

            # Runge-Step to calculate the Position
            self._x_position[step + 1] = self._x_position[0] + self._x_velocity[step] * delta_time * delta_delta_time
            self._y_position[step + 1] = self._y_position[0] + self._y_velocity[step] * delta_time * delta_delta_time

            # Runge-Step to calculate the Velocity
            self._x_velocity[step + 1] = self._x_velocity[step] + self._x_acceleration[step] * delta_time * delta_delta_time
            self._y_velocity[step + 1] = self._y_velocity[step] + self._y_acceleration[step] * delta_time * delta_delta_time

            # Runge-Step to calculate the Acceleration at the new position
            self._x_acceleration[step + 1], self._y_acceleration[step + 1] = self.acceleration(step)

        # Sums up the arithmetic mean of the accelerations and velocities and calculates the new velocity and position
        self.velocity_after_runge_step()
        self.position_after_runge_step()

    # Draws a circle for every planet at its position
    def circle_drawing(self, window):
        pygame.draw.circle(window, (255, 255, 255), (int(self._x_position[0]), int(self._y_position[0])), int(self._radius), 0)


def planet_creation():

    # Lets the user input the number of planets the solar system should have
    number_planets = int(input("How many Planets should there be?:"))
    # Creates the planets with random positions and random velocities
    for planets in range(0, number_planets):
        list_of_planets.append(Planet())

def esc_key_pressed():

    # Sees if the ESC-Key is pressed
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
    return True


def main():

    # Initializing pygame
    pygame.init()

    # Creates the sun
    sun = Planet()
    sun._x_position[0] = WIDTH/2
    sun._y_position[0] = HEIGHT/2
    sun._x_velocity[0] = 0
    sun._y_velocity[0] = 0
    sun._mass = 10000
    sun._density = 1.
    sun.setRadiusFromMass()
    list_of_planets.append(sun)

    # Information for and from the user
    print("Hello Spacetraveler. Ready to construct your own solar-system?")
    print("With Esc you can always abort the whole Simulation!")
    planet_creation()

    # Creates a window
    window = pygame.display.set_mode((WIDTH, HEIGHT))

    # Simulation is running equals True
    simulation_running = True

    # Loops the entire simulation until the ESC-Key is pressed
    while simulation_running:

        #Updates the window
        pygame.display.flip()

        # Updates the Planets and draws them
        for planet in list_of_planets:
            if planet != sun:
                planet.update_planet()
            planet.circle_drawing(window)

        # Looks if the esc-key is pressed
        simulation_running = esc_key_pressed()

        # Waits for an amount of time to process
        pygame.time.wait(int(1/(delta_time * 24)))



#Starts the Simulation
main()
