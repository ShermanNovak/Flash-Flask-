# FLASH
## Video Demo: https://youtu.be/2wrWAk9c3qQ

## Introducing my project

My Final Project is an online flashcard web application made using Flask.
This was made with active recall in mind, allowing the user to test themselves using virtual 'flashcards'.
Initially I made this project envisioning a web application that allowed the user to make notes, which could instantly be converted into flashcard format.
However, I have to admit that I was not able to fully achieve my vision, yet I am proud of what I have made.
In the beginning, I tried to develop my Flask web application outside of CS50 IDE, but struggled heavily, especially with the login authentication.
Hence, I decided to move to CS50 IDE to expedite the process, since I have a limited period of time that I can spend on this course.
Nonetheless, I hope to improve upon this in future when I have the time to do so, to attempt to run it outside of CS50, and add more functions.

What I really gained from this project was:
- working with dynamic urls
- thinking flexibly yet logically
- a deeper understanding of javascript
- a greater appreciation for web design and aesthetics

### helpers.py

Referencing CS50's pset9 Finance, I used the same login function and adapted the apology function to suit my app.

### app.py

Similarly, referencing CS50's pset9 Finance, I used similar code for the sessions and login functions.

#### '/'

This is the 'welcome' page, and it was supposed to be the face of the app, but I also didn't know how to make it aesthetically pleasing.
I added the cards logo at the top left hand corner which redirects the user to the 'welcome' page.
I also added buttons for users to navigate to either the Sign Up or Login pages.

#### Sign Up, Log In && Log Out 

For this page, I mostly adapted the code from what I wrote previously in pset9 Finance.

#### Home

I wanted this page to be an overview of sorts for users to see what they have and what is going on.

A few special things I did for this page:
1. For the deck name displayed in the table, I used javascript to make it redirect to the card viewer urls.
2. For the delete button, I created a form to post to a dynamic delete url (/delete/<deck_name>).
3. I added a + button next to the Decks and Number of Cards table header to redirect users to make decks or cards.
4. I added an edit button which redirects the user to a dynamic editdeck url (/editdeck/<deck_name>)

#### Create Deck && Create Card

As I mentioned in the project description, I originally planned to have something similar to note-taking format which could instantly be convevrted into cards.
My initial idea was to dynamically append new inputs to the form using javascript, which I was able to code.
However, I got stuck at trying to abstract the data from the dynamically generated inputs and save it into the database.
Hence, I arrived at my current structure, consisting of simple forms, which I hope to find a better workaround for.

#### Card Viewer 

For the card viewer, this was where I first started using dynamic urls, having inspiration from blogs.
In the beginning, I coded out javascript for the functions to show/reveal the content and to direct the user to the next card instead of using a form.
Afterwards, when I decided to implement the idea of having a 'status'/rating for the card, I decided to use a form instead for the redirecting.
Something special I did for this page:
1. I removed the next card button on the last card of the deck, to make sure that the user will not click it and go to an error page.
2. I had to code javascript to make sure that only one checkbox can be checked at any point in time. I also find it odd that radios cannot be unchecked??
For this I have no idea why a forEach loop worked but not a for (var i = 0; i < checkboxes.length; i++)

#### Edit Deck

This page was quite similar to the home page, querying a database for a dictionary to pass to the html in jinja.
Here I became quite comfortable with using dynamic urls and passing variables in the url to use.
Notably, I wrote javascript to change the color of the status span according to the innerHTML of a hidden p tag, which I used jinja to pass values to.
I also implemented a delete button for users to delete individual cards.
At the start I was also thinking of implementing an edit function to edit existing cards, but I decided against it.

#### Delete Deck && Delete Card

For the Delete Deck page, the issue I encountered was handling foreign and primary keys in the database.
I tried deleting the deck before the cards, but found out that I had to do the opposite instead.

For the Delete Card page, the obstacle for me was how to renumber the cards after the user deleted a card.

### schema.sql

This is what I used to keep track of my database structure and to type my code so I could easily drop and recreate tables.

### Website Design

For the website design, I originally used a grey-yellow color scheme and I got CSS for staircase-like h1 tags.
However, it just did not fit with the overall design, and I had to seriously rethink my design choices.
I scrolled through website designs on dribble for inspiration, but I did not have my own graphics so I just chose portrait photos off of unsplash that can easily be replaced.
For the 'welcome' page I can tell that it is slightly too empty, so if I work on this project again in the future I hope to improve that.









