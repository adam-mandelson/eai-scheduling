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

visual_box_design_diff <- function(id,
                                   box1, box2) {
  box_width <- 6
  fluidRow(
    div(
      id=box1,
      valueBoxOutput(
        box1,
        width=box_width
      )
    ),
    div(
      id=box2,
      valueBoxOutput(
        box2,
        width=box_width
      )
    )
  )
}

visual_box_design_full <- function(id,
                              box1, box2, box3, box4) {
  box_width <- 3
  fluidRow(
    div(
      id=box1,
      valueBoxOutput(
        box1,
        width=box_width
      )
    ),
    div(
      id=box2,
      valueBoxOutput(
        box2,
        width=box_width
      )
    ),
    div(
      id=box3,
      valueBoxOutput(
        box3,
        width=box_width
      )
    ),
    div(
      id=box4,
      valueBoxOutput(
        box4,
        width=box_width
      )
    )
  )
}

valueBox2 <- function(value, title, subtitle = NULL, icon = NULL, color = "aqua", width = 4, href = NULL){
  
  shinydashboard:::validateColor(color)
  
  if (!is.null(icon))
    shinydashboard:::tagAssert(icon, type = "i")
  
  boxContent <- div(
    class = paste0("small-box bg-", color),
    div(
      class = "inner",
      tags$small(title),
      h3(value),
      p(subtitle)
    ),
    if (!is.null(icon)) div(class = "icon-large", icon)
  )
  
  if (!is.null(href)) 
    boxContent <- a(href = href, boxContent)
  
  div(
    class = if (!is.null(width)) paste0("col-sm-", width), 
    boxContent
  )
}

vbox_helper <- function(person, category, data, box_icon, chosen_month, diff=FALSE) {
  
  chosen_month <- month(fast_strptime(chosen_month, '%m'), label=TRUE, abbr=TRUE)

  value <- data[data$DataType==category, chosen_month]
  
  if (category=='Leave Used') {
    s_leave <- data[data$DataType=='Sick Leave', chosen_month]
    a_leave <- data[data$DataType=='Annual Leave', chosen_month]
    p_leave <- data[data$DataType=='Parental Leave', chosen_month]
    
    value <- s_leave + a_leave + p_leave
  }
  
  if (diff==TRUE) {
    value_diff <- data[data$DataType=='Hours Contracted', chosen_month]
    if (category=='Shifts Worked') {
      value_diff <- value_diff/8
      category <- 'Shifts Worked Over/Under the Number of Workdays in the Month'
    } else {
      category <- paste(category, 'Balance')
    }
    value <- value-value_diff
    if (value > 0) {
      value <- paste0('+', value)
    } else {
      value <- paste0('-', abs(value))
    }
  }
  
  valueBox2(
    value=value,
    title=category,
    icon=icon(box_icon),
    subtitle=chosen_month
    # icon='',
    # color='' # TODO: color dependent on ranking
    # TODO: add league avg
    # TODO: add avg to win
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
    select(Name, DataType, colnames(f_data))
  
  if (!is.null(f_employee_name)) {
    df_full <- df_full %>%
      filter(Name == f_employee_name)
    df_view <- df_view %>%
      filter(Name == f_employee_name)
  }
  
  return(list(df_full, df_view))
}
