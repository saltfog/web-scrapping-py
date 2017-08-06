# -------------------------------------------------------------------------------
# Name:        webscrapper for BC
# Purpose:
#
# Author:      casey.jenkins
#
# Created:     26/10/2012
# Copyright:   (c) casey.jenkins 2012
# Licence:     <your licence>
# -------------------------------------------------------------------------------

import urllib, re

url = "http://api.wunderground.com/weatherstation/WXCurrentObXML.asp?ID=KIDGRACE5"

webpage = urllib.urlopen(url).read()

match = re.search("<observation_time_rfc822>([^<]*)</observation_time_rfc822>", webpage)
time = match.group(1)

match = re.search("<temperature_string>([^<]*)</temperature_string>", webpage)
temp = match.group(1)

match = re.search("<wind_string>([^<]*)</wind_string>", webpage)
wind = match.group(1)

match = re.search("<relative_humidity>([^<]*)</relative_humidity>", webpage)
rh = match.group(1)

print "         Temperature", temp
print "         Wind", wind
print "         RH", rh, "%"
print "         Time", time
