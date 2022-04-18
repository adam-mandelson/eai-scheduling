###########################################################
#
# Script: data_import.R
# Date: Mon Apr 18 15:15:16 2022
#
# Purpose:
#  - Load data from the database
#  - Initial filters and slight cleanup for shiny
#
###########################################################

# TODO: Update method
config <- read.ini('../config/database.ini')

con <- dbConnect(RPostgres::Postgres(),
                 host = config$postgresql$host,
                 port = config$postgresql$port,
                 dbname = config$postgresql$database,
                 user = config$postgresql$user,
                 password = config$postgresql$password)

res_reports <- dbSendQuery(con, 'SELECT * from pday_reports')
df_reports <- dbFetch(res_reports)
dbClearResult(res_reports)

res_departments <- dbSendQuery(con, 'SELECT * FROM pday_departments')
df_departments <- dbFetch(res_departments)
dbClearResult(res_departments)

res_employees_list <- dbSendQuery(con, 'SELECT * FROM pday_employees_list')
df_employees <- dbFetch(res_employees_list)
dbClearResult(res_employees_list)

dbDisconnect(con)

# DATA HELPER FUNCTIONS ---------------------------------------------------------------
# Add employeename field
df_employees <- df_employees %>%
  mutate(employeename = str_c(firstname, " ", lastname))

# Change data type names
df_reports <- df_reports %>%
  mutate(DataType = str_to_title(str_replace_all(datatypes, '_', ' '))) %>%
  rename(Name = employeename) %>%
  select(-c(datatypes, id)) %>%
  group_by(Name, DataType) %>%
  pivot_wider(names_from=period,
              values_from=value) %>%
  rename(Jan = January,
         Feb = February,
         Mar = March,
         Apr = April,
         Jun = June,
         Jul = July,
         Aug = August,
         Sep = September,
         Oct = October,
         Nov = November,
         Dec = December,
         YTD = ytd,
         Expected_YTD = ytd_contracted,
         `Under/Over` = `under/over`,
         Expected_Full_Year = full_year_contracted)
