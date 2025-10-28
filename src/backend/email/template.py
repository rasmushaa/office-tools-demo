import yaml
import streamlit as st
from backend.email.parameters import StringParameter, OptionParameter, DateParameter



class Template():
    def __init__(self):
        self.__path = None
        self.__name = None
        self.__version = None
        self.__description = None


    @property
    def name(self):
        return self.__name
    
    @property
    def version(self):
        return self.__version
    
    @property
    def description(self):
        return self.__description 
    
    @property
    def path(self):
        return self.__path
    
    def update_defaults(self):
        for key, params in self.__parameters.items():
            for param in params:
                param.update_default()

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
            # If template comes from repo files, use those
            if self.__path:
                with open(self.path) as f:
                    return f.read()
            # Otherwise, template was uploaded to runtime and it has TextIOWrapper as stored data
            else:
                return self.__data
        except Exception as e:
            st.error(f'Error: Was not able to return Template() source file due to {e}')
            return None
    
    def get_filled_template(self):
        template = self.__template
        for _, params in self.__parameters.items():
            for param in params:
                template = param.fill_template(template)
        return template
    
    def load_file(self, path: str):
        try:
            self.__path = path
            with open(self.__path) as f:
                self.load_yaml_bytes(f)
        except Exception as e:
            st.error(f"Error loading template from {self.__path}: {e}")

    def load_yaml_bytes(self, bytes):
        try:
            self.__data = bytes
            data = yaml.safe_load(bytes)
            self.__version = data.get('version', 'unknown')
            self.__name = data.get('name', 'unnamed')
            self.__description = data.get('description', '')
            self.__template = data.get('template', '')
            self.__parameters = {}
            self.__parameters['option'] = [OptionParameter(key=key, settings=values) for key, values in data.get('option_parameters', {}).items()]
            self.__parameters['string'] = [StringParameter(key=key, settings=values) for key, values in data.get('string_parameters', {}).items()]
            self.__parameters['date'] = [DateParameter(key=key, settings=values) for key, values in data.get('date_parameters', {}).items()]
        except Exception as e:
            st.error(f"Error loading template from YAML {data.name}: {e}")

    def __str__(self):
        string = f"\nTemplateLoader()\nname: {self.__name}\nversion: {self.__version}\ndescription: {self.__description}\ntemplate: {self.__template}\n"
        string += f"String Parameters:\n"
        for key, params in self.__parameters.items():
            string += f"{key.capitalize()} - parameters\n"
            for param in params:
                string += f"  - {param}\n"
        return string