from dasher.base import DasherComponent


class DashComponent(DasherComponent):
    @property
    def layout(self):
        if getattr(self.x, "id", None) is None:
            self.x.id = self.name
        else:
            raise ValueError("Component id must be empty.")
        return self.x
