import streamlit as st
import pandas as pd
# from pandas_profiling import ProfileReport
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
import sys
import os

# Change page config to wide
st.set_page_config(
    page_title='Date Profiler',
    layout='wide'
)

# Define the maximum allowed file size (MB)
MAX_SIZE = 10

def get_filesize(file):
    """"
    Returns the file size in MB
    """
    size_bytes = sys.getsizeof(file)
    return size_bytes / (1024 * 1024)


def validate_file(file):
    """
    Verify the extension of the file and returns it if and only if
    this extension is either .csv or .xlsx otherwise it returns Fals
    """
    filename = file.name
    name, ext = os.path.splitext(filename)
    if  ext.lower() in ('.csv', '.xlsx'):
        return ext      # Return the extension
    else:
        return False    # Return False

# Create a sidebar
with st.sidebar:
    # Request the user to upload .csv and .xlsx files
    uploaded_file = st.file_uploader(
        label="Upload .csv or .xlsx file not exceding 10 MB"
    )
    if uploaded_file is not None:
        st.write("Modes more operations")
        minimal = st.checkbox(
            label="Use minimal report"
        )
        display_mode = st.radio(
            label="Display mode",
            options=('Primary', 'Dark', 'Orange')
        )
        dark_mode, orange_mode = display_mode == 'Dark', display_mode == 'Orange'

if uploaded_file is not None:
    ext = validate_file(uploaded_file)
    if ext:  # Either .csv or .xlsx
        if get_filesize(uploaded_file) <= MAX_SIZE:
            if ext == '.csv':
                # time being let's load csv
                df = pd.read_csv(uploaded_file)
            else:
                xl_file = pd.ExcelFile(uploaded_file)
                sheet_tuple = tuple(xl_file.sheet_names)
                sheet_name = st.sidebar.selectbox(
                    label="Select the sheet",
                    options=sheet_tuple
                )
                df = xl_file.parse(
                    sheet_name=sheet_name
                )

            # Generate a report (Take time so use spinner)
            with st.spinner("Generating report"):
                pr = ProfileReport(
                    df=df,
                    minimal=minimal,
                    dark_mode=dark_mode,
                    orange_mode=orange_mode
                )

            st_profile_report(pr)
        else:
            st.error(f"Maximum allowed size is {MAX_SIZE} MB")
    else:
        st.error(
            body="Kindly upload only .csv or .xlsx file"
        )
else:
    st.title("Data Profiler")
    st.info("Upload your data in the left sidebar to generate profiling")