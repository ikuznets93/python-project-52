from django import forms

INPUT_CLASS = (
    'block w-full rounded-md border border-gray-300 bg-white px-3 py-2 '
    'text-sm text-gray-900 shadow-sm focus:border-blue-500 '
    'focus:outline-none focus:ring-1 focus:ring-blue-500'
)
TEXTAREA_CLASS = f'{INPUT_CLASS} min-h-32'
SELECT_CLASS = INPUT_CLASS
SELECT_MULTIPLE_CLASS = f'{INPUT_CLASS} h-32'
CHECKBOX_CLASS = 'h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500'


class StyledFormMixin:
    """Apply Tailwind classes to every widget of a form."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            widget = field.widget

            if isinstance(widget, forms.CheckboxInput):
                css_class = CHECKBOX_CLASS
            elif isinstance(widget, forms.SelectMultiple):
                css_class = SELECT_MULTIPLE_CLASS
            elif isinstance(widget, forms.Select):
                css_class = SELECT_CLASS
            elif isinstance(widget, forms.Textarea):
                css_class = TEXTAREA_CLASS
            else:
                css_class = INPUT_CLASS

            widget.attrs.setdefault('class', css_class)
