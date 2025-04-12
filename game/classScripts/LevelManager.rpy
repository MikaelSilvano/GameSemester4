default grid_manager = None
default building_list = []
default desired_images = None
default build_xpos = None
default build_ypos = None
default game = None

##########################################################################
## Level Selection
##########################################################################
label level_selection:
    hide screen main_menu  
    call screen level_selection_screen
    return

label level_1:
    $ build_xpos = 0.62
    $ build_ypos = 450
    hide screen level_selection
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
    $ build_xpos = 0.62
    $ build_ypos = 290
    hide screen level_selection
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

##########################################################################
## Level Selection
##########################################################################

# For Level 1 (Hut)
label hut_sublevel_1:
    $ level = 1
    $ sublevel = 1   
    $ desired_images = 1
    $ current_objectives = Objectives({
        "rocks": 3,
        "wood": 3,
        "glass": 3
    })
    $ moves = 5
    $ t_score = 1000
    $ icpr = 5
    $ grid_size = 25
    jump start_game

    return

label hut_sublevel_2:
    $ level = 1
    $ sublevel = 2   
    $ desired_images = 2
    $ current_objectives = Objectives({
        "rocks": 10,
        "wood": 10,
        "glass": 10
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
        "rocks": 20,
        "wood": 15,
        "glass": 15
    })
    $ moves = 20
    $ t_score = 2500
    $ icpr = 4
    $ grid_size = 24
    jump start_game

    return

label hut_sublevel_4:
    $ level = 1
    $ sublevel = 4
    $ desired_images = 4
    $ current_objectives = Objectives({
        "rocks": 15,
        "wood": 20,
        "glass": 10
    })
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
    $ level = 2
    $ sublevel = 1   
    $ desired_images = 1
    $ current_objectives = Objectives({
        "glass": 10,
        "brick": 10,
        "steel": 20
    })
    $ moves = 15
    $ t_score = 3000
    $ icpr = 5
    $ grid_size = 30
    jump start_game
    return

label house_sublevel_2:
    $ level = 2
    $ sublevel = 2   
    $ desired_images = 2
    $ current_objectives = Objectives({
        "glass": 5,
        "brick": 20,
        "steel": 10
    })
    $ moves = 20
    $ t_score = 4500
    $ icpr = 5
    $ grid_size = 25
    jump start_game
    return

label house_sublevel_3:
    $ level = 2
    $ sublevel = 3   
    $ desired_images = 3
    $ current_objectives = Objectives({
        "glass": 10,
        "brick": 15,
        "steel": 5
    })
    $ moves = 15
    $ t_score = 5500
    $ icpr = 4
    $ grid_size = 32
    jump start_game
    return

label house_sublevel_4:
    $ level = 2
    $ sublevel = 4   
    $ desired_images = 4
    $ current_objectives = Objectives({
        "glass": 5,
        "brick": 25,
        "steel": 5
    })
    $ moves = 10
    $ t_score = 2000
    $ icpr = 6
    $ grid_size = 18
    jump start_game
    return

label house_sublevel_5:
    $ level = 2
    $ sublevel = 5   
    $ desired_images = 5
    $ current_objectives = Objectives({
        "glass": 5,
        "brick": 10,
        "steel": 5
    })
    $ moves = 15
    $ t_score = 7500
    $ icpr = 3
    $ grid_size = 18
    jump start_game
    return

##########################################################################
## Level Selection
##########################################################################

# For Level 3 (Mansion)
label mansion_sublevel_1:
    $ level = 3
    $ sublevel = 1   
    $ desired_images = 1
    $ current_objectives = Objectives({
        "glass": 5,
        "brick": 10,
        "steel": 5,
        "rocks": 10,
    })
    $ moves = 10
    $ t_score = 3000
    $ icpr = 6
    $ grid_size = 24
    jump start_game
    return

label mansion_sublevel_2:
    $ level = 3
    $ sublevel = 2   
    $ desired_images = 2
    $ current_objectives = Objectives({
        "glass": 10,
        "brick": 15,
        "steel": 10,
        "rocks": 10,
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
        "glass": 5,
        "brick": 17,
        "steel": 7,
        "rocks": 20,
    })
    $ moves = 10
    $ t_score = 2500
    $ icpr = 5
    $ grid_size = 15
    jump start_game
    return

label mansion_sublevel_4:
    $ level = 3
    $ sublevel = 4   
    $ desired_images = 4
    $ current_objectives = Objectives({
        "glass": 5,
        "brick": 10,
        "steel": 5,
        "rocks": 10,
    })
    $ moves = 20
    $ t_score = 3500
    $ icpr = 4
    $ grid_size = 20
    jump start_game
    return

label mansion_sublevel_5:
    $ level = 3
    $ sublevel = 5   
    $ desired_images = 5
    $ current_objectives = Objectives({
        "glass": 7,
        "brick": 13,
        "steel": 8,
        "rocks": 6,
    })
    $ moves = 15
    $ t_score = 4000
    $ icpr = 3
    $ grid_size = 15
    jump start_game
    return

label mansion_sublevel_6:
    $ level = 3
    $ sublevel = 6   
    $ desired_images = 6
    $ current_objectives = Objectives({
        "glass": 9,
        "brick": 13,
        "steel": 15,
        "rocks": 8,
    })
    $ moves = 15
    $ t_score = 5000
    $ icpr = 7
    $ grid_size = 21
    jump start_game
    return

