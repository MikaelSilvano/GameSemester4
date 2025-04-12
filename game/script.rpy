default bgm_on = True

label before_main_menu:
    #play music "audio/audioEcoCity.ogg"
    return

init python:
    current_objectives = None
    
    config.rollback_enabled = False

transform crush_anim:
    linear 0.3 zoom 0.0 alpha 0.0

transform move_anim(new_x, new_y):
    linear 0.3 xpos new_x ypos new_y

transform skill_button_transform:
    # Adjust the zoom factor to scale down the button.
    zoom 0.2

transform building_resized:
    xpos build_xpos
    ypos build_ypos 
    zoom 0.4

transform fade_out:
    linear 0.5 alpha 0.0

label setup_icons:
    $ grid.create_sprite_manager()
    python:
        sprite_manager = grid.create_sprite_manager()
        for icon in grid.icons:
            icon.update_chain_overlay()  
            idle_image = Image("Icons/{}.png".format(icon.icon_type))
            icon.sprite = sprite_manager.create(Transform(child=idle_image, zoom=0.08))
            icon.sprite.x = icon.x
            icon.sprite.y = icon.y
    call screen Match_Three

screen Score_UI:
    frame:
        align (0.05, 0.05)
        background "#2d467a"
        xysize (450, 100)
        padding (4, 4)
        frame:
            background "#9a90f3"
            xfill True
            yfill True
            grid 2 2:
                xfill True
                spacing 0
                text "[game.score]/" align (1.0, 0.5) color "#000000"
                text "[game.target_score]" align (0.0, 0.5) color "#000000"
                text "Moves Left:"align (1.0, 0.5) color "#000000"
                text "{}".format(game.moves) align (0.0, 0.5) color "#000000"

screen Skill2Overlay():
    # This screen shows the Forced Compression skill button for Level 2.
    # It will appear only if the game level is 2.
    if game.level == 2:
        if not game.forced_compression_used:
            imagebutton:
                idle "gui/button/Skill2.png"
                hover "gui/button/Skill2.png"  
                action Function(game.forced_compression)
                xpos 0.815
                ypos 0.14015
                at skill_button_transform
                tooltip Text("Forced Compression: Clear one row (usable once)", style="tooltip_text")
        else:
            # If already used, show a grayed-out version so the player knows it’s disabled.
            add "gui/button/Skill2Gray.png" xpos 0.815 ypos 0.14015 at skill_button_transform

style tx_button:
    color "#000000"
    size 50
    hover_color "#578f91"

style alpha_color:
    color "#00000000"
    size 80

screen reset_grids:
    frame:
        xysize (200, 100)
        background "#fff6c0"
        align(0.05, 0.95)
        textbutton "Reset":
            align (0.5,0.5)
            text_style "tx_button"
            action If(len(grid.icons) != 0, [Function(grid.clear_grid), Function(grid.initialize_grid), Jump("setup_icons")])


screen Match_Three:
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
            
            image "Icons/grid-cell.png" xpos xp ypos yp zoom 1.0
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

    if game.level == 2:
        use Skill2Overlay

    frame:
        background None  # clear default
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
                    $ collected = target  # Display full completion
                    use objective_meter(icon_name=name, current=collected, target=target)
    if current_objectives.all_aims:
        frame:
            background None  # clear default
            fixed:
                add building_list[desired_images-1] at building_resized

label start_game:
    $ my_objectives = current_objectives  # Pull the passed-in objectives
    $ game = GameManager(moves, t_score, level, sublevel)
    $ grid = GridManager(icpr, grid_size)
    
    if game.level == 2:
        $ game.forced_compression_used = False

    $ grid = GridManager(icpr, grid_size)
    $ grid.initialize_grid()

    hide screen menu_screen
    scene backgroundpuzzle

    show screen Score_UI
    show screen reset_grids
    show screen timer_screen

    call setup_icons()
    return

screen result:
    text "{size=+20}Total Score: [game.score]{/size}" color "#FFFFFF" xysize (600, 200)

label start:
    #play music "audio/audioEcoCity.ogg" if_changed

    jump level_selection
    return

