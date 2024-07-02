# Notes

## 240701

### next todos

- test algoritmhs - parameters
- agent-collision?
- dump json
- create-ptcloud > compas_view


## meeting notes 240626

### design parameters: combination of algorithms

"controlling the generative design with a combination of agent algoritms in a simulated environment"

algorithms meaning

'different ways strategies and concepts how and why to build'

active and passive impulses from the enviroment

effect the behaviour of the agents

in the simulation

### what triggers a build

when would a worker drop? while they move absolutly random

#### movement

the way of movement triggers the workers to fill a voxel.

the direction of the move

the speed of move

the topology they move on

- corners
- edges

#### pheromons

- combination of pheromes
- specific densitiy of pheromes

changing environment (the built staff) modifies the impacting pheromones constantly
so the construction will morph, dont worry

### micro and macro scale structure charecteristix

microscale - sphongy built termite funghi gardens

macroscale - large vaults and thin coloumns

### 3Dscanning

#### including 3D scans in the voxel design

constant buildup of scanned data

scanned mesh has an inside outside information

### OpenVDB

later

### Todos next

### first

just explore build_algorithms,
behaviours strategies interactions whatever

### later

- novel visualisation
- openvdb convert (data or code)
- dump


## saved parameters:

<!-- # # grounds_offset
# offset_ph = Layer(name = 'offset_ph', voxel_size=voxel_size, rgb = [0.25, 0.25, 0.25])
# offset_ph.decay_linear_value = 1/6
# offset_ph.decay_ratio = 0
# offset_ph.diffusion_ratio = 1/3
# grounds_emission_value = 2 -->