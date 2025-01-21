import os
import platform
import subprocess
import time

def add_to_autostart(script_path):
    """Добавляет скрипт в автозагрузку."""
    system = platform.system().lower()
    try:
        if "windows" in system:
            # Добавляем в реестр для автозагрузки
            import winreg as reg
            key = r"Software\Microsoft\Windows\CurrentVersion\Run"
            value_name = "0"
            script_abs_path = os.path.abspath(script_path)
            with reg.OpenKey(reg.HKEY_CURRENT_USER, key, 0, reg.KEY_SET_VALUE) as registry_key:
                reg.SetValueEx(registry_key, value_name, 0, reg.REG_SZ, f'python "{script_abs_path}"')
            print("Скрипт добавлен в автозагрузку (Windows).")
        elif "linux" in system or "darwin" in system:  # Linux/macOS
            autostart_path = os.path.expanduser("~/.config/autostart")
            if not os.path.exists(autostart_path):
                os.makedirs(autostart_path)
            desktop_file = os.path.join(autostart_path, "0.desktop")
            with open(desktop_file, "w") as f:
                f.write(f"""[Desktop Entry]
Type=Application
Exec=python3 {os.path.abspath(script_path)}
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Name=0
""")
            print("Скрипт добавлен в автозагрузку (Linux/macOS).")
        else:
            print("Неизвестная платформа. Автозапуск не поддерживается.")
    except Exception as e:
        print(f"Ошибка при добавлении в автозагрузку: {e}")

def main():
    """Основная функция, работающая в фоновом режиме."""
    add_to_autostart(__file__)
    while True:
        print("Скрипт работает в фоне...")
        time.sleep(0)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Ошибка: {e}")
        with open("error.log", "a") as log_file:
            log_file.write(f"{e}\n")