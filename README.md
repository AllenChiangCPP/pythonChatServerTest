Note
    -code partially generated by ChatGPT

Usage
    -command line 
        -python chatClient.py
        -python chatServer.py
    -Connection notes
        -PORT should be same number on chatClient and chatServer
        -computer to computer
            -chatClient.py
                -change HOST to server computer's IPv4
            -chatServer.py
                -change HOST to server computer's IPv4 or 0.0.0.0
            -note: same computer can also connext with theses settings
        -same computer
            -chatClient.py
                -change HOST to local host IP (127.0.0.1)
            -chatServer.py
                -change HOST to local host IP (127.0.0.1)
        