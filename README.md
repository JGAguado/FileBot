# FileBot
Telegram based Bot for edit files (copy, move and rename) remotely. 

Steps:
1. The Python script checks if a determined file (according to it's file extension) has been added to a certain folder.
2. New files are added to the log.txt with a "Status".
3. The user is notified via Telegram about the pending files to process and the actions to take.
4. User action is applied.
