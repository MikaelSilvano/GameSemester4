Sinit python:
    def update_icon(st):
        pass

    def events_icon(event, x, y, st):
        if event.type == 1025:
            if event.button == 1:
                for icon in icons_list:
                    if icon is not None:
                        if icon.x <= x <= (icon.x + icon_size) and icon.y <= y <= (icon.y + icon_size): 
                            find_Match(icon)
                            break
    #Find Matches
    def find_Match(cur_icon):
        matches = []
        matches.append(cur_icon)

        for icon in matches:
            right_index = icon.index + 1
            bot_index = icon.index + icons_per_row
            left_index = icon.index - 1
            top_index = icon.index - icons_per_row

            if icons_list[cur_icon.index] in matches:
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
                    if icon.icon_type == icons_list[left_index].icon_type and icon.index % icons_per_row != 0 and icons_list[left_index] not in matches:
                        matches.append(icons_list[left_index])
                # Match Top
                if icon.index >= icons_per_row and icons_list[top_index] is not None:
                    if icon.icon_type == icons_list[top_index].icon_type and icons_list[top_index] not in matches:
                        matches.append(icons_list[top_index])
            
        print(len(matches))
        if len(matches) >= 2:
            deleteMatch(matches)

    #Delete objects in matches
    def deleteMatch(matches):
        for icon in matches:
            icons_list[icon.index] = None
            icon.destroy()

        renpy.restart_interaction()
        icons.redraw(0)
        shift_icons()

    def shift_icons():

        #Shifting Down
        for i, icon in enumerate(reversed(icons_list)):
            r_index = (grid_size - 1) - i
            if icon is None and r_index >= icons_per_row:
                row_mult = 0
                while icons_list[r_index - (icons_per_row * row_mult)] is None and r_index - (icons_per_row * row_mult) >= icons_per_row:
                    row_mult += 1
                if icons_list[r_index - (icons_per_row * row_mult)] is not None:
                    icons_list[r_index - (icons_per_row * row_mult)].y += (icon_size * row_mult) + (icon_padding * row_mult)
                    icons_list[r_index] = icons_list[r_index - (icons_per_row * row_mult)]
                    icons_list[r_index - (icons_per_row * row_mult)] = None
                    icons_list[r_index].index = r_index
        #Shifting Left if 1 coluuumn is cleared
        #To-Do: Shifting Right & randomness shift      
        for i in range(grid_size - icons_per_row, grid_size - 1):
            if icons_list[i] is None:
                col_mult = 0
                while icons_list[i + col_mult] is None and i + col_mult < grid_size - 1:
                    col_mult += 1
                if icons_list[i + col_mult] is not None:
                    icons_list[i + col_mult].x -= (icon_size * col_mult) + (icon_padding * col_mult)
                    icons_list[i] = icons_list[i + col_mult]
                    icons_list[i + col_mult] = None
                    icons_list[i].index = i
                    for icon in range(grid_size//icons_per_row):
                        print(grid_size/icons_per_row)
                        if icons_list[(i + col_mult) - (icons_per_row * icon)] is not None:
                            icons_list[(i + col_mult) - (icons_per_row * icon)].x -= (icon_size * col_mult) + (icon_padding * col_mult)
                            icons_list[i - (icons_per_row)] = icons_list[(i + col_mult) - (icons_per_row * icon)]
                            icons_list[(i + col_mult) - (icons_per_row * icon)] = None
                            icons_list[i - (icons_per_row)].index -= col_mult

        global moves
        moves -= 1
        icons.redraw(0)
        renpy.show_screen("Score_UI")
        renpy.retain_after_load()

#Setup Icons
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
            
screen Score_UI:
    text "{}".format(moves) color "#000000"

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

    $grid_size = 25
    $icon_size = 100
    $icon_padding = 10
    $icons_per_row = 5
    $icons = SpriteManager(update= update_icon, event= events_icon)
    $icon_images = ["brick", "glass", "rocks", "steel", "wood"]
    $icons_list = []
    $moves = 10

    scene background
    show screen Score_UI
    jump setup_icons

    return

