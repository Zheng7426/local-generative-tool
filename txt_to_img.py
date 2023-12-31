import streamlit as st
import os
import requests
import base64

st.markdown("# Image Generation 🎈")
st.sidebar.markdown("# Text-to-Image")

engine_id = "stable-diffusion-v1-6"
api_host = os.getenv('STABILITY_API_HOST', 'https://api.stability.ai')
api_key = os.getenv("STABILITY_API_KEY")
if api_key is None:
    raise Exception("Missing Stability API key.")
st.markdown("#### Prompt")
text_input = st.text_area(
    "在下列文本框中输入 prompt 👇"
)
st.write(f'你写了 {len(text_input)} 个字符。')
col1, col2 = st.columns(2)
with col1:
    st.markdown("#### Height")
    height = st.number_input('height',
      label_visibility='collapsed',
      value=512,
      min_value=128)

    st.markdown("#### cfg_scale [0-35]")
    cfg_scale = st.number_input('cfg_scale', 
        label_visibility='collapsed',
        value=7,
        min_value=0,
        max_value=35,
        step=1,
        placeholder='输入介于0-35之间的数值...')
    st.write('How strictly the diffusion process adheres to the prompt text (higher values keep your image closer to your prompt)')

with col2:
    st.markdown("#### Width")
    width = st.number_input('width',
      label_visibility='collapsed',
      value=512,
      min_value=128)

    st.markdown("#### Steps [10-50]")
    steps = st.number_input('steps',
        label_visibility='collapsed',
        value=30,
        min_value=10,
        max_value=50,
        step=1,
        placeholder='输入介于10-50之间的数值...')
    st.write('Number of diffusion steps to run.')


col3, col4 = st.columns(2)
with col3:
    st.markdown("#### Style Preset 预置画风")
    style_preset = st.selectbox("Style Preset",
    ("3d-model", "analog-film", "anime", "cinematic", "comic-book", "digital-art"
    ,"enhance", "fantasy-art", "isometric", "line-art", "low-poly", "modeling-compound"
    ,"neon-punk", "origami", "photographic", "pixel-art", "tile-texture"),
    index=None,
    label_visibility='collapsed',
    placeholder="选择一种画风...")
with col4:
    st.markdown("#### Samples [1-10]")
    samples = st.number_input('samples',
        label_visibility='collapsed',
        value=1,
        min_value=1,
        max_value=10,
        step=1,)
    st.write('Number of images to generate.')
if st.button("生成图像"):
    with st.spinner("正在生成中...", cache=False):
        response = requests.post(f"{api_host}/v1/generation/{engine_id}/text-to-image",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}"
        },
        json={
            "text_prompts": [
                {
                    "text": text_input
                }
            ],
            "cfg_scale": cfg_scale,
            "height": height,
            "width": width,
            "samples": samples,
            "steps": steps,
            "style_preset": style_preset,
        },
        )

        if response.status_code != 200:
            st.write("Non-200 response: " + str(response.text))
            raise Exception("Non-200 response: " + str(response.text))
        
        data = response.json()
        for i, image in enumerate(data["artifacts"]):
            with open(f"./out/v1_txt2img_{i}.png", "wb") as f:
                f.write(base64.b64decode(image["base64"]))
            st.success('已生成！')
            st.image(f"./out/v1_txt2img_{i}.png")