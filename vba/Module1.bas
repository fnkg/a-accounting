Attribute VB_Name = "Module1"
Sub AutomateExcelTasks()
    Dim ws As Worksheet
    Dim firstEmptyCol As Integer
    Dim lastRow As Long
    Dim colLetter As String
    Dim i As Integer
    Dim cell As Range
    
    ' Set the worksheet to the currently active sheet
    Set ws = ActiveSheet

    ' Find the first empty column
    firstEmptyCol = ws.Cells(1, ws.Columns.Count).End(xlToLeft).Column + 1

    ' Convert column number to letter for range insertion
    colLetter = Split(Cells(1, firstEmptyCol).Address, "$")(1)
    
    ' Insert six new columns starting from the first empty column
    For i = 0 To 5
        ws.Columns(firstEmptyCol + i).Insert Shift:=xlToRight
    Next i

    ' Get the last row with data in the first column (assumes Column A always has data if any row has data)
    lastRow = ws.Cells(ws.Rows.Count, 1).End(xlUp).Row

    ' Add headers to the new columns
    ws.Cells(1, firstEmptyCol).Value = "id"
    ws.Cells(1, firstEmptyCol + 1).Value = "date"
    ws.Cells(1, firstEmptyCol + 2).Value = "sum"
    ws.Cells(1, firstEmptyCol + 3).Value = "type"
    ws.Cells(1, firstEmptyCol + 4).Value = "store_uuid"
    ws.Cells(1, firstEmptyCol + 5).Value = "company_uuid"

    ' Add formulas to the new columns
    ws.Range(ws.Cells(2, firstEmptyCol), ws.Cells(lastRow, firstEmptyCol)).Formula = "=C2&1" ' Formula for id

    ' Format date and add to new column
    For Each cell In ws.Range(ws.Cells(2, 2), ws.Cells(lastRow, 2)) ' Assuming the original dates are in column B
        If IsDate(cell.Value) Then
            ws.Cells(cell.Row, firstEmptyCol + 1).Value = Format(cell.Value, "yyyymmdd")
        End If
    Next cell

    ws.Range(ws.Cells(2, firstEmptyCol + 2), ws.Cells(lastRow, firstEmptyCol + 2)).Formula = "=E2" ' Formula for sum
    ws.Range(ws.Cells(2, firstEmptyCol + 3), ws.Cells(lastRow, firstEmptyCol + 3)).Formula = "=""online""" ' Formula for type
    ws.Range(ws.Cells(2, firstEmptyCol + 4), ws.Cells(lastRow, firstEmptyCol + 4)).Formula = "=""720b6201-a0c4-11e1-9f3c-001e37ed2a0b"""  ' Formula for store_uuid
    ws.Range(ws.Cells(2, firstEmptyCol + 5), ws.Cells(lastRow, firstEmptyCol + 5)).Formula = "=""4d0460ff-a0cb-11e2-9494-91acf06830ea"""  ' Formula for company_uuid

    ' Autofit the columns to match the content
   ws.Range(ws.Columns(firstEmptyCol), ws.Columns(firstEmptyCol + 5)).AutoFit
End Sub


