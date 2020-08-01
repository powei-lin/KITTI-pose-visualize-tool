import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pytransform3d.transformations as pt
from pytransform3d.transform_manager import TransformManager

def addPose(num, w_list, ax0, s):
    print("num:", num)
    ax = tm.plot_frames_in("o", s=s, ax = ax0, show_name=False, whitelist=w_list[num-1:num])

if __name__ == "__main__":
    posefile = open("00.txt").readlines()

    tm = TransformManager()
    max_m = [0, 0, 0]
    min_m = [0, 0, 0]
    w_list = []
    for i, l in enumerate(tqdm(posefile[::15])):
        m = np.array(l[:-1].split(' ')).reshape(3,4)
        r = m[:3,:3]
        t = m[:3,3]
        for j in range(3):
            max_m[j] = max(max_m[j], float(t[j]))
            min_m[j] = min(min_m[j], float(t[j]))
        pose = pt.transform_from(r, t)
        tm.add_transform("p"+str(i), "o", pose)
        w_list.append("p"+str(i))

    fig = plt.figure(figsize=(8, 8))
    fig.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, 
            hspace = 0, wspace = 0)
    # fig.tight_layout()
    
    scale = max([i-j for i, j in zip(max_m, min_m)])/1.5
    ax = tm.plot_frames_in("o", s=scale/50, show_name=False, whitelist=w_list[:1])
    centor = [(i+j)/2.0 for i, j in zip(max_m, min_m)]

    ax.set_xlim((centor[0]-scale, centor[0]+scale))
    ax.set_ylim((centor[1]-scale, centor[1]+scale))
    ax.set_zlim((centor[2]-scale, centor[2]+scale))

    ax.view_init(-0, -90)
    # plt.show()
    fargs = [w_list, ax, scale/50]
    rot_animation = animation.FuncAnimation(fig, addPose, frames=np.arange(0, len(w_list), 1), fargs=fargs, interval=40)
    plt.show()
    # rot_animation.save('pose1.mp4', writer='ffmpeg', dpi=200)
    # rot_animation.save('pose1.gif', writer='pillow', dpi=200)