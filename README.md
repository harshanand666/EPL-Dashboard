# EPL-Dashboard
A dash based interactive dashboard to analyse the English Premier League between 2000 and 2022

## Overview
This dashboard visualizes various stats for the English Premier League between 2000 and 2022. 
The dataset used can be found here - https://www.kaggle.com/datasets/quadeer15sh/premier-league-standings-11-seasons-20102021?resource=download, and has also been included in the data folder above.

The dashboard has an upload button where the csv file must be uploaded. The user then has the option to choose start/end season for which the data needs to be analysed.
[![Screenshot-2022-11-23-at-2-44-42-AM.png](https://i.postimg.cc/jCVZ4scN/Screenshot-2022-11-23-at-2-44-42-AM.png)](https://postimg.cc/RJR7MxjV)

There are 3 tabs:
1. __Overview Tab__

   This tab has overall data on number of trophies, relegations, top 4 finishes, etc.
   
[![Screenshot-2022-11-23-at-2-45-24-AM.png](https://i.postimg.cc/cJ4ynmrW/Screenshot-2022-11-23-at-2-45-24-AM.png)](https://postimg.cc/nX5P8q4S)

2. __Club stats Tab__

   This tab has a dropdown from which the user can select a specific club which they want to analyze. Multiple graphs are plotted regarding season-wise position, goals, points, etc. along with some text stats.
   
[![Screenshot-2022-11-23-at-2-46-07-AM.png](https://i.postimg.cc/dtKfCBxf/Screenshot-2022-11-23-at-2-46-07-AM.png)](https://postimg.cc/fkB5nxZ7)

3. __Comparsion Tab__

   This tab has 2 dropdowns from which the user can select 2 clubs which they want to compare. Similar to the club stats tab, multiple graphs and text stats are generated.
   
[![Screenshot-2022-11-23-at-2-47-02-AM.png](https://i.postimg.cc/wTHWMBt8/Screenshot-2022-11-23-at-2-47-02-AM.png)](https://postimg.cc/HjZ0Pd4B)

## Usage
To use this dashboard, only the provided CSV needs to be uploaded. The code is separated into tab-wise files and can be easily modified to add further graphs or tabs. 
