import streamlit as st
import pandas as pd
from pandas.api import types as ptypes
from frontend.excel.navigation import init_sidebar

st.set_page_config(
    page_title="Excel Analyser",
    layout="wide",
)

uploaded_file = init_sidebar()

df = pd.read_excel(uploaded_file)
st.session_state.backend.excel.filtter.detect_columns(df)

col1, _, col2 = st.columns([5, 1, 10])
with col1:
    st.session_state.backend.excel.filtter.render()


with col2:
    st.header('Filtered Data')

    filtered_df = st.session_state.backend.excel.filtter.apply(df)
    st.dataframe(filtered_df, hide_index=True)

    st.subheader('Statistics') 
    if filtered_df.empty:
        st.write("No rows after filtering")
    else:

        # Prepare separate stats containers per datatype
        numeric_stats = {'min': [], 'max': [], 'sum': [], 'mean': [], 'count': []}
        numeric_cols = []

        date_stats = {'min': [], 'max': [], 'count': []}
        date_cols = []

        object_stats = {'count': [], 'unique': [], 'top': [], 'freq': []}
        object_cols = []

        for col in filtered_df.columns:
            ser_raw = filtered_df[col]
            ser = ser_raw.dropna()
            cnt = int(ser.count())

            # Numeric columns
            if ptypes.is_numeric_dtype(ser_raw):
                numeric_cols.append(col)
                if cnt > 0:
                    numeric_stats['min'].append(ser.min())
                    numeric_stats['max'].append(ser.max())
                    numeric_stats['sum'].append(ser.sum())
                    numeric_stats['mean'].append(ser.mean())
                    numeric_stats['count'].append(cnt)
                else:
                    numeric_stats['min'].append(None)
                    numeric_stats['max'].append(None)
                    numeric_stats['sum'].append(None)
                    numeric_stats['mean'].append(None)
                    numeric_stats['count'].append(0)

            # Datetime columns
            elif ptypes.is_datetime64_any_dtype(ser_raw) or ptypes.is_object_dtype(ser_raw):
                # try to coerce to datetime to detect date-like columns
                ser_dt = pd.to_datetime(ser, errors='coerce').dropna()
                if not ser_dt.empty:
                    date_cols.append(col)
                    date_stats['min'].append(ser_dt.min().date())
                    date_stats['max'].append(ser_dt.max().date())
                    date_stats['count'].append(int(ser_dt.count()))
                    continue  # handled as date

                # otherwise fallthrough to object handling

                if ptypes.is_object_dtype(ser_raw) and (col not in date_cols):
                    object_cols.append(col)
                    object_stats['count'].append(cnt)
                    if cnt > 0:
                        uniques = ser.unique()
                        object_stats['unique'].append(len(uniques))
                        top = ser.mode()
                        if not top.empty:
                            top_val = top.iloc[0]
                            freq = int((ser == top_val).sum())
                        else:
                            top_val = None
                            freq = 0
                        object_stats['top'].append(top_val)
                        object_stats['freq'].append(freq)
                    else:
                        object_stats['unique'].append(0)
                        object_stats['top'].append(None)
                        object_stats['freq'].append(0)
            else:
                # Fallback: treat as object
                object_cols.append(col)
                object_stats['count'].append(cnt)
                if cnt > 0:
                    uniques = ser.unique()
                    object_stats['unique'].append(len(uniques))
                    top = ser.mode()
                    if not top.empty:
                        top_val = top.iloc[0]
                        freq = int((ser == top_val).sum())
                    else:
                        top_val = None
                        freq = 0
                    object_stats['top'].append(top_val)
                    object_stats['freq'].append(freq)
                else:
                    object_stats['unique'].append(0)
                    object_stats['top'].append(None)
                    object_stats['freq'].append(0)

        # Build DataFrames per datatype and display them
        if numeric_cols:
            numeric_df = pd.DataFrame(numeric_stats, index=numeric_cols)
            st.dataframe(numeric_df)
        else:
            st.write("No numeric columns found")

        if date_cols:
            date_df = pd.DataFrame(date_stats, index=date_cols)
            st.dataframe(date_df)
        else:
            st.write("No date columns found")

        if object_cols:
            object_df = pd.DataFrame(object_stats, index=object_cols)
            st.dataframe(object_df)
        else:
            st.write("No object/string columns found")
