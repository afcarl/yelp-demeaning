Yelp Star Exchange Rates
===================

Moving to SF from LA, I have experienced a massive Yelp inflation.  For example, Burma Superstar is very much not a 5-star place.  I think a LA equivalent rating is more like 3.5 for Burma Superstar.

Using a standardized place of reference, such as Starbucks, which is equally bad/good/mediocre across locations, here is a simple way to calculate Yelp Star Exchange Rates.

Config file
-----------

Requires a JSON file with Yelp developer credentials

Example
-------

Using
```
get_ratings_in_city('starbucks','San Francisco',hoods_df)
```
the mean StarBucks rating in LA is 3.36 compared to 3.41 in SF.  Not a huge deal but a deal. 
