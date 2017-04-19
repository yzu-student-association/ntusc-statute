# generator/printing.py
from .task import render_custom_item
from renderer import HtmlRenderer

def generate(task):
    buf = open(task.output, 'w+')
    renderer = HtmlRenderer(buf=buf)
    renderer.render_head(title=task.title, meta=task.meta, base=task.base)

    # Read in
    for category in task.categories:
        category.load(base_path=task.source)

    # Process prepends
    for item in task.prepend:
        render_custom_item(renderer, item)

    # Build cover and TOC
    renderer.render_index_head()
    for category in task.categories:
        renderer.render_index_category(category)
    renderer.render_index_tail()

    # Render individual categories
    for category in task.categories:
        renderer.render_category(category)
        if category.is_intp:
            for entry in category.entries:
                renderer.render_interpretation(entry)
        else:
            for entry in category.entries:
                renderer.render_act(entry)

    # Process appends
    for item in task.prepend:
        render_custom_item(renderer, item)

    renderer.render_tail()
    buf.close()