label delete_matches_callback(game_manager, matches, check):
    $ game_manager._delete_matches_callback(matches, check)
    return

label win_screen:
    show screen Score_UI
    show screen reset_grids
    show screen timer_screen
    show screen Match_Three
    play sound "audio/building_start.ogg"
    pause 3.0
    play sound "audio/building_finish.ogg"  
    pause 0.5
    hide screen Score_UI
    hide screen reset_grids
    hide screen Match_Three
    hide screen timer_screen
    with Dissolve(0.3) 
    call screen level_complete_screen
    return

label lose_screen:
    hide screen Score_UI
    hide screen reset_grids
    hide screen Match_Three
    hide screen timer_screen
    with Dissolve(0.3) 
    call screen level_lose_screen
    return

##########################################################################
## Level 1 Lore
##########################################################################

image hutbg = "images/Backgrounds/HutBackground.png"
image CharacterLevel1 = "images/Characters/Character1.png"
image SideCharacterLevel1 = "images/Characters/Cewe1.png"

transform left_side:
    xpos 0.2       
    ypos 1.0
    anchor (0.5, 1.0)

transform right_side:
    xpos 0.8       
    ypos 1.0
    anchor (0.5, 1.0)

define mainchar = Character("Ko Khrisna", color="#c8f2ff")
define sidechar = Character("Jordan", color="#ffc8c8")

label level1_intro:
    scene hutbg with fade

    # Show side character first
    show SideCharacterLevel1 at right_side:
        zoom 0.5
        linear 0.2 zoom 1.0
    pause 0.3

    # Then main character
    show CharacterLevel1 at left_side:
        zoom 0.5
        linear 0.2 zoom 1.0

    sidechar "Welcome to your first site, Ko Khrisna. It may look like just dirt and rocks, but it’s a place waiting to become a home."
    mainchar "Oh this is exciting! Where do I even start Jordan?"
    sidechar "Right here—with your hands, your heart, and a whole lot of sustainable thinking. Let’s build your first hut using natural materials by entering the sublevels and prove your skills."
    mainchar "Okay! I’ll show you I’ve got what it takes."

    window hide

    show CharacterLevel1 at left_side:
        linear 0.2 zoom 0.5 alpha 0.0
    show SideCharacterLevel1 at right_side:
        linear 0.2 zoom 0.5 alpha 0.0

    $ renpy.pause(0.2, hard=True)
    scene black with None
    jump sublevel_level1

##########################################################################
## Level 2 Lore
##########################################################################

image housebg = "images/Backgrounds/HouseBackground.png" # udah diubah
image CharacterLevel2 = "images/Characters/CharacterLevel2.png"
image SideCharacterLevel2 = "images/Characters/SideCharacterLevel2.png"

transform left_side:
    xpos 0.2       
    ypos 1.0
    anchor (0.5, 1.0)

transform right_side:
    xpos 0.8       
    ypos 1.0
    anchor (0.5, 1.0)

define mainchar = Character("Ko Khrisna",color="#c8f2ff")
define sidechar = Character("Jordan", color="#ffc8c8")

label level2_intro:
    scene housebg with fade

    # Show side character first
    show SideCharacterLevel2 at right_side:
        zoom 0.5
        linear 0.2 zoom 0.7
    pause 0.3

    # Then main character
    show CharacterLevel2 at left_side:
        zoom 0.2
        linear 0.2 zoom 0.3

    sidechar "Great job Ko Khrisna. You did well, look where you are now!"
    mainchar "They all want homes. Safe ones. Beautiful ones. And… green ones."
    sidechar "That’s why you’re here, Architect Ko Khrisna. These aren’t just houses—they’re a chance to build resilience and community."
    mainchar "I’ve only built huts before… but I’ll try. No shortcuts, no waste right Jordan?"
    sidechar "Exactly. Reuse materials. Let nature into the design. Show them that sustainability isn’t a style—it’s a responsibility!"
    mainchar "Okay Miss Jordan, I won't let you down!"

    window hide

    show CharacterLevel2 at left_side:
        linear 0.1 zoom 0.2 alpha 0.0
    show SideCharacterLevel2 at right_side:
        linear 0.2 zoom 0.5 alpha 0.0

    $ renpy.pause(0.2, hard=True)
    scene black with None
    jump sublevel_level2

