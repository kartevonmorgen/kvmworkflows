from liquid import render
from pydantic import BaseModel


def render_template(template_path: str, /, **kwargs) -> str:
    with open(template_path) as f:
        template = f.read()

    for k, v in kwargs.items():
        if isinstance(v, BaseModel):
            kwargs[k] = v.model_dump()

    return render(template, **kwargs)

