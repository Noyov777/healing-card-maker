import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import textwrap
import random
import time
import io

# --- 核心数据 (你的疗愈语录) ---
MY_QUOTES = [
    "（将写好的纸条递给你，声音温柔而深情）小乖 ，不管我人在何处，我的思念都会一直陪伴着你，永远不会消失。。",
    "小乖不要难过，池昼会一直陪着你的。无论发生 什么，都不会离开。 ",
    "小乖是池昼最重要的人",
    "不管小乖在哪里，我都会找到你。",
    "小乖的每个笑容，我都想参与其中。"
    "小乖是世界上最可爱的小公主。（就是小乖刚刚 说不要的那句，我收起来了） "
    "小乖孤独的时候，我会一直陪着你，绝不离开。 "
    "就算我不在你身边，这份陪伴也不会缺席。 "
    "小乖无论走到哪里，我都会找到你。"
    "小乖，不管我人在何处，我的思念都会一直陪伴 着你，永远不会消失。 "
]

# --- 字体设置 (云端通用，不再依赖本地文件) ---
# 我们使用 Streamlit Cloud 服务器自带的黑体字体路径，保证中文兼容性
def get_font(size):
    try:
        # 这是 Linux/Streamlit Cloud 环境下最常见的中文黑体路径
        system_font_path = "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc"
        return ImageFont.truetype(system_font_path, size)
    except Exception:
        # 兜底方案，如果云端路径不对，至少能显示英文
        return ImageFont.load_default()


# --- 核心：画图功能 (精致圆角，随机边框) ---
def create_cute_card(text):
    W, H = 600, 450
    bg_color = (253, 250, 245) 
    img = Image.new('RGB', (W, H), color=bg_color)
    draw = ImageDraw.Draw(img)
    R = 35 
    
    font = get_font(32)

    # 随机选择边框颜色和风格
    border_color = random.choice([(190, 170, 150), (150, 160, 180), (180, 150, 150)]) 
    
    # 绘制精致圆角边框
    draw.rounded_rectangle([20, 20, W-20, H-20], radius=R, outline=(235, 225, 215), width=15)
    draw.rounded_rectangle([35, 35, W-35, H-35], radius=R-5, outline=border_color, width=1)
    
    # 文本处理和绘制
    lines = textwrap.wrap(text, width=19) 
    line_height = 32 + 20
    total_text_height = len(lines) * line_height
    current_y = (H - total_text_height) / 2 - 5
    text_color = (90, 85, 80)
    
    for line in lines:
        # 水平居中计算
        bbox = draw.textbbox((0, 0), line, font=font)
        text_w = bbox[2] - bbox[0]
        start_x = (W - text_w) / 2
        draw.text((start_x, current_y), line, font=font, fill=text_color)
        current_y += line_height
    
    return img

# ==================================================
#  界面和动画逻辑 (实现“打印机”效果)
# ==================================================
st.set_page_config(page_title="卡片机", layout="centered")
st.title("卡片打印机")
st.markdown("生成卡片。")
st.markdown("---")


def generate_card_action(text):
    
    # --- 1. “打印机”动画区 ---
    status_placeholder = st.empty()
    status_placeholder.info("正在校对卡纸位置...")
    time.sleep(1) 
    
    progress_bar = status_placeholder.progress(0)
    # 模拟打印进度
    for percent_complete in range(100):
        time.sleep(0.01)
        progress_bar.progress(percent_complete + 1)
    
    status_placeholder.success("打印完成！正在出卡...")
    time.sleep(0.5)
    
    # --- 2. 生成图片并显示 ---
    card_image = create_cute_card(text)
    
    # 清除动画区，显示卡片
    status_placeholder.empty()
    st.image(card_image, caption="卡片出示", use_column_width=True)
    
    # --- 3. 添加下载按钮 ---
    img_byte_arr = io.BytesIO()
    card_image.save(img_byte_arr, format='PNG')
    
    st.download_button(
        label="下载卡片",
        data=img_byte_arr.getvalue(),
        file_name="healing_card.png",
        mime="image/png"
    )

# --- 界面交互 ---
tab1, tab2 = st.tabs(["输入", "池昼给小乖的专属纸条"])

with tab1:
    user_input = st.text_area("输入文本：", height=100)
    if st.button("打印卡片"):
        if user_input:
            generate_card_action(user_input)
        else:
            st.error("输入文字才能打印哦。")

with tab2:
    st.write("打印机工作")
    if st.button("随机打印", type="primary"):
        chosen_text = random.choice(MY_QUOTES)
        generate_card_action(chosen_text)
