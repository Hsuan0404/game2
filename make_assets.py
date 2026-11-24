import bpy
import math
import os
from mathutils import Vector

out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
os.makedirs(out_dir, exist_ok=True)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

def mat(name, color, roughness=0.72):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1)
    m.roughness = roughness
    m.use_nodes = True
    m.node_tree.nodes.get("Principled BSDF").inputs["Base Color"].default_value = (*color, 1)
    m.node_tree.nodes.get("Principled BSDF").inputs["Roughness"].default_value = roughness
    return m

skin = mat("柔軟小白人・奶油白", (0.88, 0.94, 0.88))
shirt = mat("探險背心・森林綠", (0.11, 0.39, 0.29))
scarf = mat("理財圍巾・檸檬黃", (0.92, 0.72, 0.20))
eye = mat("眼睛・深森林", (0.035, 0.12, 0.10))
gold = mat("鑰匙・金色", (0.95, 0.61, 0.10), 0.3)

def uv(name, loc, scale, material, segments=16, rings=10):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=segments, ring_count=rings, location=loc)
    o = bpy.context.object
    o.name = name
    o.scale = scale
    bpy.ops.object.shade_smooth()
    o.data.materials.append(material)
    return o

def limb(name, a, b, radius, material):
    mid = (Vector(a) + Vector(b)) / 2
    direction = Vector(b) - Vector(a)
    bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=radius, depth=direction.length, location=mid)
    o = bpy.context.object
    o.name = name
    o.rotation_mode = 'QUATERNION'
    o.rotation_quaternion = direction.to_track_quat('Z', 'Y')
    o.data.materials.append(material)
    bevel = o.modifiers.new("圓潤邊緣", 'BEVEL')
    bevel.width = radius * .45
    bevel.segments = 3
    o.modifiers.new("柔和法線", 'WEIGHTED_NORMAL')
    return o

# A friendly, slightly wobbly low-poly explorer.
uv("圓圓頭", (0, 0, 2.05), (.46, .42, .46), skin, 20, 12)
uv("身體", (0, 0, 1.23), (.43, .34, .62), shirt)
uv("圍巾結", (0, -.33, 1.62), (.28, .12, .14), scarf)
limb("圍巾垂帶", (.13, -.34, 1.62), (.24, -.38, 1.35), .09, scarf)
for x in (-.16, .16):
    uv("亮晶晶眼睛", (x, -.395, 2.10), (.045, .027, .065), eye, 12, 8)
    limb("小腿", (x*.8, 0, .76), (x*1.15, -.02, .25), .13, skin)
    uv("圓圓腳", (x*1.15, -.08, .19), (.19, .27, .14), skin)
limb("左手臂", (-.34, 0, 1.58), (-.60, -.02, 1.12), .13, skin)
uv("左手", (-.61, -.02, 1.08), (.15, .14, .14), skin)
limb("右手臂", (.34, 0, 1.58), (.59, -.02, 1.30), .13, skin)
uv("右手", (.60, -.02, 1.27), (.15, .14, .14), skin)

# A large collectible key displayed alongside the character.
bpy.ops.mesh.primitive_torus_add(major_radius=.18, minor_radius=.065, major_segments=24, minor_segments=10, location=(1.05, -.05, 1.72), rotation=(math.radians(90),0,0))
ring=bpy.context.object; ring.name="鑰匙圓環"; ring.data.materials.append(gold)
bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=.075, depth=.55, location=(1.34, -.05, 1.46), rotation=(0, math.radians(90), 0))
shaft=bpy.context.object; shaft.name="鑰匙柄"; shaft.data.materials.append(gold)
for z in (1.25, 1.36):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(1.50, -.05, z))
    tooth=bpy.context.object; tooth.name="鑰匙齒"; tooth.scale=(.18,.13,.07); tooth.data.materials.append(gold)

# Small display plinth.
bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=1.25, depth=.18, location=(0, 0, .0))
plinth=bpy.context.object; plinth.name="展示底座"; plinth.data.materials.append(mat("草地底座", (.26,.48,.32)))
bev=plinth.modifiers.new("底座圓角",'BEVEL'); bev.width=.08; bev.segments=3
plinth.modifiers.new("底座法線",'WEIGHTED_NORMAL')

scene=bpy.context.scene
scene.render.engine='BLENDER_EEVEE'
scene.render.resolution_x=900; scene.render.resolution_y=900; scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG'
scene.render.filepath=os.path.join(out_dir,"soft-explorer.png")
scene.world.color=(.12,.16,.14)
def area(name, loc, power, size, color):
    data=bpy.data.lights.new(name,'AREA'); data.energy=power; data.shape='DISK'; data.size=size; data.color=color
    obj=bpy.data.objects.new(name,data); scene.collection.objects.link(obj); obj.location=loc
    obj.rotation_euler=(Vector((0,0,1))-obj.location).to_track_quat('-Z','Y').to_euler()
area("大面積暖光",(1,-4,6),480,4,(1.0,.84,.64))
area("柔和補光",(-4,-1,3),260,3,(.65,.83,1.0))
cam_data=bpy.data.cameras.new("展示相機"); cam=bpy.data.objects.new("展示相機",cam_data); scene.collection.objects.link(cam)
cam.location=(3,-7,3.2); cam.rotation_euler=(Vector((.25,0,1.1))-cam.location).to_track_quat('-Z','Y').to_euler(); cam_data.type='ORTHO'; cam_data.ortho_scale=4.6; scene.camera=cam
scene.render.image_settings.color_mode='RGBA'
scene.view_settings.view_transform='AgX'

# Save editable Blender source and export the character/key model for reuse.
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(out_dir,"soft-explorer.blend"))
for o in bpy.context.selected_objects: o.select_set(False)
for o in scene.objects:
    if o.name.startswith("展示底座") or o.name.startswith("展示相機") or o.name.startswith("大面積暖光") or o.name.startswith("柔和補光"):
        continue
    o.select_set(True)
bpy.ops.export_scene.gltf(filepath=os.path.join(out_dir,"soft-explorer.glb"), export_format='GLB', use_selection=True)
bpy.ops.render.render(write_still=True)

# Transparent player sprite rendered from the same Blender model for the game UI.
for o in scene.objects:
    if o.name.startswith(("鑰匙", "鑰匙圓環", "鑰匙柄", "鑰匙齒", "展示底座")):
        o.hide_render = True
scene.render.film_transparent = True
scene.render.resolution_x = 420
scene.render.resolution_y = 520
scene.render.filepath = os.path.join(out_dir, "soft-explorer-sprite.png")
cam.location = (2.5, -7, 2.6)
cam.rotation_euler = (Vector((0, 0, 1.18))-cam.location).to_track_quat('-Z','Y').to_euler()
cam_data.ortho_scale = 3.25
bpy.ops.render.render(write_still=True)
