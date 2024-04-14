import speedtest
import datetime
import json 
from pathlib import Path
import time 

def test_speed():
    """インターネットの速度を計測する
    Returns:
        dict: インターネットの速度情報(download_speed, upload_speed, ping)
    """
    st = speedtest.Speedtest()
    st.get_best_server()
    download_speed = st.download()
    upload_speed = st.upload()
    download_speed = download_speed / 1024 / 1024 # convert to Mbps
    upload_speed = upload_speed / 1024 / 1024 # convert to Mbps
    ping = st.results.ping # ms

    return {
        "download_speed": download_speed,
        "upload_speed": upload_speed,
        "ping": ping,
    }

def save_speed_info(speed_info: dict, filename: str):
    """インターネットの速度情報をファイルに保存する
    Args:
        speed_info (dict): インターネットの速度情報
        filename (str): 保存するファイル名
    """
    if filename is None:
        filename = "speedtest.log"
    # 実行パスの取得
    save_path = Path("logs") / filename

    # ファイルに保存
    try: 
        with open(save_path, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []

    now = datetime.datetime.now()
    timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
    speed_info["timestamp"] = timestamp

    data.append(speed_info)

    # 結果の保存
    with open(save_path, "w") as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    """ 1回分のチェック
    speed_info = test_speed()
    print(speed_info)
    save_speed_info(speed_info, filename="speedtest.log")
    """

    # loop
    INTERVAL = 180
    while True:
        try:
            speed_info = test_speed()
            print(speed_info)
            save_speed_info(speed_info, filename="speedtest.log")
            time.sleep(INTERVAL)
        except Exception as e:
            print(e)
            time.sleep(INTERVAL)
            continue