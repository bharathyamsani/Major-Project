import streamlit as st

def Container(name,email_id,git):
    container=st.container(border=True)
    container.subheader(name)
    container.write(f"Email:<{email_id}>")
    container.markdown("GitHub:"+git)
    return container
    

def show():
    with st.container(border=True):
        st.header("Source Code")
        st.divider()
        st.write("This project was completed in fulfillment of the major project requirement at Gokaraju Rangaraju Institute of Engineering and Technology.")
        st.write("For source code, please visit the below link...")
        github_url = "https://github.com/bharathyamsani/Major-Project"
        st.markdown(f"[View source code on GitHub]({github_url})")
        st.header("Contact Us")
        st.divider()
        st.write("For any queries:")
        col1,col2,col3=st.columns(3)
        with col1:
            Container("Sai Bharath Yamsani","saibharathyamsani@gmail.com",github_url)
        with col2:
            col2=Container("Ram Praneeth Reddy","rampraneethreddypothula15@gmail.com",github_url)
        with col3:
            col3=Container("Sai Shashank Harish","saishashank1411@gmail.com",github_url)
