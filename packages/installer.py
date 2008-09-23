import sys, os

from seishub.core import SeisHubError

class PackageInstaller(object):
    """The PackageInstaller allows file system based registration of:
     * packages
     * resource types
     * schemas
     * stylesheets
     * aliases
      
    A package/resourcetype etc. is installed automatically when found the 
    first time, but not if an already existing package was updated to a new
    version. To find out about updated packages and resourcetypes use 
    the getUpdated() method.
    """
    
    @staticmethod
    def _install_package(env, p):
        if hasattr(p, 'version'):
            version = p.version
        else:
            version = ''
        env.registry.db_registerPackage(p.package_id, version)
        PackageInstaller._install_pre_registered(env, p)
    
    @staticmethod
    def _install_resourcetype(env, rt):
        if hasattr(rt, 'version'):
            version = rt.version
        else:
            version = ''
        if hasattr(rt, 'version_control'):
            version_control = rt.version_control
        else:
            version_control = False
        env.registry.db_registerResourceType(rt.package_id,
                                             rt.resourcetype_id,
                                             version,
                                             version_control)
        PackageInstaller._install_pre_registered(env, rt)
    
    @staticmethod
    def _install_pre_registered(env, o):
        package_id = o.package_id
        if hasattr(o, 'resourcetype_id'):
            resourcetype_id = o.resourcetype_id
        else:
            resourcetype_id = None
        if hasattr(o, '_registry_schemas'):
            for entry in o._registry_schemas:
                try:
                    data = file(entry['filename'], 'r').read()
                    type = entry['type']
                    env.registry.schemas.register(package_id, 
                                                  resourcetype_id, 
                                                  type, data)
                except Exception, e:
                    env.log.warn(("Registration of schema failed: " +\
                                 "%s (%s)") % (entry['filename'] ,e))
        
        if hasattr(o, '_registry_stylesheets'):
            for entry in o._registry_stylesheets:
                try:
                    data = file(entry['filename'], 'r').read()
                    type = entry['type']
                    env.registry.stylesheets.register(package_id, 
                                                      resourcetype_id, 
                                                      type, data)
                except Exception, e:
                    env.log.warn(("Registration of stylesheet failed: " +\
                                 "%s (%s)") % (entry['filename'], e))
                    
        if hasattr(o, '_registry_aliases'):
            for entry in o._registry_aliases:
                try:
                    env.registry.aliases.register(package_id, 
                                                  resourcetype_id,
                                                  **entry)
                except Exception, e:
                    env.log.warn(("Registration of alias failed: " +\
                                 "%s/%s/@%s (%s)") %\
                                (package_id, resourcetype_id, entry['name'], e))
                    
    @staticmethod
    def _pre_register(*args, **kwargs):
        """pre-register an object from filesystem"""
        reg = args[0]
        # get package id and resorcetype_id from calling class
        frame = sys._getframe(2)
        locals_ = frame.f_locals
        # Some sanity checks
        assert locals_ is not frame.f_globals and '__module__' in locals_, \
               'registerStylesheet() can only be used in a class definition'
        package_id = locals_.get('package_id', None)
        resourcetype_id = locals_.get('resourcetype_id', None)
        assert package_id, 'class must provide package_id'
        if reg in ['_stylesheets', '_schemas']:
            assert resourcetype_id, 'class must provide resourcetype_id'
        # relative path -> absolute path
        filename = kwargs.get('filename', None)
        if filename:
            kwargs['filename'] = os.path.join(os.path.dirname(
                                           frame.f_code.co_filename), filename)
        locals_.setdefault('_registry' + reg, []).append(kwargs)
        #import pdb;pdb.set_trace()
            
    @staticmethod
    def install(env, package_id = None):
        """auto install all known packages
        if package is given, only the specified package will be installed"""
        # XXX: problem: if installation fails here, packages still show up in the
        # registry but adding of resources etc. is not possible => possible solution
        # mark those packages as 'defect' and handle that seperately in the admin interface
        if package_id:
            packages = [package_id]
        else:
            packages = env.registry.getPackageIds()
        # install new packages
        for p in packages:
            fs_package = env.registry.getPackage(p)
            db_packages = env.registry.db_getPackages(p)
            if len(db_packages) == 0:
                try:
                    PackageInstaller._install_package(env, fs_package)
                except Exception, e:
                    env.log.warn(("Registration of package with id '%s' "+\
                                  "failed. (%s)") % (p, e))
                    continue
                
            # install new resourcetypes for package p
            for rt in env.registry.getResourceTypes(p):
                db_rt = env.registry.db_getResourceTypes(p, rt.resourcetype_id)
                if len(db_rt) == 0:
                    try:
                        PackageInstaller._install_resourcetype(env, rt)
                    except Exception, e:
                        env.log.warn(("Registration of resourcetype "+\
                                      "with id '%s' in package '%s'"+\
                                      " failed. (%s)") % \
                                      (rt.resourcetype_id, p, e))

    @staticmethod        
    def cleanup(env):
        """automatically remove unused packages"""
        db_rtypes = env.registry.db_getResourceTypes()
        #import pdb;pdb.set_trace()
        for rt in db_rtypes:
            if [rt.package.package_id, rt.resourcetype_id] not in \
               [[o.package_id, o.resourcetype_id] for o in env.registry.getResourceTypes(rt.package.package_id)]:
                try:
                    env.registry.db_deleteResourceType(rt.package.package_id, 
                                                       rt.resourcetype_id)
                except SeisHubError:
                    pass
        db_packages = env.registry.db_getPackages()
        fs_packages = env.registry.getPackageIds()
        for p in db_packages:
            if p.package_id not in fs_packages:
                try:
                    env.registry.db_deletePackage(p.package_id)
                except SeisHubError:
                    pass

    @staticmethod
    def getUpdatedPackages():
        pass

    @staticmethod
    def getUpdatedResourcetypes(package_id = None):
        pass 

registerSchema = lambda type, filename: PackageInstaller._pre_register\
                                                  ('_schemas', 
                                                   type = type,
                                                   filename = filename)
registerStylesheet = lambda type, filename: PackageInstaller._pre_register\
                                                  ('_stylesheets', 
                                                   type = type,
                                                   filename = filename)
registerAlias = lambda name, expr, limit = None, order_by = None: \
                        PackageInstaller._pre_register('_aliases',
                                                        name = name,
                                                        expr = expr,
                                                        limit = limit,
                                                        order_by = order_by)          