label mansion_sublevel_7:
    $ level = 3
    $ sublevel = 7   
    $ desired_images = 7
    $ current_objectives = Objectives({
        "glass": 5,
        "brick": 17,
        "steel": 11,
        "rocks": 13,
    })
    $ moves = 10
    $ t_score = 3000
    $ icpr = 5
    $ grid_size = 25
    jump start_game
    return

label mansion_sublevel_8:
    $ level = 3
    $ sublevel = 8   
    $ desired_images = 8
    $ current_objectives = Objectives({
        "glass": 7,
        "brick": 10,
        "steel": 6,
        "rocks": 10,
    })
    $ moves = 15
    $ t_score = 5000
    $ icpr = 4
    $ grid_size = 28
    jump start_game
    return

##########################################################################
## Level Selection
##########################################################################

# For Level 4 (Apartment)
label apartment_sublevel_1:
    $ level = 4
    $ sublevel = 1   
    $ desired_images = 1
    $ current_objectives = Objectives({
        "glass": 5,
        "brick": 10,
        "steel": 15,
        "rocks": 8,
        "wood" : 14
    })
    $ moves = 15
    $ t_score = 7500
    $ icpr = 5
    $ grid_size = 20
    jump start_game
    return

label apartment_sublevel_2:
    $ level = 4
    $ sublevel = 2  
    $ desired_images = 2
    $ current_objectives = Objectives({
        "glass": 10,
        "brick": 13,
        "steel": 12,
        "rocks": 7,
        "wood" : 10
    })
    $ moves = 15
    $ t_score = 4500
    $ icpr = 4
    $ grid_size = 24
    jump start_game
    return

label apartment_sublevel_3:
    $ level = 4
    $ sublevel = 3  
    $ desired_images = 3
    $ current_objectives = Objectives({
        "glass": 5,
        "brick": 14,
        "steel": 16,
        "rocks": 6,
        "wood" : 10
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
        "glass": 5,
        "brick": 10,
        "steel": 5,
        "rocks": 10,
        "wood" : 10
    })
    $ moves = 15
    $ t_score = 5000
    $ icpr = 5
    $ grid_size = 15
    jump start_game
    return

label apartment_sublevel_5:
    $ level = 4
    $ sublevel = 5  
    $ desired_images = 5
    $ current_objectives = Objectives({
        "glass": 12,
        "brick": 7,
        "steel": 16,
        "rocks": 9,
        "wood" : 14
    })
    $ moves = 15
    $ t_score = 3500
    $ icpr = 7
    $ grid_size = 21
    jump start_game
    return

label apartment_sublevel_6:
    $ level = 4
    $ sublevel = 6  
    $ desired_images = 6
    $ current_objectives = Objectives({
        "glass": 8,
        "brick": 15,
        "steel": 6,
        "rocks": 10,
        "wood" : 13
    })
    $ moves = 15
    $ t_score = 5500
    $ icpr = 3
    $ grid_size = 15
    jump start_game
    return

label apartment_sublevel_7:
    $ level = 4
    $ sublevel = 7  
    $ desired_images = 7
    $ current_objectives = Objectives({
        "glass": 14,
        "brick": 9,
        "steel": 17,
        "rocks": 6,
        "wood" : 12
    })
    $ moves = 15
    $ t_score = 4000
    $ icpr = 5
    $ grid_size = 20
    jump start_game
    return

label apartment_sublevel_8:
    $ level = 4
    $ sublevel = 8  
    $ desired_images = 8
    $ current_objectives = Objectives({
        "glass": 11,
        "brick": 16,
        "steel": 7,
        "rocks": 8,
        "wood" : 10
    })
    $ moves = 15
    $ t_score = 4600
    $ icpr = 4
    $ grid_size = 12
    jump start_game
    return

label apartment_sublevel_9:
    $ level = 4
    $ sublevel = 9  
    $ desired_images = 9
    $ current_objectives = Objectives({
        "glass": 9,
        "brick": 12,
        "steel": 18,
        "rocks": 14,
        "wood" : 7
    })
    $ moves = 15
    $ t_score = 5300
    $ icpr = 6
    $ grid_size = 30
    jump start_game
    return

label apartment_sublevel_10:
    $ level = 4
    $ sublevel = 10  
    $ desired_images = 10
    $ current_objectives = Objectives({
        "glass": 7,
        "brick": 14,
        "steel": 10,
        "rocks": 16,
        "wood" : 8
    })
    $ moves = 15
    $ t_score = 3000
    $ icpr = 3
    $ grid_size = 18
    jump start_game
    return

label apartment_sublevel_11:
    $ level = 4
    $ sublevel = 11  
    $ desired_images = 11
    $ current_objectives = Objectives({
        "glass": 13,
        "brick": 8,
        "steel": 9,
        "rocks": 17,
        "wood" : 15
    })
    $ moves = 15
    $ t_score = 3300
    $ icpr = 5
    $ grid_size = 25
    jump start_game
    return

label apartment_sublevel_12:
    $ level = 4
    $ sublevel = 12  
    $ desired_images = 12
    $ current_objectives = Objectives({
        "glass": 10,
        "brick": 13,
        "steel": 11,
        "rocks": 5,
        "wood" : 6
    })
    $ moves = 15
    $ t_score = 5100
    $ icpr = 4
    $ grid_size = 12
    jump start_game
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
