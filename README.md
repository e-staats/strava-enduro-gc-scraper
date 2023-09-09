# What Is This?

This is a tool that uses an automated browser to collect all the times for a set of Strava segments completed _today_, then adds up the times and outputs the results. It is intended to simplify the scoring process for an event like and Enduro, where the goal is to collect the lowest time over a variety of segments on the day.

## How to Use

Firstly, this is an automated browser, so please make sure to use it responsibly. It logs in to your own account, so what you do will be tied back to you.

### Usage

1. Create a virtual environment, activate it, and install `requirements.txt`
1. Rename `secrets_template.py` to `my_secrets.py`
1. Replace the email and password in the environment variables definitions of `my_secrets.py` with your username and password.
1. Create a .txt file called whatever you want and start pasting in Strava segment IDs, one per line. You can put comments after a `#` to note what the names of the segments are.
   1. You get the Strava segments by looking at the URL of the segment page. For example, for the UW Arboretum Northbound segment is at `https://www.strava.com/segments/704038`, so the segment ID is `704038`
   1. For example, you could have a file called `weekly_shop_ride_sprints.txt` and it would look like this:
   ```
   29713412  # Rutland-Dunn Kicker
   7321846  # Sun Valley - Only Up
   10768746  # Krooked Tree Sprint
   704038  # UW Arboretum Northbound
   ```
1. Run the tool with `python cli.py [OPTIONS]`. Run `python cli.py --help` to get help information about the options. Examples:
   1. `python cli.py -s ./my_segment_list.txt` to run the scraper on a list of segments
   1. `python cli.py -c` to use the cached data
1. Check the `/printouts` folder for the output.

### Interpreting the output

In the `/printouts` folder, there's one file per segment, and also a `raw_seconds.csv` that can be useful for validating the math. Each file contains the information for all the segments, which I admit is a little odd, but each segment's file is pre-sorted by that segment's times. If you're doing prizes for the top time on each segment, it's convenient to have this on each file instead of sorting the same file on a different columns every time. It is weird though, and maybe this will change in the future.

## It keeps failing to hit the next page, or some other issue

Such is life as an automated browser. It has to wait for a bunch of Javascript to load, then find the right button, then click it, and if the timing gets messed up on any of that, it will fail. You can try again, and if it consistently fails, you may need to adjust the sleep times in the scraper.

## Automated browser scraping? Really?

Yeah...If Strava would make this information accessible through the API, this would be much easier and better, but they took away segment leaderboards from the API a few years ago. If they bring it back, I'll update this to use that.
