# ChatrNet
- Uses Python Flask Framework
- Utilizes SQLAlchemy and SQLite DB files to store data when a user posts
- The SQLite DB file is stored at ```instance/posts.db```
- When an image is uploaded, it is stored in ```static/uploads```. Only allows png, jpg, and gif's.
- Homepage, with 4 most recent posts
- By default, ChatrNet has 4 'places'. When a user posts, they choose what place they want to post
- A 'place' can easily be added by including a new dictionary item in 'place_list'. Dictionary key is what shows in the URL, the dictionary item is the name of the place
![ChatrNet](chatrnet.png)
