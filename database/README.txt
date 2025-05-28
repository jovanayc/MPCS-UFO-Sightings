(sorry, I strongly dislike writing in markdown!)

To build and populate the table (as it exists so far) follow these steps:

1. Install dependencies from the `requirements.txt` file

2. In our shared google drive folder 
    (https://drive.google.com/drive/u/0/folders/1rckUsM9W9-URgi4lUfDNXGWwBKK0f9C6)
    there is now a folder called ufo-data in the main directory. Download it and
    drop the whole folder in ~/database/clean-data. It's a bit too big for me to
    feel good about pushing it to GitHub.

    Otherwise, don't worry about the clean-data directory at all – it just contains 
    scripts that produced the main .csv files I used to upload data to the database. 
    These files are called `combined_deduped.csv`, `keywords.csv`, and `sightid_keyid.csv` 
    (I'd like your opinions on the third one when we meet). If you don't feel like
    downloading the whole folder (it's about 110 MB), you can get by with just the 
    three .csv files listed above. Just make sure they're in the correct directory.

3. Navigate to ~/database/mysql-insertion and first run `python build_database.py` 
    (making sure that you don't already have a version of the DB on your computer,
    because this will not delete and recreate that if so).

4. Now, run `python populate_database.py` (first be sure to change the MYPASSWORD field
    to your MySQL password!!) and the data *should* all load. I have not done 
    anything with articles / historical events yet, but I did create a keyword mapping,
    and all of the other stuff should connect correctly too. I haven't gone through this
    with a fine-toothed comb, but it should be more or less working. Note that both UFO and
    Sighting have kind of null value entries – this was necessary to connect the tables by
    IDs without getting a lot of errors. I forgot about the NaN woes of using Pandas....
    until today.

5. Once it's loaded, you can check it out and MySQL and provide feedback as desired! I will 
    work on getting the articles/historical events section done before our meeting tomorrow.

Note: I wanted to be able to add a sample of the data to the GitHub repo, but unfortunately
without creating entirely fake data, that created a series of dependency issues re various
IDs and relationships, and no data would load successfully. Sorry!