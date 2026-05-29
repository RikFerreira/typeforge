from docxtpl import DocxTemplate
import jinja2
import inspect
import warnings

from typeforge.jinja_context_builder import filters

class Context:
    def __init__(self, dict_context: dict | list, labels: str | list, dict_list_as_feature_list: bool = False):
        self._context = {}
        self._jinja_env = jinja2.Environment()
        self._empty_filters = {}

        # input_validation = {
        #     'dict_context is dict or list': isinstance(dict_context, (dict, list)),
        #     'labels is str or list': isinstance(labels, (str, list)),
        #     'dict_list but single feature'
        # }

        dict_context_list = [dict_context] if isinstance(dict_context, dict) else dict_context
        labels_list = [labels] if isinstance(labels, str) else labels

        if len(dict_context_list) != len(labels_list):
            raise Exception("The length of dict_context and labels must be the same.")

        # if not all(isinstance(item, dict) for item in dict_context_list):
        #     raise Exception("All items in dict_context must be dictionaries.")
        
        if not all(isinstance(item, str) for item in labels_list):
            raise Exception("All items in labels must be strings.")

        self._context = {name: content for name, content in zip(labels_list, dict_context_list)}

        for name, func in inspect.getmembers(filters, inspect.isfunction):
            self.add_filter(name, func)

        self._templates = {
            'docx': None
        }
    
    def __repr__(self):
        return f"Context(dict_context={self._context})"

    def add_filter(self, name: str, function: callable):
        if name in self._jinja_env.filters:
            raise Exception(f"A filter with the name << {name} >> already exists. Please choose a different name.")
        
        self._jinja_env.filters.update({name: function})

    def remove_filter(self, name):
        if name not in self._jinja_env.filters:
            warnings.warn(f"No filter with the name << {name} >> exists. No filter will be removed.")
            return None

        self._jinja_env.filters.pop(name, None)

    def render_docx(self, template_path, output_path):
        self._templates['docx'] = DocxTemplate(template_path)
        self._templates['docx'].render(self._context, self._jinja_env)
        self._templates['docx'].save(output_path)

