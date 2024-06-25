"""Simulate microstructure evolution using the Ising model.

Animate evolution of a 2 component system discretized into a 2D h x w
array. Each site of the system has a state of as 0 or 1. The total
energy of the system is influenced by each site's neighbours. A site is
randomly chosen to change state, where the change in energy of the
system influences the probability of the change occuring.
"""

from copy import deepcopy
from math import exp
from random import random, randint


# Type definitions

State = int
# State is a value of either 0 or 1
# Represents the one of the two components in the system
# Examples:
#   st_0 = 0
#   st_1 = 1

Site = tuple[int, int]
# Site is (int, int)
# Represents the column and row of the site of a system
# Example:
#   site_0 = (0, 0)
#   site_1 = (20, 20)

System = list[list[State]]
# System is a list containing a list of State
# 2D grid of states of h x w sites of some state. State[i] refers to
# vertical dimension containing h rows and returns list[State].
# Examples:
#   h = 3, w = 3
#   sys_0 = [[0, 0, 0],
#            [0, 0, 0],
#            [0, 0, 0]]
#
#   h = 3, w = 4
#   sys_1 = [[1, 0, 0, 1],
#            [0, 0, 0, 1],
#            [0, 0, 0, 1]]


# Function definitions

def intialize_system(h: int, w: int) -> System:
    """Create system of size h x w where each site has a random State"""

    sys = []
    if h==0 or w==0:
        return sys

    for row in range(0, h):
        sys.append([])
        for col in range(0, w):
            sys[-1].append(randint(0,1))

    return sys


def random_site(h: int, w: int) -> Site:
    """Pick a random site from system of size h x w"""

    return (randint(0,h-1), randint(0,w-1))


def random_state() -> State:
    """Produces random state"""
    return randint(0,1)


def energy_difference(sys: System, site: Site) -> int:
    """Energy difference for site swapping state"""

    spin_old = sys[site[1]][site[0]]
    spin_new = not spin_old

    likes_old = like_neighbours(sys, site, spin_old)
    likes_new = like_neighbours(sys, site, spin_new)

    delta_E = likes_old - likes_new

    return delta_E


def like_neighbours(sys: System, site: Site, state: State) -> int:
    """Counts number of nearest neigbours around site with same state"""

    neighbours = neighbour_states(sys, site)

    return neighbours.count(state)


def neighbour_states(sys: System, site: Site) -> list[State]:
    """Neighbours around a given site, adjusted for bounaries"""

    h = len(sys) - 1
    w = len(sys[0]) - 1

    (x,y) = site

    # Remeber: sys is nested list
    # Correct coords are sys[y,x] for site (x,y)

    # Top left corner
    if (x,y) == (0,0):
        return [
            sys[0  ][1  ],
            sys[1  ][0  ],
            sys[1  ][1  ]
            ]
        
    # Top right corner
    if (x,y) == (w,0):
        return [
            sys[0  ][w-1],
            sys[1  ][w-1],
            sys[1  ][w  ]
            ]
        
    # Bottom left corner
    if (x,y) == (0,h):
        return [
            sys[h-1][0  ],
            sys[h-1][1  ],
            sys[h  ][1  ]
            ]

    # Bottom right corner
    if (x,y) == (w,h):
        return [
            sys[h-1][w-1],
            sys[h-1][w  ],
            sys[h  ][w-1]
            ]

    # Top edge
    if y == 0:
        return [
            sys[0  ][x-1],
            sys[0  ][x+1],
            sys[1  ][x-1],
            sys[1  ][x  ],
            sys[1  ][x+1]
            ]

    # Bottom edge
    if y == h:
        return [
            sys[h-1][x-1],
            sys[h-1][x  ],
            sys[h-1][x+1],
            sys[h  ][x-1],
            sys[h  ][x+1]
            ]

    # Left edge
    if x == 0:
        return [
            sys[y-1][0  ],
            sys[y-1][1  ],
            sys[y  ][1  ],
            sys[y+1][0  ],
            sys[y+1][1  ]
            ]
        
    # Right edge
    if x == w:
        return [
            sys[y-1][w-1],
            sys[y-1][w  ],
            sys[y  ][w-1],
            sys[y+1][w-1],
            sys[y+1][w  ]
            ]
        
    # Non-boundary
    return [
        sys[y-1][x-1],
        sys[y-1][x  ],
        sys[y-1][x+1],
        sys[y  ][x-1],
        sys[y  ][x+1],
        sys[y+1][x-1],
        sys[y+1][x  ],
        sys[y+1][x+1]
        ]


def successful_swap(delta_E: int, T) -> bool:
    """True if swap occurs based on probability transition function"""

    if delta_E <= 0:
        return True
    
    if T > 0:
        swap_prob = exp(-delta_E / (k * T))

        if random() < swap_prob:
            return True

    return False


def animate_sim(snapshots, save=False):
    """Optionally save or displays simulation"""

    import matplotlib.pyplot as plt

    import matplotlib.animation as animation

    fig, ax = plt.subplots()

    ax.set_xticks([])
    ax.set_yticks([])

    ims = []
    for i, snapshot in enumerate(snapshots):
        im = ax.imshow(snapshot, animated=True)
        if i == 0:
            ax.imshow(snapshot)  # show an initial one first
        ims.append([im])

    ani = animation.ArtistAnimation(fig, ims, interval=50, blit=True,
                                    repeat_delay=1000)

    if save:
        ani.save("movie.gif")

    plt.show()


def run_simulation(h, w, k, T, max_mcs=100, initial_sys=None, save_animation=False):

    # Average number of timesteps to swap every site
    mcs = w *  h

    timestep = 0
    
    # Create initial simulation geometry
    if initial_sys == None:
        sys = intialize_system(h, w)
    else:
        sys = initial_sys

    snapshots = [deepcopy(sys)]
    max_timesteps = max_mcs * w * h
    while timestep < max_timesteps:
    
        # Pick a random site and state
        site = random_site(h, w)
        state = random_state()

        if state != sys[site[1]][site[0]]:

            # Compute change in energy for site spin swap
            delta_E = energy_difference(sys, site)
        
            # Compute probability of the change
            if successful_swap(delta_E, T):
                sys[site[1]][site[0]] = not sys[site[1]][site[0]]

        timestep += 1

        if timestep % (mcs*10) == 0:
            snapshots.append(deepcopy(sys))

    animate_sim(snapshots,save_animation)


def ellipse_seed(h, w, x0, y0, a, b):
    
    import numpy as np
                                
    x = np.linspace(0, w, w)
    y = np.linspace(0, h, h)[:,None]
    ellipse = ((x-x0)/a)**2 + ((y-y0)/b)**2 <= 1  # True for points inside the ellipse

    return ellipse.tolist()



if __name__ == "__main__":
  
    # Constants
    w = 50
    h = 50

    T = 0
    k = 1

    max_mcs = 500

    initial_sys = ellipse_seed(w, h, w//2, h//2, 12, 12)

    run_simulation(w,h,T,k,max_mcs,initial_sys)
