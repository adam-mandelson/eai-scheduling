###########################################################
#
# Script: global.R
# Date: Sun Feb 20 14:28:47 2022
#
# Purpose:
#  - Import packages
#  - Source helper files
#
###########################################################


library(dplyr)
library(DBI)
library(data.table)
library(DT)
library(ini)
library(reticulate)
library(RPostgres)
library(shinycssloaders)
library(shinydashboard)
library(shinyWidgets)
library(stringr)
library(tidyr)

source('static/r/data_import.R')
source('static/r/utils.R')
