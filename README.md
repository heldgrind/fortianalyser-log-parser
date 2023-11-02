# README
This script simplifies log parsing from Fortigate and Fortianalyzer by keeping a hitcount on duplicate entries and only display one. This minimize the output from the logs. The output could be written to an Excel sheet that could be used for further analyzing the logs. If you want to add/remove columns, change the `FIELDS` variable. 

- Files downloaded from Fortigate will come in `.log` format
- Files downloaded from Fortianalyzer will come in `.csv` format

When `.log` is used, the script will convert the files to the same format as when downloaded from the Fortianalyzer. Therefor an additional `.csv` file will be created in the working directory.

The script operates in the CMD, execute `-h` to display help screen.
![Alt text](image.png)

Example on output written to excel file
![Alt text](image-1.png)

Example on output written to the prompt
![Alt text](image-2.png)