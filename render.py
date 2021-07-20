import bpy

bl_info = {
    "name": "Render Animation with nodes frame by frame",
    "author": "Barckley75",
    "blender": (3, 93, 1),
    "location": "Properties > Output Properties",
    "description": "Render the animation frame by frame avoiding crashes with node animation nodes when the auto execution is active.",
    "category": "Render",
    "doc_url": "https://github.com/barckley75/Blender_addon_render_animation_nodes"
}


class RenderAnimationNodes(bpy.types.Operator):
    """Render animation nodes frame by frame avoiding crash"""
    bl_idname = "render.render_animation_nodes"
    bl_label = "Render Animation Nodes"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        path = context.scene.render.filepath
        fileOut = path
        for frame in range(bpy.data.scenes["Scene"].frame_start, bpy.data.scenes["Scene"].frame_end + 1):
            context.scene.frame_set(frame)
            context.scene.render.filepath = fileOut + "%04d" % frame
            bpy.ops.render.render(write_still=True)

        context.scene.render.filepath = path
        print(f'Rendered in {path}')
        return {'FINISHED'}


class PROPERTIES_PT_properties(bpy.types.Panel):
    COMPAT_ENGINES = {'BLENDER_RENDER', 'BLENDER_EEVEE', 'BLENDER_WORKBENCH'}
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "output"
    bl_label = "Render Animation"

    def draw(self, context):
        layout = self.layout
        props = layout.operator("render.render_animation_nodes")


def register():
    bpy.utils.register_class(RenderAnimationNodes)
    bpy.utils.register_class(PROPERTIES_PT_properties)


def unregister():
    bpy.utils.unregister_class(RenderAnimationNodes)
    bpy.utils.unregister_class(PROPERTIES_PT_properties)


if __name__ == "__main__":
    register()
