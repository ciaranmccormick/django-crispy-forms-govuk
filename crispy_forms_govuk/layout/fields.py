"""
Fields
======

.. _django-crispy-forms: https://github.com/maraujop/django-crispy-forms
.. _DS: https://design-system.service.gov.uk/

References
    * `Checkboxes <https://design-system.service.gov.uk/components/checkboxes/>`_;

"""  # noqa: E501

import enum

from crispy_forms import layout as crispy_forms_layout
from crispy_forms.bootstrap import Accordion, AccordionGroup
from crispy_forms.utils import TEMPLATE_PACK
from crispy_forms_govuk.layout.buttons import render_template

__all__ = [
    "CheckboxField",
    "CheckboxMultipleField",
    "RadioAccordion",
    "RadioAccordionGroup",
    "LegendSize",
]


class LegendSize(enum.Enum):
    xl = "xl"
    l = "l"  # noqa: E741
    m = "m"
    s = "s"


class LegendMixin(object):
    @property
    def heading_size(self) -> int:
        return 1


class Field(crispy_forms_layout.Field):
    def render(
        self,
        form,
        form_style,
        context,
        template_pack=TEMPLATE_PACK,
        extra_context=None,
        **kwargs,
    ):
        # Treat all attribute values as template strings
        self.attrs = {k: render_template(context, v) for k, v in self.attrs.items()}
        return super().render(form, form_style, context, template_pack, extra_context)


class HiddenField(Field):
    """
        Layout object, that marks the field's input widgets as type="hidden".

        This is useful when you want to hide an existing field, e.g. generated by a
        ModelForm, while keep its other attributes intact i.e. name, value, etc. If you
        want to create a hidden input from scratch, use
        `crispy_forms.layout.Hidden`.

        Example::

            HiddenField('field_name')
        """

    def render(
        self,
        form,
        form_style,
        context,
        template_pack=TEMPLATE_PACK,
        extra_context=None,
        **kwargs,
    ):
        self.attrs.update({"type": "hidden"})
        return super().render(form, form_style, context, template_pack, extra_context)


# TODO - this is wrong a checkbox field should render a single checkbox
class CheckboxField(Field):
    template = "%s/field.html"

    def __init__(
        self,
        field: str,
        legend: str = None,
        legend_size: LegendSize = LegendSize.m,
        hyperlink_label=False,
        inline=False,
        dont_use_label_as_legend=False,
        *args,
        **kwargs,
    ):
        self.legend = legend
        self.inline = inline
        self.legend_size = legend_size
        self.dont_use_label_as_legend = dont_use_label_as_legend
        self.hyperlink_label = hyperlink_label
        super().__init__(field, *args, **kwargs)

    def heading_lookup(self, legend_size: LegendSize) -> int:
        lookup = {LegendSize.xl: 1, LegendSize.l: 2, LegendSize.m: 3, LegendSize.s: 4}
        return lookup[legend_size]

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK, **kwargs):
        context["legend_classes"] = f"govuk-fieldset__legend--{self.legend_size.value}"
        context["legend"] = self.legend
        context["hyperlink_label"] = self.hyperlink_label
        context["inline"] = self.inline
        context["dont_use_label_as_legend"] = self.dont_use_label_as_legend

        return super().render(form, form_style, context, template_pack, **kwargs)


# NOTE - use this rather than CheckboxField for forms.BooleanField
class CheckboxSingleField(Field):
    def __init__(
        self, field: str, small_boxes: bool = False, *args, **kwargs,
    ):
        # TODO - test small-boxes functionality
        self.small_boxes = small_boxes
        super().__init__(field, *args, **kwargs)

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK, **kwargs):
        context["small_boxes"] = self.small_boxes

        return super().render(form, form_style, context, template_pack, **kwargs)


class CheckboxMultipleField(Field):
    template = "%s/field.html"

    def __init__(
        self,
        field: str,
        legend: str = None,
        legend_size: LegendSize = LegendSize.m,
        hint: str = None,
        *args,
        **kwargs,
    ):
        self.legend = legend
        self.legend_size = legend_size
        self.hint = hint
        super().__init__(field, *args, **kwargs)

    def heading_lookup(self, legend_size: LegendSize) -> int:
        lookup = {LegendSize.xl: 1, LegendSize.l: 2, LegendSize.m: 3, LegendSize.s: 4}
        return lookup[legend_size]

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK, **kwargs):
        context["legend_classes"] = f"govuk-fieldset__legend--{self.legend_size.value}"
        context["legend_heading"] = self.heading_lookup(self.legend_size)
        context["legend"] = self.legend
        context["hint"] = self.hint

        return super().render(form, form_style, context, template_pack, **kwargs)


class RadioAccordion(Accordion):
    template = "%s/radio_accordion.html"

    def __init__(
        self,
        *fields,
        legend: str = None,
        use_legend_as_heading: bool = False,
        legend_size: LegendSize = LegendSize.m,
        hint: str = None,
        errors=None,
        **kwargs,
    ):
        self.legend = legend
        self.use_legend_as_heading = use_legend_as_heading
        self.hint = hint
        self.errors = errors
        self.legend_size = legend_size
        super().__init__(*fields, **kwargs)

    def heading_lookup(self, legend_size: LegendSize) -> int:
        lookup = {LegendSize.xl: 1, LegendSize.l: 2, LegendSize.m: 3, LegendSize.s: 4}
        return lookup[legend_size]

    def open_target_group_for_form(self, form):
        """All targets are closed by defaults.

        Opens first target with errors.
        """
        target = self.first_container_with_errors(form.errors.keys())
        if target:
            target.active = True
        return target

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK, **kwargs):
        context[
            "legend_classes"
        ] = f"govuk-fieldset__legend--{self.legend_size.value}"  # noqa: E501
        context["legend_heading"] = self.heading_lookup(self.legend_size)
        context["legend_text"] = self.legend
        context["use_legend_as_heading"] = self.use_legend_as_heading
        context["hint"] = self.hint

        # Add errors to the template, not sure what this should contain yet
        context["errors"] = self.errors

        return super().render(form, form_style, context, template_pack, **kwargs)


class RadioAccordionGroup(AccordionGroup):
    template = "%s/radio_accordion_group.html"
    suppress_form_group_error = True
    has_errors = False

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK, **kwargs):

        # check fields for errors
        for field in self.fields:
            if field in form.errors.keys() or len(form.errors) > 0:
                self.has_errors = True
                context["has_errors"] = self.has_errors
                break

        # Suppress error styling on inner form group
        context["suppress_form_group_error"] = self.suppress_form_group_error

        return super().render(form, form_style, context, template_pack, **kwargs)
