import frida
from frida.core import Device

from FileManager import save_log


def get_devices():
    return frida.get_device_manager().enumerate_devices()


def get_apps(device: Device):
    apps = device.enumerate_applications()
    print(apps)
    iden = [app.identifier for app in apps]
    print(iden)
    return iden


def get_processes(device: Device):
    process = device.enumerate_processes()
    print(process)
    names = [process.name for process in process]
    print(names)
    return names


def on_message(message, data):
    if message["type"] == "send":
        save_log(message["payload"])
    else:
        save_log(message)
        save_log(data)


def run_script(device_id, app_identifier, script_text):
    selected_device: Device = [dev for dev in get_devices() if dev.id == device_id][0]
    app = [app for app in selected_device.enumerate_applications() if app.identifier == app_identifier][
        0]
    try:
        app_id = app.pid
        if app_id == 0 or app_id is None:
            app_id = selected_device.spawn([app.identifier])
            save_log(f"App {app.identifier} is not running. Starting the app with PID: {app_id}")
            selected_device.resume(app_id)
            save_log(f"App {app.identifier} is started with PID: {app_id}")

        session = selected_device.attach(app_id)
        save_log(f"Attaching to the app {app.identifier} with PID: {app_id}")
        script = session.create_script(script_text)
        script.on('message', on_message)
        script.load()
        save_log(f"Script is loaded to the app {app.identifier} with PID: {app_id}")
        selected_device.resume(app_id)
        save_log(f"Resuming the app {app.identifier} with PID: {app_id}")
    except Exception as e:
        save_log("!!!! -------------- Error occurred while running the script----------------!!!! ")
        save_log(str(selected_device))
        save_log(str(app))
        save_log(str(e))
