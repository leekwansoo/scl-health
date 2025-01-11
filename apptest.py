import streamlit as st

# Markdown 텍스트를 문자열로 작성
markdown_text = """
# 예제 제목

이곳을 클릭하여 [Google](https://www.google.com) 홈페이지로 이동하세요.
"""

# Streamlit을 사용하여 Markdown 텍스트 출력
st.markdown(markdown_text)

# Markdown 텍스트를 문자열로 작성
markdown_text = """
# 목차
- [1. 소개](#소개)
- [2. 기능](#기능)
- [3. 결론](#결론)


# 소개
이 부분은 소개 섹션입니다.\np

## 기능
이 부분은 기능 섹션입니다.\np

### 결론
이 부분은 결론 섹션입니다.
"""

# Streamlit을 사용하여 Markdown 텍스트 출력
st.markdown(markdown_text)
