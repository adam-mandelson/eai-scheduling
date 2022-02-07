Data needed:
    - Employee
    - Shifts
    - Filter shifts by month
    Fields:
        Sick Day:
        - all_shifts:
            - Filter out 'status': 'Open'
            - Join employees_list on all_shifts.employeeId = employees_list.id
                - Add employees_list.firstName, .lastName
            - Join shift_types on all_shifts.shiftTypeId = shift_types.id
                - Filter out 'isActive': false
                - Add shift_types.name
                - Filter by 'name' = 'Sick leave' or 'id' = 19036.
        Holidays
                - Filter by shift_types.name = 'Annual leave' or 'id' = 19045
        Hours worked
            - Filter out shift_types.name = 'Weekend / Evening Supplement' or id = 19046, and 'Annual Leave' or 19045, and 'Sick leave' and 'HOLIDAY'
            - Subtract all_shifts.endDateTime - all_shifts.startDateTime
        Hours counted
            - Subtract all_shifts.endDateTime - all_shifts.startDateTime
        Shifts worked
            - Filter out shift_types.name = 'Weekend / Evening Supplement' or id = 19046, and 'Annual Leave' or 19045, and 'Sick leave' and 'HOLIDAY'
            - Count shifts
        - Shifts counted
            - Count shifts
        - Shifts WFH:
            - Filter by all_shifts.comment = 'WFH'

    - Absences?

Filter by dates
Export to file or google sheets
Run update_all and reports weekly
Deployment
Update document process
