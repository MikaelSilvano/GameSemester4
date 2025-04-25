default grid_manager = None
default building_list = []
default desired_images = None
default build_xpos = None
default build_ypos = None
default game = None
default icon_image_use = None

label level_selection:
    hide screen main_menu  
    call screen level_selection_screen
    return

label level_1:
    $ build_xpos = 0.62
    $ build_ypos = 450
    hide screen level_selection
    $ icon_image_use = ["Rocks", "Steel", "Wood", "Dirt", "Plant"]
    $ building_list.clear()
    $ building_list.append("images/Building/Hut/hut1.png")
    $ building_list.append("images/Building/Hut/hut2.png")
    $ building_list.append("images/Building/Hut/hut3.png")
    $ building_list.append("images/Building/Hut/hut4.png")
    call screen level_1_preview
    return

label level_2:
    $ build_xpos = 0.62
    $ build_ypos = 450
    hide screen level_selection
    $ icon_image_use = ["Brick", "Glass", "Steel", "Wood", "Cement", "Plant"]
    $ building_list.clear()
    $ building_list.append("images/Building/House/house1.png")
    $ building_list.append("images/Building/House/house2.png")
    $ building_list.append("images/Building/House/house3.png")
    $ building_list.append("images/Building/House/house4.png")
    $ building_list.append("images/Building/House/house5.png")
    call screen level_2_preview
    return

label level_3:
    $ build_xpos = 0.50
    $ build_ypos = 450
    hide screen level_selection
    $ icon_image_use = ["Brick", "Glass", "Rocks", "Steel", "Wood", "Cement", "SolarPanel", "Plant"]
    $ building_list.clear()
    $ building_list.append("images/Building/Mansion/mansion1.png")
    $ building_list.append("images/Building/Mansion/mansion2.png")
    $ building_list.append("images/Building/Mansion/mansion3.png")
    $ building_list.append("images/Building/Mansion/mansion4.png")
    $ building_list.append("images/Building/Mansion/mansion5.png")
    $ building_list.append("images/Building/Mansion/mansion6.png")
    $ building_list.append("images/Building/Mansion/mansion7.png")
    $ building_list.append("images/Building/Mansion/mansion8.png")
    call screen level_3_preview
    return

label level_4:
    $ time_countdown_left = 30
    $ non_violatable_time = 30
    $ build_xpos = 0.62
    $ build_ypos = 290
    hide screen level_selection
    $ icon_image_use = ["Glass", "Rocks", "Steel", "Wood", "Cement", "SolarPanel", "Plant"]
    $ building_list.clear()
    $ building_list.append("images/Building/Apartment/apartment1.png")
    $ building_list.append("images/Building/Apartment/apartment2.png")
    $ building_list.append("images/Building/Apartment/apartment3.png")
    $ building_list.append("images/Building/Apartment/apartment4.png")
    $ building_list.append("images/Building/Apartment/apartment5.png")
    $ building_list.append("images/Building/Apartment/apartment6.png")
    $ building_list.append("images/Building/Apartment/apartment7.png")
    $ building_list.append("images/Building/Apartment/apartment8.png")
    $ building_list.append("images/Building/Apartment/apartment9.png")
    $ building_list.append("images/Building/Apartment/apartment10.png")
    $ building_list.append("images/Building/Apartment/apartment11.png")
    $ building_list.append("images/Building/Apartment/apartment12.png")
    call screen level_4_preview
    return
# For Level 1 (Hut)
label hut_sublevel_1:
    $ level = 1
    $ sublevel = 1   
    $ desired_images = 1
    $ current_objectives = Objectives({
        "Dirt": 7, 
        "Rocks": 3, 
        "Wood": 1
    })
    $ moves = 5
    $ t_score = 1000
    $ icpr = 6
    $ grid_size = 36
    jump start_game

    return

label hut_sublevel_2:
    $ level = 1
    $ sublevel = 2   
    $ desired_images = 2
    $ current_objectives = Objectives({
        "Dirt": 2, 
        "Rocks": 10, 
        "Wood": 3
    })
    $ moves = 10
    $ t_score = 1500
    $ icpr = 6
    $ grid_size = 36
    jump start_game

    return 

label hut_sublevel_3:
    $ level = 1
    $ sublevel = 3   
    $ desired_images = 3
    $ current_objectives = Objectives({
        "Dirt": 3, 
        "Rocks": 5, 
        "Wood": 10,
        "Plant": 2
    })
    $ moves = 20
    $ t_score = 2500
    $ icpr = 5
    $ grid_size = 30
    jump start_game

    return

label hut_sublevel_4:
    $ level = 1
    $ sublevel = 4
    $ desired_images = 4
    $ current_objectives = Objectives({
        "Dirt": 5, 
        "Rocks": 1, 
        "Wood": 6,
        "Plant": 12
    })
    $ moves = 25
    $ t_score = 4000
    $ icpr = 8
    $ grid_size = 40
    jump start_game

    return

