bl_info = {
    "name": "Unity Export Util",
	"author" : "Carl Baumann",
	"version" : (1, 0, 0),
	"blender" : (2, 7, 9),
	"description": "Exports meshes to FBX such that Unity3D imports them oriented correctly and without a default rotation",
    "category": "Export",
}
    
import bpy
import math
from mathutils import Euler

class UnityExportUtil(bpy.types.Operator):
    """Exports meshes to FBX such that Unity3D imports them oriented correctly and without a default rotation"""
    bl_idname = 'export.to_unity'
    bl_label = 'Export to Unity'
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        if context.selected_objects == []:
            self.report({'ERROR_INVALID_INPUT'}, "No objects selected.")

        selected_objects = context.selected_objects
        bpy.ops.object.select_all(action='DESELECT')

        # rotate for unity
        for obj in selected_objects:
            if obj.type == "MESH":
                obj.select = True
                bpy.context.scene.objects.active = obj
                obj.rotation_euler = Euler((math.pi * (-90) / 180, 0, 0), 'XYZ')
        
		# apply transform
        bpy.ops.object.transform_apply(location = True, scale = True, rotation = True)                
        
		# hack to get unity to import mesh without applying a default rotation
        for obj in selected_objects:
            if obj.type == "MESH":
                obj.select = True
                bpy.context.scene.objects.active = obj
                obj.rotation_euler = Euler((math.pi * (90) / 180, 0, 0), 'XYZ')
        
		# setup file path
        file_path = bpy.path.abspath("//")
        blend_name = bpy.path.basename(bpy.data.filepath)
        
        # change .blend to .fbx
        split = '.'
        split_blend = blend_name.split(split)
        split_blend[-1] = 'fbx'
        file_name = split.join(split_blend)
        
		# export to fbx file
        bpy.ops.export_scene.fbx(filepath=(bpy.path.abspath("//") + file_name), axis_forward='Z', axis_up='Y', use_selection=True, object_types={'MESH'})

        # apply the transform to reverse the earlier transform
        bpy.ops.object.transform_apply(location = True, scale = True, rotation = True)                
        
        return {'FINISHED'}
    
def register():
    bpy.utils.register_class(UnityExportUtil)
    
def unregister():
    bpy.utils.unregister_class(UnityExportUtil)

if __name__ == "__main__":
    register()