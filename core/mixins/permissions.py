class PermissionMixin:
    def get_permissions(self):
        permission_classes = list(self.permission_classes)
        for actions, permission in self.permissions_mapping.items():
            if self.action in actions:
                permission_classes.append(permission)
        return [permission_class() for permission_class in permission_classes]