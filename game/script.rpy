#test
init python:
    def update_icon(st):
        pass

    def events_icon(event, x, y, st):
        if event.type == 1025:
            if event.button == 1:
                for icon in icons_list:
                    if icon.x <= x <= (icon.x + icon_size) and icon.y <= y <= (icon.y + icon_size): 
                        find_Match(icon)
                        break

    def find_Match(cur_icon):
        matches = []
        matches.append(cur_icon)

        for icon in matches:
            right_index = icon.index + 1
            bot_index = icon.index + icons_per_row
            left_index = icon.index - 1
            top_index = icon.index - icons_per_row

            # Match Right
            if right_index < grid_size and icons_list[right_index] is not None:
                if icon.icon_type == icons_list[right_index].icon_type and right_index % icons_per_row != 0 and icons_list[right_index] not in matches:
                    matches.append(icons_list[right_index])
            # Match Bot
            if icon.index <= grid_size - icons_per_row - 1 and icons_list[bot_index] is not None:
                if icon.icon_type == icons_list[bot_index].icon_type and icons_list[bot_index] not in matches:
                    matches.append(icons_list[bot_index])
            # Match Left
            if left_index >= 0 and icons_list[left_index] is not None:
                if icon.icon_type == icons_list[left_index].icon_type and icon.index % icons_per_row != 0:
                    matches.append(icons_list[left_index])
            # Match Top
            if icon.index >= icons_per_row and icons_list[top_index] is not None:
                if icon.icon_type == icons_list[top_index].icon_type and icons_list[top_index] not in matches:
                    matches.append(icons_list[top_index])
        if len(matches) != 1:
            deleteMatch(matches)

    def deleteMatch(matches):
        for icon in matches:
            icons_list[icon.index] = None
            icon.destroy()

        renpy.restart_interaction()
        icons.redraw(0)
        shiftIcons()

    def shiftIcons():
        for i, icon in enumerate(reversed(icons_list)):
            r_index = (grid_size - 1) - i

            if icon is None and r_index >= icons_per_row:
                row_mult = 0
                while icons_list[r_index - (icons_per_row * row_mult)] is None and r_index - (icons_per_row * row_mult) >= icons_per_row:
                    row_mult += 1
                if icons_list[r_index - (icons_per_row * row_mult)] is not None:
                    icons_list[r_index - (icons_per_row * row_mult)].y += (icon_size * row_mult) + (icon_padding * row_mult)
                    icons_list[r_index] = icons_list[r_index - (icons_per_row * row_mult)]
                    icons_list[r_index - (icons_per_row * row_mult)]
label setup_icons:
    python:
        for i in range(grid_size):
            rand_image = icon_images[renpy.random.randint(0, 4)]
            idle_path = "Icons/{}.png".format(rand_image)
            idle_image = Image(idle_path)

            icons_list.append(icons.create(Transform(child= idle_image, zoom= 0.08)))
            icons_list[-1].index = i
            icons_list[-1].icon_type = rand_image
            icons_list[-1].idle_image = idle_image

    call screen Match_Three


screen Match_Three:
                
    $frame_xSize = (icons_per_row * icon_size) + (icons_per_row * icon_padding) + 6
    frame:
        background "#FFFFFF50"

        xalign 0.5
        yalign 0.5
        xsize frame_xSize
        ysize frame_xSize

        $cur_row = 0
        $cur_col = 0

        for icon in icons_list:
            $xp = (icon_size * cur_col) + (icon_padding * cur_col) 
            $yp = (icon_size * cur_row) + (icon_padding * cur_row)

            image "Icons/grid-cell.png" xpos xp ypos yp zoom 1.0
            if icon is not None:
                $icon.x = xp
                $icon.y = yp

            python:
                if cur_col % (icons_per_row -1) != 0 or cur_col == 0:
                    cur_col += 1
                else:
                    cur_col = 0
                    cur_row += 1

        add icons

label start:

    $grid_size = 36
    $icon_size = 100
    $icon_padding = 10
    $icons_per_row = 6
    $icons = SpriteManager(update= update_icon, event= events_icon)
    $icon_images = ["brick", "glass", "rocks", "steel", "wood"]
    $icons_list = []

    scene background
    jump setup_icons

    return

