import streamlit as st
import pandas as pd


class DateFiltter():
    def __init__(self, settings: dict):
        self.__min = settings.get('min')
        self.__max = settings.get('max')
        self.__col = settings.get('col')
        self.__values = [None, None]

    def render(self):
        self.__values = st.slider(f"Filter ({self.__col})", min_value=self.__min , max_value=self.__max, value=(self.__min, self.__max))

    def apply(self, df):
        filtered_df = df[
                (pd.to_datetime(df[self.__col]).dt.date >= self.__values[0]) & 
                (pd.to_datetime(df[self.__col]).dt.date <= self.__values[1])
            ]
        return filtered_df
    

class NumericFiltter():
    def __init__(self, settings: dict):
        self.__min = settings.get('min')
        self.__max = settings.get('max')
        self.__col = settings.get('col')
        self.__values = (None, None)

    def render(self):
        self.__values = st.slider(f"Filter ({self.__col})", min_value=self.__min , max_value=self.__max, value=(self.__min, self.__max))

    def apply(self, df):
        filtered_df = df[
                (df[self.__col] >= self.__values[0]) & 
                (df[self.__col] <= self.__values[1])
            ]
        return filtered_df
    

class ObjectFiltter():
    def __init__(self, settings: dict):
        self.__col = settings.get('col')
        self.__defaults = settings.get('values')
        self.__values = [None]

    def render(self):
        self.__values = st.multiselect(f"Filter ({self.__col})", options=self.__defaults, default=self.__defaults)

    def apply(self, df):
        filtered_df = df[df[self.__col].isin(self.__values)]
        return filtered_df


class ExcelFiltter():
    def __init__(self):
        self.__filtters = {}

    def detect_columns(self, df: pd.DataFrame):
        columns = df.columns.tolist()
        dtypes = df.dtypes.astype(str).tolist()

        date_filters = []
        numeric_filters = []
        object_filters = []

        for col, dtype in zip(columns, dtypes):

            if 'datetime' in dtype:
                min = pd.to_datetime(df[col].min()).date()
                max= pd.to_datetime(df[col].max()).date()
                settings = {'col': col, 'min': min, 'max': max}
                date_filters.append(DateFiltter(settings))

            elif 'int' in dtype or 'float' in dtype:
                min = float(df[col].min())
                max = float(df[col].max())
                settings = {'col': col, 'min': min, 'max': max}
                numeric_filters.append(NumericFiltter(settings))

            elif 'object' in dtype:
                values = df[col].dropna().unique().tolist()
                settings = {'col': col, 'values': values} 
                object_filters.append(ObjectFiltter(settings))

        self.__filtters = {'datetime': date_filters, 'numeric': numeric_filters, 'object': object_filters}

    
    def render(self):
        st.header('Auto detected filtter')
        for dtype_key, filtters in self.__filtters.items():
            st.divider()
            st.write(f'### {dtype_key.capitalize()} - filtters')
            for filtter in filtters:
                filtter.render()
                    

    def apply(self, df):
        temp = df.copy()
        for dtype_key, filtters in self.__filtters.items():
            for filtter in filtters:
                temp = filtter.apply(temp)
        return temp