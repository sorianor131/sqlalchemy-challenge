# sqlalchemy-challenge
Module 10 Homework Assignment - SQLAlchemy Challenge

## Part 1: Analyze and Explore the Climate Data
In this section we were tasked with using Python and SQLAlchemy to do a basic climate analysis and data exploration of the climate database by completeing the following steps:

1. Use the provided files to complete the analysis and data exploration.

2. Use the SQLAlchemy create_engine() function to connect to the SQLite database. 

3. Use the SQLAlchemy automap_base() function to reflect the tables into classes, and then save references to the classes named station and measurement.

4. Link Python to the database by creating a SQLAlchemy session.

### Precipitation Analysis
1. Find the most recent date in the dataset.

2. Using the date, get the previous 12 months of precipitation data.

3. Select only the date and prcp values.

4. Load the query results into a Pandas DataFrame and explicitly set the column names.

5. Sort the DataFrame values by date.

6. Plot the results by using the DataFrame plot method.

7. Use Pandas to print the summary statistics for the precipitation data. 

### Station Analysis
1. Design a query to calculate the total number of stations in the dataset. 

2. Design a query to find the most-active stations.

3. Design a query that calculates the lowest, highest, and average temperature that filters on the most-active station id found in the previous query. 

4. Design a query to get a previous 12 months of temperature observation data. 

## Part 2: Design Your Climate App
For the second part we were tasked with designing a Flask API based on the queries that have been developed. Using Flask we created the following routes:

* /
* /api/v1.0/precipitaion
* /api/v1.0/stations
* /api/v1.0/tobs
* /api/v1.0/<start> and /api/v1.0/<start>/<end>