##########################################################################
## Level 3 Lore
##########################################################################

image mansionbg = "images/Backgrounds/MansionBackground.png" # nanti diubah
image CharacterLevel3 = "images/Characters/Character3.png"
image SideCharacterLevel3 = "images/Characters/SideCharacterLevel1.png"

transform left_side:
    xpos 0.2       
    ypos 1.0
    anchor (0.5, 1.0)

transform right_side:
    xpos 0.8       
    ypos 1.0
    anchor (0.5, 1.0)

define mainchar = Character("Ko Khrisna",color="#c8f2ff")
define sidechar = Character("Jordan", color="#ffc8c8")


label level3_intro:
    scene mansionbg with fade

    # Show side character first
    show SideCharacterLevel3 at right_side:
        zoom 0.5
        linear 0.2 zoom 0.7
    pause 0.2

    # Then main character
    show CharacterLevel3 at left_side:
        zoom 0.9
        linear 0.1 zoom 0.93

    sidechar "You are making a very good progress, Ko Khrisna, you are now an Architectural Businessman! Let's step up our game and build a mansion!"
    mainchar "A mansion? Isn’t that… the opposite of sustainability?"
    sidechar "Not if you do it using our way. Think of it as an opportunity to prove that eco-luxury is possible. Make it solar-powered, self-sufficient, and filled with light."
    mainchar "Alright then, let's bring up this building by using cement, metal, glass, and solar panels, let's get straight into it!"

    window hide

    show CharacterLevel3 at left_side:
        linear 0.2 zoom 0.5 alpha 0.0
    show SideCharacterLevel3 at right_side:
        linear 0.2 zoom 0.5 alpha 0.0

    $ renpy.pause(0.2, hard=True)
    scene black with None
    jump sublevel_level3

##########################################################################
## Level 4 Lore
##########################################################################

image apartmentbg = "images/Backgrounds/ApartBackground.png" # nanti diubah
image CharacterLevel4 = "images/Characters/Character4.png"
image SideCharacterLevel4 = "images/Characters/Cewe4.png"

transform left_side:
    xpos 0.2       
    ypos 1.0
    anchor (0.5, 1.0)

transform right_side:
    xpos 0.8       
    ypos 1.0
    anchor (0.5, 1.0)

define mainchar = Character("Ko Khrisna",color="#c8f2ff")
define sidechar = Character("Jordan", color="#ffc8c8")

label level4_intro:
    scene apartmentbg with fade

    # Show side character first
    show SideCharacterLevel4 at right_side:
        zoom 0.5
        linear 0.2 zoom 0.7
    pause 0.3

    # Then main character
    show CharacterLevel4 at left_side:
        zoom 0.9
        linear 0.1 zoom 0.93

    sidechar "Amazing! Now look, world leaders are watching you, Ko Khrisna. You are now a world known icon for your sustainable traits. Cities across the globe are asking for your designs."
    mainchar "It’s overwhelming. But I can’t stop now. The planet doesn’t have time."
    sidechar "I am excited to see this sustainable live in the future. Thank you for saving us Ko Khrisna!"
    mainchar "You are most welcome Jordan, I focus on the 11th Sustainable Development Goal."

    window hide

    show CharacterLevel4 at left_side:
        linear 0.2 zoom 0.5 alpha 0.0
    show SideCharacterLevel4 at right_side:
        linear 0.2 zoom 0.5 alpha 0.0

    $ renpy.pause(0.2, hard=True)
    scene black with None
    jump sublevel_level4


    #Profile Page Icon
    default levels_completed = 0

    $ levels_completed += 1

    init python:
        def get_profile_frame():
            # If using levels_completed as a number:
            frame_number = min(levels_completed + 1, 5)  # +1 to match ProfileFrame1.png for 0 completed, ProfileFrame2.png for 1 completed, etc.
            return f"gui/profilePage/ProfileFrame{frame_number}.png"

    #Profile Page Current Level
    init python:
        def get_current_level_text():
            # If using `levels_completed` as an integer
            return f"Current Level: {levels_completed + 1}"