#!/usr/bin/env python

'''
 Make a groundplane for gazebo with a texture created from a path
'''

import sys, os, time, logging, math, numpy as np, yaml
import rospkg
import PIL.Image, PIL.ImageDraw

import pdb
import two_d_guidance.path
import common_simulations.gazebo_worlds as gzw

#
# originated from julie_worlds/scripts/test_04_make_gazebo_model.py
# which creates ground planes from googlemap images
#
def pixel_to_world(px, py):
        return  np.array([(px+0.5)/texture_resolution, (texture_size[1]-py-1+0.5)/texture_resolution, 0]) - [model_size[0]/2, model_size[1]/2, 0]

def world_to_pixel(p, texture_resolution, img_size, origin):
    return ([1, -1]*(p+origin)*texture_resolution+img_size/2).astype('int')

    #return (p*texture_resolution).astype('int')

    #    [2., 1.8]):
#def create_texture(path_filename, texture_filename, model_size, texture_resolution, path_width=0.02, origin=[-0.6, 0.]):
def create_texture(path_filename, texture_filename, model_size, texture_resolution, path_width=0.02, origin=[0., 0.]):
    print('Writing texture to {}'.format(texture_filename))
    path = two_d_guidance.path.Path(load=path_filename)
    texture_size = np.round(model_size*texture_resolution).astype(int)
    texture_image = PIL.Image.new('RGB', tuple(texture_size), (255, 255, 255))
    # texture_pixels = texture_image.load()
    # for px in range(texture_size[0]):
    #     for py in range(texture_size[1]):
    #         texture_pixels[px, py] = (255, 255, 255)
    draw =  PIL.ImageDraw.Draw(texture_image)
    #draw.line((0, 0) + texture_image.size, fill=0, width=int(path_width*texture_resolution))
    if 0:
        pws = np.array([[1, 1], [1, 0]])
    else:
        pws = path.points
    pxs = [tuple(world_to_pixel(p, texture_resolution, np.array(texture_image.size), origin)) for p in pws]
    draw.line(pxs, fill=0, width=int(path_width*texture_resolution))
    #for p, px in zip(path.points, pxs):
    #    print p, px
    texture_image.save(texture_filename) 

def create_world(path_filename, model_name, texture_name, texture_resolution):
    cs_path = rospkg.RosPack().get_path('common_simulations')
    # write world
    gzw.write_world(model_name, os.path.join(cs_path, 'worlds/{}.world'.format(model_name)))
                    

    # write textured ground plane model
    #   Model config
    model_dir = os.path.join(cs_path, 'models/', model_name)
    print model_dir
    if not os.path.exists(model_dir): os.makedirs(model_dir)
    gzw.write_model_config(model_name, os.path.join(model_dir, 'model.config'), "A textured ground plane.")
    #   Model
    model_size = np.array([10., 8.])
    material_name = "{}_floor/Image".format(model_name)
    gzw.write_model_sdf(model_name, os.path.join(model_dir, 'model.sdf'), model_size, material_name)

    #   Material
    script_dir = os.path.join(model_dir, 'materials/scripts/')
    if not os.path.exists(script_dir): os.makedirs(script_dir)
    outfile =  os.path.join(script_dir, '{}.material'.format(model_name))
    gzw.write_material(outfile, material_name, texture_name)
    #   texture
    texture_dir = os.path.join(model_dir, 'materials/textures/')
    if not os.path.exists(texture_dir): os.makedirs(texture_dir)
    outfile =  os.path.join(texture_dir, texture_name)
    create_texture(path_filename, outfile, model_size, texture_resolution)
    
if __name__ == '__main__':

    #create_world(path_filename, "track_ethz", "photo_track_ethz.png")
    texture_resolution = 500. # pixel per meter

    if 0:
        path_filename = os.path.join(rospkg.RosPack().get_path('two_d_guidance'), 'paths/demo_z/oval_01.npz')
        create_world(path_filename, "oval_01", "oval_01_line.png", texture_resolution)

    if 0:
        path_filename = os.path.join(rospkg.RosPack().get_path('two_d_guidance'), 'paths/demo_z/line_01.npz')
        create_world(path_filename, "line_01", "line_01_line.png", texture_resolution)
    
    if 0:
        path_filename = os.path.join(rospkg.RosPack().get_path('two_d_guidance'), 'paths/demo_z/track_ethz_cam1_new.npz')
        create_world(path_filename, "ethz_cam1", "ethz_cam1_line.png", texture_resolution)
