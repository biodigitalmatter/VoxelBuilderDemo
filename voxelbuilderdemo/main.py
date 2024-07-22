import json

from voxel_builder_library import *
from show_voxel_plt import *
from helpers import *
from show_voxel_plt import timestamp_now
from matplotlib import animation
from class_agent import Agent
from class_layer import Layer
from voxelbuilderdemo import IMG_DIR

# SELECT ALGORITM PRESET FOR IMPORT
from agent_algorithms_setup_5_reset import *
# from agent_algorithms_setup_5_test import *
# from agent_algorithms_setup_6_moisture import *
# from algoritm_7 import *


# PREP
def prep_simulation():
    global layers, layers_to_scatter, agents, global_sim_counter

    global_sim_counter = 0

    # SETUP ENVIRONMENT
    settings, layers = layer_setup(iterations)
    print("env made. voxel size:", voxel_size)
    layers_to_scatter = select_layers_to_show(layers, selected_to_plot)

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
        # print(agent.pose)
        # print(moved)
        if not moved:
            reset_agent(agent)
        # BUILD DEMO
        # if moved:
        #     if np.random.random(1) >= 0:
        #         x,y,z = agent.pose
        #         ground.array[x,y,z] = 1
        # BUILD
        if moved:
            build_chance, erase_chance = calculate_build_chances(agent, layers)
            built, erased = build(agent, layers, build_chance, erase_chance)
            # if built:
            #     print('built:', agent.pose)
            if built and reset_after_build:
                reset_agent(agent)
    # 2.b clay dries

    # 3. make frame for animation
    if show_animation or save_animation:
        scatter_layers(axes, layers_to_scatter, trim_below=1)
    global_sim_counter += 1

    # 4. DUMP JSON
    if save_json:
        suffix = "%s_a%s_i%s" % (note, agent_count, iterations)
        if simulate.counter % save_json_every_nth == 0:
            a1 = layers["ground"].array.copy()
            a1[:,:,:ground_level_Z] = 0
            sortedpts, values = sort_pts_by_values(a1, multiply=100)
            list_to_dump = {"pt_list": sortedpts, "values": values}
            filename = "data/json/points_values/pts_%s_%s.json" % (time__, suffix)
            with open(filename, "w") as file:
                json.dump(list_to_dump, file)
            print("\npt_list saved as %s:\n" % filename)

            # save compas pointcloud and values

            filename = "data/json/compas_pointclouds/ptcloud_%s_%s.json" % (
                time__,
                suffix,
            )
            with open(filename, "w") as file:
                pointcloud = Pointcloud(sortedpts)
                pointcloud.to_json(file)

            # save values
            filename = "data/json/values/values_%s_%s.json" % (time__, suffix)
            with open(filename, "w") as file:
                json.dump(values, file)

            print("\ncompas_pointcloud saved as %s:\n" % filename)
    print(global_sim_counter)

# RUN
if __name__ == "__main__":
    prep_simulation()
    if show_animation or save_animation:
        scale = voxel_size
        fig = plt.figure(figsize=[4, 4], dpi=200)
        axes = plt.axes(
            xlim=(0, scale), ylim=(0, scale), zlim=(0, scale), projection="3d"
        )
        axes.set_xticks([])
        axes.set_yticks([])
        axes.set_zticks([])
        scatter_layers(axes, layers_to_scatter, trim_below=ground_level_Z)

        suffix = "%s_a%s_i%s" % (note, agent_count, iterations)

        global_sim_counter = 0
        anim = animation.FuncAnimation(fig, simulate, frames=iterations, interval=1)

        if save_animation:
            anim.save(f"{IMG_DIR}/gif/gif_{timestamp_now}_{suffix}.gif")
            print("animation saved")

            plt.savefig(
                f"{IMG_DIR}/img_{timestamp_now}_{suffix}.png",
                bbox_inches="tight",
                dpi=200,
            )
            print("image saved")

        plt.show()

    else:
        for i in range(iterations):
            simulate(None)

        if show_scatter_img_bool or show_voxel_img_bool or save_img:
            scale = voxel_size
            fig = plt.figure(figsize=[4, 4], dpi=200)
            axes = plt.axes(
                xlim=(0, scale), ylim=(0, scale), zlim=(0, scale), projection="3d"
            )
            if show_scatter_img_bool:
                axes.set_xticks([])
                axes.set_yticks([])
                axes.set_zticks([])
                scatter_layers(axes, layers_to_scatter, trim_below=ground_level_Z)

            elif show_voxel_img_bool:
                if not color_4D:
                    colors = [layer.rgb for layer in layers_to_scatter]
                    voxel_grids = [
                        layer.array[:, :, ground_level_Z:]
                        for layer in layers_to_scatter
                    ]
                elif color_4D:
                    colors = [
                        np.clip(
                            layer.color_array * scale_colors - scale_colors + 1, 0, 1
                        )
                        for layer in layers_to_scatter
                    ]
                    voxel_grids = [layer.array for layer in layers_to_scatter]
                plot_voxels_2(axes, voxel_grids, colors, edgecolor=None, trim_below=ground_level_Z)
                suffix = "%s_a%s_i%s" % (note, agent_count, iterations)

            if save_img:
                plt.savefig(
                    f"{IMG_DIR}/img_{timestamp_now}_{suffix}.png",
                    bbox_inches="tight",
                    dpi=200,
                )
                print("image saved")

            plt.show()
