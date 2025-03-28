from liquid import Template
from pydantic import BaseModel


def render_template(template_path: str, /, **kwargs) -> str:
    with open(template_path) as f:
        template = f.read()

    for k, v in kwargs.items():
        if isinstance(v, BaseModel):
            kwargs[k] = v.model_dump()    

    template_obj = Template(template)
    rendered = template_obj.render(**kwargs)
    
    return rendered
