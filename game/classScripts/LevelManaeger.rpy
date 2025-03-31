default grid_manager = None

##########################################################################
## Level Selection
##########################################################################
label level_selection:
    hide screen main_menu  
    call screen level_selection_screen
    return

label level_1:
    hide screen level_selection  
    call screen level_1_preview
    return

label level_2:
    hide screen level_selection
    call screen level_2_preview
    return

label level_3:
    hide screen level_selection
    call screen level_3_preview
    return

label level_4:
    hide screen level_selection
    call screen level_4_preview
    return

##########################################################################
## Level Selection
##########################################################################

# For Level 1 (Hut)
label hut_sublevel_1:
#   if not grid_manager:
#       $ grid_manager = GridManager(icons_per_row=8, grid_size=64)
#  $ grid = grid_manager  # Assign grid_manager to the global variable 'grid'
#  $ grid_manager.initialize_grid()
    $ moves = 5
    $ t_score = 1000
    $ icpr = 5
    $ grid_size = 25
    jump start_game

    return

label hut_sublevel_2:
    $ moves = 10
    $ t_score = 1500
    $ icpr = 6
    $ grid_size = 36
    jump start_game

    return 
label hut_sublevel_3:
    $ moves = 20
    $ t_score = 2500
    $ icpr = 4
    $ grid_size = 24
    jump start_game

    return
label hut_sublevel_4:
    $ moves = 25
    $ t_score = 4000
    $ icpr = 8
    $ grid_size = 32
    jump start_game
    
    return

##########################################################################
## Level Selection
##########################################################################

# For Level 2 (House)
label house_sublevel_1:
    "House Sublevel 1 chosen."
    return
label house_sublevel_2:
    "House Sublevel 2 chosen."
    return
label house_sublevel_3:
    "House Sublevel 3 chosen."
    return
label house_sublevel_4:
    "House Sublevel 4 chosen."
    return
label house_sublevel_5:
    "House Sublevel 5 chosen."
    return

##########################################################################
## Level Selection
##########################################################################

# For Level 3 (Mansion)
label mansion_sublevel_1:
    "Mansion Sublevel 1 chosen."
    return
label mansion_sublevel_2:
    "Mansion Sublevel 2 chosen."
    return
label mansion_sublevel_3:
    "Mansion Sublevel 3 chosen."
    return
label mansion_sublevel_4:
    "Mansion Sublevel 4 chosen."
    return
label mansion_sublevel_5:
    "Mansion Sublevel 5 chosen."
    return
label mansion_sublevel_6:
    "Mansion Sublevel 6 chosen."
    return
label mansion_sublevel_7:
    "Mansion Sublevel 7 chosen."
    return
label mansion_sublevel_8:
    "Mansion Sublevel 8 chosen."
    return

##########################################################################
## Level Selection
##########################################################################

# For Level 4 (Apartment)
label apartment_sublevel_1:
    "Apartment Sublevel 1 chosen."
    return
label apartment_sublevel_2:
    "Apartment Sublevel 2 chosen."
    return
label apartment_sublevel_3:
    "Apartment Sublevel 3 chosen."
    return
label apartment_sublevel_4:
    "Apartment Sublevel 4 chosen."
    return
label apartment_sublevel_5:
    "Apartment Sublevel 5 chosen."
    return
label apartment_sublevel_6:
    "Apartment Sublevel 6 chosen."
    return
label apartment_sublevel_7:
    "Apartment Sublevel 7 chosen."
    return
label apartment_sublevel_8:
    "Apartment Sublevel 8 chosen."
    return

##########################################################################
## Level Selection
##########################################################################

# Level 1 Sublevel Page
label sublevel_level1:
    hide screen level_1_preview
    call screen sublevel_hut_screen
    return

# Level 2 Sublevel Page
label sublevel_level2:
    hide screen level_2_preview
    call screen sublevel_house_screen
    return

# Level 3: Mansion sublevel pages
label sublevel_level3:
    hide screen level_3_preview
    call screen mansion_sublevel1_screen
    return

label level_3_page2:
    hide screen mansion_sublevel1_screen
    call screen mansion_sublevel2_screen
    return

label mansion_sublevel1:
    hide screen mansion_sublevel2_screen
    call screen mansion_sublevel1_screen
    return

# Level 4: Apartment sublevel pages
label sublevel_level4:
    hide screen level_4_preview
    call screen apartment_sublevel1_screen
    return

label level_4_page2:
    hide screen apartment_sublevel1_screen
    call screen apartment_sublevel2_screen
    return

label apartment_sublevel1:
    hide screen apartment_sublevel2_screen
    call screen apartment_sublevel1_screen
    return
