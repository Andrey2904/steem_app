import os
import requests
import subprocess
import winreg

def download_settings(url, save_path):
    """
    Загружает файл настроек по указанной ссылке.
    :param url: Ссылка для скачивания файла.
    :param save_path: Путь для сохранения файла.
    """
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print(f"Файл настроек загружен в {save_path}")
    else:
        print("Ошибка загрузки файла.")

def apply_registry_settings(file_path):
    """
    Применяет настройки из .reg файла в реестр Windows.
    :param file_path: Путь к файлу .reg.
    """
    try:
        subprocess.run(["regedit", "/s", file_path], check=True)
        print("Настройки успешно применены в реестр.")
    except Exception as e:
        print(f"Ошибка при внесении настроек в реестр: {e}")

def find_steam_path():
    """
    Пытается найти путь к Steam в реестре Windows.
    :return: Путь к Steam.exe или None, если не найден.
    """
    try:
        # Открываем ключ реестра, где хранится путь к Steam
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
        print("Steam не найден. Убедитесь, что Steam установлен.")
        return

    try:
        # Запуск игры через Steam
        subprocess.run([steam_path, "-applaunch", str(app_id)], check=True)
        print(f"Игра с AppID {app_id} успешно запущена.")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при запуске игры: {e}")

if __name__ == "__main__":
    # Ссылка для скачивания файла настроек
    url = "https://drive.google.com/uc?export=download&id=18Yr6wfSAJZTqhttMFVDNx7pZkez2vJBq"
    
    # Текущая директория для сохранения файла настроек
    current_dir = os.getcwd()
    settings_file = os.path.join(current_dir, "settings.reg")
    
    # Загрузка и применение настроек
    download_settings(url, settings_file)
    apply_registry_settings(settings_file)
    
    # AppID игры (например, Goose Goose Duck)
    game_app_id = "1568590"  # Замените на AppID нужной игры
    
    # Запуск игры
    launch_steam_game(game_app_id)