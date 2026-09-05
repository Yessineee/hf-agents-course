import gradio_client.utils

_original_get_type = gradio_client.utils.get_type

def _patched_get_type(schema):
    if isinstance(schema, bool):
        return "bool"
    return _original_get_type(schema)

gradio_client.utils.get_type = _patched_get_type

_original_json_schema_to_python_type = gradio_client.utils._json_schema_to_python_type

def _patched_json_schema_to_python_type(schema, defs=None):
    if isinstance(schema, bool):
        return "Any"
    return _original_json_schema_to_python_type(schema, defs)

gradio_client.utils._json_schema_to_python_type = _patched_json_schema_to_python_type