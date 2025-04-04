init python:
    class Objectives:
        def __init__(self, Aims):
            self.Aims = Aims.copy()
            self.total_collected = {}
            self.CompletedAims = {}
            self.order = list(Aims.keys())  # 🔥 Track order like ['rocks', 'woods', 'glass']

        def AimsMet(self, icon_type, amount=1):
            if icon_type in self.Aims:
                self.total_collected[icon_type] = self.total_collected.get(icon_type, 0) + amount

                if self.total_collected[icon_type] >= self.Aims[icon_type]:
                    self.CompletedAims[icon_type] = self.Aims[icon_type]
                    game.score += 200
                    del self.Aims[icon_type]

            if not self.Aims:
                game.check_target_score()
