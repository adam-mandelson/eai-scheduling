###########################################################
#
# Script: ui.R
# Date: Sun Feb 20 14:31:01 2022
#
# Purpose:
#  - Shiny UI
#
###########################################################


# SOURCE LIBARIES, FUNCTIONS ---------------------------------------------------------------
source('global.R')

# SHINY DEBUG OPTIONS ---------------------------------------------------------------
# options(shiny.autoreload = TRUE, shiny.launch.browser = FALSE)

# SHINY UI ---------------------------------------------------------------
ui <- fluidPage(

  # Load custom stylesheet
  includeCSS('static/css/style.css'),
  dashboardPage(
    skin = 'red',

    dashboardHeader(title = 'EAI Planning', titleWidth = 250),
    
    # DASHBOARD SIDEBAR ---------------------------------------------------------------
    dashboardSidebar(
      width = 250,

      # SIDEBAR MENU ---------------------------------------------------------------
      sidebarMenu(
        menuItem(
          text = 'Main Page',
          tabName = 'main_page',
          icon = icon('home')
        ),
        menuItem(
          text = 'Planday Data',
          tabName = 'pday_reports',
          icon = icon('calendar'),
          
          menuItem(
            text = 'Reports by Department',
            tabName = 'pday_dept_reports',
            icon = icon('users')
          ),
          menuItem(
            text = 'Reports by Individual',
            tabName = 'pday_indiv_reports',
            icon = icon('user-plus')
          )
          
        ),
        menuItem(
            text = 'Releases',
            tabName = 'releases',
            icon = icon('tasks')
        ),
        menuItem(
            text = 'Improvements / Bug Fixes',
            tabName = 'updates',
            icon = icon('clock')
        )
      )
    ),

    # DASHBOARD BODY ---------------------------------------------------------------
    dashboardBody(
      tabItems(
        
        # MAIN PAGE ---------------------------------------------------------------
        tabItem(
          tabName = 'main_page',
          includeMarkdown('static/www/home.md'),
          uiOutput('pday.last_update'),
          br(),
          actionButton(
            'pday.data_update.button',
            'Refresh data',
            icon = icon('sync'),
            class = 'butt'
          ),
          # Future versions will feature a 4-box dashboard.
          # fluid_design('main_page_panel', 'box1', 'box2', 'box3', 'box4')
        ),
        
        # PLANDAY REPORTS ---------------------------------------------------------------
        tabItem(
          tabName = 'pday_reports',
          fluidRow(
          )
        ),
        
        # DEPARTMENT REPORTS ---------------------------------------------------------------
        tabItem(
          tabName = 'pday_dept_reports',
          fluidRow(
            div(
              id = 'pday.dept_reports',
              column(
                width=9,
                tags$h3(
                  'Planday Reports',
                  style='text-align: left'
                )
              ),
              column(
                width=3,
                tags$head(
                  tags$style(
                    '.butt{background-color:#230682;} .butt{color: #e6ebef; margin-left: 18px; margin-right: 18px}'
                  )
                ),
                uiOutput('pday.box5.download_button')
              )
            )
          ),
          fluidRow(
            column(
              width=3,
              selectizeInput(
                inputId = 'select.pday_dept',
                label = 'Select a Department:',
                choices = c(Choose = NULL,
                            df_departments$name),
                multiple=FALSE,
                options = list(
                  placeholder='Choose a department',
                  onInitialize = I('function() { this.setValue(""); }')
                )
              )
            )
          ),
          fluidRow(
            column(
              width=12,
              uiOutput('pday.box5.ytd_message')
            )
          ),
          fluidRow(
            tags$head(
              tags$style(HTML(
                '
                                            modal-lg {
                                            width: 800px;
                                            }
                                            '
              ))
            ),
            column(
              width=12,
              uiOutput('pday.box5.reports')
            )
          )
        ),
        
        # INDIVIDUAL REPORTS ---------------------------------------------------------------
        tabItem(
          tabName = 'pday_indiv_reports',
          fluidRow(
            div(
              id = 'pday.indiv_reports',
              column(
                width=9,
                tags$h3(
                  'Planday Reports',
                  style='text-align: left'
                )
              ),
              column(
                width=3,
                tags$head(
                  tags$style(
                    '.butt{background-color:#230682;} .butt{color: #e6ebef; margin-left: 18px; margin-right: 18px}'
                  )
                ),
                uiOutput('pday.box6.download_button')
              )
            )
          ),
          fluidRow(
            column(
              width=3,
              selectizeInput(
                inputId = 'select.pday_person',
                label = 'Select a Person:',
                choices = c(Choose = NULL,
                            df_employees$employeename),
                multiple=FALSE,
                options = list(
                  placeholder='Choose a person',
                  onInitialize = I('function() { this.setValue(""); }')
                )
              )
            ),
            column(
              width=3,
              conditionalPanel(
                condition = "output.pday_select_person != ''",
                tags$div(
                  selectizeInput(
                    inputId = 'select.pday_month',
                    label = 'Select a month to highlight:',
                    choices = c(Choose = NULL,
                                c('January',
                                  'February',
                                  'March',
                                  'April',
                                  'May',
                                  'June',
                                  'July',
                                  'August',
                                  'September',
                                  'October',
                                  'November',
                                  'December')
                    ),
                    multiple=FALSE,
                    options = list(
                      placeholder='Choose a month',
                      onInitialize = I('function() { this.setValue(""); }')
                    )
                  )
                )
              ),
            )
          ),
          fluidRow(
            column(
              width=12,
              uiOutput('pday.box6.ytd_message')
            )
          ),
          fluidRow(
            column(
              width=12,
              uiOutput('pday.box6.curr_month')
            )
          ),
          fluidRow(
            column(
              width=12,
              div(
                id='pday.box6.vbox1',
                visual_box_design_diff(
                  'pday.box6.boxes_curr_diff',
                  'box01', 'box02'
                )
              )
            )
          ),
          fluidRow(
            column(
              width=12,
              div(
                id='pday.box6.vbox2',
                visual_box_design_full(
                  'pday.box6.boxes',
                  'box03', 'box04', 'box05', 'box06'
                )
              )
            )
          ),
          fluidRow(
            tags$head(
              tags$style(HTML(
                '
                                            modal-lg {
                                            width: 800px;
                                            }
                                            '
              ))
            ),
            column(
              width=12,
              uiOutput('pday.box6.reports')
            )
          )
        ),
        
        # RELEASES ---------------------------------------------------------------
        tabItem(
          tabName = 'releases',
          includeMarkdown('static/www/releases.md')
        ),
        
        # UPDATES ---------------------------------------------------------------
        tabItem(
          tabName = 'updates',
          includeMarkdown('static/www/updates.md')
        )
      )
    )
  )
)