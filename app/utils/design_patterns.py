"""
Design patterns utils module
"""


def singleton(class_):
    """
    singleton design pattern
    """
    instances = {}

    def get_instance(*args, **kwargs):
        """
        get instance
        """
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return get_instance
