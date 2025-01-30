<h1 align='center' style="text-align:center; font-weight:bold; font-size:2.5em"> Detecting key factors influencing job applications on linkedin
 </h1>

<p align='center' style="text-align:center;font-size:1em;">
    <a href="https://github.com/bar256">Bar Oren</a>&nbsp;,&nbsp;
    <a href="https://github.com/sivanmaspin">Sivan Maspin</a>&nbsp;,&nbsp;
    <a>Yuval Rains</a>&nbsp;,&nbsp;
    <br/> 
    Technion - Israel Institute of Technology


<br>
<br>

<p align="center">
  <img src="Assets/Icon.png" alt="Logo" width="1000" height="400">



# Contents
- [Overview](#Overview)
- [Install](#install)
- [Running the code](#Running-the-code)
- [special mentions and details](#special-mentions-and-details)

  
# Overview

this code was created to help recruiters write more attractive job listings on Linkedin.
we have gathered and analyzed 20,000 job postings using this scraping method, and with combination of data supplied by outside sources were able to predict normalized job listings performance.
you can use the code to gather data and fit your own models, or use the tips we reached as can be seen in the poster.
 

# Install

#### To run the data analysis you will need a strong pyspark enabled environment. we used Microsoft DataBricks.

to get the code all you need to do is clone this repository


# Running the code

getting job postings from Linkedin:
<br>
the "scraping.py" has a linkedin_jobs_url variable. place a search url you want to scrape in the variable and run the code.
<br>
the code works in batches in case there is a sudden stoping in scraping. it will create a file for each 100 job postings and consolidate all files by the end.
<br>
after scraping a wanted search term you can move  the files to a different location and do another search.
<br>
use json cleaner.py to cosolidate all json files to one table.

getting compy details:
<br>
we have used a closed source data set from BrightData website.
<br>
the data is avalible for purchase in the companys website.

data analysis:
upload the data analysis notebook.ipynb file to a Pyspark enabled environment
<br>
upload scraped and purchased data to your environment and update the paths in:
<br>
companies = spark.read.parquet('/dbfs/linkedin_train_data')
<br>
and in:
<br>
file_location = "dbfs:/user/hive/warehouse/syb2"
<br>
run all the notebook. by the end you will get a model that can predict job applicants based on title and description under the "model" paremeter.


# special mentions and details
this code was written during the course "Data Gathering and Management Lab" in the Technion.
<br>
the finished product was this code and a poster:
<p align="center">
  <img src="Assets/poster.jpeg" alt="poster" width="600" height="800">


