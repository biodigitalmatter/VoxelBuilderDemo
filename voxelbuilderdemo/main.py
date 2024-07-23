import json

import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np
from compas.geometry import Pointcloud

from voxelbuilderdemo import IMG_DIR
from voxelbuilderdemo.helpers import sort_pts_by_values
from voxelbuilderdemo.show_voxel_plt import plot_voxels_2, scatter_layers, timestamp_now
from voxelbuilderdemo.voxel_builder_library import select_layers_to_show

# import voxelbuilderdemo.agent_algorithms_setup_5_reset as algo
# import voxelbuilderdemo.agent_algorithms_setup_6_moisture as algo
import voxelbuilderdemo.algoritm_7 as algo


class SimulationState:
    def __init__(self, iterations, voxel_size, selected_to_plot):
        self.counter = 0

        _, self.layers = algo.layer_setup(iterations)
        self.layers_to_scatter = select_layers_to_show(self.layers, selected_to_plot)

        print("env made. voxel size:", voxel_size)

        # prediffuse
        for i in range(algo.wait_to_diffuse):
            algo.diffuse_environment(self.layers)

        # MAKE AGENTS
        self.agents = algo.setup_agents(self.layers)


global_sim_state = None  # set up in __main__


# SIMULATION FUNCTION
def simulate(frame):
    # 1. diffuse environment's layers
    algo.diffuse_environment(global_sim_state.layers)

    # 2. MOVE and BUILD
    for agent in global_sim_state.agents:
        # MOVE
        moved = algo.move_agent(agent, global_sim_state.layers)
        # print(agent.pose)
        # print(moved)
        if not moved:
            algo.reset_agent(agent)
        # BUILD DEMO
        # if moved:
        #     if np.random.random(1) >= 0:
        #         x,y,z = agent.pose
        #         ground.array[x,y,z] = 1
        # BUILD
        if moved:
            build_chance, erase_chance = algo.calculate_build_chances(
                agent, global_sim_state.layers
            )
            built, erased = algo.build(
                agent, global_sim_state.layers, build_chance, erase_chance
            )
            # if built:
            #     print('built:', agent.pose)
            if built and algo.reset_after_build:
                algo.reset_agent(agent)
    # 2.b clay dries

    # 3. make frame for animation
    if algo.show_animation or algo.save_animation:
        scatter_layers(axes, global_sim_state.layers_to_scatter, trim_below=1)
    global_sim_state.counter += 1

    # 4. DUMP JSON
    if algo.save_json:
        suffix = f"{algo.note}_a{algo.agent_count}_i{algo.iterations}"
        if simulate.counter % algo.save_json_every_nth == 0:
            a1 = global_sim_state.layers["ground"].array.copy()
            a1[:, :, :algo.ground_level_Z] = 0
            sortedpts, values = sort_pts_by_values(a1, multiply=100)
            list_to_dump = {"pt_list": sortedpts, "values": values}
            filename = "data/json/points_values/pts_%s_%s.json" % (algo.time__, suffix)
            with open(filename, "w") as file:
                json.dump(list_to_dump, file)
            print("\npt_list saved as %s:\n" % filename)

            # save compas pointcloud and values

            filename = "data/json/compas_pointclouds/ptcloud_%s_%s.json" % (
                algo.time__,
                suffix,
            )
            with open(filename, "w") as file:
                pointcloud = Pointcloud(sortedpts)
                pointcloud.to_json(file)

            # save values
            filename = "data/json/values/values_%s_%s.json" % (algo.time__, suffix)
            with open(filename, "w") as file:
                json.dump(values, file)

            print("\ncompas_pointcloud saved as %s:\n" % filename)
    print(global_sim_state.counter)


# RUN
if __name__ == "__main__":
    global_sim_state = SimulationState(algo.iterations, algo.voxel_size, algo.selected_to_plot)
    global_sim_state.counter = 0
    suffix = f"{algo.note}_a{algo.agent_count}_i{algo.iterations}"

    if algo.show_animation or algo.save_animation:
        scale = algo.voxel_size
        fig = plt.figure(figsize=[4, 4], dpi=200)
        axes = plt.axes(
            xlim=(0, scale), ylim=(0, scale), zlim=(0, scale), projection="3d"
        )
        axes.set_xticks([])
        axes.set_yticks([])
        axes.set_zticks([])
        scatter_layers(axes, global_sim_state.layers_to_scatter, trim_below=algo.ground_level_Z)

        
        anim = animation.FuncAnimation(fig, simulate, frames=algo.iterations, interval=1)

        if algo.save_animation:
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
        for i in range(algo.iterations):
            simulate(None)

        if algo.show_scatter_img_bool or algo.show_voxel_img_bool or algo.save_img:
            scale = algo.voxel_size
            fig = plt.figure(figsize=[4, 4], dpi=200)
            axes = plt.axes(
                xlim=(0, scale), ylim=(0, scale), zlim=(0, scale), projection="3d"
            )
            if algo.show_scatter_img_bool:
                axes.set_xticks([])
                axes.set_yticks([])
                axes.set_zticks([])
                scatter_layers(
                    axes, global_sim_state.layers_to_scatter, trim_below=algo.ground_level_Z
                )

            elif algo.show_voxel_img_bool:
                if not algo.color_4D:
                    colors = [layer.rgb for layer in global_sim_state.layers_to_scatter]
                    voxel_grids = [
                        layer.array[:, :, algo.ground_level_Z:]
                        for layer in global_sim_state.layers_to_scatter
                    ]
                elif algo.color_4D:
                    colors = [
                        np.clip(
                            global_sim_state.layer.color_array * algo.scale_colors
                            - algo.scale_colors
                            + 1,
                            0,
                            1,
                        )
                        for layer in global_sim_state.layers_to_scatter
                    ]
                    voxel_grids = [
                        layer.array for layer in global_sim_state.layers_to_scatter
                    ]
                plot_voxels_2(axes, voxel_grids, colors, edgecolor=None)

            if algo.save_img:
                plt.savefig(
                    f"{IMG_DIR}/img_{timestamp_now}_{suffix}.png",
                    bbox_inches="tight",
                    dpi=200,
                )
                print("image saved")

            plt.show()
