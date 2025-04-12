init python:
    # Only set these if they don't exist or are None (possible leftover from old saves).
    if not hasattr(persistent, "levels_unlocked") or persistent.levels_unlocked is None:
        # For example, assume we have 4 levels total
        persistent.levels_unlocked = [True, False, False, False]

    if not hasattr(persistent, "level_progress") or persistent.level_progress is None:
        # E.g. level 1 has 4 sublevels, level 2 has 5, level 3 has 8, level 4 has 12.
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
        # Mark the current sublevel as complete
        persistent.level_progress[level][sublevel - 1] = True

        # If not last sublevel in this level, unlock the next sublevel
        if sublevel < len(persistent.level_progress[level]):
            persistent.level_progress[level][sublevel] = True
        else:
            # If this is the last sublevel of the level, unlock next level if any
            if level < len(persistent.levels_unlocked):
                persistent.levels_unlocked[level] = True

        renpy.save_persistent()

    def sublevel_unlocked(level, sublevel):
        """
        Returns True if the specified sublevel is unlocked.
        """
        return persistent.level_progress.get(level, [])[sublevel - 1]
