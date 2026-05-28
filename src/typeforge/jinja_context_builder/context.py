from docxtpl import DocxTemplate
import jinja2

class Context:
    def __init__(self, dict_context: dict | list, labels: list):
        self._context = {}
        self._jinja_env = jinja2.Environment()

        dict_context_list = [dict_context] if isinstance(dict_context, dict) else dict_context
        labels_list = [labels] if isinstance(labels, str) else labels

        if len(dict_context_list) != len(labels_list):
            raise Exception("The length of dict_context and labels must be the same.")

        if not all(isinstance(item, dict) for item in dict_context_list):
            raise Exception("All items in dict_context must be dictionaries.")
        
        if not all(isinstance(item, str) for item in labels_list):
            raise Exception("All items in labels must be strings.")

        self._context = {name: content for name, content in zip(labels_list, dict_context_list)}
    
    def __repr__(self):
        return f"Context(dict_context={self._context})"

    def render_docx(self, template_path, output_path):
        # doc = DocxTemplate(template_path)
        # doc.render(self._context)
        # doc.save(output_path)