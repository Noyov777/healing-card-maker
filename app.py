import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import textwrap
import random
import time
import io
import os
import urllib.request

# --- 1. 核心数据 ---
MY_QUOTES = [
    "今天的星星为你闪烁，请好好休息。",
    "允许一切发生，你原本就很完整。",
    "慢慢来，好运藏在努力里。",
    "去吹吹风吧，风会带走叹息。",
    "把自己还给自己，把别人还给别人。",
    "你很可爱，值得世间所有温柔。",
    "你无需追赶任何人，你走得很好。",
]

# --- 2. 字体设置 (关键修复！) ---
def get_font(size):
    # 我们使用一个特定的文件名
    font_filename = "MaShanZheng-Regular.ttf"
    
    # 如果本地没有这个字体，就去下载
    if not os.path.exists(font_filename):
        try:
            # 这是一个非常稳定的 GitHub Raw 链接，下载可爱的马善政手写体
            url = "https://raw.githubusercontent.com/googlefonts/mashanzheng/main/ttf/MaShanZheng-Regular.ttf"
            # 伪装成浏览器下载，防止被拦截
            opener = urllib.request.build_opener()
            opener.addheaders = [('User-agent', 'Mozilla/5.0')]
            urllib.request.install_opener(opener)
            urllib.request.urlretrieve(url, font_filename)
        except Exception as e:
            # 如果下载失败，在屏幕上报错，方便调试
            st.error(f"⚠️ 字体下载失败: {e}")
            return ImageFont.load_default()

    # 尝试加载下载好的字体
    try:
        return ImageFont.truetype(font_filename, size)
    except Exception as e:
        st.error(f"⚠️ 字体加载出错: {e}")
        return ImageFont.load_default()

# --- 3. 画图功能 (粉色蕾丝可爱风) ---
def create_cute_card(text):
    W, H = 600, 450
    bg_color = (255, 248, 245) 
    img = Image.new('RGB', (W, H), color=bg_color)
    draw = ImageDraw.Draw(img)
    
    # 获取字体 (中文手写体)
    font = get_font(32)
    # 获取 emoji 字体 (稍微大一点)
    emoji_font = get_font(40) 
    
    # 粉色双层边框
    draw.rounded_rectangle([10, 10, W-10, H-10], radius=30, outline=(255, 200, 210), width=8)
    draw.rounded_rectangle([25, 25, W-25, H-25], radius=20, outline=(255, 150, 170), width=2)
    
    # 装饰点
    dot_color = (255, 180, 200)
    # 左上
    draw.ellipse([35, 35, 45, 45], fill=dot_color)
    draw.ellipse([50, 35, 60, 45], fill=dot_color)
    draw.ellipse([35, 50, 45, 60], fill=dot_color)
    # 右下
    draw.ellipse([W-45, H-45, W-35, H-35], fill=dot_color)
    draw.ellipse([W-60, H-45, W-50, H-35], fill=dot_color)
    draw.ellipse([W-45, H-60, W-35, H-50], fill=dot_color)

    # 文字绘制
    lines = textwrap.wrap(text, width=18) 
    line_height = 32 + 15
    total_text_height = len(lines) * line_height
    current_y = (H - total_text_height) / 2 
    text_color = (120, 80, 90) # 暖棕色文字
    
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        text_w = bbox[2] - bbox[0]
        start_x = (W - text_w) / 2
        draw.text((start_x, current_y), line, font=font, fill=text_color)
        current_y += line_height
    
    return img

# --- 4. 界面逻辑 ---
st.set_page_config(page_title="治愈卡片 v5.0", layout="centered")
st.title("💖 治愈卡片机 v5.0") 
st.caption("现在应该支持中文手写体啦！")
st.markdown("---")

def generate_card_action(text):
    progress_text = "✨ 正在绘制魔法阵..."
    my_bar = st.progress(0, text=progress_text)
    for percent_complete in range(100):
        time.sleep(0.01)
        my_bar.progress(percent_complete + 1, text=progress_text)
    time.sleep(0.5)
    my_bar.empty()
    
    card_image = create_cute_card(text)
    st.image(card_image, caption="你的专属卡片 (长按保存)", use_column_width=True)
    
    img_byte_arr = io.BytesIO()
    card_image.save(img_byte_arr, format='PNG')
    st.download_button("📥 下载原图", img_byte_arr.getvalue(), "card.png", "image/png")

# --- 选项卡交互区 ---
tab1, tab2 = st.tabs(["✍️ 自己写", "🎲 随机抽取"])

with tab1:
    user_input = st.text_area("输入你想打印的话：", height=100)
    if st.button("生成粉色卡片 🌸"):
        if user_input:
            generate_card_action(user_input)
        else:
            st.warning("请先输入文字哦~")

with tab2:
    st.write("不知道写什么？让魔法为你选一句吧。")
    if st.button("✨ 随机抽取一张", type="primary"):
        chosen = random.choice(MY_QUOTES)
        generate_card_action(chosen)
