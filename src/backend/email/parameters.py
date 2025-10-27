import pandas as pd
import re
import calendar
import streamlit as st



class BaseParameter():
    def __init__(self, key: str):
        self.__key = key
        self.__value = None

    def __str__(self):
        return f"BaseParameter(key={self.__key}, value={self.__value})"

    def render(self):
        raise st.write("BaseParameter render method called. This should be overridden in subclasses.")
    
    def fill_template(self, template: str):
        clean_key = self.key.strip()
        pattern = r'{{\s*' + re.escape(clean_key) + r'\s*}}'
        return re.sub(pattern, str(self.value), template)
    
    @property
    def value(self):
        return f'{self.__value}'

    @property
    def key(self):
        return f'{self.__key}'


class StringParameter(BaseParameter):
    def __init__(self, key: str, settings: dict):
        super().__init__(key)
        self.__default = settings.get('default', '') if settings else ''
        self.__value = self.__default

    def render(self):
        self.__value = st.text_input(
            f'Enter value for "{self.key}":',
            value=self.__default
        )

    @property
    def value(self):
        return self.__value

    def __str__(self):
        return f"StringParameter(key={self.key}, default={self.__default}).value={self.value}"


class OptionParameter(BaseParameter):
    def __init__(self, key: str, settings: dict):
        super().__init__(key)
        self.__options = settings.get('options', [])
        self.__leading_line = settings.get('leading_line')
        self.__if_not_selected_remove_trailing = settings.get('if_not_selected_remove_trailing', [])
        self.__if_multiple_selected_add_between = settings.get('if_multiple_selected_add_between', [])
        self.__selection_mode = 'multi' if self.__if_multiple_selected_add_between else 'single'
        self.__value = None

    def render(self):
        self.__value = st.pills(
            f'Select option for "{self.key}":',
            options=self.__options,
            selection_mode=self.__selection_mode
        )

    @property
    def value(self):
        if not self.__value:
            return None
        elif self.__selection_mode == 'single':
            return self.__leading_line + self.__value if self.__leading_line else self.__value
        else:
            result = self.__leading_line if self.__leading_line else ''
            for i, value in enumerate(self.__value):
                result += value
                if i < len(self.__value) - 1:
                    result += self.__if_multiple_selected_add_between[0]
            return result

    
    def fill_template(self, template: str):
        if self.value:
            result = super().fill_template(template)
            return result

        elif self.__if_not_selected_remove_trailing:
            clean_key = self.key.strip()
            item = self.__if_not_selected_remove_trailing[0]
            pattern = r'{{\s*' + re.escape(clean_key) + r'\s*}}' + re.escape(item)
            result = re.sub(pattern, '', template, flags=re.MULTILINE)
            return result
        
        else:
            return template

    def __str__(self):
        return f"OptionParameter(key={self.key}, options={self.__options}, selection_mode={self.__selection_mode}).value={self.value}"


class DateParameter(BaseParameter):
    def __init__(self, key: str, settings: dict):
        super().__init__(key)
        self.__format = settings.get('format', 'YYYY-MM-DD')
        self.__delay = settings.get('delay', 0)
        self.__value = pd.Timestamp('today') + pd.Timedelta(days=self.__delay)

    def render(self):
        self.__value = st.date_input(
            f'Select date for "{self.key}":',
            value=self.__value,
            format='YYYY-MM-DD'
        )

    @property
    def value(self):
        def get_ordinal_suffix(value):
            if 10 <= value % 100 <= 20:
                return 'th'
            else:
                return {1: 'st', 2: 'nd', 3: 'rd'}.get(value % 10, 'th')
        result = self.__format
        result = result.replace('<yyyy>', str(self.__value.year))
        result = result.replace('<yy>', str(self.__value.year)[2:])
        result = result.replace('<mmo>', f"{self.__value.month:02d}{get_ordinal_suffix(self.__value.month)}")
        result = result.replace('<mm>', f"{self.__value.month:02d}")
        result = result.replace('<MM>', calendar.month_name[self.__value.month])
        result = result.replace('<DD>', calendar.day_name[self.__value.weekday()])
        result = result.replace('<ddo>', f"{self.__value.day:02d}{get_ordinal_suffix(self.__value.day)}")
        result = result.replace('<dd>', f"{self.__value.day:02d}")
        result = result.replace('<delay>', f"{self.__delay:d}")
        return result

    def __str__(self):
        return f"DateParameter(key={self.key}, delay={self.__delay}, format={self.__format}).value={self.value}"