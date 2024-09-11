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


def initialize(server):
    state, ctrl = server.state, server.controller

    # Create two render views
    view1 = simple.CreateRenderView()
    view2 = simple.CreateRenderView()

    # state
    state.trame__title = "MTU Visualizer"
    state.trame__favicon = asset_manager.icon
    state.view_names = ["view1", "view2"]
    state.active_view = "view1"
    state.current_view = view1 
    state.show_second_view = False  # Initial state: Only one view is visible
 

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

    # Ensure the active view is updated
    ctrl.change_active_view = change_active_view
    ctrl.update_active_view = update_active_view

    with SinglePageWithDrawerLayout(server, show_drawer=True, width=300) as layout:
        layout.root = simput_widget

        # -----------------------------------------------------------------------------
        # Toolbar
        # -----------------------------------------------------------------------------
        layout.title.set_text("Visualizer")

        with layout.icon as icon:
            html.Img(src=asset_manager.icon, height=40)
            icon.click = None

        with layout.toolbar as tb:
            tb.dense = True
            tb.clipped_right = True
            vuetify.VSpacer()

            # Add a button to show/hide the second view
            with vuetify.VBtn(click=toggle_second_view, icon=False):
                vuetify.VIcon("mdi-plus")
                

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

                
                with html.Div(style=f"width: 50%; height: 100%; float: left;"):
                    html_view = paraview.VtkRemoteLocalView(
                        view1,
                        interactive_ratio=("view1_interactive_ratio", 1),
                        interactive_quality=("view1_interactive_quality", 70),
                        mode="remote",
                        namespace="view1",
                        style="width: 100%; height: 100%;",
                    )
                    ctrl.view_replace = html_view.replace_view
                    ctrl.view_update = html_view.update
                    ctrl.view_reset_camera = html_view.reset_camera
                    

                with html.Div(v_show=("show_second_view",), style="width: 50%; height: 100%; float: right;"):
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
