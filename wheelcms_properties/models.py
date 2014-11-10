from operator import itemgetter

from django.db import models
from two.ol.base import json

from json import loads as load_json, dumps as dump_json

from wheelcms_axle.models import Configuration as BaseConfiguration
from wheelcms_axle.configuration import BaseConfigurationHandler

from wheelcms_axle.registries.configuration import configuration_registry

from wheelcms_axle.content import type_registry
from wheelcms_axle.actions import action

class Properties(models.Model):
    main = models.ForeignKey(BaseConfiguration, related_name="spoke_properties")

class PropertyForm(models.Model):
    conf = models.ForeignKey(Properties, related_name="forms")
    name = models.CharField(max_length=60, blank=False)
    form = models.TextField(default="[]", blank=False)

    types = models.TextField(default="")

"""
    List all known spokes
    Provide option to define additional properties on each of them

"""

class PropertiesConfigurationHandler(BaseConfigurationHandler):
    id = "spoke_properties"
    label = "Content Properties"
    model = Properties
    form = None

    def view(self, handler, instance):
        ## it's a SPA!
        return handler.template("wheelcms_properties/configure_properties.html")

    @action
    @json
    def formlist(self, handler, instance):
        ## sort?
        spokes=[dict(key=k, value=v.title) for (k, v) in type_registry.items()]

        spokes.sort(key=itemgetter('value'))
        return dict(spokes=spokes,
                    forms=[dict(name=f.name, id=f.id, spokes=f.types.split(","))
                           for f in PropertyForm.objects.filter(conf=instance)])

    @action
    @json
    def formdata(self, handler, instance):
        request = handler.request

        id = int(request.REQUEST.get('id', -1))
        if request.method == "POST":
            formdata = load_json(request.POST.get('data', '{}'))
            extra = load_json(request.POST.get('extra', '{}'))
            formname = extra.get('name', 'new form')
            spokes = ",".join(extra.get('spokes', []))

            if id == -1:
                pf = PropertyForm(conf=instance, name=formname,
                                  form=dump_json(formdata),
                                  types=spokes)
                pf.save()
                id = pf.id
            else:
                pf = PropertyForm.objects.get(pk=id)
                pf.name = formname
                pf.form = dump_json(formdata)
                pf.types = spokes
                pf.save()

        if id != -1:
            pf = PropertyForm.objects.get(pk=id)
            return dict(form=load_json(pf.form),
                        extra=dict(name=pf.name, id=pf.id,
                                   spokes=pf.types.split(",")))
        return dict(form=[], extra={'name':'', 'spokes':[]})

from wheelcms_axle.spoke import tab

from wheelcms_axle import permissions as p
from wheelcms_axle.actions import action_registry

def has_form(spoke):
    """ TODO: check if any forms have been assigned XXX """
    return True

@action(p.edit_content)
@json
def properties_data_handler(handler, request, action):
    """ return relevant form data """
    ## return first form that matches. TODO: combine forms into groups

    ## combine with data

    # import pdb; pdb.set_trace()
    
    spokename = handler.spoke().name()
    forms = []
    for pf in PropertyForm.objects.all():
        types = pf.types.split(",")
        if spokename in types:
            forms.append(dict(name=pf.name, form=load_json(pf.form)))

    return dict(forms=forms)


@tab(p.edit_content, label="Object properties", condition=has_form)
def properties_handler(handler, request, action):
    """ only show tab if actions registered on spoke ? """
    return handler.template("wheelcms_properties/object_properties_tab.html")

action_registry.register(properties_handler, 'properties')
action_registry.register(properties_data_handler, 'properties_data')

configuration_registry.register(PropertiesConfigurationHandler)

