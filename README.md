setdb - choose or create the database file. usage: setdb <path to file>

addscope - add comma seperated(no spaces) list to scope (wildcards allowed). usage: addscope *.example.com,*.google.com

setquery - setquery sets query to results of "SELECT <column> FROM <tablename> WHERE <column> LIKE %<string>%"
           usage: setquery <column> <tablename> <column> [<string>] (<string> is optional)

show - shows the results of the current query.

findsubdomains - run sublister on the set query.

masscan - run masscan on set query.

dirb - run dirb on set query.

crlfscan - run a crlf injection test on set query.

burp - request all items in set query through a proxy 127.0.0.1:8080

help - this screen

exit - close BBF
