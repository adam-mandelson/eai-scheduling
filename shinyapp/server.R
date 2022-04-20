###########################################################
#
# Script: server.R
# Date: Sun Feb 20 14:51:58 2022
#
# Purpose:
#  - Shiny server script
#
###########################################################



# SHINY SERVER ---------------------------------------------------------------
server <- function(input, output, session) {
  
  # TODO: MAIN PAGE BOXES IN FUTURE VERSIONS
  
  # MAIN PAGE ---------------------------------------------------------------
  filePath <- '../pday/last_update.txt'
  lastUpdate <- reactiveFileReader(1000, session, filePath, readLines)
  output$pday.last_update <- renderText({
    lastUpdate()
  })

  # MAIN PAGE  - BOX1 ---------------------------------------------------------------
  # output$box1 <- renderUI({
  #   div(
  #     style = "position: relative",
  #     box(
  #       id = "box1",
  #       width = NULL,
  #       height = 400,
  #       includeMarkdown("static/www/updates.md")
  #     )
  #   )
  # })
  # 
  # # MAIN PAGE  - BOX2 ---------------------------------------------------------------
  # output$box2 <- renderUI({
  #   div(
  #     style = "position: relative",
  #     box(
  #       id = "box2",
  #       width = NULL,
  #       height = 400,
  #       tags$h2("This is box 2")
  #     ),
  #   )
  # })
  # 
  # # MAIN PAGE  - BOX3 ---------------------------------------------------------------
  # output$box3 <- renderUI({
  #   div(
  #     style = "position: relative",
  #     box(
  #       id = "box3",
  #       width = NULL,
  #       height = 400,
  #       tags$h2("This is box 3")
  #     )
  #   )
  # })
  # 
  # # MAIN PAGE  - BOX4 ---------------------------------------------------------------
  # output$box4 <- renderUI({
  #   div(
  #     style = "position: relative",
  #     box(
  #       id = "box4",
  #       width = NULL,
  #       height = 400,
  #       tags$h2("This is box 4")
  #     )
  #   )
  # })
  
  # PDay REPORTS - BOX5 ---------------------------------------------------------------
  # Download button
  output$pday.box5.download_button <- renderUI({
    shiny::validate(
      need(input$select.pday_dept, message = FALSE)
    )
    downloadButton("pday.box5.report_csv",
                   "Download to CSV",
                   class="butt")
  })
  
  # YTD_MESSAGE
  output$pday.box5.ytd_message <- renderUI({
    shiny::validate(
      need(input$select.pday_dept, message = FALSE)
    )
    tags$p('Note: YTD is through the previous month')
  })
  
  # UI output for the datatable
  output$pday.box5.reports <- renderUI({
    shiny::validate(
      need(input$select.pday_dept, message = "Please choose a department to display the table.")
    )
    DT::dataTableOutput("box5_reports_datatable")
  })
  
  # Reactive value that calls df.pday_reports function to filter data
  box5.df_reports <- reactive({
    df.pday_reports(
      f_data = df_reports,
      f_selected_department = input$select.pday_dept
    )
  })
  
  # Datatable
  output$box5_reports_datatable <- DT::renderDataTable({
    # Item 2 is the view report
    df <- box5.df_reports()[[2]]
    
    datatable(
      data = df,
      selection="single",
      rownames=FALSE,
      extensions = 'RowGroup',
      options = list(
        rowGroup = list(
          dataSrc=0
        ),
        paging=FALSE,
        dom='t',
        rowCallback = JS("function(r,d) {$(r).attr('height', '10px')}"),
        autoWidth=TRUE
      ),
      escape = FALSE
    )
  })
  
  # Report download handler
  output$pday.box5.report_csv <- downloadHandler(
    filename = function() {
      paste("monthly_report", Sys.Date(), ".csv", sep="")
    },
    # Item 1 is the full report
    content = function(file) {
      write.csv(data.frame(box5.df_reports()[[1]]), file, row.names = FALSE)
    }
  )
  
  # PDay REPORTS - BOX6 ---------------------------------------------------------------
  # Download button
  output$pday.box6.download_button <- renderUI({
    shiny::validate(
      need(input$select.pday_person, message = FALSE)
    )
    downloadButton("pday.box6.report_csv",
                   "Download to CSV",
                   class="butt")
  })
  
  
  output$pday_select_person <- reactive({
    input$select.pday_person
  })
  
  outputOptions(output, 'pday_select_person', suspendWhenHidden = FALSE)
  
  output$pday_select_month <- reactive({
    input$select.pday_month
  })
  
  # YTD_MESSAGE
  output$pday.box6.ytd_message <- renderUI({
    shiny::validate(
      need(input$select.pday_person, message = FALSE)
    )
    tags$p('Note: YTD is through the previous month')
  })
  
  # UI output for the datatable
  output$pday.box6.reports <- renderUI({
    shiny::validate(
      need(input$select.pday_person, message = "Please choose a person to display the table.")
    )
    DT::dataTableOutput("box6_reports_datatable")
  })
  
  # Reactive value that calls df.pday_reports function to filter data
  box6.df_reports <- reactive({
    df.pday_reports(
      f_data = df_reports,
      f_employee_name = input$select.pday_person
    )
  })
  
  current_month <- month(Sys.Date(), label=TRUE, abbr=FALSE)
  
  # Valueboxes for current month
  output$pday.box6.curr_month <- renderUI({
    shiny::validate(
      need(input$select.pday_month, message = FALSE)
    )
    tags$h3(input$select.pday_month)
  })
  
  output$box01 <- renderValueBox({
    shiny::validate(
      need(input$select.pday_month, message=FALSE))
    vbox_helper(person=input$select.pday_person,
                category='Hours Counted',
                data=box6.df_reports()[[2]],
                box_icon='plus',
                chosen_month=input$select.pday_month,
                diff=TRUE
    )
  })
  
  output$box02 <- renderValueBox({
    shiny::validate(
      need(input$select.pday_month, message=FALSE))
    vbox_helper(person=input$select.pday_person,
                category='Shifts Worked',
                data=box6.df_reports()[[2]],
                box_icon='plus',
                chosen_month=input$select.pday_month,
                diff=TRUE
    )
  })
  
  output$box03 <- renderValueBox({
    shiny::validate(
      need(input$select.pday_month, message=FALSE))
    vbox_helper(person=input$select.pday_person,
                category='Hours Worked',
                data=box6.df_reports()[[2]],
                box_icon='clock',
                chosen_month=input$select.pday_month
    )
  })
  
  output$box04 <- renderValueBox({
    shiny::validate(
      need(input$select.pday_month, message=FALSE))
    vbox_helper(person=input$select.pday_person,
                category='Hours Counted',
                data=box6.df_reports()[[2]],
                box_icon='clock',
                chosen_month=input$select.pday_month
    )
  })
  
  output$box05 <- renderValueBox({
    shiny::validate(
      need(input$select.pday_month, message=FALSE))
    vbox_helper(person=input$select.pday_person,
                category='Leave Used',
                data=box6.df_reports()[[2]],
                box_icon='calendar',
                chosen_month=input$select.pday_month
    )
  })
  
  output$box06 <- renderValueBox({
    shiny::validate(
      need(input$select.pday_month, message=FALSE))
    vbox_helper(person=input$select.pday_person,
                category='Shifts Worked',
                data=box6.df_reports()[[2]],
                box_icon='calendar',
                chosen_month=input$select.pday_month
    )
  })
  
  
  # Datatable
  output$box6_reports_datatable <- DT::renderDataTable({
    # Item 2 is the view report
    df <- box6.df_reports()[[2]]
    
    datatable(
      data = df,
      selection="single",
      rownames=FALSE,
      extensions = 'RowGroup',
      options = list(
        rowGroup = list(
          dataSrc=0
        ),
        paging=FALSE,
        dom='t',
        rowCallback = JS("function(r,d) {$(r).attr('height', '10px')}"),
        autoWidth=TRUE
      ),
      escape = FALSE
    )
  })
  
  # Report download handler
  output$pday.box6.report_csv <- downloadHandler(
    filename = function() {
      paste("monthly_report", Sys.Date(), ".csv", sep="")
    },
    # Item 1 is the full report
    content = function(file) {
      write.csv(data.frame(box6.df_reports()[[1]]), file, row.names = FALSE)
    }
  )
  
  # PDAY.UPDATE_DATA ---------------------------------------------------------------
  observeEvent(input$pday.data_update.button, {
    setwd('../')
    use_virtualenv('./.env')
    py_run_file('./pday/update_data.py', convert=FALSE)
    shinyalert::shinyalert(title='Data updated', type='success')
    setwd('./shinyapp')
  })
  
}