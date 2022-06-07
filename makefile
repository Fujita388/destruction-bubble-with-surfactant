all:

# Adjust the magnitude of gravity
gravity-test:
	rm gravity.lammpstrj
	source /home/issp/materiapps/intel/lammps/lammpsvars.sh
	srun lammps < gravity.input

clean: 
	$(RM) *.lammpstrj *.atoms *.out *.lammps
