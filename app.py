import streamlit as st
import json
import urllib.parse
import random
from datetime import datetime
from lunar_python import Lunar, Solar

trigrams = ["☰", "☱", "☲", "☳", "☴", "☵", "☶", "☷"]
trigram_names = ["乾", "兑", "离", "震", "巽", "坎", "艮", "坤"]
hexagrams = [
    "䷀",
    "䷁",
    "䷂",
    "䷃",
    "䷄",
    "䷅",
    "䷆",
    "䷇",
    "䷈",
    "䷉",
    "䷊",
    "䷋",
    "䷌",
    "䷍",
    "䷎",
    "䷏",
    "䷐",
    "䷑",
    "䷒",
    "䷓",
    "䷔",
    "䷕",
    "䷖",
    "䷗",
    "䷘",
    "䷙",
    "䷚",
    "䷛",
    "䷜",
    "䷝",
    "䷞",
    "䷟",
    "䷠",
    "䷡",
    "䷢",
    "䷣",
    "䷤",
    "䷥",
    "䷦",
    "䷧",
    "䷨",
    "䷩",
    "䷪",
    "䷫",
    "䷬",
    "䷭",
    "䷮",
    "䷯",
    "䷰",
    "䷱",
    "䷲",
    "䷳",
    "䷴",
    "䷵",
    "䷶",
    "䷷",
    "䷸",
    "䷹",
    "䷺",
    "䷻",
    "䷼",
    "䷽",
    "䷾",
    "䷿",
]
hexagram_names = [
    "乾",
    "坤",
    "屯",
    "蒙",
    "需",
    "讼",
    "师",
    "比",
    "小畜",
    "履",
    "泰",
    "否",
    "同人",
    "大有",
    "谦",
    "豫",
    "随",
    "蛊",
    "临",
    "观",
    "噬嗑",
    "贲",
    "剥",
    "复",
    "无妄",
    "大畜",
    "颐",
    "大过",
    "坎",
    "离",
    "咸",
    "恒",
    "遁",
    "大壮",
    "晋",
    "明夷",
    "家人",
    "睽",
    "蹇",
    "解",
    "损",
    "益",
    "夬",
    "姤",
    "萃",
    "升",
    "困",
    "井",
    "革",
    "鼎",
    "震",
    "艮",
    "渐",
    "归妹",
    "丰",
    "旅",
    "巽",
    "兑",
    "涣",
    "节",
    "中孚",
    "小过",
    "既济",
    "未济",
]
# hexagram_name = [
#     "乾", "坤", "屯", "蒙", "需", "訟", "師", "比", "小畜", "履", "泰", "否", "同人", "大有",
#     "謙", "豫", "隨", "蠱", "臨", "觀", "噬嗑", "贲", "剝", "複", "無妄", "大畜", "頤", "大過",
#     "坎", "離", "鹹", "恒", "遁", "大壯", "晉", "明夷", "家人", "睽", "蹇", "解", "損", "益",
#     "夬", "姤", "萃", "升", "困", "井", "革", "鼎", "震", "艮", "漸", "歸妹", "豐", "旅", "巽",
#     "兌", "渙", "節", "中孚", "小過", "既濟", "未濟"
# ]
moving_lines = ["初", "二", "三", "四", "五", "上"]


def get_binstr(num, nbits=3):
    return bin(num)[2:].zfill(nbits)


def trigrams_to_hexagram_binstr(upper_idx, lower_idx):
    return get_binstr(lower_idx) + get_binstr(upper_idx)


def flip_bits(bits):
    return "".join("1" if bit == "0" else "0" for bit in bits)


def flip_bit(bits, n):
    return bits[:n] + ("1" if bits[n] == "0" else "0") + bits[n + 1 :]


def normalize(n):
    if n == 0:
        return 10
    else:
        return n


st.set_page_config(page_title="简易算卦", page_icon="☯")
st.title("简易算卦")

