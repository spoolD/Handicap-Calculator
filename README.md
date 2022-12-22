# HANDI
This project was completed in accordance to the Capstone Project requirements for CS50w. 

## Description
Handi is a website that allows you to track your golf handicap as well as connect with other golfers to see how to stack up. A golf handicap is a numerical measure of a golfer's potential and is used to allow players of various skills levels the ability to compete with each other. It is also a good way to track your improvement.

The handicap calculations are all in accordance with the [USGA's World Handicap Index Calculations] (https://www.usga.org/content/usga/home-page/handicapping/world-handicap-system/topics/handicap-index-calculation.html). For each round of either 18 holes or 9 holes the player enters the course rating and slope in addition to their score. The differential is calculated for each round, and once a sufficient number of rounds has been completed (minimum 3) a handicap is calculated for the player.

A user is also able to search for and follow other golfers to compare scores and skill levels

## Distinctiveness and Complexity
This projects meets the requirements for distinctiveness and complexity as described. The project implements several features that are independent of projects in the course such as:

1. The ability to add and organize scores
2. Calculation of differentials for each round
3. Calculation of a golfer's handicap in accordance with USGA guidelines
4. The ability to add 9 hole scores which are then combined with other 9 hole scores to contibute to the golfer's handicap.
5. A search feature written in Javascript to search for other golfers on the platform and get results updated as you type.

The project uses Django on the backend to direct the user accordingly, perform all neccessary calculations, and store user data and models. Two models are used to store data. The first is the User model which includes basic user information as well as the user's handicap and follow information. Second, a score model was added. The score model includes the information related to each round entered by the user and contains fields for the course, date, number of holes, score, rating, slope, and calculated differential. 

JavaScript is used on the front-end for two functions. The first is to follow and unfollow golfers. The second is to search the Handi database for golfers to follow and/or compare handicaps and scores.

## Files Added
###follow.js
Contains logic to follow/unfollow a fellow golfer when the appropriate button is clicked. A post request is sent to modify the database, and the button text is updated accordingly.

### search.js
Based on the input into the text box the backend is search for matching results for users. The resulting query is then displayed below with golfers and their handicaps. Golfers are returned as a link that when clicked directs you to a page that displays all of their recent scores and allows you to follow for easy access. If no users are returned 'No Golfers Found' is displayed.

### font folder
Contains files related to the font used on the front-end

### Handi-logo.png
Logo created for the website using the free Adobe Express logo creator

### styles.css
CSS for application

### add.html
Page to allow user input for scores. Uses Django form created using the Score model

### golfer.html
Page for each golfer to display scores, handicap, and follow/unfollow button

### index.html
If logged in displays the users scores and handicap. Otherwise is the login page

### layout.html
Base formatting for webpage

### lookup.html
Page that displays golfers current followed in addition to the search function to find other golfers

### register.html
Page to register for Handi

## How to run
Application is executed the same as others in CS50w. From the Handicap-Calculator folder execute python manage.py runserver.

## More info
For simplicity, no adjustments are made in Handi for exceptional scores or excessive upward movement in a single year. These are rules implemented by the USGA to prevent handicaps from fluctuating too severely.