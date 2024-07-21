from voxel_builder_library import *
from show_voxel_plt import *
from helpers import *
from show_voxel_plt import timestamp_now
from matplotlib import animation
from class_agent import Agent
from class_layer import Layer

# import presets from here
from agent_algorithms_setup_5_reset import *

note = 'setup_5_test_queen_bee_diffuse_function'
iterations = 30
time__ = timestamp_now
save_json_every_nth = 100
# plot = True
trim_floor = False

### SAVE
# _save = True
save_img = False
save_json = False
save_animation = False
show_animation = True
# img plot type
show_scatter_img_bool = False
show_voxel_img_bool = True

# SETUP ENVIRONMENT
settings, layers = layer_env_setup(iterations)
# call layers
agent_space = layers['agent_space']
ground = layers['ground']
queen_bee_pheromon = layers['queen_bee_pheromon']
# print info
print('env made. voxel size:',voxel_size)
# print(queen_bee_pheromon.name, queen_bee_pheromon.diffusion_ratio, queen_bee_pheromon.decay_ratio, queen_bee_pheromon.gradient_resolution)

# select layers to PLOT
global layers_to_scatter
layers_to_scatter = []
layers_to_scatter = [queen_bee_pheromon, ground]
color_4D = True
scale_colors = 1

# prediffuse
for i in range(wait_to_diffuse):
    diffuse_environment(layers)


# MAKE AGENTS
agents = setup_agents(layers)

# SIMULATION FUNCTION
def simulate(frame):
    # 1. diffuse environment's layers
    diffuse_environment(layers)

    # 2. MOVE and BUILD
    for agent in agents:
        # MOVE
        moved = move_agent(agent, layers)
        # print(moved)
        if not moved:
            reset_agent(agent)
        # BUILD DEMO
        # if moved:
        #     if np.random.random(1) >= 0:
        #         x,y,z = agent.pose
        #         ground.array[x,y,z] = 1
        # # BUILD
        # if moved:
        #     build_chance, erase_chance = calculate_build_chances(agent, layers)
        #     built, erased = build(agent, layers, build_chance, erase_chance, False)
        #     if built and reset_after_build:
        #         reset_agent(agent)
    # 2.b clay dries
    

    # 3. make frame for animation
    if show_animation or save_animation:
        scatter_layers(axes, layers_to_scatter, trim_below=1) 
    simulate.counter += 1
    
    # 4. DUMP JSON
    if save_json:
        suffix = '%s_a%s_i%s' %(note, agent_count, iterations)
        if simulate.counter % save_json_every_nth == 0:
            # if trim_floor:
            #     # trim floor
            #     a1 = layers['clay_moisture_layer'].array.copy()
            #     a1[:,:,:ground_level_Z] = 0
            # else:
            #     a1 = layers['clay_moisture_layer'].array.copy()
            # save points
            a1 = ground.array.copy()
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
    print(simulate.counter)
     
simulate.counter = 0

# RUN
if __name__ == '__main__':
    if show_animation: 
        scale = voxel_size
        fig = plt.figure(figsize = [4, 4], dpi = 200)
        axes = plt.axes(xlim=(0, scale), ylim =  (0, scale), zlim = (0, scale), projection = '3d')
        axes.set_xticks([])
        axes.set_yticks([])
        axes.set_zticks([])
        scatter_layers(axes, layers_to_scatter) 

        suffix = '%s_a%s_i%s' %(note, agent_count, iterations)

        simulate.counter = 0
        anim = animation.FuncAnimation(fig, simulate, frames=iterations, interval = 1)

        if save_animation:
            anim.save('img/gif/gif_%s_%s.gif' %(timestamp_now, suffix))
            print('animation saved')
        if save_img:
            plt.savefig('img/img_%s_%s.png' %(timestamp_now, suffix), bbox_inches='tight', dpi = 200)
            print('image saved')

        plt.show()

    else:
        for i in range(iterations):
            simulate(None)
        
        if show_scatter_img_bool or show_voxel_img_bool or save_img:
            scale = voxel_size
            fig = plt.figure(figsize = [4, 4], dpi = 200)
            axes = plt.axes(xlim=(0, scale), ylim =  (0, scale), zlim = (0, scale), projection = '3d')
            if show_scatter_img_bool:
                axes.set_xticks([])
                axes.set_yticks([])
                axes.set_zticks([])
                
                # # scatter plot special
                # a1 = ground.array.copy()
                # a1[:,:,:ground_level_Z] = 0
                # pts_built = convert_array_to_points(a1, False)
                # agent_space_pts = convert_array_to_points(layers['agent_space'].array, False)
                # arrays_to_show = [pts_built, agent_space_pts]
                # colors = [layers['clay_moisture_layer'].rgb, agent_space.rgb]
                # for array, color in zip(arrays_to_show, colors):
                #     p = array.transpose()
                #     axes.scatter(p[0, :], p[1, :], p[2, :], marker = 's', s = 1, facecolor = color)
                
                # scatter plot as preset:
                scatter_layers(axes, layers_to_scatter) 
                
            
            elif show_voxel_img_bool:
                if not color_4D:
                    colors = [layer.rgb for layer in layers_to_scatter]
                    voxel_grids = [layer.array[:,:,ground_level_Z:] for layer in layers_to_scatter]
                elif color_4D:
                    colors = [np.clip(layer.color_array * scale_colors - scale_colors + 1, 0, 1) for layer in layers_to_scatter]
                    voxel_grids = [layer.array for layer in layers_to_scatter]
                plot_voxels_2(axes, voxel_grids, colors, edgecolor=None)
                suffix = '%s_a%s_i%s' %(note, agent_count, iterations)

            if save_img:
                plt.savefig('img/img_%s_%s.png' %(timestamp_now, suffix), bbox_inches='tight', dpi = 200)
                print('image saved')

            plt.show()

