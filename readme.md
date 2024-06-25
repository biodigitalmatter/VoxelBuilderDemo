# Voxel Builder Demo

this repo focuses on conceptualising the agent-simulation based geometry generation for reactive 3D printing
below other modules of the robotic fabrication platform are drafted to, to give the context

## The Builder engine

### concept

diffusion mechanism
several layers of the environment effects the agents' behaviour
the agents react to the environment and form it in the same time

### mechanism

the layers of the environment: voxel-like objects (numpy arrays)
agents in the environment: general objects
mechanism: the diffusion

## Objects

### Layers

examples:

- Earth *solid ground*
- Air *we could consider forming structures by building negative spaces*
- PathPheromons *way of agent communication*
- FoodPheromons *way of agent attraction*
- AsBuilt *input from the 3Dscan*
- CollisionArea *precalculated unreachable area based on the ground and asbuilt layer*

#### layer properties

- density *the voxel array*
- diffusion_strength
- show_color
- attraction_strength *the attraction strength between a Layer and an Agent class*

### Agents

- Builders
- Explorers
- others?

#### Agent Behaviours: methods and properties - controlling through impulses

methods:

- move *
- check_move_options
- get_impulse
- get_neighbor_voxels

properties:

- position
- movement_limitations
- pathpheromon_strength

global properties:

- pheromon_attraction_strength

### Mechanisms

it could perhaphs make sense to create mechanism Classes instead of inbuilt functions

- VoxelEngine *every layer refers to this object to build its own array accordingly*
- DiffuseALayer
- OverlaySomeLayers
- DumpState *dumps a state of a layer or the entire world*
- LoadAsBuilt
- Wind
- Gravity

## Visualisers

standalone visualiser of one layer or the world State

## DesignerTools

1. initial design goal-parameters-constrains definition
2. enabling realtime designer interaction (3D or text-based)

## RoboticPathPlanner

tool to generate a robotic path plan to 3Dprint the sequence from the as built state to a given state
