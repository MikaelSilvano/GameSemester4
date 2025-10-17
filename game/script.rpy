default blueprint_swap_used = False
default forced_compression_used = False
default masterpiece_build_skill_used = False
default non_violatable_objectives = { }
default icon_skill_collected = []
default Reset_Grid = False
default Reset_Usage = 0
default lv_FT = False
default idle_player = False
default mouse_inputted = False

label before_main_menu:
    $ renpy.music.play("audio/menu.ogg", loop=True, if_changed=True, fadein=2.0)
    if persistent.bgm_on:
        $ renpy.music.set_volume(1)
    else:
        $ renpy.music.set_volume(0)
    return

init python:
    import time
    import random

    current_objectives = None
    temp_objectives = None
    skill_active = False
    icon_skill_collected = []
    required_targets = None
    config.rollback_enabled = False

    config.layers.insert(1, "match3")

    def clear_icon_selection():
        store.icon_skill_collected.clear()
        renpy.restart_interaction()
    
    def move_sprite(sprite, target_x, target_y, duration=1.2, fps=30):
        """
        Moves a sprite to (target_x, target_y) gradually, visible to the human eye.
        Works like a Pygame loop — frame-based animation using renpy.redraw().
        """

        start_x, start_y = sprite.x, sprite.y
        total_frames = int(duration * fps)
        frame = 0
        delay = 1.0 / fps  # frame delay in seconds

        def update(st, at):
            nonlocal frame

            # Calculate progress based on frame count (like in pygame loop)
            progress = frame / total_frames
            if progress >= 1.0:
                sprite.x = target_x
                sprite.y = target_y
                return None  # stop when done

            # Lerp (linear interpolate) between start and target
            sprite.x = start_x + (target_x - start_x) * progress
            sprite.y = start_y + (target_y - start_y) * progress

            # Increment frame counter
            frame += 1

            # Request another redraw at fixed FPS (like clock.tick(FPS))
            renpy.redraw(sprite, delay)
            return 0  # continue updating next frame

        sprite.update = update
        # Start the animation loop right away
        renpy.redraw(sprite, 0)
        
    def update_two_sprites(sprite_a, sprite_b, duration=0.3):
        """
        Smoothly updates two sprites by swapping their positions over time.
        Works exactly like move_sprite(), but for both simultaneously.
        """

        # Record start and target positions
        start_ax, start_ay = sprite_a.x, sprite_a.y
        start_bx, start_by = sprite_b.x, sprite_b.y

        target_ax, target_ay = start_bx, start_by
        target_bx, target_by = start_ax, start_ay

        start_time = time.perf_counter()

        def update(st, at):
            elapsed = time.perf_counter() - start_time
            t = min(elapsed / duration, 1.0)

            # Linear interpolation for both sprites
            sprite_a.x = start_ax + (target_ax - start_ax) * t
            sprite_a.y = start_ay + (target_ay - start_ay) * t

            sprite_b.x = start_bx + (target_bx - start_bx) * t
            sprite_b.y = start_by + (target_by - start_by) * t

            # Continue until done
            if t >= 1.0:
                return None

            # Schedule next frame
            renpy.redraw(sprite_a, 0)
            renpy.redraw(sprite_b, 0)
            return 0

        # Assign the update callback to both sprites
        sprite_a.update = update
        sprite_b.update = update

        # Trigger the redraw loop
        renpy.redraw(sprite_a, 0)
        renpy.redraw(sprite_b, 0)

    class Delayer:
        def __init__(self):
            self.Dragged_icon = False
            self.AM_icon = False

        def reinit():
            self.Dragged_icon = False
            self.AM_icon = False
            
        def Set_Dragged_Icon(Input):
            self.Dragged_icon = Input
            
        def Set_AM_Icon(Input):
            self.AM_icon = Input
        
        def CheckBoth():
            if self.Dragged_icon == True:
                if self.AM_icon == True:
                    return True
                else: 
                    return False
            
            return False

transform crush_anim:
    linear 10 zoom 0.0 alpha 0.0

transform slow_fall:
    linear 0.6 yoffset 0  # 0.6 seconds fall duration

transform move_anim(new_x, new_y):
    linear 10 xpos new_x ypos new_y

transform skill_button_transform:
    zoom 0.2

