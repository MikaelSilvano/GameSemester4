init python:
    import time
    def format_user_dict(d):
        # repr(d) gives the "{…}" string; doubling braces escapes them
        return repr(d).replace("{", "{{").replace("}", "}}")
    
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

    if not hasattr(persistent, "lvl_score") or persistent.lvl_score is None:
        persistent.lvl_score = {
            1: [0, 0, 0, 0],
            2: [0, 0, 0, 0, 0],
            3: [0, 0, 0, 0, 0, 0, 0, 0],
            4: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        }

    if not hasattr(persistent, "leaderboard") or persistent.leaderboard is None:
        persistent.leaderboard = []

    if not hasattr(persistent, "saved_user") or persistent.saved_user is None:
        persistent.saved_user = {}
        renpy.save_persistent()
    
    if not hasattr(persistent, "start_time_session") or persistent.start_time_session is None:
        persistent.start_time_session = {}

    if not hasattr(persistent, "current_user") or persistent.current_user is None:
        persistent.current_user = None
        renpy.save_persistent()

    def update_leaderboard():
        persistent.leaderboard = [
            (username, user_data["tot_score"])
            for username, user_data in persistent.saved_user.items()
        ]

        persistent.leaderboard.sort(key=lambda x: x[1], reverse=True)

        for rank, (username, score) in enumerate(persistent.leaderboard, start=1):
            print(f"{rank}. {username} - {score} points")

    def new_data():
        return {
            "password": "",
            "levels_unlocked": [True, False, False, False],
            "level_progress" : {
                1: [True, False, False, False],
                2: [False, False, False, False, False],
                3: [False, False, False, False, False, False, False, False],
                4: [False, False, False, False, False, False, False, False, False, False, False, False]
            },
            "level_score" : {
                1: [0, 0, 0, 0],
                2: [0, 0, 0, 0, 0],
                3: [0, 0, 0, 0, 0, 0, 0, 0],
                4: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            },
            "tot_score": 0,
            "time_played": 0.0
        }

    

    def complete_sublevel(level, sublevel, score):
        """
        Mark the given sublevel as complete and unlock the next sublevel (and next level, if needed).
        """
        #User
        curr_user = persistent.saved_user[persistent.current_user]

        curr_level = curr_user["level_progress"][level]
        score_curr_level = curr_user["level_score"][level]

        score_curr_level[sublevel-1] = score
        
        if sublevel >= len(curr_level):
            # If all sublevels are complete, unlock the next level
            print("Level Unlocked:", level)
            if level < len(curr_user["levels_unlocked"]) and curr_user["levels_unlocked"][level] is False:
                curr_user["levels_unlocked"][level] = True
        else:
            print("Curent Level:", level)
            print("Sublevel Unlocked:", sublevel)
            curr_user["level_progress"][level][sublevel] = True

        curr_user["tot_score"] = sum(sum(sublist) for sublist in curr_user["level_score"].values())

        print(curr_user)

        update_play_time()
        renpy.save_persistent()
        print(f"Sublevel {sublevel} of Level {level} completed with score: {score}")

    def sublevel_unlocked(level, sublevel):
        """
        Returns True if the specified sublevel is unlocked.
        """
        curr_user = persistent.saved_user[persistent.current_user]

        curr_level = curr_user["level"][level]

        curr_sub = curr_level[sublevel]


        return curr_sub

    def load_user_data(user):

        print(user)
        
        if user == "Guest" or user is None:
            persistent.current_user = "Guest"
            if "Guest" not in persistent.saved_user:
                persistent.saved_user["Guest"] = {
                    "password": "",
                    "levels_unlocked": [True, False, False, False],
                    "level_progress": {
                        1: [True, False, False, False],
                        2: [False, False, False, False, False],
                        3: [False, False, False, False, False, False, False, False],
                        4: [False, False, False, False, False, False, False, False, False, False, False, False]
                    },
                    "level_score" : {
                        1: [0, 0, 0, 0],
                        2: [0, 0, 0, 0, 0],
                        3: [0, 0, 0, 0, 0, 0, 0, 0],
                        4: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                    },
                    "tot_score": 0,
                    "time_played": 0.0,
                }

        print(persistent.saved_user)

        curr_user = persistent.saved_user[user]

        persistent.levels_unlocked = curr_user['levels_unlocked']
        persistent.level_progress = curr_user['level_progress']

        persistent.start_time_session[user] = time.time()

        renpy.save_persistent()

    def update_play_time():
        user = persistent.current_user
        if user and user in persistent.start_time_session:
            elapsed = time.time() - persistent.start_time_session[user]
            persistent.saved_user[user]["time_played"] += elapsed
            renpy.save_persistent()

    def reset_persistent():
        user = persistent.current_user

        if user in persistent.saved_user:
            old_data = persistent.saved_user[user]
            password = old_data.get("password", "")

            # Save the updated user data
            persistent.saved_user[user] = {
                "password": password,
                "levels_unlocked": [True, False, False, False],
                "level_progress": {
                    1: [True, False, False, False],
                    2: [False, False, False, False, False],
                    3: [False, False, False, False, False, False, False, False],
                    4: [False, False, False, False, False, False, False, False, False, False, False, False]
                },
                "level_score": {
                    1: [0, 0, 0, 0],
                    2: [0, 0, 0, 0, 0],
                    3: [0, 0, 0, 0, 0, 0, 0, 0],
                    4: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                },
                "tot_score": 0,
                "time_played": 0.0
            }

            update_leaderboard()
            renpy.save_persistent()
            renpy.notify("Game progress has been reset.")
        