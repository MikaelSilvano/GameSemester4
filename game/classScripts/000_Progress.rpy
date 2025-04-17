init python:
    if not hasattr(persistent, "levels_unlocked") or persistent.levels_unlocked is None:
        persistent.levels_unlocked = [True, False, False, False]

    if not hasattr(persistent, "level_progress") or persistent.level_progress is None:
        persistent.level_progress = {
            1: [True, False, False, False],
            2: [False, False, False, False, False],
            3: [False, False, False, False, False, False, False, False],
            4: [False, False, False, False, False, False, False, False, False, False, False, False]
        }
        renpy.save_persistent()

    def complete_sublevel(level, sublevel):
        """
        Mark the given sublevel as complete and unlock the next sublevel (and next level, if needed).
        """
        persistent.level_progress[level][sublevel - 1] = True

        if sublevel < len(persistent.level_progress[level]):
            persistent.level_progress[level][sublevel] = True
        else:
            if level < len(persistent.levels_unlocked):
                persistent.levels_unlocked[level] = True

        renpy.save_persistent()

    def sublevel_unlocked(level, sublevel):
        """
        Returns True if the specified sublevel is unlocked.
        """
        return persistent.level_progress.get(level, [])[sublevel - 1]

    def reset_persistent():
        persistent.levels_unlocked = [True, False, False, False]

        persistent.level_progress = {
            1: [True, False, False, False],
            2: [False, False, False, False, False],
            3: [False, False, False, False, False, False, False, False],
            4: [False, False, False, False, False, False, False, False, False, False, False, False]
        }

        renpy.save_persistent()
        renpy.notify("Game progress has been reset.")