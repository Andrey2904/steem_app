import subprocess
import winreg
import os

def find_steam_path():
    """
    Пытается найти путь к Steam в реестре Windows.
    :return: Путь к Steam.exe или None, если не найден.
    """
    try:
        
        reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\\WOW6432Node\\Valve\\Steam")
        steam_path = winreg.QueryValueEx(reg_key, "InstallPath")[0]
        steam_exe = os.path.join(steam_path, "Steam.exe")
        if os.path.exists(steam_exe):
            return steam_exe
    except FileNotFoundError:
        pass
    return None

def launch_steam_game(app_id):
    """
    Запускает игру в Steam по её AppID.
    :param app_id: AppID игры в Steam.
    """
    steam_path = find_steam_path()

    if not steam_path:
        print("Steam не найден.")
        return

    try:
        
        subprocess.run([steam_path, "-applaunch", str(app_id)], check=True) 
        print(f"Игра с AppID {app_id} успешно запущена.")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при запуске игры: {e}")


if __name__ == "__main__":
    
    game_app_id = "1568590"  

    launch_steam_game(game_app_id)