from ..views.translations import tr

class Condition:
    def __init__(self, name, bad=False,id=-67):
        self._name = name
        self.bad = bad
        self.id=id
    def get_name(self, lang):
        return tr(f"condition.{self._name}",0,lang)
    
CONDITIONS = [
    Condition("PracticePoor", True, 0)
]
