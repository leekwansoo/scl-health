import streamlit as st

# Example keyword and hyperlink
keyword = "Streamlit"
url = "https://streamlit.io/"

# Text with hyperlink in Markdown format
text = f"Check out [this amazing tool]({url}) for building web apps with Python, called {keyword}!"

# Display the text with hyperlink using st.write()
st.write(text)

# Create an anchor point
st.write('<a id="section1"></a>', unsafe_allow_html=True)

# Some content
st.write("This is Section 1")

st.write("This is Section 2")

st.write("This is Section 3")

# Create the hyperlink to the anchor
st.write("[Go to Section 1](#section1)")
st.write("[Go to Section 2](#section2)")
st.write("[Go to Section 3](#section3)")