transform building_resized:
    xpos build_xpos
    ypos build_ypos 
    zoom 0.4

transform building_resized_FT:
    xpos build_xpos_FT
    ypos build_ypos_FT
    zoom 0.4

transform fade_out:
    linear 0.5 alpha 0.0

label setup_icons:
    if Reset_Grid and len(grid.icons) != 0 and Reset_Usage < 3:    
        $ idle_player = True
        hide screen Match_Three
        $ print("Reset Usage:", Reset_Usage)
        $ grid.icons.clear()
        $ grid = None
        $ grid = GridManager(icpr, grid_size)
        $ grid.initialize_grid()
    elif Reset_Usage >= 3:
        $ Reset_Usage = 3
    $ grid.create_sprite_manager()
    python:
        print("reset grid:", Reset_Grid)
        sprite_manager = grid.create_sprite_manager()
        for icon in grid.icons:
            icon.update_chain_overlay()  
            idle_image = Image("Icons/{}.png".format(icon.icon_type))
            icon.sprite = sprite_manager.create(Transform(child=idle_image, zoom=0.08))
            icon.sprite.x = icon.x
            icon.sprite.y = icon.y
            renpy.restart_interaction()
    if Reset_Grid:    
        $ idle_player = False
        $ Reset_Usage += 1
        $ Reset_Grid = False
    python:
        renpy.show_screen("Match_Three", _layer="match3")
        result = renpy.ui.interact()
    call screen Match_Three 

transform rotation(angle):
    rotate angle
    
screen SkillOverlay():
    if persistent.current_skill == 1:
        if not timer_freeze_used:
            if timer_running:
                imagebutton:
                    auto "gui/button/Skill1_%s.png"
                    action Show("time_freeze")
                    xpos 0.768
                    ypos 0.14015
                    at skill_button_transform
            else:
                frame:
                    xysize (1920, 1080)
                    align (0.3, 0.2)
                    background "#ecc1fa24" at rotation(30)
                frame:
                    xysize (1920, 1080)
                    align (-0.1, 0.2)
                    background "#6bf3ff27" at rotation(-30)
                frame:
                    xysize (1920, 1980)
                    align (-0.3, 0.2)
                    background "#87a6fb1e" at rotation(-70)
                frame:
                    xysize (1920, 1080)
                    background "#87d2fb34"
                fixed:
                    xpos 0.768
                    ypos 0.14015
                    at skill_button_transform
                    add "gui/button/Skill1HoverOnTimeFreeze.png"
        else:
            fixed:
                xpos 0.768
                ypos 0.14015
                at skill_button_transform
                add "gui/button/Skill1Gray.png"

    
    elif persistent.current_skill == 2:
        if not forced_compression_used:
            imagebutton:
                auto "gui/button/Skill2_%s.png"
                action Function(skill.forced_compression)
                xpos 0.768
                ypos 0.14015
                at skill_button_transform
        else:
            add "gui/button/Skill2Gray.png" xpos 0.768 ypos 0.14015 at skill_button_transform

    elif persistent.current_skill == 3:
        if not blueprint_swap_used:
            if not skill_active:
                imagebutton:
                    auto "gui/button/Skill3_%s.png"
                    action [
                        Function(clear_icon_selection),
                        SetVariable("skill_active", True)
                    ]
                    xpos 0.768
                    ypos 0.14015
                    at skill_button_transform
            else:
                imagebutton:
                    idle "gui/button/Skill3SkillActive.png"
                    action [
                        Function(clear_icon_selection),
                        SetVariable("skill_active", False)
                    ]
                    xpos 0.768
                    ypos 0.14015
                    at skill_button_transform
                frame:
                    xysize (1920, 1080)
                    background "#37d27334"
                frame:
                    xysize (1920, 1080)
                    background "#1fc25e34" 
                    
        else:
            fixed:
                xpos 0.768
                ypos 0.14015
                at skill_button_transform
                add "gui/button/Skill3Gray.png"
    
    elif persistent.current_skill == 4:
        if not masterpiece_build_skill_used:
            if not skill_active:
                imagebutton:
                    auto "gui/button/Skill4_%s.png" 
                    action SetVariable("skill_active", True)
                    xpos 0.768
                    ypos 0.14015
                    at skill_button_transform
            else:
                imagebutton:
                    idle "gui/button/Skill4SkillActive.png"
                    action SetVariable("skill_active", False)
                    xpos 0.768
                    ypos 0.14015
                    at skill_button_transform
                frame:
                    xysize (1920, 1080)
                    background "#f2744d34"
                frame:
                    xysize (1920, 1080)
                    background "#ff3c0034"
        else:
            add "gui/button/Skill4Gray.png" xpos 0.768 ypos 0.14015 at skill_button_transform