# For Level 2 (House)
label house_sublevel_1:
    $ level = 2
    $ sublevel = 1   
    $ desired_images = 1
    $ current_objectives = Objectives({
        "Cement": 5, 
        "Steel": 15, 
        "Brick": 2
    })
    $ moves = 15
    $ t_score = 3000
    $ icpr = 7
    $ grid_size = 35
    jump start_game
    return

label house_sublevel_2:
    $ level = 2
    $ sublevel = 2   
    $ desired_images = 2
    $ current_objectives = Objectives({
        "Cement": 3, 
        "Steel": 5, 
        "Brick": 15
    })
    $ moves = 20
    $ t_score = 4500
    $ icpr = 6
    $ grid_size = 36
    jump start_game
    return

label house_sublevel_3:
    $ level = 2
    $ sublevel = 3   
    $ desired_images = 3
    $ current_objectives = Objectives({
        "Steel": 5, 
        "Wood": 7, 
        "Glass": 8, 
        "Brick": 7
    })
    $ moves = 15
    $ t_score = 5500
    $ icpr = 8
    $ grid_size = 40
    jump start_game
    return

label house_sublevel_4:
    $ level = 2
    $ sublevel = 4   
    $ desired_images = 4
    $ current_objectives = Objectives({
        "Glass": 5, 
        "Wood": 13, 
        "Steel": 13, 
        "Brick": 5
    })
    $ moves = 10
    $ t_score = 2000
    $ icpr = 7
    $ grid_size = 35
    jump start_game
    return

label house_sublevel_5:
    $ level = 2
    $ sublevel = 5   
    $ desired_images = 5
    $ current_objectives = Objectives({
        "Cement": 3, 
        "Glass": 5, 
        "Wood": 15, 
        "Steel": 7, 
        "Plant": 4
    })
    $ moves = 15
    $ t_score = 7500
    $ icpr = 7
    $ grid_size = 35
    jump start_game
    return

label mansion_sublevel_1:
    $ level = 3
    $ sublevel = 1
    $ desired_images = 1
    $ current_objectives = Objectives({
        "Steel": 10,
        "Rocks": 10,
        "Cement": 8
    })
    $ moves = 10
    $ t_score = 3000
    $ icpr = 6
    $ grid_size = 36
    jump start_game
    return

label mansion_sublevel_2:
    $ level = 3
    $ sublevel = 2
    $ desired_images = 2
    $ current_objectives = Objectives({
        "Cement": 10,
        "Rocks": 8,
        "Steel": 5
    })
    $ moves = 15
    $ t_score = 4500
    $ icpr = 6
    $ grid_size = 30
    jump start_game
    return

label mansion_sublevel_3:
    $ level = 3
    $ sublevel = 3
    $ desired_images = 3
    $ current_objectives = Objectives({
        "Cement": 15,
        "Rocks": 13,
        "Steel": 10
    })
    $ moves = 10
    $ t_score = 2500
    $ icpr = 6
    $ grid_size = 36
    jump start_game
    return

label mansion_sublevel_4:
    $ level = 3
    $ sublevel = 4
    $ desired_images = 4
    $ current_objectives = Objectives({
        "Cement": 5,
        "Glass": 10,
        "Brick": 3,
        "Steel": 5
    })
    $ moves = 20
    $ t_score = 3500
    $ icpr = 7
    $ grid_size = 35
    jump start_game
    return

label mansion_sublevel_5:
    $ level = 3
    $ sublevel = 5
    $ desired_images = 5
    $ current_objectives = Objectives({
        "Glass": 12,
        "Cement": 5,
        "Brick": 3,
        "Steel": 5
    })
    $ moves = 15
    $ t_score = 4000
    $ icpr = 7
    $ grid_size = 35
    jump start_game
    return

label mansion_sublevel_6:
    $ level = 3
    $ sublevel = 6
    $ desired_images = 6
    $ current_objectives = Objectives({
        "Glass": 4,
        "Brick": 15,
        "Steel": 10,
        "Cement": 7
    })
    $ moves = 15
    $ t_score = 5000
    $ icpr = 6
    $ grid_size = 36
    jump start_game
    return

label mansion_sublevel_7:
    $ level = 3
    $ sublevel = 7
    $ desired_images = 7
    $ current_objectives = Objectives({
        "Steel": 10,
        "Cement": 7,
        "SolarPanel": 15,
        "Glass": 10,
        "Brick": 10
    })
    $ moves = 10
    $ t_score = 3000
    $ icpr = 7
    $ grid_size = 35
    jump start_game
    return

label mansion_sublevel_8:
    $ level = 3
    $ sublevel = 8
    $ desired_images = 8
    $ current_objectives = Objectives({
        "Cement": 3,
        "Glass": 5,
        "Steel": 15,
        "Rocks": 15,
        "Plant": 10
    })
    $ moves = 15
    $ t_score = 5000
    $ icpr = 6
    $ grid_size = 36
    jump start_game
    return

