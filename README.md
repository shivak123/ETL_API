# ETL_API

1.In this Project our aim is to extract the data from API - public API

2.Then ingest the data into a MySql server and perform full load and inc load based on the flag 


## API USED : https://polygon.io/docs/stocks/get_v2_reference_news  --- One Endpoint which gives the most recent news articles relating to a stock ticker symbol, including a summary of the article and a link to the original source.

## Handling full and inc load 

<br> 1. We have one date column in the data we have extracted which is Published_utc. which Return results published on, before, or after this date. So we have utilized this as our lastmodified date column for our full and inc load 

<br> 2. Case 1:  Initial_load in our function by default set to False which means its a full load. And when our published_utc = '1900:01:01' 

<br> 3. Case 2 : when the flag is set to False. the fucntion will take the data from yesterday as our inc load 

![image](https://user-images.githubusercontent.com/19462859/183293767-15a77b90-0644-43d1-8893-a56becad3b7c.png)

##Note :As shown in the above snippet we need to change the flag to True for full and to False for Inc load to happen 


<br> 4. Once the table is created with the required fields and during the initial or full load we inserting the records into the table.

<br> 5. During the inc load that is assume we are doing the inc load the very next day . then the fucntion will take only those records which are created and after that we are deleteing those id which are already in our final table to handle the updates and then we are inserting the data into the table 


## MySQL Table OUTPUT :

![image](https://user-images.githubusercontent.com/19462859/183294252-6f734848-a710-466b-aa4c-4003c9c10cda.png)



## steps to Installing Mysql server 

<br>1. Open up a browser and go to: http://dev.mysql.com/downloads/mysql/
<br>2. Scroll to the list of available downloads. Click the 'Download' button next to the applicable download.
<br>3.Windows 64 bit - Windows (x86, 64-bit), MSI
<br>4.Windows 32 bit - Windows (x86, 32-bit), MSI
<br>5.If you are unsure, assume you are on a 32 bit machine.
<br>6.To begin the download, you must either login using pre-existing credentials by clicking the 'Proceed' button under the New Users section or click the 'No thanks, just start my download' link at the bottom of the screen.
<br>7.Save the file to your desktop.
<br>8.Double click the file.
<br>9.On the Welcome screen click 'Next'.
<br>10.Accept the terms in the license agreement and click 'Next'.
<br>11.When presented with a list of available Setup Types, Select 'Typical'.
<br>12.When ready to install, click 'Install'.
<br>13.If a system message pops up asking if you want the software to be installed on your machine, click 'Yes'.
<br>14.If a MySQL enterprise pop up window appears, click 'Next' until it disappears.
<br>15.When the Setup Wizard has completed, Click 'Finish'.
<br>16.If you receive another pop up message asking if you want the software to be installed on your machine, click 'Yes'.
<br>17.When the Server Instance Configuration Wizard displays, Click 'Next'.
<br>18.When displayed the available Server Instance Configuration types select 'Standard Configuration' and click 'Next'.
<br>19.When on the Windows Options scree, keep 'Install as a Service' selected as well as 'Launch the MySQL Server automatically'. Select the 'Include Bin Directory in Windows PATH' option and select 'Next'.
<br>20.On the Security Options scree, specify a new root password and select 'Next'. Remember this password as it will be needed later!
<br>21.When the Ready to Execute screen displays, click 'Execute'.
<br>22.After all the Configuration steps have successfully run, Click 'Finish'.
<br>23.You have successfully installed MySQL.
