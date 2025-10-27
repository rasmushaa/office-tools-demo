import yaml
from pathlib import Path
from typing import Dict, Any


TEMPLATE_PATH = Path('src/assets/templates')


class ValidityLevel:
    VALID = "validity"
    INVALID = "invalid"
    WARNING = "warning"


class FileSystem:
    def __init__(self):
        self.validity_levels = ValidityLevel()

    def is_valid_template_yaml_object(self, data) -> dict:
        """ Check if the given opened yaml object is a valid template.

        Parameters
        ----------
        data : str
            Already opened yaml object

        Returns
        -------
        bool
            True if the file is a valid template file, False otherwise.
        """ 
        def check_parameter_options(template: dict, key: str, mandatory_values: list, optional_values: list):
            if key in template.keys():
                for parameter, options in data[key].items():
                    # Mandatory options
                    keys = [] if not options else options.keys()
                    for manadory_key in mandatory_values:
                        if manadory_key not in keys:
                            return {"validity": self.validity_levels.INVALID, "error": f"{key}: {parameter} is missing {manadory_key}"}
                    # Optional options
                    for option in options:
                        if option not in optional_values:
                            return {"validity": self.validity_levels.WARNING, "error": f"{key}: {parameter} has unsupported option {option}"}
            return False
        
        if not isinstance(data, dict):
            return {"validity": self.validity_levels.INVALID, "error": "Invalid YAML structure."}

        # Mandatory keys
        for key in ("name", "version", "description"):
            if key not in data:
                return {"validity": self.validity_levels.INVALID, "error": f"Missing mandatory key: {key}."}
            
        # Check for unsupported Parameters
        supported_keys = {"name", "version", "description", "template", "string_parameters", "option_parameters", "date_parameters"}
        for key in data.keys():
            if key not in supported_keys:
                return {"validity": self.validity_levels.WARNING, "error": f"Unsupported key found: {key}."}
                        
        val = check_parameter_options(
            data, 
            key='date_parameters', 
            mandatory_values=['delay', 'format'], 
            optional_values=['delay', 'format']
            )
        if val:
            return val
        
        val = check_parameter_options(
            data, 
            key='string_parameters', 
            mandatory_values=['default'], 
            optional_values=['default']
            )
        if val:
            return val
        
        val = check_parameter_options(
            data, 
            key='option_parameters', 
            mandatory_values=['options'], 
            optional_values=['options', 'if_not_selected_remove_trailing', 'if_multiple_selected_add_between', 'leading_line']
            ) 
        if val:
            return val 
        
        return {"validity": self.validity_levels.VALID}
    

    def is_valid_template_file(self, file_path: str) -> dict:
        """ Check if the given file path is a valid YAML template file.

        A valid template file must exist and contain 'name', 'version', and 'description' keys.

        Parameters
        ----------
        file_path : str
            The path to the template file.

        Returns
        -------
        bool
            True if the file is a valid template file, False otherwise.
        """ 
        path = Path(file_path)
        if not path.exists() or not path.is_file():
            return {"validity": self.validity_levels.INVALID, "error": "File does not exist."}

        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
        except Exception:
            return {"validity": self.validity_levels.INVALID, "error": "Failed to parse YAML."}
        
        return self.is_valid_template_yaml_object(data)



    def scan_templates(self) -> Dict[str, Dict[str, Any]]:
        """ Scan src/assets/templates for .yml/.yaml files and collect entries.

        Returns
        -------
        Dict[str, Dict[str, Any]]
            A dictionary where keys are template file stems and values are dictionaries
        """
        templates: Dict[str, Dict[str, Any]] = {}

        for pattern in ("*.yml", "*.yaml"):
            for f in TEMPLATE_PATH.glob(pattern):
                check = self.is_valid_template_file(str(f))
                if check["validity"] != self.validity_levels.INVALID:
                    data = yaml.safe_load(f.read_text(encoding="utf-8"))
                    templates[f.stem] = {
                        "name": data.get("name"),
                        "version": data.get("version"),
                        "description": data.get("description"),
                        "path": str(f),
                        "validity": check["validity"],
                        "error": check.get("error")
                    }
                else:
                    templates[f.stem] = {
                        "validity": check["validity"],
                        "error": check.get("error")
                    }

        templates_sort = dict(sorted(templates.items(), 
                       key=lambda x: (x[1].get('name', ''), 
                            x[1].get('version', ''))))

        return templates_sort