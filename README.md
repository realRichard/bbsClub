![Ask](https://github.com/realRichard/bbsClub/blob/master/pictures/1170859.gif "Ask")

#   **bbsClub**

###  *bbsClub is a community where people can exchange ideas and answers*

***

##  **Technology stack**

-   python3

-   flask

-   jinja2

-   restful

-   mvc

-   orm

-   mongodb

***

##  **GUI design**

    1. index 
    ![index](https://github.com/realRichard/bbsClub/blob/master/pictures/1.png "index")

    2. add new post
    ![new_post](https://github.com/realRichard/bbsClub/blob/master/pictures/2.png "add_new_post")

    3. post detail and replies
    ![post_detail_and_replies](https://github.com/realRichard/bbsClub/blob/master/pictures/3.png "post_detail_and_replies")

    4. user profile
    ![user_profile](https://github.com/realRichard/bbsClub/blob/master/pictures/4.png "user_profile")

    5. send and receive private letters
    ![send_and_receive_private_letters](https://github.com/realRichard/bbsClub/blob/master/pictures/5.png "send_and_receive_private_letters")

    6. private letter detail
    ![private_letter_detail](https://github.com/realRichard/bbsClub/blob/master/pictures/7.png "private_letter_detail")

    7. admin manage board
    ![administrator_manage_board](https://github.com/realRichard/bbsClub/blob/master/pictures/6.png "administrator_manage_board")

***

##  **Functional specification**

-   Firstly, a green hand comes to the home page, he could browse all kinds of posts belonged to different board, sent by users, included username, userHeadPortrait, the replies, page views, boardname, is top, post title, created time, besides, we also grab out the unreplied posts in the side bar, so that we guys can response more convenient and quickly. Finally we also support for paging display.

-   If we new friends are eager to posting. he should register a valid account in the beginning. The most important thing i wanna tell everyone is you guys do't need worry about the security of your account, cause we nerver hold any clear-text passwords, although cracker stolen the database, he is scarcely possible to figure out your password. meanwhile, it is impossible to find back your password if you forget, the only way is to reset the password. keep in mind, keep in mind, keep in mind.

-   After registering a valid account, we are enable to logging to the community with our account. Due to our site implemented with Cookie technique, the server keeps a session with your client, once you login in, you not repeat to login that you access the site next time for a long time. Is that very convenient and humanized.

-   If one is interesting in a post or adept at some topics, he can reply the items, and anyone else can see that, so we can help others and ask for help. That what we want to do.
 

-   We also support user to use signature, upload headportrait, send private letters, and logout. user can easily know whether their mail read by others.

-   Only administrator has the privilege to manage the post board.

-   In the last, supposing that no one in our community can solve your problem, it seems we have to call google search to serve you.


