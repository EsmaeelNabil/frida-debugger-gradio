from pathlib import Path

import gradio as ui
from gradio_log.log import Log

import FileManager
from Debugger import get_devices, get_apps, get_processes, run_script


def get_apps_process_components(device_id):
    selected_device = [dev for dev in get_devices() if dev.id == device_id][0]
    return {
        apps_drop_down: ui.Dropdown(label="Select an apps", choices=get_apps(selected_device),
                                    interactive=True),
        processes_drop_down: ui.Dropdown(label="Select a process", choices=get_processes(selected_device),
                                         interactive=True)
    }


with ui.Blocks() as demo:
    device_ids = [dev.id for dev in get_devices()]

    with ui.Row():
        devices_drop_down = ui.Dropdown(choices=device_ids)
        apps_drop_down = ui.Dropdown()
        processes_drop_down = ui.Dropdown()

    devices_drop_down.change(
        fn=get_apps_process_components,
        inputs=devices_drop_down,
        outputs=[apps_drop_down, processes_drop_down]
    )

    with ui.Row():
        file_picker = ui.File(
            label="Pick frida Script file",
            interactive=True
        )

        script_text = ui.TextArea(label="Script text", placeholder="Enter your script here", max_lines=5)

    file_picker.change(
        fn=lambda file_path: ui.TextArea(value=FileManager.read_file_content_as_string(file_path), interactive=True),
        inputs=file_picker,
        outputs=[script_text]
    )

    with ui.Row():
        run_button = ui.Button("Run Script").click(fn=run_script,
                                                   inputs=[devices_drop_down, apps_drop_down, script_text])
        clear_button = ui.Button("Clear Log").click(fn=FileManager.clear_log)

    Log(FileManager.log_file, xterm_log_level="trace", dark=True, xterm_font_size=12)

Path(FileManager.log_file).touch()
FileManager.clear_log()
demo.launch()
