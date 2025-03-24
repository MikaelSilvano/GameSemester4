init python:
    config.rollback_enabled = False

default grid = GridManager(5, 30)
default game = GameManager(10, 2000)

label setup_icons:
    python:
        sprite_manager = grid.create_sprite_manager()  # Create new sprite manager
        
        # Create new icons for all grid positions
        for i in range(grid.grid_size):
            rand_image = grid.icon_images[renpy.random.randint(0, 4)]
            idle_image = Image("Icons/{}.png".format(rand_image))
            
            # Calculate initial position
            col = i % grid.icons_per_row
            row = i // grid.icons_per_row
            xpos = (grid.icon_size * col) + (grid.icon_padding * col)
            ypos = (grid.icon_size * row) + (grid.icon_padding * row)
            
            # Create and add new Icon object
            grid.icons.append(Icon(
                index=i,
                x=xpos,
                y=ypos,
                icon_type=rand_image,
                sprite=sprite_manager.create(Transform(child=idle_image, zoom=0.08))
            ))

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

screen reset_grids:
    frame:
        xysize (200, 100)
        background "#fff6c0"
        align(0.2, 0.5)
        textbutton "Reset":
            align (0.5,0.5)
            text_style "tx_button"
            action If(len(grid.icons) != 0, [Function(grid.clear_grid), Jump("setup_icons")])

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

screen result:
    frame:
        background Solid("#00000067")
        align (0.5, 0.5)
        xsize 1300
        ysize 1080
        text "Total Score:[game.score]" align(0.5, 0.5) color "#FFFFFF"

label start:
    scene background
    show screen Score_UI
    show screen reset_grids
    jump setup_icons

    return