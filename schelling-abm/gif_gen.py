import imageio.v2 as imageio

frame_folder = r"C:\Users\User_1\Desktop\frames"
# frames = [0, 2, 5, 10, 12, 17, 29, 44, 59, 74, 89, 109, 199, 249, 388]
frames = [0, 1, 2, 5, 7, 10, 14, 19, 24, 29, 34, 39, 44, 49, 54 ,64 , 74, 84, 99, 109, 149, 199, 249, 299, 388]

with imageio.get_writer('schelling_sim.gif', mode='I', fps=4) as writer:
    for i in frames:
        filename = f"{frame_folder}/frame_{i:04d}.png"
        image = imageio.imread(filename)
        writer.append_data(image)