style tx_button:
    color "#000000"
    size 50
    hover_color "#578f91"

style alpha_color:
    color "#00000000"
    size 80

default idle_time_max = 30
default Aim_time = 300

screen reset_grids:
    frame:        
        xysize (200, 100)
        background "#0000"
        align(0.83, 0.04)
        at Transform(zoom=0.5)

        if not idle_player:
            timer 30 action SetVariable("idle_player", True)

        if Reset_Usage < 3:
            if not idle_player:
                imagebutton:
                    idle "gui/button/Resetgridbutton.png"
                    hover "gui/button/Resetgridbutton_hover.png"
                    align (0.5, 0.5)
                    action [
                        SetVariable("Reset_Grid", True),
                        Jump("setup_icons")
                    ]
            else:
                imagebutton:
                    idle "gui/button/Resetgridbutton_idle.png"
                    hover "gui/button/Resetgridbutton_hover.png"
                    align (0.5, 0.5)
                    action [
                        SetVariable("Reset_Grid", True),
                        Jump("setup_icons"),
                        SetVariable("idle_player", False)
                    ]
        
        $ reset_remaining = 3 - Reset_Usage
        if reset_remaining < 0:
            $ reset_remaining = 0
        if reset_remaining == 0:
            add "gui/button/Resetgridbutton_finish.png" align (0.5, 0.5) at Transform(zoom=1)
        text f"{reset_remaining}":
            align (0.5, 0.5)
            xoffset 130
            size 100
            color "#000000"
            outlines [(1, "#fff", 0, 0)]
        
        
        # xysize (200, 100)
        # background "#fff6c0"
        # align(0.05, 0.95)
        # textbutton "Reset":
        #     align (0.5,0.5)
        #     text_style "tx_button"
        #     action [
        #         SetVariable("Reset_Grid", True),
        #         Jump("setup_icons")
        #     ]

