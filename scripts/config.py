import os


# 从环境变量中提取教务系统的URL、用户名、密码和TOKEN等信息
force_push_message = os.environ.get("FORCE_PUSH_MESSAGE")
github_actions = os.environ.get("GITHUB_ACTIONS")
url = os.environ.get("URL")
username = os.environ.get("USERNAME")
password = os.environ.get("PASSWORD")
token = os.environ.get("TOKEN")
github_ref_name = os.environ.get("GITHUB_REF_NAME")
github_event_name = os.environ.get("GITHUB_EVENT_NAME")
github_actor = os.environ.get("GITHUB_ACTOR")
github_actor_id = os.environ.get("GITHUB_ACTOR_ID")
github_triggering_actor = os.environ.get("GITHUB_TRIGGERING_ACTOR")
repository_name = os.environ.get("REPOSITORY_NAME")
github_sha = os.environ.get("GITHUB_SHA")
github_workflow = os.environ.get("GITHUB_WORKFLOW")
github_run_number = os.environ.get("GITHUB_RUN_NUMBER")
github_run_id = os.environ.get("GITHUB_RUN_ID")
beijing_time = os.environ.get("BEIJING_TIME")
github_step_summary = os.environ.get("GITHUB_STEP_SUMMARY")

# 将字符串转换为布尔值
# 是否强制推送信息
# 若是非GitHub Actions环境,则默认强制推送信息
force_push_message = force_push_message == "True" if github_actions else True


def read_local_config():
    """读取配置文件中的URL、用户名、密码和TOKEN等信息。
    如果环境变量中未设置这些信息，则从同级目录中的config.txt文件读取。
    如果config.txt文件不存在，则创建该文件并提示用户填写必要的配置项。
    开发或本地运行环境下，默认从config.txt文件读取配置。
    生产环境下，通常通过环境变量设置这些信息。
    Raises:
        ValueError: 如果config.txt中缺少必要的配置项。
        FileNotFoundError: 如果config.txt文件不存在。
    Returns:
        dict: 包含URL、用户名、密码和TOKEN的字典。
    """
    global url, username, password, token
    # 如果是开发/本地运行环境，读取同级目录中config.txt中的配置
    if not url or not username or not password:
        config_file_path = os.path.join(os.path.dirname(__file__), "config.txt")
        # 检查config.txt文件是否存在
        if os.path.exists(config_file_path):
            with open(config_file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            for line in lines:
                if line.startswith("URL="):
                    url = line.split("=", 1)[1].strip()
                elif line.startswith("USERNAME="):
                    username = line.split("=", 1)[1].strip()
                elif line.startswith("PASSWORD="):
                    password = line.split("=", 1)[1].strip()
                elif line.startswith("TOKEN="):
                    token = line.split("=", 1)[1].strip()
            if not url or not username or not password or not token:
                raise ValueError("config.txt中缺少必要的配置项，请检查URL、USERNAME、PASSWORD和TOKEN是否已填写。")
        # 如果config.txt文件不存在，则创建config.txt文件
        else:
            with open(config_file_path, "w", encoding="utf-8") as f:
                f.write("URL=\n")
                f.write("USERNAME=\n")
                f.write("PASSWORD=\n")
                f.write("TOKEN=\n")
            raise FileNotFoundError(
                f"config.txt文件不存在，已在同级目录创建，请填写URL、USERNAME、PASSWORD和TOKEN。")
    return {
        "url": url,
        "username": username,
        "password": password,
        "token": token
    }

if not github_actions:
    url, username, password, token = read_local_config().values()

if __name__ == "__main__":
    print(f"URL: {url}")
    print(f"USERNAME: {username}")
    print(f"PASSWORD: {password}")
    print(f"TOKEN: {token}")