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

```
D:\
└──path\
   │   
   └───to\
       │
       └───GOES\
           └───GOES_16\
           |
           └───GOES_17\
```

4. To the line starting with "partial_save_path" add the drive letter followed by a ":" and "/"
so it looks something like this:
```
partial_save_path = D:/
```

<h1>Background & Explanation</h1>
This is a program that downloads weather satellite images from the National Oceanic and Atmospheric Administration (NOAA). They have a website for the GOES-16 and GOES-17 satellites in geostationary orbit. On the particular sites listed below the full disk and so called CONUS images are uploaded every 10 minutes (600 seconds) but with a 20 minute (1200 second) lag behind "real time"; so if an image was taken at 12:00:00 UTC it only appears on the website at 12:20:00 UTC.

What further simplified the project was that the image URLs are highly predictable, they can look like this:
https://cdn.star.nesdis.noaa.gov/GOES16/ABI/FD/GEOCOLOR/20211861830_GOES16-ABI-FD-GEOCOLOR-10848x10848.jpg

Here 2021 is the year, 186 is the day number (described here for Python programmers: https://docs.python.org/3/library/datetime.html#date-objects) and 1830 is the time of day in UTC.

Using all this information I wrote a series of programs that downloaded the GOES-16 and GOES-17 images retrospecitvely and prospectively; though for some reason no images older than three days (259200 seconds) can be downloaded from these particular servers. Over time I fixed bugs and added new features like generating dummy images when I got an HTTP 400 or 500 series error. This program could probably be set to run for a long time with enough storage space. There's also a bunch of logging features and simple statistics for the downloaded data and program operation.

Some bugs might very well still be present, so run at your own risk.

My code only downloads the GeoColor images in all resolutions except the "GeoTIFF" and "Animation Loop" options. The choice of GeoColor was made as I originally wrote this code to make full disk time lapse sequences of the Earth.

- GOES-16 full disk images:
https://www.star.nesdis.noaa.gov/GOES/fulldisk.php?sat=G16

- GOES-17 full disk images:
https://www.star.nesdis.noaa.gov/GOES/fulldisk.php?sat=G17
