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
        ## show listing or specific spoke
        ctx = {}
        ## sort by .name?
        ctx['forms'] = [dict(name=f.name, id=f.id) for f in PropertyForm.objects.filter(conf=instance)]
        # import pdb; pdb.set_trace()


        return handler.template("wheelcms_properties/configure_properties.html", **ctx)

    @action
    @json
    def formdata(self, handler, instance):
        request = handler.request

        id = request.REQUEST.get('id', None)
        if request.method == "POST":
            data = load_json(request.POST.get('data', '{}'))
            extra = load_json(request.POST.get('extra', '{}'))
            if id is None:
                pf = PropertyForm(conf=instance, name=extra.get('formname'), form=dump_json(data)).save()
                pf.save()
                id = pf.id
            else:
                pass

        if id is not None:
            return load_json(PropertyForm.objects.get(pk=id).form)
        return []

configuration_registry.register(PropertiesConfigurationHandler)

