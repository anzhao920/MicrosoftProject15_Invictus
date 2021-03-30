# COMP0016_2020-21_Team12_Project15_Saint_Lucia_Fishing_Aggregating_Device

To download the package:
git clone <https://github.com/UCLComputerScience/COMP0016_2020_21_Team12.git>

## Setting up your azure

Please check <https://docs.microsoft.com/en-us/azure/storage/common/storage-account-create?tabs=azure-portal> to set up your azure storage account
Please check <https://docs.microsoft.com/en-us/azure/storage/common/storage-configure-connection-string> to configure your own azure storage account's connection string

## To run the UrlToAzureStorage.py

Please add your storage's connection string in the Dockerfile
In order to download the data from urls to azure storage, please check Main/docs/Deployment of UrlToAzureStorage.pdf
which tells you how to deploy the function.

## To deploy the azure function

In order to deploy the azure function to your azure service, please check Main/docs/Deployment of Azure Funtion.pdf
which tells you how to deploy the function.

## User Performance

User needs to provide the urls of the online datasets, he/she wants to download from. After running, he/she is expected to see the downloaded JSON formatted datasets on his/her Azure Blob Storage

The code can only be run in a docker container!

To understand the system workflow better, please check ./docs/System Workflow

## To download the data from URL

Users need to add his/her own azure storage account connection string to the .env file. And also the user needs to add a container name for hloding all data.

In order to download the wanted data, users need to add the url links behind the variable "filecontent" in UrlToAzureStorage.py

## PWA UI Instruction

Our Progressive Web App (PWA) provides various features to interact with the data in Azure Storage.

![PWAUIImage](https://github.com/UCLComputerScience/COMP0016_2020_21_Team12/blob/datasetsExperimentsAna/Main/docs/homePage.png)

Over the search bar on the top of the UI, you can input a FAD's ID and the system will bring the related data of that particular FAD back to you in the form of table.

Below the search bar there are two main section. If you click on them, they will show all the existing data by either map or table. For the map view, (Plz add some discription about azure map) As for the table view, it will show you all the current data the Azure storage account have, including all the details.

Then at the bottom of the UI, you can also search FAD data according to special searching elements, and the result can be shown by tables or graphs. Detailed explanations shown below. In the results page, you can click "Export" to print the results or save it as PDF file.

Searching elements explanations:
* FAD's Locations:  
    (The FAD records with the same FAD_ID and Location but different data in other aspects will not be shown twice.)
    * Table View - Shows latitude and longitude  
    * Graph View - Shows histogram of distance away from the capital of Saint Lucia

* Country of FADs:  
    (The FAD records with the same FAD_ID and Country but different data in other aspects will not be shown twice.)
    * Table View - Shows which country does the FADs belong to  
    * Graph View - Shows a bar chart and a pie chart for counties distribution

* Depth(m) vs. Temperature(℃):  
    * Table View - Shows the depth and the corresponding temperature for all records. Different FADs will be seperated by black lines  
    * Graph View - Shows a line chart of depth as the X-axis and temperature as the Y-axis

* Depth(m) vs. Salinity:  
    * Table View - Shows the depth and the corresponding salinity for all records. Different FADs will be seperated by black lines  
    * Graph View - Shows a line chart of depth as the X-axis and salinity as the Y-axis
