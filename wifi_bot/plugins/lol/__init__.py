import re
import json
import requests
from PIL import Image, ImageDraw, ImageFont
from nonebot.plugin import on_command
from nonebot.adapters.onebot.v11 import MessageSegment

from wifi_bot.plugins.lol.constants import *
from wifi_bot.utils.image import image_to_base64

lol_free_legends = on_command("lol周免", aliases={"LOL周免"}, priority=20, block=True)


@lol_free_legends.handle()
async def _get_lol_free_legends():
    # 获取周免英雄id列表
    response = requests.get(FREE_LEGENDS_URL)
    regex = re.match("(.+)return(.+)}\);(.+)", response.text)
    all_free_legends_dict = json.loads(regex.groups()[1][:-1])
    free_legends_dict = all_free_legends_dict.get(str(max(list(map(int, list(all_free_legends_dict.keys()))))))
    free_legends = free_legends_dict['freeHero'].split(',')
    # 读取英雄信息json文件
    with open(LEGENDS_INFO_PATH, 'r') as f:
        legends_list = json.loads(f.readline())["hero"]
    # 按英雄id顺序从小到大获取周免英雄在英雄信息json中的索引位置index
    free_legends_idx_in_legends_list = [i for i, legend_info in enumerate(legends_list) if legend_info["heroId"] in free_legends]
    # 加载背景图片、边框图片、字体文件、背景叠加图层
    free_legends_bg = Image.open(FREE_LEGENDS_BG_PATH).convert("RGBA")
    legends_mask = Image.open(LEGENDS_MASK_PATH).convert("RGBA")
    font = ImageFont.truetype(FONT_CN_PATH, 18, encoding="utf-8")
    draw = ImageDraw.Draw(free_legends_bg)
    # 生成2行10列的周免英雄图片
    for i in range(2):
        for j in range(10):
            print(free_legends[i * 10 + j])
            # 加载英雄icon图片
            icon = Image.open(LEGENDS_ICON_PATH + legends_list[free_legends_idx_in_legends_list[i * 10 + j]]["heroId"] + IMG_EXTENSION_NAME).convert("RGBA").resize((100, 100))
            # 在icon上叠加边框图片（通过RGBA的A通道选择mask位置）
            icon.paste(legends_mask, (0, 0), mask=legends_mask.split()[3])
            # 在背景图片上叠加上述带边框英雄图片
            free_legends_bg.paste(icon, (40 + 120 * j, 40 + 165 * i))
            # 从英雄信息json文件中获取对应id的中文英雄名和称号
            free_legend_info = legends_list[free_legends_idx_in_legends_list[i * 10 + j]]
            name, title = free_legend_info["name"], free_legend_info["title"]
            # 在背景图片对应位置添加文本（英雄名和称号）
            w = draw.textlength(name, font=font)
            draw.text((40 + 120 * j + (100 - w) / 2, 40 + 165 * i + 105), name, (202, 196, 181), font)
            w = draw.textlength(title, font=font)
            draw.text((40 + 120 * j + (100 - w) / 2, 40 + 165 * i + 130), title, (202, 196, 181), font)
    # 保存样例图片
    # free_legends_bg.save("wifi_bot/static/lol/free_legends_result_example.png")
    # TODO: 判断是哪个driver使用，返回对应结果
    # 以base64格式发送图片（QQ机器人用）
    await lol_free_legends.finish(MessageSegment.image(f"base64://{str(image_to_base64(free_legends_bg), encoding='utf-8')}"))


# TODO: 加入大乱斗周免英雄列表展示功能
# lol_aram_free_legends = on_command("lol大乱斗周免", aliases={"LOL大乱斗周免"}, priority=20, block=True)