with open("gua.json", "r") as f:
    data = json.load(f)

st.write("集中精力想象需要算卦的事由，任意输入三个数，点击算卦，即可得到卦象和卦辞。")

# 初始化 session state
if "random_n1" not in st.session_state:
    st.session_state.random_n1 = 0
if "random_n2" not in st.session_state:
    st.session_state.random_n2 = 0
if "random_n3" not in st.session_state:
    st.session_state.random_n3 = 0

submitted = False
with st.form(key="divination"):
    reason = st.text_input("简述起卦的事由", placeholder="一事一卦，心诚则灵")
    col1, col2, col3 = st.columns(3)
    with col1:
        n1 = st.number_input(
            "第一个数", min_value=0, value=st.session_state.random_n1, format="%i"
        )
        n1 = normalize(n1)
    with col2:
        n2 = st.number_input(
            "第二个数", min_value=0, value=st.session_state.random_n2, format="%i"
        )
        n2 = normalize(n2)
    with col3:
        n3 = st.number_input(
            "第三个数", min_value=0, value=st.session_state.random_n3, format="%i"
        )
        n3 = normalize(n3)

    col_random, col_submit = st.columns([1, 1])
    with col_random:
        random_clicked = st.form_submit_button("🎲 随机生成", use_container_width=True)
    with col_submit:
        submitted = st.form_submit_button(
            "算卦", type="primary", use_container_width=True
        )

if random_clicked:
    st.session_state.random_n1 = random.randint(1, 100)
    st.session_state.random_n2 = random.randint(1, 100)
    st.session_state.random_n3 = random.randint(1, 100)
    st.rerun()

if not submitted:
    st.stop()

# 检查事由是否为空
if not reason or reason.strip() == "":
    st.error("❌ 请填写起卦事由。一事一卦，心诚则灵。")
    st.stop()

upper_trigram_idx = n1 % 8 - 1
if upper_trigram_idx == -1:
    upper_trigram_idx = 7
lower_trigram_idx = n2 % 8 - 1
if lower_trigram_idx == -1:
    lower_trigram_idx = 7
moving_line_idx = n3 % 6 - 1
if moving_line_idx == -1:
    moving_line_idx = 5

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"#### 上卦：{trigram_names[upper_trigram_idx]}")
    st.markdown(f"# {trigrams[upper_trigram_idx]}")
with col2:
    st.markdown(f"#### 下卦：{trigram_names[lower_trigram_idx]}")
    st.markdown(f"# {trigrams[lower_trigram_idx]}")
with col3:
    st.markdown(f"#### 动爻：{moving_lines[moving_line_idx]}")

st.markdown("""---""")

bin_hexagram_mappings = {}

hexagram_data = data["gua"]
for idx, gua in enumerate(data["gua"]):
    bin_hexagram_mappings[gua["gua-xiang"]] = idx

bin_num = trigrams_to_hexagram_binstr(upper_trigram_idx, lower_trigram_idx)
bin_hexagram = flip_bits(bin_num)
bin_hexagram2 = flip_bit(bin_hexagram, moving_line_idx)
hexagram_idx = bin_hexagram_mappings[bin_hexagram]
hexagram_idx2 = bin_hexagram_mappings[bin_hexagram2]

if reason:
    st.markdown(f"### 起卦事由：{reason}")

col1, col2 = st.columns(2)
with col1:
    st.markdown(
        f"### 得第{hexagram_idx + 1}卦：{hexagram_data[hexagram_idx]['gua-name']}卦"
    )
    st.markdown(f"# {hexagrams[hexagram_idx]}")
    st.markdown(f"##### 卦象：{hexagram_names[hexagram_idx]}")
    st.markdown(
        f"{hexagram_data[hexagram_idx]['gua-name']}。{hexagram_data[hexagram_idx]['gua-detail']}"
    )
    for line in hexagram_data[hexagram_idx]["yao-detail"]:
        st.markdown(line)
