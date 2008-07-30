# -*- coding: utf-8 -*-

from seishub.core import Component, implements
from seishub.packages.interfaces import IPackage, IResourceType


class SeisHubPackage(Component):
    """The SeisHub package.""" 
    implements(IPackage)
    
    package_id = 'seishub'
    version = '0.1'

class StylesheetResource(Component):
    """A stylesheet resource type for SeisHub."""
    implements(IResourceType)
    
    package_id = 'seishub'
    resourcetype_id = 'stylesheet'


class SchemaResource(Component):
    """A schema resource type for SeisHub."""
    implements(IResourceType)
    
    package_id = 'seishub'
    resourcetype_id = 'schema'