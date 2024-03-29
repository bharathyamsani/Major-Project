import streamlit as st
import time
import os
from PIL import Image

def show():
    with st.container(border=True):
        st.title("Audio Cloning Detection")
        st.divider()
        st.header("Introduction")
        paragraph="<p style='text-align:justify;text-indent:30px'>In today's data-driven world, a prevailing challenge confronting us all is the ability to determine the authenticity of data. This problem extends to audios as well. Current voice cloning systems have become so intelligent that they can learn speech characteristics from a few samples and generate perceptually unrecognizable speech. Voice cloning systems not only have advantages but also many disadvantages. It is difficult to classify what is real and what is fake. Cloned audio has been employed for malicious uses. 'Audio Cloning Detection' Using Deep Learning is a system that can detect cloned voices quickly and accurately. It uses deep learning algorithm to detect the authenticity of the audio.</p>"
        st.write(paragraph,unsafe_allow_html=True)
        _,col,_=st.columns([2,1,2])
        if st.button("Let's Go"):
            st.session_state["selected_page"] = "Model"
            st.rerun()
        st.caption("Click on above button to use the model")
        st.header("Results")
        paragraph="""<p style="text-align:justify;text-indent:30px">The model used here is trained on the audio dataset called "for_norm" from the collection "FakeOrReal" curated by York University. It achieved outstanding results on various metrics. It showed strong generalization with an accuracy of 96.87% in training data, 99.95 % in testing data, and 99.3% in validation data and it proves its efficiency to distinguish real audio samples from fake ones.</p>"""
        st.write(paragraph,unsafe_allow_html=True)
        script_directory = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(script_directory, "../Images/confusion_matrix.png")
        image=Image.open(image_path)
        _,col,_=st.columns([1,3,1])
        with col:
            st.image(image,caption="Confusion Matrix")
        paragraph="""<p style="text-align:justify;text-indent:30px">The figure above, depicting classification performance against the testing set, further emphasizes the capabilities of this model. Using the Nadam optimizer with a batch size of 49 during training, the confusion matrix provides a detailed representation of how the model behaves when faced with different circumstances, distinguishing between genuine and fake sounds. Thus, its excellent performance was evident across all classes.</p>"""
        st.write(paragraph,unsafe_allow_html=True)
        
            