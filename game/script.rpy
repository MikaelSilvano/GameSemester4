init python:
    current_objectives = None

transform move_anim(new_x, new_y):
    linear 0.3 xpos new_x ypos new_y

transform fade_out:
    linear 0.5 alpha 0.0

init python:
    config.rollback_enabled = False

label setup_icons:
    python:
        sprite_manager = grid.create_sprite_manager()
        for icon in grid.icons:
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

        # Position the sprite manager relative to the frame

        # Grid positioning code remains the same
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
                    $ collected = target  # ✅ Display full completion
                    use objective_meter(icon_name=name, current=collected, target=target)

label start_game:
    $ my_objectives = current_objectives  # Pull the passed-in objectives
    $ game = GameManager(moves, t_score)
    $ grid = GridManager(icpr, grid_size)
    $ grid.initialize_grid()

    hide screen menu_screen
    scene background

    show screen Score_UI
    show screen reset_grids
    show screen timer_screen

    call setup_icons()
    return
        
screen result:
    frame:
        background Solid("#00000067")
        align (0.5, 0.5)
        xsize 1300
        ysize 1080
        text "Total Score:[game.score]" align(0.5, 0.5) color "#FFFFFF"

label start:
    #play music "audio/audioEcoCity.ogg" fadein 1.0 loop
    jump level_selection

label delete_matches_callback(game_manager, matches, check):
    $ game_manager._delete_matches_callback(matches, check)
    return

label win_screen:
    call screen level_complete_screen
    hide screen timer_screen
    return

##########################################################################
## Level 1 Lore
##########################################################################

image backgroundnew = "images/Backgrounds/backgroundnew.png"
image CharacterLevel1 = "images/Characters/CharacterLevel1.png"
image SideCharacterLevel1 = "images/Characters/SideCharacterLevel1.png"

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
    scene backgroundnew with fade

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

image hutbackground = "images/Backgrounds/backgroundnew.png" # nanti diubah
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
    scene hutbackground with fade

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
        linear 0.2 zoom 0.5 alpha 0.0
    show SideCharacterLevel2 at right_side:
        linear 0.2 zoom 0.5 alpha 0.0

    $ renpy.pause(0.2, hard=True)
    scene black with None
    jump sublevel_level2

##########################################################################
## Level 3 Lore
##########################################################################

image hutbackground = "images/Backgrounds/backgroundnew.png" # nanti diubah
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

label level3_intro:
    scene hutbackground with fade

    # Show side character first
    show SideCharacterLevel2 at right_side:
        zoom 0.5
        linear 0.2 zoom 0.7
    pause 0.3

    # Then main character
    show CharacterLevel2 at left_side:
        zoom 0.2
        linear 0.2 zoom 0.3

    sidechar "You are making a very good progress, Ko Khrisna! Let's step up our game and build a mansion!"
    mainchar "A mansion? Isn’t that… the opposite of sustainability?"
    sidechar "Not if you do it using our way. Think of it as an opportunity to prove that eco-luxury is possible. Make it solar-powered, self-sufficient, and filled with light."
    mainchar "Alright then, let's bring up this building by using cement, metal, glass, and solar panels!"
    sidechar "Great! No waste, no excess. Just purpose, comfort, and clean energy. This mansion will hold more people inside which will make it sustainable for living."
    mainchar "True! And remember—what you build now influences how the world builds tomorrow."
    sidechar "Who knew sustainability could be this stunning?"
    mainchar "Let's get straight into it!"

    window hide

    show CharacterLevel2 at left_side:
        linear 0.2 zoom 0.5 alpha 0.0
    show SideCharacterLevel2 at right_side:
        linear 0.2 zoom 0.5 alpha 0.0

    $ renpy.pause(0.2, hard=True)
    scene black with None
    jump sublevel_level3

label level4_intro:
    scene hutbackground with fade

    # Show side character first
    show SideCharacterLevel2 at right_side:
        zoom 0.5
        linear 0.2 zoom 0.7
    pause 0.3

    # Then main character
    show CharacterLevel2 at left_side:
        zoom 0.2
        linear 0.2 zoom 0.3

    sidechar "Amazing! Now look, world leaders are watching you, Ko Khrisna. Cities across the globe are asking for your designs."
    mainchar "It’s overwhelming. But I can’t stop now. The planet doesn’t have time."
    sidechar "You are wrong! Let’s build a smart skyscrapper where vertical gardens and solar glass is the dominance of this building. This apartment will be the model of eco-urban living."
    mainchar "Soo... this is the future?!"
    sidechar "No. This is the present, because you made it happen. You didn’t just build structures—you built a legacy of sustainability."
    mainchar "What a great insight that you gave to me, let's get started then!"
    sidechar "Yes, I am excited to see this sustainable apartment to be built ASAP!"

    window hide

    show CharacterLevel2 at left_side:
        linear 0.2 zoom 0.5 alpha 0.0
    show SideCharacterLevel2 at right_side:
        linear 0.2 zoom 0.5 alpha 0.0

    $ renpy.pause(0.2, hard=True)
    scene black with None
    jump sublevel_level4