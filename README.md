# What's my vote worth?

Your state's voting power in the electoral college.

[You can find the application hosted on Heroku here.](https://whats-my-vote-worth.herokuapp.com).

## About

Created by: [Oliver K. Ernst](https://oliver-ernst.com) (2020)
Source code: [GitHub](https://github.com/smrfeld/whats-my-vote-worth)

## Explanation

This application allows you to explore what your vote is worth 
in the electoral college system in the United States.
It uses [2010 census data](https://www.census.gov/content/dam/Census/library/publications/2011/dec/c2010br-08.pdf) for the population of each state.

For any given population of the states, the app ultimately computes the vote fraction defined as:

<img style="width: 40%" src="static/vote_frac.png"/>

The first fraction here is the state's share of the electoral college votes:

<img style="width: 20%" src="static/electoral_frac.png"/>

If there were no electoral college, we can view this 
as if each person could vote in the electoral college:

<img style="width: 40%" src="static/limit.png"/>

and the vote fraction would be unity for every state:

<img style="width: 8%" src="static/limit_2.png"/>

In the electoral college system, each state has different vote fractions.
With the 2010 census populations, California has the lowest fraction: 0.84809,
while Wyoming has the highest fraction: 3.03964.
This means that every vote cast in California is worth c.a. 0.27 the vote of a voter in Wyoming,
or equivalently every voter in Wyoming has the power of 3.58 Californians in deciding the U.S. presidential race.

In this application, you can also shift the populations from 
one state to another to explore how the vote fraction changes.
For example, as the c.a. 35 million people in California are redistributed to the other states,
the number of house representatives decreases, such that the electoral college votes decreases,
such that the vote fraction grows - first to unity, and then beyond.

The number of electoral college votes for each state is equal to:
* One for each senator (two for every state).
* One for each **voting** member of the house of representatives (territories and Washington DC only have **non-voting** members). 
        The number of voting representatives is currently fixed at 435.
* Three for Washington DC.

For any given population distribution among the states, 
it remains to determine [how many representatives are assigned to each state.](https://www.everycrsreport.com/reports/R41357.html)
This process is not trivial, using a priority list algorithm implemented in this application:
* Every state (excluding Washington DC) is assigned the mandatory minimum of 1 representative. 
    The total number of representatives assigned is now 50.
* While the total number of voting representatives assigned is less 435 (fixed limit):
    * Calculate a priority for each state:

        <img style="width: 70%" src="static/priority.png"/>
    
        <img style="width: 30%" src="static/geometric_mean.png"/>
    
        where the number of reps assigned refers to the **current** number of reps assigned.
    * Assign the next representative to the state with the highest priority.
    
This calculation is performed every time the population distribution in the application is adjusted.
From this, the electoral votes and the vote fraction are determined.

## Image source 

U.S. map [source](https://commons.wikimedia.org/wiki/File:Blank_US_Map_(states_only).svg) released under [Creative Commons Attribution-Share Alike 3.0 Unported.](https://en.wikipedia.org/wiki/en:Creative_Commons).

## License 

Distributed under MIT License:

Copyright 2020 Oliver K. Ernst

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
    
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
    
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.