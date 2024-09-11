# from ansible.plugins.inventory import BaseInventoryPlugin, Constructable, Cacheable
from ansible.errors import AnsibleParserError
from ansible.inventory.helpers import get_group_vars
from ansible.module_utils.common.text.converters import to_native
from ansible.plugins.inventory.ini import InventoryModule as BaseInventoryModule
from ansible.utils.vars import combine_vars
from ansible.vars.fact_cache import FactCache


class InventoryModule(BaseInventoryModule):
    NAME = "ini_jinja_hvault"

    def verify_file(self, path):
        """return true/false if this is possibly a valid file for this plugin to consume"""
        valid = False
        if super(InventoryModule, self).verify_file(path):
            if path.endswith((".hvault.ini")):
                valid = True
        return valid

    def get_all_host_vars(self, host, loader, sources):
        """requires host object"""
        return combine_vars(
            self.host_groupvars(host, loader, sources),
            self.host_vars(host, loader, sources),
        )

    def host_groupvars(self, host, loader, sources):
        """requires host object"""
        gvars = get_group_vars(host.get_groups())

        return gvars

    def host_vars(self, host, loader, sources):
        """requires host object"""
        hvars = host.get_vars()

        return hvars

    def parse(self, inventory, loader, path, cache):
        super(InventoryModule, self).parse(inventory, loader, path, cache)

        sources = []

        fact_cache = FactCache()
        try:
            # Go over hosts (less var copies)
            for host in inventory.hosts:
                for _ in range(2):
                    # get available variables to templar
                    hostvars = self.get_all_host_vars(inventory.hosts[host], loader, sources)
                    if host in fact_cache:  # adds facts if cache is active
                        hostvars = combine_vars(hostvars, fact_cache[host])

                    # create composite vars
                    self._set_composite_vars(hostvars, hostvars, host)

        except Exception as e:
            raise AnsibleParserError("failed to parse %s: %s " % (to_native(path), to_native(e)), orig_exc=e)

    def _compose(self, template, variables):
        """helper method for plugins to compose variables for Ansible based on jinja2 expression and inventory vars"""
        t = self.templar

        try:
            use_extra = self.get_option("use_extra_vars")
        except Exception:
            use_extra = False

        if use_extra:
            t.available_variables = combine_vars(variables, self._vars)
        else:
            t.available_variables = variables

        return t.template(
            "%s%s%s" % (t.environment.variable_start_string, template, t.environment.variable_end_string), disable_lookups=False
        )

    def _set_composite_vars(self, compose, variables, host):
        """loops over compose entries to create vars for hosts"""
        if compose and isinstance(compose, dict):
            for varname in compose:
                try:
                    composite = self._compose(compose[varname], variables)
                except Exception:
                    continue
                self.inventory.set_variable(host, varname, composite)
