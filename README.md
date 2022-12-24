# CS50w Capstone
## NI Brew Guide
### About
NI Brew Guide is catalogue, review and search site for the Northern Irish speciality coffee scene. It aims to showcase the best NI has to offer, based solely on the quality of the coffee the shop provides. This means sites are only added by administrator access. I believe this market is currently unserved.

This was produced as my final project for CS50w. Refactoring, optimisation and reimplementation of certain features would be required for production. Aesthetic improvement is required for production.

### Files
#### brewguide.js
This JavaScript file runs on every page and the initial body of code begins to operate when the DOM content is loaded.
It runs various functions based on the page, detailed below:

1. pagination
Pagination allows easy pagination on the index page via a resubmit to the server without the need to include numbers in the url. It submits a hidden form.

2. contactValidation
ContactValidation provides client-side validation on the contact page preventing careless submission, limiting unnecessary server requests and providing a faster UI. This function makes use of the charLimit function I wrote to adapt the page to display remaining characters.

3. geoLocate
GeoLocate prompts the user to allow access to information data for the "near me" results. It notes the user's longitude and latitude, places them in a hidden form and submits the form.

4. review
Review submits an asynchronous request to the server to add a review to the database. If successful it adds this to the page with a "Just now" timestamp until reload.

#### favicon.ico
This file is the page icon.

#### styles.css
This is the page stylesheet. It contains items relating to responsive design however a large part of this is covered by html design and CSS.

#### aboutUs.html
This file contains a carousel of coffee images along with a section on the site's philosophy.

#### best.html
This page displays the highest rated shops at a given time. From here users can access individual shop pages.

#### contact.html
This contains a form allowing the users to contact the admin with feedback and questions by calling the "contact" view.

#### index.html
This page displays a catalogue of all the listed shops. Each shops has a single pictures along with a small amount of information. From here users can access individual shop pages. It can also be used to find shops near your location, filter by location or display search results. It will be rendered slightly differently in these cases.

#### layout.html
This contains a responsive navigation bar along with basic information for the page such as the JavaScript links and stylesheet links. The navbar adapts depending on authentication.

#### login/register.html
These each contain a form for logging in/registering.

#### shop.html
This is the individual shop page template. It contains a carousel of shop photos along with shop information, a google maps iframe, a form for submitting reviews if the user is logged in and the current reviews.

#### models.py
This defines the database structure containing models for users, locations, shops and two types of images.

#### views.py
This begins with a list of imports for the project followed a list of functions detailed below:

1. Index 
This view displays the index.html page after performing the appropriate function. It finds shops and locations from the database paginates them if appropriate and gives them to the render function. The pagination value is low for demonstration purposes. If appropriate it will tell the render function that this is a personalised request. If appropriate, it will filter by location or distance using a longitude and latitude attained using JavaScript.

2. About
This view acquires the about images and renders the About Us page.

3. Contact 
This renders the contact page on a GET request. On a POST request it performs server side validation using the validEmail function and sends an email to a site account using the smtplib library. It makes use of the os library to avoid placing the email and password in the code.

4. Register and login_view
These are largely based on previous projects and allow the user to login or register.

5. Search
This performs a database search for the terms searched. It redirects the shop if an exact match is found but otherwise renders index.html passing relevant shops to the render function.

6. Shop
This view renders the shop page after finding the shop, reviews and images from the database.

7. Logout_view
This view logs the user out.

8. validEmai
This is the function used for server-side validation on the contact page.

9. Best
This view finds the 5 highest rated shops and renders the best page.

10. Review
This view adds a review to the database.

### Additional Information
The site can be ran using the "manage.py runserver" command prepended by the appropriate python command for your system.