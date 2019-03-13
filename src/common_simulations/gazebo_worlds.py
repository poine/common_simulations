



def write_model_config(name, outfile, description):
    print('Writing model config to {}'.format(outfile))
    with open(outfile, 'w') as f:
      f.write('''<?xml version="1.0"?>
<model>
  <name>{}</name>
  <version>1.0</version>
  <sdf version="1.6">model.sdf</sdf>

  <author>
    <name>Antoine Drouin</name>
    <email>poinix@gmail.com</email>
  </author>

  <description>
    
  </description>
</model>
'''.format(name, description))


      
def write_model_sdf(model_name, outfile, size, material_name):
    print('Writing sdf model to {}'.format(outfile))
    with open(outfile, 'w') as f:
        size_str = '{} {}'.format(size[0], size[1])
        f.write('''<?xml version="1.0"?>
<sdf version="1.6">
<model name="{}">
  <pose>0 0 0 0 0 0</pose>
  <static>true</static>
    <link name="link">
      <collision name="collision">
        <geometry>
          <plane>
            <normal>0 0 1</normal>
            <size>{}</size>
          </plane>
        </geometry>
        <surface>
          <friction>
            <ode>
              <mu>100</mu>
              <mu2>50</mu2>
            </ode>
          </friction>
        </surface>
      </collision>
      <visual name="visual">
        <cast_shadows>false</cast_shadows>
        <geometry>
          <plane>
            <normal>0 0 1</normal>
            <size>{}</size>
          </plane>
        </geometry>
        <material>
          <script>
            <uri>model://{}/materials/scripts</uri>
            <uri>model://{}/materials/textures</uri>
	    <name>{}</name>
          </script>
        </material>
      </visual>
    </link>
  </model>
</sdf>
'''.format(model_name, size_str, size_str, model_name, model_name, material_name))


def write_material(outfile, material_name, texture_name):
    print('Writing material to {}'.format(outfile))
    with open(outfile, 'w') as f:
        f.write('''material {}
{{
  technique
  {{
    pass
    {{
      ambient 0.5 0.5 0.5 1.0
      diffuse 1.0 1.0 1.0 1.0
      specular 0.0 0.0 0.0 1.0 0.5

      texture_unit
      {{
        texture {}
        filtering trilinear
        }}
      }}
   }}
 }}
        '''.format(material_name, texture_name)) 
        


def write_world(world_name, outfile):
    print('Writing world to {}'.format(outfile))
    with open(outfile, 'w') as f:
      f.write('''<?xml version="1.0" ?>
<sdf version="1.6">
  <world name="default">
    <!-- A global light source -->
    <include>
      <uri>model://sun</uri>
    </include>
    <!-- A textured ground plane -->
    <include>
      <uri>model://{}</uri>
    </include>
  </world>
</sdf>'''.format(world_name))
