# Documentation

------------------------------------------------------------------------

## Architecture decisions:

As this was a small scale project where I was not attempting to have a
particularly secure or extensive backend, a lot of my decisions were
more based around familiarity and documentation rather than

-   I used the framework Django (and hence the language python) as a
    backend framework for this project. This is because:
    -   I have had more practice with Django than a lot of other backend
        frameworks.
    -   I know Django is still a very commonly used framework in
        industry.
    -   Django being open source and very widely used in industry means
        it has great documentation.
-   I decided to use Data Import Wizard to input the data files into a
    simple database instead of just using the .csv file directly. This
    is because:
    -   Parsing fields in the file to fields in the serializer is done
        automatically in Data Import Wizard.
    -   Testing validators with Data Import Wizard is more effective as
        it provides well described error messages for why an object was
        not added.
    -   It is easier to handle large data-bases than files, especially
        for sorting and searching.
-   I used Chart.js for displaying some simple bar and line graphs. This
    is because:
    -   Chart.js is the current most popular charting library according
        to {1}.
    -   It is well documented and has easily implemented default config
        files, which only needs a few tweaks to be functional.
    -   Clean UI and animations.

------------------------------------------------------------------------

## Data Handling:

I will explain choices for how I handled data and data inconsistencies.

-   Duplicates
    -   As discussed with you, I only had to implement validators for 
        duplicates at the same time and location. I used the Django 
        constraints to make a unique constraint that fit this criteria,
        and Data Import Wizard will detect and throw sensible errors if
        the constraints are violated.
-   Invalid parameters
    -   One of the advantages of Data Import Wizard is if an imported 
        record has invalid fields, it will give me a message, and 
        import the rest of the records.
-   Data Import Wizard is made to handle and process large datasets. It
    does this in several ways, other than the ones I mentioned before:
    -   It performs the actual imports using Celery, which is a
        'distributed task queue that processes asynchronously' {2},
        which is supposed to keep the application responsive during
        large imports.
    -   It works with Django's validators, which validate the data on
        import. It also does not crash when one record is not imported,
        instead blocking just that record.
    -   It has a viewer where you can look at the records in the
        database for easy testing and

------------------------------------------------------------------------

## Endpoints:

I will briefly describe each endpoint, why I gave it specific parameters
and give an example that will return sensible data. All of these pages
use very basic HTML to make it more readable, instead of just returning
raw data (except test/ticks/).

### `/api/tests/ticks/`

-   This is a test for me to see if data has been uploaded correctly.
-   Returns the raw json data of all ticks.

### `/api/tick-sightings/time/{datetime:from?}{datetime:to?}`

-   This returns all tick sightings between the query parameters 'from'
    and 'to'.
-   I made these query parameters so it could default 'from' or 'to' if
    not specified.
-   If 'from' isn't found, it returns all values from the earliest to
    'to'.
-   If 'to' isn't found, it returns all values to the earliest to
    'from'.
-   Hence, if neither are found it will return all ticks from first
    sighting to last sighting.

### `/api/tick-sightings/location/<str:location>/{str:species?}`

-   This returns all the sightings of ticks in the location and can be
    filtered by the query parameter species.
-   If species isn't specified, it returns all ticks in location
-   I made location a path parameter instead of a query parameter as
    without a specific location endpoint doesn't make sense (returning
    all should be a different endpoint).

### `/api/statistics/trends/monthly/{datetime:from?}{datetime:to?}{str:species?}{str:location?}`

-   This returns a page containing a line graph, where x is the set of
    valid months and y is the number of ticks that month.
-   Uses chart.js to create the graph.
-   If given a 'from' parameter, it returns entries past the 'from'
    datetime. Defaults to the earliest sighting if not (of all ticks,
    not valid ticks).
-   If given a 'to' parameter, it returns entries up to the 'to'
    datetime. Defaults to the latest sighting if not (of all ticks, not
    valid ticks).
-   If given a 'location' parameter, it returns entries with the same
    location. If not given, it returns all locations of ticks.
-   If given a 'species' parameter, it returns entries with the same
    species. If not given, it returns all species of ticks.

### `/api/statistics/sightings-per-region/{str:species?}`

-   This returns a page containing a bar chart, where x is the set of
    all locations in the database and y is the number of ticks at that
    location.
-   If given a 'species' parameter, it returns entries with the same
    species. If not given, it returns all species of ticks.

------------------------------------------------------------------------

## Error Handling:

I will explain what measures I took to hankle errors by the user and the 
server.

### Api failures:

-   I created a custom 404 error page that you are taken to if you enter 
    the url incorrectly or provide an invalid error. The page states what 
    went wrong and lists hyperlinks to all valid url paths. 

### Data inconsistencies:

-   I set validators so only dates up to present can be imported into the 
    database.
-   Every field except latin-name in the TickModel has null and blank set
    to true, because they are used to filter the data and must not be 
    missing.

------------------------------------------------------------------------

## Problems, Fixes and Improvements:

I have noted down some of the problems I had that I fixed, some that I
didn't and what I would do if I had more time.

### Problems:

a.  I hardcoded the 404 error page hyperlinks to the other endpoints.
    This is definitely not ideal, as every new page would need you to
    add a new hyperlink to the HTML page.

b.  When getting all months from the data set, I originally had a
    function that looked at every new month in the appropriate range.
    This did not span across years however, so if the range was
    01/01/2024 - 01/01/2024, January would only appear once and data
    from both years would be combined.

c.  When getting all months within the dataset, I originally added any
    new month in the valid set of ticks, e.g. the only months returned
    are the months that a tick had been sighted. This meant that the set
    of months (and hence the x axis) might be \['January', 'February',
    'April' ...\] if there was no tick sighting in March.

### Fixes:

b.  I used a list of strings where the month and year are separated by a
    ',' and then split them later when iterating through them. Now every
    month had a year to go with it, and the data spanning years of the
    same month didn't sum together.

c.  I used the dateutil.rrule function to get all months between the
    start and end times. Now every month in the range showed even if
    there were no tick sightings that month.

### Improvements:

a.  If I had more time and this was actually going to be implemented
    with HTML pages, I would make a list of all url endpoints and create
    hyperlinks for them all. This way if a new url endpoint was added it
    would not change the 404 page.

### Further improvements:

-   If I had more time and was more experienced using AI/ML to actually
    find trends in the data, I would probably try to find links between
    specific months and the number of tick sightings and the general
    gradient of tick numbers over the whole dataset to predict future
    values.
-   I haven't used chart.js before, so I do not currently know how to
    create graphs with varying numbers of datasets. If I had more time,
    I would have used chart.js to create a graph with the trends of tick
    numbers over time with different lines for different species. This
    way you could see on one graph which species have different trends
    at the same time, instead of on separate HTML pages.
-   I would make my HTML pages more user friendly and clean. The pages I
    made are functional and readable but ugly and poorly formatted.
-   As I have used a database, the project should have a way to add new
    entries to the database.

------------------------------------------------------------------------

## Sources:

{1} https://github.com/chartjs/Chart.js\
{2}
https://realpython.com/asynchronous-tasks-with-django-and-celery/#:\~:text=Celery%20is%20a%20distributed%20task,tasks%2C%20ensuring%20smooth%20user%20experiences.
