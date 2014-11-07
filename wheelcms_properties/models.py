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
        return [dict(name=f.name, id=f.id, spokes=["a", "b", "c"])
                for f in PropertyForm.objects.filter(conf=instance)]

    @action
    @json
    def formdata(self, handler, instance):
        request = handler.request

        id = int(request.REQUEST.get('id', -1))
        if request.method == "POST":
            formdata = load_json(request.POST.get('data', '{}'))
            extra = load_json(request.POST.get('extra', '{}'))
            formname = extra.get('name', 'new form')

            if id == -1:
                pf = PropertyForm(conf=instance, name=formname,
                                  form=dump_json(formdata)).save()
                pf.save()
                id = pf.id
            else:
                pf = PropertyForm.objects.get(pk=id)
                pf.name = formname
                pf.form = dump_json(formdata)
                pf.save()

        if id != -1:
            pf = PropertyForm.objects.get(pk=id)
            return dict(form=load_json(pf.form),
                        extra=dict(name=pf.name, id=pf.id))
        return []

configuration_registry.register(PropertiesConfigurationHandler)

