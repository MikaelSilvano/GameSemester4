init python:
    import renpy.atl as atl

    @atl.atl_warper
    def easeinout(t):
        # Hermite curve (same as "ease")
        return t ** 5.0
    
