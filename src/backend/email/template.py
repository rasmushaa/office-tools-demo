import yaml
import streamlit as st
from backend.email.parameters import StringParameter, OptionParameter, DateParameter

class Template():
    def render(self):
        st.header(f"Template: {self.__name} (v{self.__version})")
        st.write(self.__description)
        for key, params in self.__parameters.items():
            st.divider()
            st.write(f'### Options for {key.capitalize()} - parameters')
            for param in params:
                param.render()

    def get_source_file(self):
        try:
            with open(self.path) as f:
                return f.read()
        except Exception as e:
            st.error(f"Error loading source file from {self.path}: {e}")
            return ""
    
    def get_filled_template(self):
        template = self.__template
        for _, params in self.__parameters.items():
            for param in params:
                template = param.fill_template(template)
        return template
    
    def load(self, path: str):
        try:
            self.path = path
            with open(self.path) as f:
                data = yaml.safe_load(f)
            self.__version = data.get('version', 'unknown')
            self.__name = data.get('name', 'unnamed')
            self.__description = data.get('description', '')
            self.__template = data.get('template', '')
            self.__parameters = {}
            self.__parameters['option'] = [OptionParameter(key=key, settings=values) for key, values in data.get('option_parameters', {}).items()]
            self.__parameters['string'] = [StringParameter(key=key, settings=values) for key, values in data.get('string_parameters', {}).items()]
            self.__parameters['date'] = [DateParameter(key=key, settings=values) for key, values in data.get('date_parameters', {}).items()]
        except Exception as e:
            st.error(f"Error loading template from {self.path}: {e}")

    def __str__(self):
        string = f"\nTemplateLoader()\nname: {self.__name}\nversion: {self.__version}\ndescription: {self.__description}\ntemplate: {self.__template}\n"
        string += f"String Parameters:\n"
        for param in self.__string_parameters:
            string += f"  - {param}\n"
        string += f"Option Parameters:\n"
        for param in self.__option_parameters:
            string += f"  - {param}\n"
        string += f"Date Parameters:\n"
        for param in self.__date_parameters:
            string += f"  - {param}\n"
        return string