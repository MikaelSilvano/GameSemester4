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

    def new_data():
        return {
            "password": "",
            "levels_unlocked": [True, False, False, False],
            "level_progress" : {
                1: [True, False, False, False],
                2: [False, False, False, False, False],
                3: [False, False, False, False, False, False, False, False],
                4: [False, False, False, False, False, False, False, False, False, False, False, False]
            }
        }

    if not hasattr(persistent, "saved_user") or persistent.saved_user is None:
        persistent.saved_user = {}
        renpy.save_persistent()
    
    if not hasattr(persistent, "current_user") or persistent.current_user is None:
        persistent.user_slot = 2
        persistent.current_user = None
        renpy.save_persistent()

    def complete_sublevel(level, sublevel):
        """
        Mark the given sublevel as complete and unlock the next sublevel (and next level, if needed).
        """
        #User
        curr_user = persistent.saved_user[persistent.current_user]
        #Level
        curr_level = curr_user[2][level]
        #Sublevel
        curr_sub = curr_level[sublevel] = True

        if sublevel < len(curr_level[level]):
            curr_sub = True
        else:
            if level < len(curr_user[1]):
                curr_user[1][level] = True

        renpy.save_persistent()

    def sublevel_unlocked(level, sublevel):
        """
        Returns True if the specified sublevel is unlocked.
        """
        curr_user = persistent.saved_user[persistent.current_user]

        curr_level = curr_user[2][level]

        curr_sub = curr_level[sublevel]

        return curr_sub

    def load_user_data(user):

        print(user)
        if user == "Guest" or user is None:
            persistent.levels_unlocked = [True, False, False, False]

            persistent.level_progress = {
                1: [True, False, False, False],
                2: [False, False, False, False, False],
                3: [False, False, False, False, False, False, False, False],
                4: [False, False, False, False, False, False, False, False, False, False, False, False]
            }
            return

        persistent.levels_unlocked = user['levels_unlocked']
        persistent.level_progress = user['level_progress']

        renpy.save_persistent()

    def reset_persistent(isGuest):

        cur_user = persistent.saved_user[persistent.current_user]

        cur_user["levels_unlocked"] = {new_data()["levels_unlocked"]}
        cur_user["levels_unlocked"] = {new_data()["level_progress"]}

        persistent.saved_user = cur_user

        renpy.save_persistent()
        renpy.notify("Game progress has been reset.")
        