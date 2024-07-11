from voxel_builder_library import *
from show_voxel_plt import *
from helpers import *
from show_voxel_plt import timestamp_now
from matplotlib import animation
from class_agent import Agent
from class_layer import Layer

# import presets from here
from agent_algorithms.simple_goals_fill_edges_1 import *


iterations = 100
note = 'fill_corner_1'
time__ = timestamp_now
_save = True
save_json_every_nth = 100
trim_floor = False

run_animation = False
save_animation = False
# SETUP ENVIRONMENT
settings, layers, _ = layer_env_setup(iterations)
print(voxel_size)

# MAKE AGENTS
agents = setup_agents(layers)

# SIMULATION FUNCTION

def simulate(frame):
# for i in range(iterations):
    # print('simulate.counter', simulate.counter)

    # 1. diffuse environment's layers
    diffuse_environment(layers)

    # 2. MOVE and BUILD
    for agent in agents:
        # MOVE
        moved = move_agent(agent, layers)
        # BUILD
        if moved:
            build_chance, erase_chance = calculate_build_chances(agent, layers)
            built, erased = build(agent, layers, build_chance, erase_chance, False)
            if built and reset_after_build:
                reset_agent(agent, voxel_size)
        else:
            if reset_after_build:
                reset_agent(agent, voxel_size)    

    # 3. make frame for animation
    if run_animation:
        scatter_plot(axes, layers=[clay_layer, layers[0]])
    
    simulate.counter += 1
    
    # 4. DUMP JSON
    if _save:
        suffix = '%s_a%s_i%s' %(note, agent_count, iterations)
        if simulate.counter % save_json_every_nth == 0:
            if trim_floor:
                # trim floor
                a1 = clay_layer.array.copy()
                a1[:,:,0] = 0
            else:
                a1 = clay_layer.array.copy()
            # save points
            sortedpts, values = sort_pts_by_values(a1, multiply=100)
            list_to_dump = {'pt_list' : sortedpts, 'values' : values}
            filename = 'data/json/points_values/pts_%s_%s.json' %(time__, suffix)
            with open(filename, 'w') as file:
                json.dump(list_to_dump, file)
            print('\npt_list saved as %s:\n' %filename)
            
            # save compas pointcloud and values
        
            filename = 'data/json/compas_pointclouds/ptcloud_%s_%s.json' %(time__, suffix)
            with open(filename, 'w') as file:
                pointcloud = Pointcloud(sortedpts)
                pointcloud.to_json(file)
            
            # save values
            filename = 'data/json/values/values_%s_%s.json' %(time__, suffix)
            with open(filename, 'w') as file:
                json.dump(values, file)

            print('\ncompas_pointcloud saved as %s:\n' %filename)

def scatter_plot(axes, layers):
    for layer in layers:
        color = layer.rgb
        pts = convert_array_to_points(layer.array, False)
        p = pts.transpose()
        axes.scatter(p[0, :], p[1, :], p[2, :], marker = 's', s = 1, facecolor = color)
        
simulate.counter = 0
### PLOTTING
### SAVE
save_img = _save
save_json = _save

# RUN
if __name__ == '__main__':
    agent_space, air_layer, clay_layer, ground = layers
    if run_animation: 
        scale = voxel_size
        fig = plt.figure(figsize = [4, 4], dpi = 200)
        axes = plt.axes(xlim=(0, scale), ylim =  (0, scale), zlim = (0, scale), projection = '3d')
        axes.set_xticks([])
        axes.set_yticks([])
        axes.set_zticks([])
        scatter_plot(axes, layers=[clay_layer, layers[0]])
        
        suffix = '%s_a%s_i%s' %(note, agent_count, iterations)

        simulate.counter = 0
        anim = animation.FuncAnimation(fig, simulate, frames=iterations, interval = 2)

        if save_animation:
            anim.save('img/gif/gif_%s_%s.gif' %(timestamp_now, suffix))
            print('animation saved')
        if save_img:
            plt.savefig('img/img_%s_%s.png' %(timestamp_now, suffix), bbox_inches='tight', dpi = 200)
            print('image saved')

        plt.show()

    else:
        for i in range(iterations):
            if i % 25 == 0:
                print(i)
            simulate(None)
        
        if save_img:
            scale = voxel_size
            fig = plt.figure(figsize = [4, 4], dpi = 200)
            axes = plt.axes(xlim=(0, scale), ylim =  (0, scale), zlim = (0, scale), projection = '3d')
            axes.set_xticks([])
            axes.set_yticks([])
            axes.set_zticks([])
            
            a1 = clay_layer.array.copy()
            # a1[:,:,0] = 0

            scatter_plot(axes, [clay_layer, layers[0]])
            
            suffix = '%s_a%s_i%s' %(note, agent_count, iterations)

            plt.savefig('img/img_%s_%s.png' %(timestamp_now, suffix), bbox_inches='tight', dpi = 200)
            print('image saved')

            plt.show()