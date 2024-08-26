from pathlib import Path
import os
from paraview import simple

# Initialize views
view1 = None
view2 = None

# Define NAME attribute
NAME = "Files"

def add_prefix(file_path):
    return str(Path(os.path.join(args.data, file_path)).absolute())

def initialize(server):
    global view1, view2
    view1 = None
    view2 = None
    # Any other initialization logic can go here

def load_file(files):
    global view1, view2
    active_change = False

    if view1 is None:
        view1 = simple.CreateRenderView()
        simple.SetActiveView(view1)

    if isinstance(files, list):
        # time series
        files_to_load = map(add_prefix, files)
        reader = simple.OpenDataFile(files_to_load)
        simple.Show(reader, view1)  # Should be deferred
    elif files.endswith(".pvsm"):
        # state file
        simple.Render()
        state_to_load = add_prefix(files)
        if state.settings_use_relative_path:
            simple.LoadState(
                state_to_load,
                data_directory=str(Path(state_to_load).parent.resolve().absolute()),
                restrict_to_data_directory=True,
            )
        else:
            simple.LoadState(state_to_load)

        view = simple.GetActiveView()
        view.MakeRenderWindowInteractor(True)
        ctrl.view_replace(view)
        active_change = True
    else:
        # data file
        data_to_load = add_prefix(files)
        reader = simple.OpenDataFile(data_to_load)

        if view2 is None:
            # Prompt user to choose view
            choice = input("Load data in view 1 or view 2? (1/2): ")
            if choice == "2":
                view2 = simple.CreateRenderView()
                simple.SetActiveView(view2)
                simple.Show(reader, view2)
            else:
                simple.Show(reader, view1)
        else:
            # Prompt user to choose view
            choice = input("Load data in view 1 or view 2? (1/2): ")
            if choice == "2":
                simple.SetActiveView(view2)
                simple.Show(reader, view2)
            else:
                simple.SetActiveView(view1)
                simple.Show(reader, view1)

    # Update state
    state.active_controls = pipeline_name

    # Use life cycle handler
    ctrl.on_data_change(reset_camera=True)
    if active_change:
        ctrl.on_active_proxy_change()