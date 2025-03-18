"""
step1:导入streamlit,导入generate_script函数
"""

import streamlit as st
from utils import generate_script

st.title("Video Script Generator")

#通过.sidebar创建侧边栏，输入api秘钥
with st.sidebar:
    openai_api_key=st.text_input("请输入OpenAI API秘钥：",type="password")
    # st.markdown("[获取OpenAI API密钥](https://platform.openai.com/account/api-keys)")

#基本信息填写
subject = st.text_input("请输入视频主题")
video_length = st.number_input("请输入视频大致时长（单位：分钟）",min_value=0.1,step=0.1)
creativity = st.slider("请输入视频的脚本创造力（数字小说明更严谨，数字大说明更多样）",min_value=0.0,max_value=1.0,value=0.2,step=0.1)
submit = st.button("生成脚本")

#校验API秘钥，校验用户输入的主题、时长、创造力等相关信息
#.info()输出提示信息,.stop()结束，
if submit and not openai_api_key:
    st.info("请输入你的OpenAI API秘钥")
if submit and not subject:
    st.info("请输入视频的主题")
    st.stop()
if submit and not video_length>=0.1:
    st.info("视频长度需要大于或等于0.1")
    st.stop()

#调用generate_script，请求AI回复内容
#.spiner()加载状态
if submit:
    with st.spinner("AI正在思考中，请稍等..."):
        search_result,title,script = generate_script(subject,video_length,creativity,openai_api_key)

#返回结果
    st.success("视频脚本已生成")
    st.subheader("标题：")
    st.write(title)
    st.subheader("视频脚本：")
    st.write(script)
    with st.expander("维基百科搜索结果"):
        st.info(search_result)