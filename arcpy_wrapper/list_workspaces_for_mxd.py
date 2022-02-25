import arcpy

def list_workspaces(mxd):
        workspaces = []
        layers = arcpy.mapping.ListLayers(mxd)
        for layer in layers:
            if layer.supports("WORKSPACEPATH"):
                workspaces.append(layer.workspacePath)
        return workspaces