# For Level 4 (Apartment)
label apartment_sublevel_1:
    $ level = 4
    $ sublevel = 1
    $ desired_images = 1
    $ current_objectives = Objectives({
        "Cement": 7,
        "Rocks": 15,
        "Steel": 2
    })
    $ moves = 15
    $ t_score = 7500
    $ icpr = 7
    $ grid_size = 35
    jump start_game
    return

label apartment_sublevel_2:
    $ level = 4
    $ sublevel = 2
    $ desired_images = 2
    $ current_objectives = Objectives({
        "Steel": 10,
        "Cement": 15,
        "Wood": 5
    })
    $ moves = 15
    $ t_score = 4500
    $ icpr = 7
    $ grid_size = 35
    jump start_game
    return

label apartment_sublevel_3:
    $ level = 4
    $ sublevel = 3
    $ desired_images = 3
    $ current_objectives = Objectives({
        "Steel": 15,
        "Cement": 10,
        "Wood": 5
    })
    $ moves = 15
    $ t_score = 4000
    $ icpr = 6
    $ grid_size = 36
    jump start_game
    return

label apartment_sublevel_4:
    $ level = 4
    $ sublevel = 4
    $ desired_images = 4
    $ current_objectives = Objectives({
        "SolarPanel": 10,
        "Plant": 7,
        "Glass": 8
    })
    $ moves = 15
    $ t_score = 5000
    $ icpr = 5
    $ grid_size = 35
    jump start_game
    return

label apartment_sublevel_5:
    $ level = 4
    $ sublevel = 5
    $ desired_images = 5
    $ current_objectives = Objectives({
        "Cement": 8,
        "SolarPanel": 15,
        "Plant": 8,
        "Glass": 9
    })
    $ moves = 15
    $ t_score = 3500
    $ icpr = 7
    $ grid_size = 35
    jump start_game
    return

label apartment_sublevel_6:
    $ level = 4
    $ sublevel = 6
    $ desired_images = 6
    $ current_objectives = Objectives({
        "Plant": 5,
        "Glass": 15,
        "Steel": 7,
        "Wood": 3
    })
    $ moves = 15
    $ t_score = 5500
    $ icpr = 6
    $ grid_size = 36
    jump start_game
    return

label apartment_sublevel_7:
    $ level = 4
    $ sublevel = 7
    $ desired_images = 7
    $ current_objectives = Objectives({
        "Plant": 3,
        "Glass": 17,
        "Steel": 7,
        "Wood": 3
    })
    $ moves = 15
    $ t_score = 4000
    $ icpr = 5
    $ grid_size = 35
    jump start_game
    return

label apartment_sublevel_8:
    $ level = 4
    $ sublevel = 8
    $ desired_images = 8
    $ current_objectives = Objectives({
        "Cement": 2,
        "Glass": 17,
        "Steel": 7,
        "Wood": 3
    })
    $ moves = 15
    $ t_score = 4600
    $ icpr = 7
    $ grid_size = 35
    jump start_game
    return

label apartment_sublevel_9:
    $ level = 4
    $ sublevel = 9
    $ desired_images = 9
    $ current_objectives = Objectives({
        "Plant": 3,
        "Glass": 7,
        "Cement": 15,
        "Steel": 7,
        "Wood": 3
    })
    $ moves = 15
    $ t_score = 5300
    $ icpr = 6
    $ grid_size = 36
    jump start_game
    return

label apartment_sublevel_10:
    $ level = 4
    $ sublevel = 10
    $ desired_images = 10
    $ current_objectives = Objectives({
        "Cement": 7,
        "Rocks": 5,
        "Glass": 15,
        "Steel": 8,
        "Wood": 6
    })
    $ moves = 15
    $ t_score = 3000
    $ icpr = 5
    $ grid_size = 30
    jump start_game
    return

label apartment_sublevel_11:
    $ level = 4
    $ sublevel = 11
    $ desired_images = 11
    $ current_objectives = Objectives({
        "Cement": 5,
        "SolarPanel": 7,
        "Glass": 15,
        "Steel": 10,
        "Wood": 16
    })
    $ moves = 15
    $ t_score = 3300
    $ icpr = 5
    $ grid_size = 35
    jump start_game
    return

label apartment_sublevel_12:
    $ level = 4
    $ sublevel = 12
    $ desired_images = 12
    $ current_objectives = Objectives({
        "SolarPanel": 7,
        "Cement": 4,
        "Rocks": 5,
        "Glass": 30,
        "Steel": 15,
        "Wood": 10
    })
    $ moves = 15
    $ t_score = 5100
    $ icpr = 6
    $ grid_size = 36
    jump start_game
    return


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

label level_4_page3:
    hide screen apartment_sublevel2_screen
    call screen apartment_sublevel3_screen
    return

label level_4_page2:
    hide screen apartment_sublevel1_screen
    call screen apartment_sublevel2_screen
    return

label apartment_sublevel1:
    hide screen apartment_sublevel2_screen
    call screen apartment_sublevel1_screen
    return
