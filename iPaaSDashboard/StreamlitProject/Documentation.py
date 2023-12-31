import streamlit as st
import Utils as utils
from streamlit.components.v1 import html
from streamlit_js_eval import streamlit_js_eval

st.set_page_config(layout="wide",
                   page_title="Hello",
                   page_icon="👋",
                   )

if "svg_height" not in st.session_state:
    st.session_state["svg_height"] = 200

if "previous_mermaid" not in st.session_state:
    st.session_state["previous_mermaid"] = ""

if 'checked' not in st.session_state:
    st.session_state.checked = False


def button_click(Key, Value):
    utils.update_flow(Key, Value)
    st.cache_data.clear()
    st.rerun()
    streamlit_js_eval(js_expressions="parent.window.location.reload()")



def mermaid(code: str) -> None:
    return html(
        f"""
        <pre class="mermaid">
            {code}
        </pre>

        <script type="module">
            import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
            mermaid.initialize({{ startOnLoad: true }});
        </script>
        """,
        height=st.session_state["svg_height"] + 50,
    )


option = st.selectbox(
    'Please select a process to review',
    (utils.getFlows()))

container = st.container(border=True)

with st.spinner("Please wait while the Process data being fetched!"):
    container.markdown(""" 
        # Process Flow: """ + option + """
        
    """)

    for item in utils.get_item("ProcessName", option):
        for key in item.keys():
            if key not in ["EOF", "TimeStamp", "ProcessName", "OperationalCategory", "ServiceName"]:
                container.markdown("""**""" + key + """**""")
                container.markdown("""""" + item[key] + """""")

            elif key == "ServiceName":
                container.markdown("""**""" + key + """**""")
                container.markdown("""
                ```f
                """ + item[key] + """
                """)
        container.markdown("""------------------------------------------------------------""")

    if_clicked = container.button("Update Flow", type="primary", help="help")
    checked = container.checkbox("Confirm Deleting")
    if if_clicked and checked:
        button_click("ProcessName",option)

st.subheader("Process Flow Chart")
st.markdown(mermaid(utils.generateMermaid_string(option)))
