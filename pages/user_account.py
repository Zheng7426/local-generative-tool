import streamlit as st
import os
import requests
import math
import pandas as pd

@st.cache_data
def get_response(url):
    response = requests.get(url, headers={
        "Authorization": f"Bearer {api_key}"
    })

    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    return response.json()

st.markdown("# 账户信息 🎈")
st.sidebar.markdown("# 账户信息")

# URLs
api_host = os.getenv('STABILITY_API_HOST', 'https://api.stability.ai')
account_url = f"{api_host}/v1/user/account"
balance_url = f"{api_host}/v1/user/balance"
engine_list_url = f"{api_host}/v1/engines/list"

api_key = os.getenv("STABILITY_API_KEY")
if api_key is None:
    raise Exception("Missing Stability API key.")

# send GET requests
with st.status("正在获取账户信息...", expanded=False) as status:

    account_response = get_response(account_url)
    balance_response = get_response(balance_url)

    # rendering
    st.markdown("### 账户及额度")
    st.write("Email: " + account_response['email'])
    st.write("Balance credits: " + str(balance_response['credits']) + "(" + str(math.floor(balance_response['credits'] * 5)) + " images)")
    status.update(label="已获取账户信息!", state="complete", expanded=True)

with st.status("正在获取可用引擎...", expanded=False) as status:
    engine_list_response = get_response(engine_list_url)
    st.markdown("### 可用引擎")
    df = pd.DataFrame(engine_list_response)
    st.write(df)
    status.update(label="已获取引擎信息!", state="complete", expanded=True)