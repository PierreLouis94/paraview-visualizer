from trame.app import dev
from trame.ui.vuetify import SinglePageWithDrawerLayout
from trame.widgets import vuetify, paraview, simput, html

from trame_simput import get_simput_manager

from paraview import simple

# from pv_visualizer import html as my_widgets
from pv_visualizer.app.assets import asset_manager
from pv_visualizer.app.ui import (
    pipeline,
    files,
    algorithms,
    settings,
    view_toolbox,
    state_change,
)


def _reload():
    dev.reload(
        pipeline,
        files,
        algorithms,
        settings,
        view_toolbox,
        state_change,
    )


# -----------------------------------------------------------------------------
# Common style properties
# -----------------------------------------------------------------------------

COMPACT = {
    "dense": True,
    "hide_details": True,
}

CONTROLS = [
    pipeline,
    files,
    algorithms,
    settings,
]

# -----------------------------------------------------------------------------
# Dynamic reloading
# -----------------------------------------------------------------------------

LIFE_CYCLES = [
    "on_data_change",
    "on_active_proxy_change",
]

# -----------------------------------------------------------------------------
# Layout
# -----------------------------------------------------------------------------

synchronization_enabled = False

def initialize(server):
    state, ctrl = server.state, server.controller

    # Create two render views
    view1 = simple.CreateRenderView()
    view2 = simple.CreateRenderView()

    # state
    state.trame__title = "MTU Visualizer"
    state.trame__favicon = asset_manager.icon

    
    state.active_view = "view1"
    state.current_view = view1 
    state.show_second_view = False  # Initial state: Only one view is visible
    state.sync_status = "unlocked"


    # controller
    ctrl.on_server_reload.add(_reload)
    ctrl.on_data_change.add(ctrl.view_update)
    ctrl.on_data_change.add(ctrl.pipeline_update)
    ctrl.toggle_second_view = lambda: toggle_second_view(server)

    # Init other components
    state_change.initialize(server)
    for m in CONTROLS:
        m.initialize(server)

    # simput
    simput_manager = get_simput_manager("pxm")
    simput_widget = simput.Simput(
        simput_manager,
        prefix="pxm",
        trame_server=server,
        ref="simput",
        query=("search", ""),
    )
    ctrl.pxm_apply = simput_widget.apply
    ctrl.pxm_reset = simput_widget.reset

    def force_render(view):
        def decorator(func):
            def wrapper(*args, **kwargs):
                result = func(*args, **kwargs)
                view.Render()
                simple.Render(view)
                return result
            return wrapper
        return decorator
    

    def change_active_view():
        if state.active_view  == "view1":
            state.active_view  = "view2"
            simple.SetActiveView(view2)
        else:
            state.active_view = "view1"
            simple.SetActiveView(view1)

    def toggle_second_view():
        state.show_second_view = not state.show_second_view

    # Update views based on which is active
    def update_active_view():
        simple.SetActiveView(state.current_view)
        ctrl.view_update()

    #@force_render(view1)
    def reset_camera_view1():
        camera = view1.GetActiveCamera()
        camera.SetPosition(1000, 0, 1000)
        camera.SetFocalPoint(0, 0, 0)
        camera.SetViewUp(0, 1, 0)

        # Force the render to refresh immediately
        view1.Render()
        ctrl.view_update()
        state.flush()

    def reset_camera_view2():
        camera = view2.GetActiveCamera()
        camera.SetPosition(1000, 0, 1000)
        camera.SetFocalPoint(0, 0, 0)
        camera.SetViewUp(0, 1, 0)

        # Force the render to refresh immediately
        view2.Render()
        ctrl.view_update()
        state.flush()

    def synchronize_cameras():
        if state.sync_status == "locked":
            camera1 = view1.GetActiveCamera()
            camera2 = view2.GetActiveCamera()
            
            camera2.SetPosition(camera1.GetPosition())
            camera2.SetFocalPoint(camera1.GetFocalPoint())
            camera2.SetViewUp(camera1.GetViewUp())
            camera2.SetViewAngle(camera1.GetViewAngle())
        else:
            pass
        
        view2.Render()
        simple.Render(view2)

    def change_sync_status():
        
        if state.sync_status == "unlocked":
            state.sync_status = "locked"
        else:
            state.sync_status = "unlocked"
            
            

        # Ensure the state change is flushed to update the UI
        state.dirty("sync_status")
        state.flush()


    # Ensure the active view is updated
    ctrl.reset_camera_view1 = reset_camera_view1
    ctrl.reset_camera_view2 = reset_camera_view2
    ctrl.change_sync_status = change_sync_status
    ctrl.change_active_view = change_active_view
    ctrl.update_active_view = update_active_view

    with SinglePageWithDrawerLayout(server, show_drawer=True, width=300) as layout:
        layout.root = simput_widget

        # -----------------------------------------------------------------------------
        # Toolbar
        # -----------------------------------------------------------------------------
        layout.title.set_text("MTU Visualizer")

        with layout.icon as icon:
            html.Img(src=asset_manager.icon, height=40)
            icon.click = None

        with layout.toolbar as tb:
            tb.dense = True
            tb.clipped_right = True
            vuetify.VSpacer()

            with vuetify.VBtn(click=toggle_second_view, icon=True):
                vuetify.VIcon("mdi-arrow-split-vertical")
                
            vuetify.VSpacer()

            with vuetify.VBtn(click=change_active_view, icon=True):
                vuetify.VIcon("mdi-swap-horizontal")
            vuetify.VTextField(
                v_model=("active_view ",),
                readonly=True,
                dense=True,
                hide_details=True,
                outlined=True,
                style="max-width: 67px;",
            )
            vuetify.VSpacer()
            vuetify.VTextField(
                v_show=("!!active_controls",),
                v_model=("search", ""),
                clearable=True,
                outlined=True,
                filled=True,
                rounded=True,
                prepend_inner_icon="mdi-magnify",
                style="max-width: 30vw;",
                **COMPACT,
            ) 

            vuetify.VSpacer()

            # Attach the function to a button click event
            with vuetify.VBtn(click=reset_camera_view1, icon=True):
                vuetify.VIcon("mdi-numeric-1-box-outline")

            # Attach the function to a button click event
            with vuetify.VBtn(click=reset_camera_view2, icon=True):
                vuetify.VIcon("mdi-numeric-2-box-outline")

            with vuetify.VBtn(click=change_sync_status, icon=True):
                vuetify.VIcon("mdi-lock")

            vuetify.VTextField(
                v_model=("sync_status",),
                readonly=True,
                dense=True,
                hide_details=True,
                outlined=True,
                style="max-width: 100px;",
            )

            with vuetify.VBtn(click=synchronize_cameras, icon=True):
                vuetify.VIcon("mdi-sync")

            vuetify.VSpacer()

            with vuetify.VBtnToggle(
                v_model=("active_controls", "files"),
                **COMPACT,
                outlined=True,
                rounded=True,
            ):
                for item in CONTROLS:
                    with vuetify.VBtn(value=item.NAME, **COMPACT):
                        vuetify.VIcon(item.ICON, **item.ICON_STYLE)
            
            

        # -----------------------------------------------------------------------------=
        # Drawer
        # -----------------------------------------------------------------------------
        with layout.drawer as dr:
            dr.left = True
            # dr.expand_on_hover = True
            for item in CONTROLS:
                item.create_panel(server)

        # -----------------------------------------------------------------------------
        # Main content
        # -----------------------------------------------------------------------------
        with layout.content:
            with vuetify.VContainer(fluid=True, classes="fill-height pa-0 ma-0"):
                view_toolbox.create_view_toolbox(server)

                
                with html.Div(style="flex: 1; height: 100%; border-right: 2px solid #ddd;"):  # border between views
                    html_view = paraview.VtkRemoteLocalView(
                        view1,
                        interactive_ratio=("view1_interactive_ratio", 1),
                        interactive_quality=("view1_interactive_quality", 70),
                        mode="remote",
                        namespace="view1",
                        style="flex: 1%; height: 100%;",
                    )
                    ctrl.view_replace = html_view.replace_view
                    ctrl.view_update = html_view.update
                    ctrl.view_reset_camera = html_view.reset_camera
                        


                with html.Div(v_show=("show_second_view",), style="flex: 1; height: 100%;"):    
                    html_view = paraview.VtkRemoteLocalView(
                        view2,
                        interactive_ratio=("view2_interactive_ratio", 1),
                        interactive_quality=("view2_interactive_quality", 70),
                        mode="remote",
                        namespace="view2",
                        style="width: 100%; height: 100%;",
                    )
                    ctrl.view_replace = html_view.replace_view
                    ctrl.view_update = html_view.update
                    ctrl.view_reset_camera = html_view.reset_camera
                    

                ctrl.on_server_ready.add(ctrl.view_update)


        # -----------------------------------------------------------------------------
        # Footer
        # -----------------------------------------------------------------------------
        # layout.footer.hide()
