import re

from ansible.plugins.action import ActionBase


class ActionModule(ActionBase):
    prefix = 'peertube'

    private_var_names = [
        'archive_file',
        'config_dir',
        'config_file',
        'current_link',
        'dir',
        'group',
        'npm',
        'service',
        'storage_dir',
        'systemd_after',
        'user',
        'version_dir',
        'versions_dir',
    ]

    path_re = re.compile(r'^({{ [_a-zA-Z][_a-zA-Z0-9]* }})?/[-_./a-z0-9]*$')

    common_name_re = re.compile(r'^[a-z_][a-z0-9_-]{0,30}(\$|[a-z0-9_-])?$')

    systemd_after_re = re.compile(r'^[-_.a-zA-Z0-9]+( [-_.a-zA-Z0-9]+)*$')

    def run(self, tmp=None, task_vars=None):
        if task_vars is None:
            task_vars = dict()

        result = super(ActionModule, self).run(tmp, task_vars)
        result['changed'] = False
        result['failed'] = False

        for var_name in self.private_var_names:
            full_var_name = '%s__%s' % (self.prefix, var_name)
            validator = getattr(self, 'validate_' + var_name)
            value = task_vars[full_var_name]
            msg_part = validator(value)

            if msg_part is not None:
                value = str(value)

                if len(value) <= 120:
                    partial_value = value
                else:
                    partial_value = '%s...' % value[0:30]

                full_msg = "Invalid var '%s' with value '%s': %s" % (
                    full_var_name,
                    partial_value,
                    msg_part,
                )

                result['failed'] = True
                result['msg'] = full_msg
                return result

        return result

    def validate_archive_file(self, value):
        if not isinstance(value, str):
            return 'is not str'
        if not self.path_re.fullmatch(value):
            return 'does not match format %s' % self.path_re

    def validate_config_dir(self, value):
        if not isinstance(value, str):
            return 'is not str'
        if not self.path_re.fullmatch(value):
            return 'does not match format %s' % self.path_re

    def validate_config_file(self, value):
        if not isinstance(value, str):
            return 'is not str'
        if not self.path_re.fullmatch(value):
            return 'does not match format %s' % self.path_re

    def validate_current_link(self, value):
        if not isinstance(value, str):
            return 'is not str'
        if not self.path_re.fullmatch(value):
            return 'does not match format %s' % self.path_re

    def validate_dir(self, value):
        if not isinstance(value, str):
            return 'is not str'
        if not self.path_re.fullmatch(value):
            return 'does not match format %s' % self.path_re

    def validate_group(self, value):
        if not isinstance(value, str):
            return 'is not str'
        if not self.common_name_re.fullmatch(value):
            return 'does not match format %s' % self.common_name_re

    def validate_npm(self, value):
        if not isinstance(value, str):
            return 'is not str'
        if not self.path_re.fullmatch(value):
            return 'does not match format %s' % self.path_re

    def validate_service(self, value):
        if not isinstance(value, str):
            return 'is not str'
        if not self.common_name_re.fullmatch(value):
            return 'does not match format %s' % self.common_name_re

    def validate_storage_dir(self, value):
        if not isinstance(value, str):
            return 'is not str'
        if not self.path_re.fullmatch(value):
            return 'does not match format %s' % self.path_re

    def validate_systemd_after(self, value):
        if not isinstance(value, str):
            return 'is not str'
        if not self.path_re.fullmatch(value):
            return 'does not match format %s' % self.path_re

    def validate_user(self, value):
        if not isinstance(value, str):
            return 'is not str'
        if not self.common_name_re.fullmatch(value):
            return 'does not match format %s' % self.common_name_re

    def validate_version_dir(self, value):
        if not isinstance(value, str):
            return 'is not str'
        if not self.path_re.fullmatch(value):
            return 'does not match format %s' % self.path_re

    def validate_versions_dir(self, value):
        if not isinstance(value, str):
            return 'is not str'
        if not self.path_re.fullmatch(value):
            return 'does not match format %s' % self.path_re
