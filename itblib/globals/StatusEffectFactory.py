import itblib.gridelements.StatusEffects as status_effects

class StatusEffectFactory:
    """
    Useful if you want to spawn the right status effect based on name
    """

    @staticmethod 
    def _find_class(name:str, classes):
        """Return a class named 'name' in 'classes' or None if not found"""
        if name in classes.__dict__.keys():
            cls = classes.__dict__[name]
            return cls
        print(f"StatusEffectFactory: Class '{name}' not found.")
        return None

    @staticmethod
    def find_status_effect_class(name:str) -> "status_effects.StatusEffect|None":
        """Return a class named 'name' in 'itblib.gridelements.StatusEffects' or None if not found"""
        return StatusEffectFactory._find_class("StatusEffect" + name, status_effects)
