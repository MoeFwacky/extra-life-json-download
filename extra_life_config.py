TeamID=51280 #ENTER YOUR TEAM ID NUMBER HERE
rateLimit=15 #API Rate Limit in Seconds

#define data files
teamFile="teamData.json"
teamParticipantsFile="teamParticipantsData.json"
teamDonationsFile="teamDonations.json"

#Define URL Strings
team="https://www.extra-life.org/api/teams/"+str(TeamID)+"?version=1.0&"
teamParticipants="https://www.extra-life.org/api/teams/"+str(TeamID)+"/participants?version=1.0&"
teamDonations="https://www.extra-life.org/api/teams/"+str(TeamID)+"/donations?version=1.0&"