screen Match_Three:
    key "K_ESCAPE" action [
        SetVariable("timer_running", False),
        Show("pause_menu")
    ]
    # $ temp_objectives = current_objectives
    $ frame_xSize = (grid.icons_per_row * grid.icon_size) + (grid.icons_per_row * grid.icon_padding) + 6
    $ frame_ySize = ((grid.grid_size // grid.icons_per_row) * grid.icon_size) + ((grid.grid_size // grid.icons_per_row) * grid.icon_padding) + 6
    frame:
        background "#FFFFFF50"
        xalign 0.5
        yalign 0.5
        xsize frame_xSize
        ysize frame_ySize

        $ cur_row = 0
        $ cur_col = 0
        for icon in grid.icons:
            $ xp = (grid.icon_size * cur_col) + (grid.icon_padding * cur_col) 
            $ yp = (grid.icon_size * cur_row) + (grid.icon_padding * cur_row)
            
            image "Icons/GridCell.png" xpos xp ypos yp zoom 1.0
            if icon:
                $ icon.x = xp
                $ icon.y = yp

            python:
                if cur_col % (grid.icons_per_row -1) != 0 or cur_col == 0:
                    cur_col += 1
                else:
                    cur_col = 0
                    cur_row += 1
        
        add grid.sprite_manager:
            xpos 0
            ypos 0
    # $ current_objectives = temp_objectives

screen Building:
    frame:
        background None 
        fixed:
            for img in building_list[:desired_images-1]:
                add img at building_resized

    frame:
        align (0.02, 0.25)
        background None
        has vbox
        spacing 100

        if current_objectives:
            for name in current_objectives.order:
                if name in current_objectives.Aims:
                    $ target = current_objectives.Aims[name]
                    $ raw = current_objectives.total_collected.get(name, 0)
                    $ collected = min(raw, target)
                    use objective_meter(icon_name=name, current=collected, target=target)

                elif name in current_objectives.CompletedAims:
                    $ target = current_objectives.CompletedAims[name]
                    $ collected = target  
                    use objective_meter(icon_name=name, current=collected, target=target)
                    
    # $ print("current_objectives:", current_objectives.Aims, current_objectives.total_collected, current_objectives.CompletedAims)
    if current_objectives.all_aims:
        frame:
            background None  
            fixed:
                if not lv_FT:
                    add building_list[desired_images-1] at building_resized
                else:
                    add building_list[desired_images-1] at building_resized_FT

image smoke_1 = "Building/Smoke/Smoke1.png"
image smoke_2 = "Building/Smoke/Smoke2.png"
image smoke_3 = "Building/Smoke/Smoke3.png"
image smoke_4 = "Building/Smoke/Smoke4.png"
image smoke_5 = "Building/Smoke/Smoke5.png"

image smoke_screen:
    "smoke_1" with Dissolve(0.05, alpha=True)
    pause 0.15
    "smoke_3" with Dissolve(0.05, alpha=True)
    pause 0.15
    "smoke_2" with Dissolve(0.05, alpha=True)
    pause 0.15
    "smoke_5" with Dissolve(0.05, alpha=True)
    pause 0.15
    "smoke_4" with Dissolve(0.05, alpha=True)
    pause 0.15

    repeat

screen smokes:
    add "smoke_screen" at smoke_pos

transform smoke_pos:
    align(0.95, 1.3)
    zoom(1.1)

label tutorial_scene:
    window hide
    scene black
    stop music fadeout 1.0

    play movie "videos/tutorial.webm"
    show screen tutorial_video_screen

    python:
        dur = renpy.music.get_duration("movie") or 148.0  
        pos = renpy.music.get_pos("movie") or 0.0         

        while pos < dur:
            renpy.pause(0.1)
            pos = renpy.music.get_pos("movie") or pos

    stop movie
    return


label start_game:
    $ pause_start = 0.0
    $ pause_duration = 0
    $ timer_on_pause = False
    $ timer_start = 0
    $ time_left = 300
    $ timer_running = True
    $ timer_countdown_start = 0
    $ skill_active = False
    $ timer_freeze_start = 0
    $ timer_freeze_left = 10
    $ timer_freeze_used = False
    $ time_freeze_running = False
    $ game = GameManager(moves, t_score, level, sublevel)
    $ grid = GridManager(icpr, grid_size)
    $ skill = Skills_list()
    $ idle_player = False
    $ Delayed = Delayer()

    #debugging purposes
    # $ current_objectives = Objectives({
    #     "Steel": 1,
    # })

    if persistent.current_skill == 2:
        $ forced_compression_used = False
    
    if persistent.current_skill == 3:
        $ blueprint_swap_used = False
        $ required_targets = 2

    if persistent.current_skill == 4:
        $ masterpiece_build_skill_used = False
        $ required_targets = 1

    $ grid = GridManager(icpr, grid_size)
    $ grid.initialize_grid()

    # if not grid.available_matches:
    #     $ renpy.notify("no matches")

    if blueprint_swap_used == True:
        show screeen countdown

    if persistent.current_skill == 0:
        $ persistent.current_skill = game.level

    $ renpy.music.play("audio/gameplay.ogg", loop=True)

    $ Reset_Usage = 0

    hide screen menu_screen
    scene backgroundpuzzle
    
    show screen Match_Three onlayer match3
    show screen timer_screen
    show screen Building
    show screen SkillOverlay
    show screen reset_grids
    # show screen check_grid

    call setup_icons() from _call_setup_icons
    return

# screen check_grid:
#     frame:
#         xysize (300, 80)
#         background "#d48934"
#         align(0.05, 0.83)
#         textbutton "Check Grid":
#             align (0.5,0.5)
#             text_style "tx_button"
#             text_size 30
#             action If(
#                 Function(grid.possible_move_exists),
#                 [
#                     Function(renpy.notify, "There are still matches " + str(grid.get_current_checked_index()) + ".")
#                 ],
#                 [
#                     Function(renpy.notify, "No more moves available, try reshuffling.")
#                 ]
            
#             )


screen result:
    text "{size=+20}Total Score: [game.score]{/size}" color "#FFFFFF" xysize (600, 200)

label start:
    if persistent.current_user == "Guest" or persistent.current_user == None:
        $ load_user_data("Guest")

    $ renpy.music.play("audio/menu.ogg", loop=True, if_changed=True, fadein=2.0)

    if persistent.bgm_on:
        $ renpy.music.set_volume(1)
    else:
        $ renpy.music.set_volume(0)
    jump level_selection
    return

label delete_matches_callback(game_manager, matches, check):
    $ game_manager._delete_matches_callback(matches, check)
    return

label win_level_screen:
    show screen timer_screen
    show screen Building
    show screen smokes
    play sound "audio/building_start.ogg"
    $ renpy.pause(3.0, hard=True)
    hide screen smokes
    play sound "audio/building_finish.ogg"  
    $ renpy.pause(1.5, hard=True)
    hide layer match3
    hide screen Building
    hide screen Score_UI
    hide screen SkillOverlay
    hide screen time_freeze
    hide layers
    hide screen Match_Three onlayer match3
    hide screen timer_screen
    $ persistent.StoryAuto = True
    call screen level_complete_screen
    return

label win_sublevel_screen:
    show screen timer_screen
    show screen Building
    show screen smokes
    play sound "audio/building_start.ogg"
    $ renpy.pause(3.0, hard=True)
    hide screen smokes
    play sound "audio/building_finish.ogg"  
    $ renpy.pause(1.5, hard=True)
    hide layer match3
    hide screen Building
    hide screen Score_UI
    hide screen SkillOverlay
    hide screen time_freeze
    hide layers
    hide screen Match_Three onlayer match3
    hide screen timer_screen
    hide screen countdown
    call screen sublevel_complete_screen
    return

label lose_screen:
    hide screen Building
    hide screen Score_UI
    hide screen SkillOverlay
    hide screen time_freeze
    hide layers
    hide screen Match_Three onlayer match3
    hide screen timer_screen
    hide screen countdown
    hide layer match3
    hide layers
    with Dissolve(0.3) 
    call screen level_lose_screen
    return

label reset_progress:
    call screen reset_progress_screen
    # call screen main_menu
    

label delay_and_continue:
    $ renpy.pause(2)
    return


##########################################################################
## Level 1 Lore
##########################################################################
$ show_overlay = False

image hutbg = "images/Backgrounds/HutBackground.png"
image CharacterLevel1 = "images/Characters/Character1.png"
image side_characterLevel1 = "images/Characters/Cewe1.png"

transform left_side:
    xpos 0.2       
    ypos 1.0
    anchor (0.5, 1.0)

transform right_side:
    xpos 0.8       
    ypos 1.0
    anchor (0.5, 1.0)

define main_char = Character("Ko Khrisna", color="#2a5246")
define side_char = Character("Jordan", color="#c25656")
define background_chat = Image("gui/button/Backgroundtxt_idle.png")

label level1_intro:
    hide layer match3
    hide layers
    hide screen Match_Three onlayer match3
    if persistent.level_progress[1][1] == False or LevelCutsceneCalled == True:
        scene hutbg with fade

        show side_characterLevel1 at right_side:
            zoom 0.5
            linear 0.2 zoom 1.0
        pause 0.3

        show CharacterLevel1 at left_side:
            zoom 0.5
            linear 0.2 zoom 1.0

        side_char "Welcome to your first site, Ko Khrisna."
        side_char "It may look like just dirt and rocks, but it’s a place waiting to become a home."
        menu:
            "A place waiting to become a home?":
                main_char "A home? Oh this sounds fun! Where do I even start Jordan?"
                side_char "Right here—with your hands, your heart, and a whole lot of sustainable thinking."
                side_char "Let’s build your first hut using natural materials by entering the sublevels and prove your skills. Are you up to it?"
            "Aren't these all just rocks...":
                main_char "Aren't these all just rocks and dirt,? I don't even have the right tools."
                side_char "What do you mean by right tools? Those two hands of yours are enough, your hands, your heart, and a whole lot of sustainable thinking."
                side_char "you'll get there in no time."
                side_char "Using simple materials here, lets build your first hut, prove your skills by entering the sublevels. So? You up for it?"
        menu:
            "I was born ready!":
                main_char "I was born ready!"
            "I've got what it takes!":
                main_char "I’ll show you I’ve got what it takes."

        window hide

        show CharacterLevel1 at left_side:
            linear 0.2 zoom 0.5 alpha 0.0
        show side_characterLevel1 at right_side:
            linear 0.2 zoom 0.5 alpha 0.0

        $ renpy.pause(0.2, hard=True)
        scene black with None
        $ LevelCutsceneCalled = False
    jump sublevel_level1


##########################################################################
## Level 2 Lore
##########################################################################

image housebg = "images/Backgrounds/HouseBackground.png" 
image CharacterLevel2 = "images/Characters/CharacterLevel2.png"
image side_characterLevel2 = "images/Characters/side_characterLevel2.png"

transform left_side:
    xpos 0.2       
    ypos 1.0
    anchor (0.5, 1.0)

transform right_side:
    xpos 0.8       
    ypos 1.0
    anchor (0.5, 1.0)

define main_char = Character("Ko Khrisna",color="#2a5246")
define side_char = Character("Jordan", color="#c25656")

label level2_intro:
    hide layer match3
    hide layers
    hide screen Match_Three onlayer match3
    if persistent.StoryAuto == True or LevelCutsceneCalled == True:
        scene housebg with fade

        show side_characterLevel2 at right_side:
            zoom 0.5
            linear 0.2 zoom 0.7
        pause 0.3

        show CharacterLevel2 at left_side:
            zoom 0.2
            linear 0.2 zoom 0.3

        # side_char "Great job Ko Khrisna. You did well, look where you are now!"
        # menu:
        #     "They all want a home":
        #         pass
        #     "They only want a safe place":
        #         pass
        # main_char "They all want homes. Safe ones. Beautiful ones. And… green ones."
        # side_char "That’s why you’re here, Architect Ko Khrisna. These aren’t just houses—they’re a chance to build resilience and community."
        # menu:
        #     "I've only built huts before...":
        #         pass
        #     "I'll give it a try!":
        #         pass
        # main_char "I’ve only built huts before… but I’ll give it a try! No shortcuts, no waste right Jordan?"
        # side_char "Exactly. Reuse materials. Let nature into the design. Show them that sustainability isn’t a style—it’s a responsibility!"
        # main_char "Okay Miss Jordan, I won't let you down!"

        side_char "Great job Ko Khrisna. You did well, look where you are now!"
        menu:
            "All they want is a safe home.":
                main_char "They all want homes. Safe ones. Beautiful ones. And… green ones."
                side_char "That’s why you’re here, Architect Ko Khrisna. These aren’t just houses—they’re a chance to build resilience and community."
            "Well of course!":
                main_char "Well of course! After all its my job to provide safe, beautiful and eco-friendly homes for them."
                side_char "Well said! However this aren't exactly houses yet..."
                side_char "They're just a chance to build resillience and community."
                menu:
                    "Hm? Not yet a house?":
                        main_char "Hm? Not yet a house?"
                        side_char "Yes, exactly not yet a house."
                    "What do you mean by that?":
                        main_char "I'm not sure by what you meant by a hut being simply a resillience and community for people."
                        side_char "Exactly by what I meant, lets' step up our game and buid a house."
        menu:
            "But.. I've only built huts before...":
                main_char "I’ve only built huts before… I'm not really..."
                side_char "But, remember no shortcuts and no wastes."
                main_char "Okay Miss Jordan!"
                side_char "Reuse materials. Let nature into the design. Show them that sustainability isn’t a style—it’s a responsibility!"
                main_char "I won't let you down Miss Jordan!"
            "I'll give it a try!":
                main_char "I’ll give it a try! No shortcuts, no waste right Jordan?"
                side_char "Exactly. Reuse materials. Let nature into the design. Show them that sustainability isn’t a style—it’s a responsibility!"
                main_char "Okay Miss Jordan, I won't let you down!"

        window hide

        show CharacterLevel2 at left_side:
            linear 0.1 zoom 0.2 alpha 0.0
        show side_characterLevel2 at right_side:
            linear 0.2 zoom 0.5 alpha 0.0

        $ renpy.pause(0.2, hard=True)
        scene black with None
        $ persistent.StoryAuto = False
        $ LevelCutsceneCalled = False
    jump sublevel_level2

##########################################################################
## Level 3 Lore
##########################################################################

image mansionbg = "images/Backgrounds/MansionBackground.png" 
image CharacterLevel3 = "images/Characters/Character3.png"
image side_characterLevel3 = "images/Characters/side_characterLevel1.png"

transform left_side:
    xpos 0.2       
    ypos 1.0
    anchor (0.5, 1.0)

transform right_side:
    xpos 0.8       
    ypos 1.0
    anchor (0.5, 1.0)

define main_char = Character("Ko Khrisna",color="#2a5246")
define side_char = Character("Jordan", color="#c7167z" )

label level3_intro:
    hide layer match3
    hide layers
    hide screen Match_Three onlayer match3
    if persistent.StoryAuto == True or LevelCutsceneCalled == True:
        scene mansionbg with fade

        show side_characterLevel3 at right_side:
            zoom 0.5
            linear 0.2 zoom 0.7
        pause 0.2

        show CharacterLevel3 at left_side:
            zoom 0.9
            linear 0.1 zoom 0.93

        side_char "You are making a very good progress, Ko Khrisna, you are now an Architectural Businessman! Let's step up our game and build a mansion!"
        menu:
            "I'm not too sure in building a mansion.":
                main_char "A mansion? Isn’t that… the opposite of sustainability?"
                side_char "Not if you do it using our way. Think of it as an opportunity to prove that eco-luxury is possible. Make it solar-powered, self-sufficient, and filled with light."
            "A mansion? Isn't that... non-sustanable?":
                main_char "Architectural Businessman? I'm not too sure in building a mansion."
                side_char "Don't you worry follow my guide and think of it as an opportunity to develop eco-luxury mansion."
                menu:
                    "How do you exactly plan on implementing it?":
                        main_char "How do you exactly plan on implementing the developing an eco-luxury mansion?"
                    "I'm not sure a mansion can be eco-friendly.":
                        main_char "I'm not sure that a mansion can be developed into an eco-luxury mansion."
                side_char "Don't worry you'll be fine, you just need to make it solar-powered, self-sufficient, and filled with light."
        menu:
            "Alright!":
                pass
            "Lets' start building!":
                pass
        main_char "Alright then, let's bring up this building by using cement, metal, glass, and solar panels, let's get straight into it!"
            

        window hide

        show CharacterLevel3 at left_side:
            linear 0.2 zoom 0.5 alpha 0.0
        show side_characterLevel3 at right_side:
            linear 0.2 zoom 0.5 alpha 0.0

        $ renpy.pause(0.2, hard=True)
        scene black with None
        $ persistent.StoryAuto = False
        $ LevelCutsceneCalled = False
    jump sublevel_level3

##########################################################################
## Level 4 Lore
##########################################################################

image apartmentbg = "images/Backgrounds/ApartBackground.png" 
image CharacterLevel4 = "images/Characters/Character4.png"
image side_characterLevel4 = "images/Characters/Cewe4.png"

transform left_side:
    xpos 0.2       
    ypos 1.0
    anchor (0.5, 1.0)

transform right_side:
    xpos 0.8       
    ypos 1.0
    anchor (0.5, 1.0)

define main_char = Character("Ko Khrisna",color="#2a5246")
define side_char = Character("Jordan", color="#c25656")

label level4_intro:
    hide layer match3
    hide layers
    hide screen Match_Three
    if persistent.StoryAuto == True or LevelCutsceneCalled == True:
        scene apartmentbg with fade

        show side_characterLevel4 at right_side:
            zoom 0.5
            linear 0.2 zoom 0.7
        pause 0.3

        show CharacterLevel4 at left_side:
            zoom 0.9
            linear 0.1 zoom 0.93

        side_char "Amazing! Now look, world leaders are watching you, Ko Khrisna. You are now a world known icon for your sustainable traits. Cities across the globe are asking for your designs."
        menu:
            "It's overwhelming.":
                main_char "It’s overwhelming. But, I can’t stop now. The planet doesn’t have time."
                side_char "I am excited to see this sustainable live in the future. Thank you for saving us Ko Khrisna!"
            "Of course! Who do you think I am!":
                main_char "Of course! Who do you take me for?"
                side_char "As expected of Ko Khrisna! But, don't stop now! We got to keep moving forward!"
                menu:
                    "Let's keep moving forward!":
                        main_char "Let's keep moving forward! Time doesn't wait for us!"
                    "There's no stopping now!":
                        main_char "There's no stopping now! The future doesn't wait for us!"
                side_char "Thank you for saving us Ko Khrisna! Keep moving forward, I'll always be here cheering you on!"
        menu:
            "You are most welcomed!":
                main_char "You are most welcome Jordan, I focus on the 11th Sustainable Development Goal."
            "Thanks to you too!":
                main_char "Thanks to you too! I'll keep on focusing on the 11th Sustainable Development Goal."

        window hide

        show CharacterLevel4 at left_side:
            linear 0.2 zoom 0.5 alpha 0.0
        show side_characterLevel4 at right_side:
            linear 0.2 zoom 0.5 alpha 0.0

        $ renpy.pause(0.2, hard=True)
        scene black with None
        $ persistent.StoryAuto = False
        $ LevelCutsceneCalled = False
    jump sublevel_level4

default SubLevel412 = False

label level4_end:
    hide layer match3
    hide screen Match_Three
    scene apartmentbg with fade

    show side_characterLevel4 at right_side:
        zoom 0.5
        linear 0.2 zoom 0.7
    pause 0.3

    show CharacterLevel4 at left_side:
        zoom 0.9
        linear 0.1 zoom 0.93

    side_char "Congratulations Ko Khrisna, you have finally reached the end of our plan for building sustainable buildings."
    side_char "Even words itself can't express my appreciation for your hardwork, if it wasn't for you who was willing to build these buildings nothing would have been a reality."
    menu:
        "It was also thanks to your help.":
            main_char "It was also thanks to your help that I was able to make it this far."
        "Thanks to you too.":
            main_char "It was also thanks to you too that I was able to make it this far."
    side_char "Well you might be correct, but your role is indispensible in building these sustainable buildings."
    side_char "So don't put yourself down too much after all there is still a long way to go!"
    menu:
        "Right! This is just the beginning!":
            main_char "You are right Miss Jordan! This ain't the end its the beginning of a future with tall and majestic buildings!"
        "An ending, yet another beginning.":
            main_char "There was never only an ending. An ending marks a new beginning, the beginning of a future with tall and majestic buildings!"
    side_char "Now that's the spirit Ko Khrisna! But remember, buildings maybe tall and majestic and you must never forget that it must always be sustainable and eco-friendly."
    main_char "You got it Miss Jordan, I will make sure to never forget about sustainability and ecofriendly factors in my buildings! Thanks for everything Miss Jordan!"

    window hide

    show CharacterLevel4 at left_side:
        linear 0.2 zoom 0.5 alpha 0.0
    show side_characterLevel4 at right_side:
        linear 0.2 zoom 0.5 alpha 0.0

    $ renpy.pause(0.2, hard=True)
    scene black with None
    $ Sublevel412 = False
    jump level_selection



default levels_completed = 0

init python:
    def get_profile_frame():
        highest_level = max([lvl for lvl, unlocked in enumerate(persistent.levels_unlocked, start=1) if unlocked])
        return f"gui/profilePage/profileFrame{highest_level}.png"

init python:
    def get_score():
        high_score = persistent.saved_user[persistent.current_user]["tot_score"]
        return f"Current Score: {high_score}"

init python:
    def get_time_played():
        seconds = int(persistent.saved_user[persistent.current_user]["time_played"])
        hours   = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"Time Played: {hours} hours, {minutes} minutes"

init python:
    def get_current_level_text():
        highest_level = max([lvl for lvl, unlocked in enumerate(persistent.levels_unlocked, start=1) if unlocked])
        update_leaderboard()
        return f"Current Level: {highest_level}"

init python:
    def get_current_position_text():
        titles = [
            "Construction Worker",
            "Architect",
            "Architectural Firm Owner",
            "World-Renowned \nArchitectural Icon"
        ]

        levels_completed = 0
        for level, sublevels in persistent.level_progress.items():
            if all(sublevels):
                levels_completed += 1

        index = min(levels_completed, len(titles) - 1)
        return f"{titles[index]}"