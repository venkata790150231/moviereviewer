import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode
from streamlit_modal import Modal
import streamlit.components.v1 as components

from db import load, delete_post

# Create the pandas DataFrame with column name is provided explicitly
posts = load()
data = []
for post in posts:
    data.append([post.id, post.post, post.huff_title, post.nypost_title, post.daily_caller])
df = pd.DataFrame(data, columns=['ID', 'Post', 'Huff Title', 'NY Post Title', 'Daily Caller Title'])


def aggrid_interactive_table(df: pd.DataFrame):
    """Creates an st-aggrid interactive table based on a dataframe.

    Args:
        df (pd.DataFrame]): Source dataframe

    Returns:
        dict: The selected row
    """
    options = GridOptionsBuilder.from_dataframe(df)

    options.configure_side_bar()

    options.configure_selection("single")
    selection = AgGrid(
        df,
        enable_quicksearch=True,
        gridOptions=options.build(),
        theme="alpine",
        update_mode=GridUpdateMode.MODEL_CHANGED,
        allow_unsafe_jscode=True,
    )

    return selection


selection = aggrid_interactive_table(df=df)

if selection:
    st.write("You selected:")
    st.json(selection["selected_rows"])
delete = st.button("Delete")

if delete:
    with st.form("key1"):
        # ask for input
        identifier = selection["selected_rows"][0]["ID"]
        button_check = st.form_submit_button("Are you sure to delete: " + str(identifier) + "?")
        if button_check:
            delete_post(identifier)
