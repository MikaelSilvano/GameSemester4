init python:
    def update_icon(st):
        pass

    def events_icon(event, x, y, st):
        shift_icons(mouse_event=False)
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
            
        if len(matches) >= 3:
            print("Matched:",len(matches))
            deleteMatch(matches)

    #Delete objects in matches
    def deleteMatch(matches):
        global score
        multiplier = len(matches) / 8
        for icon in matches:
            icons_list[icon.index] = None
            icon.destroy()
            score += round(base_points * (len(matches) + multiplier))
            print(score)

        renpy.restart_interaction()
        icons.redraw(0)
        shift_icons(mouse_event=True)
        check_target_score()

    def check_target_score():
        global score
        if moves <= 0 or score >= target_score:
            print(round((moves/score + 1)))
            score += round(score * (moves/score + 1))
            renpy.show_screen("result")
        else:
            pass

    def shift_icons(mouse_event):
        #Shifting Down
        # Iterate from the bottom cell (grid_size - 1) upward to the first row that can have a cell above it.
        for i in range(grid_size - 1, icons_per_row - 1, -1):
            # Only process if the current cell is empty.
            if icons_list[i] is None:
                # Determine the row and column for the current cell.
                row = i // icons_per_row
                col = i % icons_per_row

                # Search upward in the same column to find an icon that can fall down.
                row_mult = 1  # How many rows above we need to look.
                source_index = i - (icons_per_row * row_mult)
                # Continue while source_index is within bounds and that cell is empty.
                while source_index >= 0 and icons_list[source_index] is None:
                    row_mult += 1
                    source_index = i - (icons_per_row * row_mult)
                
                # If we found a non-None icon above, shift it down.
                if source_index >= 0 and icons_list[source_index] is not None:
                    # Move the icon from the source cell to the current (empty) cell.
                    icons_list[i] = icons_list[source_index]
                    icons_list[source_index] = None

                    # Update the icon's y position: it falls row_mult rows,
                    # so increase y by (icon_size + icon_padding) * row_mult.
                    icons_list[i].y += (icon_size + icon_padding) * row_mult
                    icons_list[i].index = i
                    # target_y = icons_list[i].y + (icon_size + icon_padding) * row_mult
                    # icons_list[i].target_y = target_y
                    # icons_list[i].index = i
                
        #Shifting Left and right
        # Only check icons that are not in the bottom row.
        for i in range(grid_size - icons_per_row):
            if icons_list[i] is not None:
                col = i % icons_per_row
                row = i // icons_per_row
                
                # Determine bottom left and bottom right indices, if within bounds.
                bottom_left_index = None
                bottom_right_index = None
                
                # Bottom left: valid if not in the first column.
                if col > 0:
                    bottom_left_index = i + icons_per_row - 1
                # Bottom right: valid if not in the last column.
                if col < icons_per_row - 1:
                    bottom_right_index = i + icons_per_row + 1
                
                # Check which of the diagonal cells is empty.
                can_shift_left = bottom_left_index is not None and icons_list[bottom_left_index] is None
                can_shift_right = bottom_right_index is not None and icons_list[bottom_right_index] is None

                # If at least one diagonal spot is available, choose where to move the icon.
                if can_shift_left or can_shift_right:
                    # If both are available, pick one randomly; otherwise, choose the available one.
                    if can_shift_left and can_shift_right:
                        direction = renpy.random.randint(0, 1)
                    elif can_shift_left:
                        direction = 0
                    else:
                        direction = 1

                    # Move the icon and update its position.
                    if direction == 0:
                        # Shift to bottom left.
                        icons_list[bottom_left_index] = icons_list[i]   
                        icons_list[i] = None
                        # Adjust x position left and y position down.
                        icons_list[bottom_left_index].x -= (icon_size + icon_padding)
                        icons_list[bottom_left_index].y += (icon_size + icon_padding)
                        icons_list[bottom_left_index].index = bottom_left_index
                    else:
                        # Shift to bottom right.
                        icons_list[bottom_right_index] = icons_list[i]
                        icons_list[i] = None
                        # Adjust x position right and y position down.
                        icons_list[bottom_right_index].x += (icon_size + icon_padding)
                        icons_list[bottom_right_index].y += (icon_size + icon_padding)
                        icons_list[bottom_right_index].index = bottom_right_index

        #For Hidden Grid to continuously add to the visible grid
        for i in range(icons_per_row):
            if icons_list[i] is None:
                # Choose a random icon type
                rand_image = icon_images[renpy.random.randint(0, 4)]
                idle_path = "Icons/{}.png".format(rand_image)
                idle_image = Image(idle_path)
                new_icon = icons.create(Transform(child=idle_image, zoom=0.08))
                new_icon.index = i
                new_icon.icon_type = rand_image
                new_icon.idle_image = idle_image

                # Calculate the x coordinate for the column
                col = i % icons_per_row
                xp = (icon_size * col) + (icon_padding * col)
                new_icon.x = xp

                # Set its initial y position above the grid (simulate hidden grid)
                new_icon.y = - (icon_size + icon_padding)
                
                # Then move it to its proper grid position (row 0, y = 0)
                new_icon.y = 0

                icons_list[i] = new_icon

        if(mouse_event == True):
            global moves
            moves -= 1
        icons.redraw(0)
        renpy.show_screen("Score_UI")
        renpy.retain_after_load()
    
    def clear_icons():
        global moves
        global score
        for icon in icons_list:
            if icon is not None:
                icon.destroy()
        icons_list.clear()
        moves = 10
        score = 0

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
                text "[score]/" align (1.0, 0.5) color "#000000"
                text "[target_score]" align (0.0, 0.5) color "#000000"
                text "Moves Left:"align (1.0, 0.5) color "#000000"
                text "{}".format(moves) align (0.0, 0.5) color "#000000"

screen reset_grids:
    textbutton "Reset" align(0.2, 0.5) action If(len(icons_list) != 0, [Function(clear_icons), Jump("setup_icons")])
        
screen Match_Three:
    $ frame_xSize = (icons_per_row * icon_size) + (icons_per_row * icon_padding) + 6
    frame:
        background "#FFFFFF50"

        xalign 0.5
        yalign 0.5
        xsize frame_xSize
        ysize frame_xSize

        $ cur_row = 0
        $ cur_col = 0

        for icon in icons_list:
            $ xp = (icon_size * cur_col) + (icon_padding * cur_col) 
            $ yp = (icon_size * cur_row) + (icon_padding * cur_row)

            image "Icons/grid-cell.png" xpos xp ypos yp zoom 1.0
            if icon is not None:
                $ icon.x = xp
                $ icon.y = yp

            python:
                if cur_col % (icons_per_row -1) != 0 or cur_col == 0:
                    cur_col += 1
                else:
                    cur_col = 0
                    cur_row += 1

        add icons

screen result:
    frame:
        background Solid("#00000067")
        align (0.5, 0.5)
        xsize 1300
        ysize 1080
        text "Total Score:[score]" align(0.5, 0.5) color "#FFFFFF"

        
label start:

    $ grid_size = 49
    $ icon_size = 100
    $ icon_padding = 10
    $ icons_per_row = 7
    $ icons = SpriteManager(update= update_icon, event= events_icon)
    $ icon_images = ["brick", "glass", "rocks", "steel", "wood"]
    $ icons_list = []
    $ moves = 10
    $ base_points = 5
    $ score = 0
    $ target_score = 5000
    $ scoreboard = {"low": [0, 100], "medium": [101, 200], "high": [201, 300]}

    scene background
    show screen Score_UI
    show screen reset_grids
    jump setup_icons

    return

