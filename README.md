<h1>Installation</h1>

To properly set up GOES Image Retriever follow the steps outlined below.

1. You need to install these libraries/packages with pip:
- Pillow
- requests
- wget

2. On a storage device of your choosing create a directory named "GOES".

3. Now go to "goes_image_settings.cfg" and on the line starting with "save_path" add the full file path to the "GOES" directory.
It should look something like this:

save_path = D:/path/to/GOES/

4. In the directory named "GOES" create two sub-directories named "GOES_16" and "GOES_17".
The directory tree should look something like this:


D:\
└──path\
   │   
   └───to\
       │
       └───GOES\
           └───GOES_16\
           |
           └───GOES_17\


4. To the line starting with "partial_save_path" add the drive letter followed by a ":" and "/"
so it looks something like this:

partial_save_path = D:/