###########################################################
#
# Script: utils.R
# Date: Wed Dec 23 13:46:39 2020
#
# Purpose:
#  - load functions and data
#
###########################################################


# FLUID DESIGN FUNCTION ---------------------------------------------------------------

# Design pages with four boxes
fluid_design <- function(id, w, x, y, z) {
  fluidRow(
    div(
      id = id,
      column(
        width = 6,
        uiOutput(w),
        uiOutput(y)
      ),
      column(
        width = 6,
        uiOutput(x),
        uiOutput(z)
      )
    )
  )
}

# DATA HELPER FUNCTIONS ---------------------------------------------------------------

# Function to pull data for datatable output
df.pday_reports <- function(f_data, f_selected_department=NULL, f_employee_name=NULL) {
  if (!is.null(f_selected_department)) {
    f_dept_id <- df_departments %>%
      filter(name %in% f_selected_department) %>%
      select(id)
    
    f_names <- df_employees %>%
      filter(str_detect(departments, as.character(f_dept_id))) %>%
      select(employeename)
  } else if (!is.null(f_employee_name)) {
    f_names <- df_employees %>%
      filter(employeename == f_employee_name)
  }

  df_full <- f_data %>%
    filter(Name %in% f_names$employeename) %>%
    select(Name, DataType, colnames(f_data))
  
  df_view <- df_full %>%
    select(Name, DataType, colnames(f_data)[3:15])
  
  if (!is.null(f_employee_name)) {
    df_full <- df_full %>%
      filter(Name == f_employee_name)
    df_view <- df_view %>%
      filter(Name == f_employee_name)
  }
  
  return(list(df_full, df_view))
}
