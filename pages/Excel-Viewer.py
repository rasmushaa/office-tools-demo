import streamlit as st
import pandas as pd

st.markdown("# Excel Viewer")

uploaded_file = st.file_uploader("Upload an Excel file", type=['xls', 'xlsx'])

filters = {}

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    
    st.markdown("### Auto detected filters")
    col1, col2 = st.columns([1, 1])

    columns = df.columns.tolist()
    dtypes = df.dtypes.astype(str).tolist()

    for col, dtype in zip(columns, dtypes):

        if 'int' in dtype or 'float' in dtype:
            min_val = float(df[col].min())
            max_val = float(df[col].max())
            selected_range = col1.slider(f"Filter {col} ({dtype})", min_value=min_val, max_value=max_val, value=(min_val, max_val))
            filters[col] = selected_range

        elif 'object' in dtype:
            unique_values = df[col].dropna().unique().tolist()
            selected_values = col2.multiselect(f"Filter {col} ({dtype})", options=unique_values, default=unique_values)
            filters[col] = selected_values

    # Apply filters
    filtered_df = df.copy()
    for col, condition in filters.items():
        if isinstance(condition, tuple) and len(condition) == 2:
            filtered_df = filtered_df[(filtered_df[col] >= condition[0]) & (filtered_df[col] <= condition[1])]
        elif isinstance(condition, list):
            filtered_df = filtered_df[filtered_df[col].isin(condition)]

    st.markdown(f"### Filtered Data ({len(filtered_df)} rows)")
    st.dataframe(filtered_df)