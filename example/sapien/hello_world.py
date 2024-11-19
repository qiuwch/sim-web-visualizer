# import sapien.core as sapien
import sapien
from meshcat.servers.zmqserver import start_zmq_server_as_subprocess
from sim_web_visualizer import create_sapien_visualizer, bind_visualizer_to_sapien_scene
import pdb


def main():
    # create simulation engine
    # engine = sapien.Engine()

    # Create renderer
    # renderer = sapien.SapienRenderer()
    # engine.set_renderer(renderer)

    # Create a simulation scene
    create_sapien_visualizer(port=6000, host="localhost", keep_default_viewer=False)
    # scene = engine.create_scene()
    scene = sapien.Scene()
    # scene = bind_visualizer_to_sapien_scene(scene, engine, renderer)
    scene = bind_visualizer_to_sapien_scene(scene)
    scene.set_timestep(1 / 100.0)  # Set the simulation frequency

    # Add actors(rigid bodies)
    scene.add_ground(altitude=0)  # Add a ground
    actor_builder = scene.create_actor_builder()
    print(actor_builder)
    # pdb.set_trace()
    actor_builder.add_box_collision(half_size=[0.5, 0.5, 0.5])
    # actor_builder.add_box_visual(half_size=[0.5, 0.5, 0.5], color=[1.0, 0.0, 0.0])
    material = sapien.render.RenderMaterial()
    material.set_base_color([1.0, 0.0, 0.0, 1.0])
    actor_builder.add_box_visual(half_size=[0.5, 0.5, 0.5], material=material)

    box = actor_builder.build(name="box")  # Add a box
    box.set_pose(sapien.Pose(p=[0, 0, 0.5]))

    # Add some lights so that you can observe the scene
    scene.set_ambient_light([0.5, 0.5, 0.5])
    scene.add_directional_light([0, 1, -1], [0.5, 0.5, 0.5])


    loader = scene.create_urdf_loader()

    loader.name = "urdf"
    loader.fix_root_link = True
    loader.load_multiple_collisions_from_file = False
    loader.disable_self_collisions = True

    # FIXME:
    from pathlib import Path
    # asset_path = Path(__file__).parent / "piano"
    asset_path = str(Path(__file__).parent.parent / "visualize_urdf/kuka_allegro_description/kuka_allegro.urdf")
    print(asset_path)
    asset_path = "/home/qiuwch/third/ManiSkill/mani_skill/assets/robots/fetch/fetch.urdf"
    asset_path = "/home/qiuwch/third/ManiSkill/mani_skill/assets/robots/panda/panda_v3.urdf"

    builder = loader.load_file_as_articulation_builder(asset_path)
    # builder = loader.parse(str(asset_path))[0][0]
    builder.initial_pose = sapien.Pose(p=[0, 0, 0.5])
    robot = builder.build("urdf")  # NOTE: the uid has no effect!
    robot.set_name("urdf")


    import sys
    sys.path += ['/home/qiuwch/code/simbase/scene']
    import sapien_scene
    sapien_scene.scene_view(scene)

    #############################
    while True:
        try:
            scene.step()  # Simulate the world
            scene.update_render()  # Update the world to the renderer

        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    start_zmq_server_as_subprocess()
    main()
