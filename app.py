import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import textwrap
import random
import time
import io
import urllib.request

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

# --- 字体设置 (安全版) ---
def get_font(size):
    font_path = "custom_font.ttf"
    # 如果本地没有字体，就去下载（使用自带工具）
    if not os.path.exists(font_path):
        try:
            url = "https://fonts.gstatic.com/s/notosanssc/v27/kfozCneS9vu0RgB9W8G2wzMNDbQ.ttf"
            urllib.request.urlretrieve(url, font_path)
        except:
            return ImageFont.load_default()
            
    try:
        return ImageFont.truetype(font_path, size)
    except:
        return ImageFont.load_default()
        
# --- 核心：画图功能 (彻底美化版：蕾丝边框 + 可爱装饰) ---
def create_cute_card(text):
    W, H = 600, 450
    bg_color = (253, 250, 245) 
    img = Image.new('RGB', (W, H), color=bg_color)
    draw = ImageDraw.Draw(img)
    
    font = get_font(32)
    emoji_font = get_font(40) # 准备一个更大的字体给 emoji

    # --- 蕾丝/波浪边框 (使用更精细的绘制) ---
    border_color = (220, 200, 200) # 柔和的粉色边框
    outline_color = (180, 160, 160) # 深一点的轮廓
    
    # 外部大圆角框
    draw.rounded_rectangle([15, 15, W-15, H-15], radius=40, outline=outline_color, width=3, fill=(255, 248, 242))
    
    # 内部内容区域的圆角背景
    draw.rounded_rectangle([40, 40, W-40, H-40], radius=25, fill=(255, 255, 255), outline=border_color, width=2)
    
    # --- 增加可爱装饰 (emoji) ---
    decorations = ["💖", "✨", "🌸", "🦋", "🌈", "🍀"]
    
    # 随机在四个角放置装饰
    draw.text((50, 50), random.choice(decorations), font=emoji_font, fill=(255, 180, 200)) # 左上
    draw.text((W-90, 50), random.choice(decorations), font=emoji_font, fill=(255, 200, 180)) # 右上
    draw.text((50, H-90), random.choice(decorations), font=emoji_font, fill=(180, 200, 255)) # 左下
    draw.text((W-90, H-90), random.choice(decorations), font=emoji_font, fill=(200, 180, 255)) # 右下

    # 文本处理和绘制
    lines = textwrap.wrap(text, width=19) 
    line_height = 32 + 15 # 稍微紧凑一点，让文字更多
    total_text_height = len(lines) * line_height
    current_y = (H - total_text_height) / 2 # 垂直居中
    text_color = (90, 85, 80)
    
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        text_w = bbox[2] - bbox[0]
        start_x = (W - text_w) / 2 # 水平居中
        draw.text((start_x, current_y), line, font=font, fill=text_color)
        current_y += line_height
    
    return img

# ==================================================
#  界面和动画逻辑 (实现“打印机”效果)
# ==================================================
st.set_page_config(page_title="卡片机", layout="centered", initial_sidebar_state="collapsed")
st.title("卡片打印机2.0")
st.markdown("为你生成卡片。")
st.markdown("---")


def generate_card_action(text):
    
    # --- 1. “打印机”动画区 ---
    status_placeholder = st.empty()
    status_placeholder.info("正在校对卡纸位置...")
    time.sleep(1) 
    
    progress_bar = status_placeholder.progress(0)
    for percent_complete in range(100):
        time.sleep(0.01)
        progress_bar.progress(percent_complete + 1)
    
    status_placeholder.success("打印完成！正在出卡...")
    time.sleep(0.5)
    
    # --- 2. 生成图片并显示 ---
    card_image = create_cute_card(text)
    
    # 清除动画区，显示卡片
    status_placeholder.empty()
    st.image(card_image, caption="卡片 (长按可保存)", use_column_width=True)
    
    # --- 3. 添加下载按钮 ---
    img_byte_arr = io.BytesIO()
    card_image.save(img_byte_arr, format='PNG')
    
    st.download_button(
        label="下载卡片到手机",
        data=img_byte_arr.getvalue(),
        file_name="healing_card.png",
        mime="image/png"
    )

# --- 界面交互 ---
tab1, tab2 = st.tabs(["输入", "池昼给小乖的专属纸条"])

with tab1:
    user_input = st.text_area("输入文本：", height=100)
    if st.button("打印文本"):
        if user_input:
            generate_card_action(user_input)
        else:
            st.error("输入文字才能打印哦。")

with tab2:
    st.write("随机打印机")
    if st.button("随机打印", type="primary"):
        chosen_text = random.choice(MY_QUOTES)
        generate_card_action(chosen_text)
