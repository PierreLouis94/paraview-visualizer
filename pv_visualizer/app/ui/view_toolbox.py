from trame.widgets import vuetify

STYLE = {"small": True, "icon": True}

def create_view_toolbox(server):
    ctrl = server.controller
    with vuetify.VCard(
        elevation=3,
        classes="d-flex flex-column rounded-lg pa-1",
        style="position: absolute; left: 20px; top: 20px; z-index: 1;",
    ):
        with vuetify.VBtn(**STYLE, click=ctrl.view_reset_camera):
            vuetify.VIcon("mdi-crop-free")
        # Add button to toggle second view
        with vuetify.VBtn(
            **STYLE,
            click="view2_active = !view2_active",
        ):
            vuetify.VIcon("mdi-arrow-split-vertical")
