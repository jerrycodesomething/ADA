# ADA (Algorithm Design and Analysis)

## Introduction 
&nbsp;&nbsp;&nbsp; For this course’s group assignment project, we decided to choose question 2. 
Question 2 concerns a UK broker looking for industrial investment opportunities in the cities 
of Asia. He already invested in a company in Kuala Lumpur and now he plans to travel to 
several cities in Asia from Kuala Lumpur to expand his investment. The cities include Jakarta, 
Bangkok, Taipei, Hong Kong, Tokyo, Beijing and Seoul. Ben decided to focus more on the 
possibilities of better return of investment in cities which have a positive economy and 
financial growth. So, Ben needs to do some analysis of the local economy and finance 
situation for the last 3 months. Furthermore, he needs to optimise his travel. He will give 
priority to cities with possible better investment return based on the analysis of local 
economic and financial situations. If the next nearest city to be visited has a less better 
economic and financial situation than any of the other cities, Ben will visit another city first 
provided that the difference of distance between the 2 cities is not more than 40% and the 
difference of sentiment analysis between the 2 cities is not less than 2%. 

<br>&nbsp;&nbsp;&nbsp;  
Throughout this project, several algorithms were used; with some being implemented 
or adapted to fit different problem cases. Among them were a couple algorithms not learnt 
in this course. For certain sub-problems, the various problem-solving techniques and 
algorithm implementations taught throughout this WIA2005 Algorithm Design and Analysis 
were adapted and modified to meet the requirements of those problems. In addition to that, 
various external libraries and APIs were used in addition to the native Python libraries to help 
solve the various problems in this project. Workloads were delegated equally among the 5 
group members with

## Problems 
&nbsp;&nbsp;&nbsp; 
Question two was split into 3 problems. For the first problem, the group interpreted it as the 
minimum Hamiltonian path problem instead of a Travelling Salesman Problem (TSP) variant. 
This was based by making a few assumptions- the first being that “Ben Sherman” is from the 
UK and has only invested in a company in Kuala Lumpur. The question states that Ben must 
start is journey from Kuala Lumpur but that does not mean that he has to return to Kuala 
Lumpur; hence why the question was not interpreted as a TSP problem/ shortest Hamiltonian 
cycle problem. Given that this is a Nondeterministic Polynomial complete problem, there are 
no polynomial-time algorithms to solve it so various algorithms and approaches were 
implemented to solve Problem 1. 

<br>&nbsp;&nbsp;&nbsp;
Problem 2 simply required the extraction of words from a text-file to determine the 
financial situation in the respective countries Ben plans to visit. This is done by calculating the 
sentiment ratio of positive words to negative words from 5 articles per city. The rest of 
problem 2 is straightforward and does not hold much bearing on the subsequent problem. A 
string-matching algorithm was needed to count the number of negative, neutral, and positive 
words in each article before plotting the words on a histogram.

<br>&nbsp;&nbsp;&nbsp;
Problem 3 was a bit more confusing as we were unsure on how to interpret the 
probability distribution part as all the routes possible are finite and not random. Because of 
this, we decided to spread out all the possible routes and rank them according to how closely 
the routes matches with the most optimal route after calculating it based on the difference 
of distance between two cities and the sentiment analysis between to cities between each 
layover. With the number of matches spread across a frequency distribution table, the routes 
were then ranked from the least recommended to the most recommended.
