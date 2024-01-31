import streamlit as st
import json

trigrams = ['☰', '☱', '☲', '☳', '☴', '☵', '☶', '☷']
trigram_names = ['乾', '兑', '离', '震', '巽', '坎', '艮', '坤']
hexagrams = [
    '䷀', '䷁', '䷂', '䷃', '䷄', '䷅', '䷆', '䷇', '䷈', '䷉', '䷊', '䷋', '䷌', '䷍', '䷎',
    '䷏', '䷐', '䷑', '䷒', '䷓', '䷔', '䷕', '䷖', '䷗', '䷘', '䷙', '䷚', '䷛', '䷜', '䷝',
    '䷞', '䷟', '䷠', '䷡', '䷢', '䷣', '䷤', '䷥', '䷦', '䷧', '䷨', '䷩', '䷪', '䷫', '䷬',
    '䷭', '䷮', '䷯', '䷰', '䷱', '䷲', '䷳', '䷴', '䷵', '䷶', '䷷', '䷸', '䷹', '䷺', '䷻',
    '䷼', '䷽', '䷾', '䷿'
]
hexagram_names = [
    "乾", "坤", "屯", "蒙", "需", "讼", "师", "比", "小畜", "履", "泰", "否", "同人", "大有",
    "谦", "豫", "随", "蛊", "临", "观", "噬嗑", "贲", "剥", "复", "无妄", "大畜", "颐", "大过",
    "坎", "离", "咸", "恒", "遁", "大壮", "晋", "明夷", "家人", "睽", "蹇", "解", "损", "益",
    "夬", "姤", "萃", "升", "困", "井", "革", "鼎", "震", "艮", "渐", "归妹", "丰", "旅", "巽",
    "兑", "涣", "节", "中孚", "小过", "既济", "未济"
]
# hexagram_name = [
#     "乾", "坤", "屯", "蒙", "需", "訟", "師", "比", "小畜", "履", "泰", "否", "同人", "大有",
#     "謙", "豫", "隨", "蠱", "臨", "觀", "噬嗑", "贲", "剝", "複", "無妄", "大畜", "頤", "大過",
#     "坎", "離", "鹹", "恒", "遁", "大壯", "晉", "明夷", "家人", "睽", "蹇", "解", "損", "益",
#     "夬", "姤", "萃", "升", "困", "井", "革", "鼎", "震", "艮", "漸", "歸妹", "豐", "旅", "巽",
#     "兌", "渙", "節", "中孚", "小過", "既濟", "未濟"
# ]
moving_lines = ['初', '二', '三', '四', '五', '上']


def get_binstr(num, nbits=3):
    return bin(num)[2:].zfill(nbits)


def trigrams_to_hexagram_binstr(upper_idx, lower_idx):
    return get_binstr(lower_idx) + get_binstr(upper_idx)


def flip_bits(bits):
    return ''.join('1' if bit == '0' else '0' for bit in bits)


def flip_bit(bits, n):
    return bits[:n] + ('1' if bits[n] == '0' else '0') + bits[n + 1:]


def normalize(n):
    if n == 0:
        return 10
    else:
        return n


st.set_page_config(page_title='简易算卦', page_icon="☯")
st.title("简易算卦")

with open('gua.json', 'r') as f:
    data = json.load(f)

st.write("集中精力想象需要算卦的事由，任意输入三个数，点击算卦，即可得到卦象和卦辞。")

submitted = False
with st.form(key='divination'):
    reason = st.text_input("简述起卦的事由（可留空）", value="")
    col1, col2, col3 = st.columns(3)
    with col1:
        n1 = st.number_input("第一个数", min_value=0, format="%i")
        n1 = normalize(n1)
    with col2:
        n2 = st.number_input("第二个数", min_value=0, format="%i")
        n2 = normalize(n2)
    with col3:
        n3 = st.number_input("第三个数", min_value=0, format="%i")
        n3 = normalize(n3)

    submitted = st.form_submit_button("算卦")

if not submitted:
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

hexagram_data = data['gua']
for idx, gua in enumerate(data['gua']):
    bin_hexagram_mappings[gua['gua-xiang']] = idx

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
        f"### 得第{hexagram_idx+1}卦：{hexagram_data[hexagram_idx]['gua-name']}卦")
    st.markdown(f"# {hexagrams[hexagram_idx]}")
    st.markdown(f"##### 卦象：{hexagram_names[hexagram_idx]}")
    st.markdown(
        f"{hexagram_data[hexagram_idx]['gua-name']}。{hexagram_data[hexagram_idx]['gua-detail']}"
    )
    for line in hexagram_data[hexagram_idx]['yao-detail']:
        st.markdown(line)
with col2:
    st.markdown(
        f"### 变第{hexagram_idx2+1}卦：{hexagram_data[hexagram_idx2]['gua-name']}卦"
    )
    st.markdown(f"# {hexagrams[hexagram_idx2]}")
    st.markdown(f"##### 卦象：{hexagram_names[hexagram_idx2]}")
    st.markdown(
        f"{hexagram_data[hexagram_idx2]['gua-name']}。{hexagram_data[hexagram_idx2]['gua-detail']}"
    )
    for line in hexagram_data[hexagram_idx2]['yao-detail']:
        st.markdown(line)

st.link_button(f"查看详解（变卦详见{moving_lines[moving_line_idx]}爻）",
               f"https://m.k366.com/gua/{hexagram_idx+1}.htm")
