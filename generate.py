###########################################################
# atom 1: solution, atom 2: hydrophobic group, atom 3: wall
# mol_id determines the bonding between atoms
# prepare atom 2 on the suface of bubble
###########################################################

import random
import numpy as np
from math import cos, sin, sqrt


random.seed(101)


class Atom:
    def __init__(self, x, y, z, atom_type, mol_id):
        self.x = x
        self.y = y
        self.z = z
        self.atom_type = atom_type
        self.mol_id = mol_id
        v0 = 1.0
        z = random.random()*2.0-1
        s = random.random()*3.14*2.0
        if atom_type == 3: # Initial velocity of atom 3 is 0
            self.vx = 0
            self.vy = 0
            self.vz = 0
        else:
            self.vx = v0*sqrt(1.0-z**2)*cos(s)
            self.vy = v0*sqrt(1.0-z**2)*sin(s)
            self.vz = v0*z


# Calculate lattice number from density, L: box size, rho: density
def get_lattice_number(L, rho):
    m = np.floor((L**3 * rho / 4.0)**(1.0 / 3.0))
    drho1 = np.abs(4.0 * m **3 / L**3 - rho)
    drho2 = np.abs(4.0 * (m + 1)**3 / L**3 - rho)
    if drho1 < drho2:
        return m
    else:
        return m + 1


# Compose liquid-phase atoms
def add_ball(atoms, l, rho):
    m = int(get_lattice_number(l, rho))  # lattice number in liquid-phase
    s = 1.7  # Length of a unit lattice edge
    h = 0.5 * s
    mol_id = 1  # molcule ID
    N = 0  # Number of bond
    index = 1  # atom ID that make up the bond
    for ix in range(0, m):
        for iy in range(0, m):
            for iz in range(0, m):
                x = ix * s
                y = iy * s
                z = iz * s
                if (x-l/2)**2 + (y-l/2)**2 + (z-l/2)**2 < 8**2:  # Hollow out of the liquid phase
                    continue
                elif (x-l/2)**2 + (y-l/2)**2 + (z-l/2)**2 < 12**2:  # Let atom type at a certain distance be 2
                    atoms.append(Atom(x, y, z, 2, mol_id))
                    atoms.append(Atom(x+h, y+h, z, 1, mol_id))
                    atoms.append(Atom(x, y+h, z+h, 1, mol_id+1))
                    atoms.append(Atom(x+h, y, z+h, 1, mol_id+2))
                    mol_id += 3
                    N += 1
                    L.append(index)
                    L.append(index+1)
                elif z == 0:  # Name the bottom atoms number 3
                    atoms.append(Atom(x, y, z, 3, mol_id))
                    atoms.append(Atom(x+h, y+h, z, 3, mol_id+1))
                    atoms.append(Atom(x, y+h, z+h, 1, mol_id+2))
                    atoms.append(Atom(x+h, y, z+h, 1, mol_id+3))
                    mol_id += 4
                else:
                    atoms.append(Atom(x, y, z, 1, mol_id))
                    atoms.append(Atom(x+h, y+h, z, 1, mol_id+1))
                    atoms.append(Atom(x, y+h, z+h, 1, mol_id+2))
                    atoms.append(Atom(x+h, y, z+h, 1, mol_id+3))
                    mol_id += 4
                index += 4
    return N


# Calculate concentration of surfactant
#def concentration():


# Save as make_bubble.atoms
def save_file(filename, atoms, N, l):
    with open(filename, "w") as f:
        f.write("Position Data\n\n")
        f.write("{} atoms\n".format(len(atoms)))
        f.write("{} bonds\n\n".format(N))
        f.write("3 atom types\n")
        f.write("1 bond types\n\n")
        f.write("0.00 {} xlo xhi\n".format(l))
        f.write("0.00 {} ylo yhi\n".format(l))
        f.write("0.00 {} zlo zhi\n".format(l))
        f.write("\n")
        f.write("Atoms\n\n")  # atom ID, molcule ID, atom type, atomic coordinates
        for i, a in enumerate(atoms):
            f.write("{} {} {} {} {} {}\n".format(i+1, a.mol_id, a.atom_type, a.x, a.y, a.z))
        f.write("\n")
        f.write("Velocities\n\n")  # atom ID, atomic velocities
        for i, a in enumerate(atoms):
            f.write("{} {} {} {}\n".format(i+1, a.vx, a.vy, a.vz))
        f.write("\n")
        f.write("Bonds\n\n")  # bond ID, bond type, atom ID1, atom ID2
        bond_id = 1  # bond ID
        index = 0
        while len(L) > index:
            f.write("{} {} {} {}\n".format(bond_id, 1, L[index], L[index+1]))
            bond_id += 1
            index += 2


atoms = []
L = []  # list of the atom ID that make up the bond

N = add_ball(atoms, 51, 0.8)

save_file("make_bubble.atoms", atoms, N, 51.0)
