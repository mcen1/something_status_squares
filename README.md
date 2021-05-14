# Something Status Squares

Based on the ideas of https://gist.github.com/welsh/9588819

Our organization utilized Server Status Squares to check certain devices at global remote locations to provide insight into the health of the remote sites. The 'Server Status Squares' served us well for quite a while, but it became too unwieldy as we added, removed, and updated new/old sites and the scope creeped like it always does. I thus took it upon myself to rewrite it using Python (since I understand Python much better than Ruby) so that all our remote locations and their devices could be expressed as a JSON file for easier editing by less-technical staff as well as other tweaks to better fit our use-case.

The code allows for monitoring 16 devices per location, but that can be expanded to as much as you want by editing the MAXDB variable in both the statuscheck.py and initdb.py files.

If everything at all sites is up, a message will display at the top indicating everything is ok:
![Alt text](ok.png?raw=true "Everything is ok")

If there are problems at sites, a warning will display at the top with links that will move the browser to the site's anchor:
![Alt text](errors.png?raw=true "Problems")


## Shortcomings compared to Server Status Squares
* Checks are not parallel. Sqlite backend DB can't handle parallel inserts, I think? I'm just a system engineer, not one of them fancy programmers.
* Refreshes browser instead of utilizing AJAX to update squares live.

## Enhancements compared to Server Status Squares for our use-case
* /cgi-bin/api URL holds JSON output of all sites and their check results for easy integrations with other utilities.
* Adding/removing a site only done in one location (powerdash.json file) as opposed to two.
* Automatic alphabetization.
* Summarized results at top allow for Servicedesk-esque people to get at-a-glance synopsis of health of environment.
* Not only ping checks, but also checks via submitting to a web URL and searching for a string in web response to determine device health.
* Erroring squares 'blink' to assist those who may have issues discerning color.


