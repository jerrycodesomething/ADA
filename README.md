# ADA (Algorithm Design and Analysis)
![ADA Banner](https://raw.githubusercontent.com/jerrykingbob/ADA/master/ADA.png)


## Introduction 
This

## Problems 
&nbsp;&nbsp;&nbsp; 
Question two was split into 3 problems. For the first problem, the group interpreted it as a 
minimum Hamiltonian path problem instead of a Travelling Salesman Problem (TSP) variant. 
This was based by making a few assumptions- the first being that “Ben Sherman” is from the 
UK and has only invested in a company in Kuala Lumpur. The question states that Ben must 
start is journey from Kuala Lumpur but that does not mean that he has to return to Kuala 
Lumpur; hence why the question was not interpreted as a TSP problem/ shortest Hamiltonian 
cycle problem. Given that this is a nondeterministic polynomial complete problem, there are 
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
