init python:
    from renpy.store import store
    import time

    class Objectives:
        def __init__(self, aims_dict):
            # Immutable copy of the original targets
            self._original_aims   = aims_dict.copy()

            # Runtime fields (set up by reset_obj)
            self.Aims             = {}    # working copy of aims
            self.total_collected  = {}    # how many of each icon_type collected
            self.CompletedAims    = {}    # which aims have been completed
            self.order            = []    # list of aim keys, in original order
            self.all_aims         = False # True once all aims are met

            # Initialize all runtime fields
            self.reset_obj()

        def AimsMet(self, icon_type, amount=1):
            """
            Call this when the player collects `amount` of icon_type.
            Awards points and removes completed aims.
            """
            # if store.Reset_Grid:
            #     print("reset grid:" + str(store.Reset_Grid))
            #     t = 0.01
            # else:
            #     t = 0
            # while t:
            #     mins, secs = divmod(t, 60)
            #     timer = '{:02d}:{:02d}'.format(mins, secs)
            #     print(timer, end="\r")
            #     time.sleep(1)
            #     t -= 1
            # print("reset grid:" + str(store.Reset_Grid))
            # print("valid grid (check build):", grid.valid_grid)
            if icon_type in self.Aims:
                self.total_collected[icon_type] = (
                    self.total_collected.get(icon_type, 0) + amount
                )

                if self.total_collected[icon_type] >= self.Aims[icon_type]:
                    # Mark that aim complete
                    self.CompletedAims[icon_type] = self.Aims[icon_type]
                    game.score += 200
                    del self.Aims[icon_type]

            # If all aims are done, fire the target‐complete check once.
            if not self.Aims and not self.all_aims:
                self.all_aims = True
                game.check_target_score(self.all_aims)

        def reset_obj(self):
            """
            Restore everything to the start of the sublevel:
            - Aims: fresh copy of original targets
            - total_collected & CompletedAims: empty
            - order: list of aim keys (for UI ordering)
            - all_aims flag: False
            """
            self.Aims            = self._original_aims.copy()
            self.total_collected = {}
            self.CompletedAims   = {}
            self.order           = list(self._original_aims.keys())
            self.all_aims        = False
        
        def reform_objectives(self, Objectives_base):

            self.Aims             = Objectives_base.Aims.copy()
            self.total_collected  = Objectives_base.total_collected.copy()
            self.CompletedAims    = Objectives_base.CompletedAims.copy()
            self._original_aims   = Objectives_base._original_aims.copy()
            self.order            = Objectives_base.order.copy()
            self.all_aims         = Objectives_base.all_aims