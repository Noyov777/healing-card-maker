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

# --- 2. 字体设置 (可爱艺术字体下载) ---
def get_font(size):
    font_filename = "ZhuoLi.ttf" # 这是一个更可爱的艺术字体
    
    # 尝试下载可爱的“字体传奇卓丽体”
    if not os.path.exists(font_filename):
        try:
            url = "https://raw.githubusercontent.com/lxgw/zhuanzhi-font/main/TTF/LXGWWenKai-Regular.ttf" # 换成一个更可靠的艺术字体
            opener = urllib.request.build_opener()
            opener.addheaders = [('User-agent', 'Mozilla/5.0')]
            urllib.request.install_opener(opener)
            urllib.request.urlretrieve(url, font_filename)
        except Exception as e:
            print(f"艺术字体下载失败: {e}")

    try:
        return ImageFont.truetype(font_filename, size)
    except:
        # 备用字体（文泉驿微米黑，确保中文显示）
        try:
            return ImageFont.truetype("/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc", size)
        except:
            return ImageFont.load_default()

# --- 3. 蕾丝边框图片下载 (核心美学实现) ---
def get_lace_border_image():
    lace_filename = "lace_border.png"
    if not os.path.exists(lace_filename):
        try:
            # 这是一个预设的、可爱的蕾丝边框透明PNG图片
            url = "https://i.ibb.co/CsgzQ9j/lace-border.png" # 请确保这个链接有效且图片是透明PNG
            opener = urllib.request.build_opener()
            opener.addheaders = [('User-agent', 'Mozilla/5.0')]
            urllib.request.install_opener(opener)
            urllib.request.urlretrieve(url, lace_filename)
        except Exception as e:
            st.error(f"蕾丝边框图片下载失败: {e}")
            return None
    try:
        return Image.open(lace_filename).convert("RGBA")
    except Exception as e:
        st.error(f"蕾丝边框图片加载失败: {e}")
        return None

# --- 4. 画图功能 (蕾丝叠加 + 艺术字体) ---
def create_cute_card(text):
    W, H = 600, 450
    bg_color = (255, 248, 245) 
    img = Image.new('RGB', (W, H), color=bg_color)
    draw = ImageDraw.Draw(img)
    
    font = get_font(32)
    
    # 绘制最底层的简单圆角底色（防止蕾丝图片下载失败）
    draw.rounded_rectangle([10, 10, W-10, H-10], radius=30, fill=(255, 240, 245)) 

    # 尝试叠加蕾丝边框
    lace_img = get_lace_border_image()
    if lace_img:
        lace_img = lace_img.resize((W, H))
        img = Image.alpha_composite(img.convert("RGBA"), lace_img) # 叠加透明蕾丝
        draw = ImageDraw.Draw(img) # 重新获取draw对象，在叠加后的图上画字
    else:
        # 如果蕾丝图下载失败，退回到之前的粉色双层边框
        draw.rounded_rectangle([10, 10, W-10, H-10], radius=30, outline=(255, 200, 210), width=8)
        draw.rounded_rectangle([25, 25, W-25, H-25], radius=20, outline=(255, 150, 170), width=2)

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

# --- 5. 界面逻辑 ---
st.set_page_config(page_title="治愈卡片 v8.0", layout="centered")
st.title("💖 治愈卡片机 v8.0") 
st.caption("现在是真·蕾丝花边和可爱艺术字体啦！")
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

# --- 交互区 ---
tab1, tab2 = st.tabs(["✍️ 自己写", "🎲 随机抽取"])

with tab1:
    user_input = st.text_area("输入你想打印的话：", height=100)
    if st.button("生成蕾丝卡片 🌸"):
        if user_input:
            generate_card_action(user_input)
        else:
            st.warning("请先输入文字哦~")

with tab2:
    if st.button("✨ 随机抽取一张", type="primary"):
        chosen = random.choice(MY_QUOTES)
        generate_card_action(chosen)
