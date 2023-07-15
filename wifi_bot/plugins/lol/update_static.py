import json
import requests
from tqdm import tqdm

from constants import *

LEGENDS_INFO_PATH = "../../static/lol/legends_info.json"
LEGENDS_ICON_PATH = "../../static/lol/icons/legends/"
LEGENDS_ICON_URL = "https://game.gtimg.cn/images/lol/act/img/champion/"
LEGENDS_URL = "https://game.gtimg.cn/images/lol/act/img/js/heroList/hero_list.js"

IMG_EXTENSION_NAME = ".png"


def update_legends_info():
    response = requests.get(LEGENDS_URL)
    # 保存所有英雄信息的json文件到本地
    with open(LEGENDS_INFO_PATH, "wb") as f:
        f.write(response.content)


def update_legends_icon():
    response = requests.get(LEGENDS_URL)
    legends_list = json.loads(response.text)["hero"]
    for legend in tqdm(legends_list):
        # 获取英雄id和别名（英文名）
        legend_id = legend["heroId"]
        legend_alias = legend["alias"]
        # 图片请求url
        legend_icon_url = LEGENDS_ICON_URL + legend_alias + IMG_EXTENSION_NAME
        # 获取英雄icon图片
        response = requests.get(legend_icon_url)
        # 图片保存路径
        legend_icon_path = LEGENDS_ICON_PATH + legend_id + IMG_EXTENSION_NAME
        # 保存英雄icon图片到本地
        with open(legend_icon_path, "wb") as f:
            f.write(response.content)


if __name__ == '__main__':
    update_legends_info()
    update_legends_icon()
