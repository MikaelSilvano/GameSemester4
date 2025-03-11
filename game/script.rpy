init python:
    def update_icon():
        pass

    def events_icon():
        pass

label setup_icons:
    python:
        for i in range(grid_size):
            rand_image = icon_images[renpy.random.randint(0, 4)]
            idle_path = "Icons/{}.png".format(rand_image)
            idle_image = Image(idle_path)

            icons_list.append(icons.create(Transform(child= idle_image, zoom= 1.0)))
            icons_list[-1].index = i
            icons_list[-1].icon_type = rand_image
            icons_list[-1].idle_image = idle_image

    call screen Match_Three


screen Match_Three:
    $frame_xSize = (icons_per_row * icon_size) + (icons_per_row * icon_padding) + 4
    frame:
        background "#FFFFFF50"

        xalign 0.5
        yalign 0.5
        xsize frame_xSize
        ysize frame_xSize

        $cur_row = 0
        $cur_col = 0

        for i in range(grid_size):
            $xp = (icon_size * cur_col) + (icon_padding * cur_col) 
            $yp = (icon_size * cur_row) + (icon_padding * cur_row)

            image "Icons/grid-cell.png" xpos xp ypos yp zoom 1.0

            python:
                if cur_col % (icons_per_row -1) != 0 or cur_col == 0:
                    cur_col += 1
                else:
                    cur_col = 0
                    cur_row += 1

label start:

    $grid_size = 36
    $icon_size = 100
    $icon_padding = 10
    $icons_per_row = 6
    $icons = SpriteManager(update= update_icon, events= events_icon)
    $icon_images = ["brick", "glass", "rocks", "steel", "wood"]
    $icons_list = []

    scene background
    jump setup_icons

    return

