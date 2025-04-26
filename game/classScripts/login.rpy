define input_username = ""
define input_password = ""
default login_error = ""
default cur_user = "Guest"

init python:

    def check_login():
        store.login_error = ""
        
        if store.input_username in persistent.saved_user:
            username = persistent.saved_user[store.input_username]
            if store.input_password == username['password']:
                persistent.current_user = store.input_username
                store.cur_user = persistent.current_user
                store.login_error = "Login Successful"
                load_user_data(persistent.saved_user[store.cur_user])
            else:   
                store.login_error = "Incorrect Password"
        else:
            store.login_error = "Username not found"

    def add_user():
        store.login_error = ""
        new_username = store.input_username
        if new_username not in persistent.saved_user:
            persistent.saved_user[new_username] = {
                "password": store.input_password,
                "levels_unlocked": new_data()["levels_unlocked"],
                "level_progress": new_data()["level_progress"],
                }
            print(persistent.saved_user)
            renpy.save_persistent()

            store.login_error = "Account successfully registered"
        else:
            store.login_error = "Username already exist"

label login():
    hide screen main_menu
    call screen login_screen()
    return

image login_border = "gui/loginPanel.png"
transform scale (ratio):
    zoom ratio

screen login_screen():

    add "login_border" align (0.025, 0.025) at scale(0.9)
    text "Current user: [persistent.current_user]" align (0.5, 0.42) color "#004a09"
    
    frame:
        background "#00000000"
        default u_name = VariableInputValue("input_username")
        button:
            background "#4dd1e6"
            xysize (340, 40)
            align (0.045, 0.08)
            action u_name.Toggle()
            input value u_name length 20  
                
        default passw = VariableInputValue("input_password")
        button:      
            background "#4dd1e6"
            xysize (340, 40)
            align (0.045, 0.18)
            action passw.Toggle()
            input value passw length 100
        
        if login_error:
            use notify_texts

        imagebutton auto "gui/button/loginButton_%s.png" action [Function(check_login), NullAction()] align (0.025, 0.25) xysize (150, 50)
        imagebutton auto "gui/button/registerButton_%s.png" action [Function(add_user), NullAction()] align (0.125, 0.25) xysize (150, 50)

screen notify_texts:
    frame:
        background "#00000000"
        text "[login_error]"
        align (0.05, 0.35) 
        xysize (350, 50)


            
              
