from openai import OpenAI
import streamlit as st
import os

from product import product_list, model_list

api_key: str = os.getenv("API_KEY")
pass_word: str = os.getenv("PASSWORD")

st.set_page_config(page_title="Haoda Appliance Data")

with st.sidebar:
    password: str = st.text_input("Password", "", key="password", type="password")
    chat_list: list = [
        "Company Profile",
        "Electric Buffet Warmer",
        "Electric Deep Fryer",
        "Electric Hotplate",
        "Electric Infrared Ceramic Cooker",
        "Electric Chopper",
        "Electric Barbecue Grill",
        "Certification",
        "Stainless Steel"]
    chat_item: str = st.selectbox("Choose a chatbot", chat_list, None, key="chat_item", help="选择一个项目后可以和AI对话，话题基本仅限所选的项目。")

    clear_btn: bool = st.button("Clear", "clear", type="primary")

    if chat_item == "Certification":
        with open("chat/certificate.txt", "r", encoding="utf-8") as f:
            certificate: str = f.read()
        st.markdown(certificate, unsafe_allow_html=True)
    elif chat_item == "Company Profile":
        with open("chat/company.txt", "r", encoding="utf-8") as f:
            company: str = f.read()
        with st.container(height=400, border=True):
            st.markdown(company, unsafe_allow_html=True)

if "p_state" not in st.session_state:
    st.session_state.p_state = False
if "m_state" not in st.session_state:
    st.session_state.m_state = False

if "chat" not in st.session_state:
    st.session_state.chat = True

if password == pass_word:
    st.session_state.chat = False
else:
    st.session_state.chat = True

if "msg" not in st.session_state:
    st.session_state.msg = []

p_list: list = product_list()
p_item: str = st.selectbox("Choose a product", p_list, None, key="p_item")

if p_item:
    st.session_state.p_state = True
    m_list: list = model_list(p_item)
    m_item: str = st.selectbox("Choose a model", m_list, None, key="m_item")
    if m_item:
        st.session_state.m_state = True
    else:
        st.session_state.m_state = False
else:
    st.session_state.p_state = False
    st.session_state.m_state = False

if st.session_state.m_state:
    with st.expander("Check the image and advantages"):
        image_file: str = f"img/{p_item}/{m_item}.png"
        st.image(image_file, width=300, output_format="PNG")

        advantage_file: str = f"data/{p_item}/{m_item}/advantage.txt"
        with open(advantage_file, "r", encoding="utf-8") as f:
            advantage: str = f.read()
        st.markdown(advantage)
    
    spec_options: list = ["Basic Specification", "Package"]
    spec_item: str = st.selectbox("Choose a specification", spec_options, 0, key="spec_item")
    
    if spec_item == "Basic Specification":
        specification_file: str = f"data/{p_item}/{m_item}/specification.txt"
        with open(specification_file, "r", encoding="utf-8") as f:
            specification: str = f.read()
        st.markdown(specification, unsafe_allow_html=True)
    elif spec_item == "Package":
        package_file: str = f"data/{p_item}/{m_item}/package.txt"
        with open(package_file, "r", encoding="utf-8") as f:
            package: str = f.read()
        st.markdown(package, unsafe_allow_html=True)

if chat_item == "Stainless Steel":
    with open("chat/stainless steel.txt", "r", encoding="utf-8") as f:
        stainless_steel: str = f.read()
    with st.container(height=450, border=True):
        st.markdown(stainless_steel, unsafe_allow_html=True)
    st.markdown("<font color='red'>不锈钢部分暂未支持AI对话，进行其他操作或查看其他内容时，请先取消选择 Stainless Steel 项目。</font>", unsafe_allow_html=True)

if not st.session_state.p_state:
    for i in st.session_state.msg:
        with st.chat_message(i["role"]):
            st.markdown(i["content"])
    
    if query := st.chat_input("Ask a question...", key="query", disabled=st.session_state.chat):
        st.session_state.msg.append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.markdown(query)
        
        info_file: str = f"chat/{chat_item}.txt"
        with open(info_file, "r", encoding="utf-8") as f:
            info_data: str = f.read()
        if chat_item == "Company Profile":
            system_prompt: str = f"""你是一名专业的企业顾问，请根据下面的公司信息回答用户的问题。

公司信息如下：

{info_data}

---

约束：
- 确保你的回复严格参照上述资料
- 不要理睬与公司情况无关的问题
"""
        elif chat_item == "Electric Buffet Warmer" or chat_item == "Electric Deep Fryer" or chat_item == "Electric Hotplate" or chat_item == "Electric Infrared Ceramic Cooker" or chat_item == "Electric Chopper" or chat_item == "Electric Barbecue Grill":
            system_prompt: str = f"""你是一名专业的产品顾问，请根据下面的产品信息回答用户的问题。

产品信息如下：

{info_data}

---

约束：
- 确保你的回复严格参照上述资料
- 不要理睬与产品情况无关的问题
"""
        elif chat_item == "Certification":
            system_prompt: str = f"""你是一名专业的认证顾问，请根据下面的认证信息回答用户的问题。

认证信息如下：

{info_data}

---

约束：
- 确保你的回复严格参照上述资料
- 不要理睬与认证情况无关的问题
"""
        messages: list = [{"role": "system", "content": system_prompt}] + st.session_state.msg

        with st.chat_message("assistant"):
            client = OpenAI(api_key=api_key, base_url="http://api.siliconflow.cn")
            response = client.chat.completions.create(
                model="Qwen/Qwen2.5-7B-Instruct",
                messages=messages,
                max_tokens=4096,
                temperature=0.50,
                top_p=0.70,
                stream=True)
            result: str = st.write_stream(chunk.choices[0].delta.content for chunk in response if chunk.choices[0].delta.content is not None)
        
        st.session_state.msg.append({"role": "assistant", "content": result})
        st.rerun()

if clear_btn:
    st.session_state.msg = []
    st.rerun()