with col2:
    st.markdown(
        f"### 变第{hexagram_idx2 + 1}卦：{hexagram_data[hexagram_idx2]['gua-name']}卦"
    )
    st.markdown(f"# {hexagrams[hexagram_idx2]}")
    st.markdown(f"##### 卦象：{hexagram_names[hexagram_idx2]}")
    st.markdown(
        f"{hexagram_data[hexagram_idx2]['gua-name']}。{hexagram_data[hexagram_idx2]['gua-detail']}"
    )
    for line in hexagram_data[hexagram_idx2]["yao-detail"]:
        st.markdown(line)

st.markdown("""---""")

# 获取当前日期信息
now = datetime.now()
gregorian_date = now.strftime("%Y年%m月%d日")
try:
    solar = Solar.fromDate(now)
    lunar = solar.getLunar()
    # 使用天干地支表示年份
    lunar_year = lunar.getYearInGanZhi()  # 天干地支年份
    lunar_month = lunar.getMonthInChinese()  # 农历月份
    lunar_day = lunar.getDayInChinese()  # 农历日期
    lunar_date = f"{lunar_year}年{lunar_month}月{lunar_day}"
    date_info = f"起卦时间：公历 {gregorian_date}，农历 {lunar_date}"
except Exception as e:
    print(f"农历信息获取失败: {e}")
    date_info = f"起卦时间：公历 {gregorian_date}"

# 构建解卦提示词
prompt = f"""请帮我解读这个周易卦象：

{date_info}
起卦事由：{reason}

本卦：第{hexagram_idx + 1}卦 {hexagram_data[hexagram_idx]["gua-name"]}卦 {hexagrams[hexagram_idx]}
卦象：{hexagram_names[hexagram_idx]}
卦辞：{hexagram_data[hexagram_idx]["gua-name"]}。{hexagram_data[hexagram_idx]["gua-detail"]}

动爻：{moving_lines[moving_line_idx]}爻

变卦：第{hexagram_idx2 + 1}卦 {hexagram_data[hexagram_idx2]["gua-name"]}卦 {hexagrams[hexagram_idx2]}
卦象：{hexagram_names[hexagram_idx2]}
卦辞：{hexagram_data[hexagram_idx2]["gua-name"]}。{hexagram_data[hexagram_idx2]["gua-detail"]}

请结合起卦事由，解读本卦和变卦的含义，给出建议。"""

# URL 编码提示词
encoded_prompt = urllib.parse.quote(prompt)

# AI 网站选项（Claude 和通义千问支持 q 参数）
ai_options = {
    "DeepSeek": "https://chat.deepseek.com/",
    "ChatGPT": "https://chatgpt.com/",
    "Claude": f"https://claude.ai/new?q={encoded_prompt}",
    "Grok": "https://x.com/i/grok",
    "Kimi": "https://kimi.moonshot.cn/",
    "通义千问": f"https://tongyi.aliyun.com/qianwen/?q={encoded_prompt}",
}

st.subheader("AI 解卦")

# 推荐的 AI (支持自动填入提示词并提交)
st.write("**推荐使用(点击即可自动解卦):**")
st.link_button(
    "✨ 通义千问 (推荐)",
    ai_options["通义千问"],
    type="primary",
    use_container_width=True,
)

st.write("其他 AI 工具(需手动复制下方提示词):")

# 使用 st.code 显示提示词，右上角自带复制按钮
st.code(prompt, language=None)

# 其他 AI 选项，Claude 放第一个
other_ai_order = ["Claude", "DeepSeek", "ChatGPT", "Grok", "Kimi"]
other_ai_options = {k: ai_options[k] for k in other_ai_order if k in ai_options}
cols = st.columns(len(other_ai_options))
for idx, (ai_name, ai_url) in enumerate(other_ai_options.items()):
    with cols[idx]:
        st.link_button(ai_name, ai_url, use_container_width=True)
