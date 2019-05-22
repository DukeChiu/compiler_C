import wx
import os
import wx.stc


class CompilerMain(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title='new1.c', size=(700, 600))
        all_menu = wx.MenuBar()
        run_menu = wx.Menu()
        run = run_menu.Append(wx.ID_ANY, 'run\tCtrl+R', 'Run Code')
        comp = run_menu.Append(wx.ID_ANY, 'compile', 'Compile Code')
        file_menu = wx.Menu()
        fitem_new = file_menu.Append(wx.ID_NEW, 'new', 'New File')
        fitem_open = file_menu.Append(wx.ID_OPEN, 'open', 'Open File')
        fitem_save = file_menu.Append(wx.ID_SAVE, 'save\tCtrl+S', '&ctrl+s')
        self.path_tem = ''
        all_menu.Append(file_menu, '&File')
        all_menu.Append(run_menu, '&Run')
        self.SetMenuBar(all_menu)
        accelTbl = wx.AcceleratorTable([(wx.ACCEL_CTRL, ord('S'), fitem_save.GetId())])
        self.SetAcceleratorTable(accelTbl)
        self.panel = wx.Panel(self)
        self.path = wx.TextCtrl(self.panel, style=wx.TE_READONLY | wx.TE_MULTILINE)
        self.path.SetValue('Console>>\n')
        self.code = wx.stc.StyledTextCtrl(self.panel, style=wx.TE_MULTILINE | wx.TE_RICH2)
        self.code.SetLexer(wx.stc.STC_LEX_CPP)
        self.code.SetKeyWords(1, "class float double char if else if else for while int return")
        self.code.StyleSetSpec(wx.stc.STC_C_WORD2, "fore:#FF8C00")
        self.code.StyleSetSpec(wx.stc.STC_C_COMMENTLINE, "fore:#D8BFD8")
        self.code.StyleSetSpec(wx.stc.STC_C_COMMENT, "fore:#D8BFD8")
        self.code.StyleSetSpec(wx.stc.STC_C_CHARACTER, "fore:#FF00FF")
        self.code.StyleSetSpec(wx.stc.STC_C_STRING, "fore:#FF00FF")
        self.code.StyleSetSpec(wx.stc.STC_C_NUMBER, "fore:#1E90FF")
        self.code.StyleSetSpec(wx.stc.STC_C_IDENTIFIER, "fore:#0000FF")
        self.code.StyleSetSpec(wx.stc.STC_C_TRIPLEVERBATIM, "fore:#0000FF")
        self.Bind(wx.EVT_MENU, self.open_file, fitem_open)
        self.Bind(wx.EVT_MENU, self.save_file, fitem_save)
        self.Bind(wx.EVT_MENU, self.new_file, fitem_new)
        self.Bind(wx.EVT_MENU, self.run, run)
        self.Bind(wx.EVT_MENU, self.comp, comp)
        accelTbl1 = wx.AcceleratorTable([(wx.ACCEL_CTRL, ord('R'), run.GetId())])
        self.SetAcceleratorTable(accelTbl1)
        self.code.SetIndent(4)
        self.code.SetMarginType(1, wx.stc.STC_MARGIN_NUMBER)

        self.InitUI()
        self.Show(True)

    def open_file(self, e):
        wildcard = 'C Source file(*.c)|*.c'
        dlg = wx.FileDialog(self, '选择要打开的文件', '', '', wildcard, style=wx.FD_OPEN)
        # print(wx.ID_OK)
        if dlg.ShowModal() == wx.ID_OK:
            # 按下OK后的逻辑  # 将选择文件的路径输出到fileName里
            self.path_tem = dlg.GetPath()
            # print(self.path_tem)
            file = open(dlg.GetPath(), encoding='UTF-8')  # 以只读打开选中文件
            self.SetTitle(self.path_tem)
            self.code.SetValue('')
            self.code.AppendText(file.read())# 将文件中的文本输出到textEdit里
            # self.code.SetDefaultStyle(wx.TextAttr(wx.WHITE))
            file.close()  # 关闭文件
        dlg.Destroy()  # 关闭对话框

    def on_color(self, e):
        styled_text = ['BFG', 'FYI', 'DPS', 'DSD']
        fulltext = self.code.GetText()
        self.code.StyleSetSpec(2, 'fore:#221dff, back:#FFFFFF,face:Courier New,size:12')
        for item in styled_text:
            pos = fulltext.find(item)
            while pos in range(0, len(fulltext)):
                self.code.StartStyling(pos, 2)
                self.code.SetStyling(len(item), 2)
                pos = fulltext.find(item, pos + 1)

    def InitUI(self):

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        fgs = wx.FlexGridSizer(5, 1, 14, 25)
        fgs.Add(self.code, 1, wx.EXPAND)
        fgs.Add(self.path, 1, wx.EXPAND)

        fgs.AddGrowableRow(0, 0)
        fgs.AddGrowableCol(0, 1)

        hbox.Add(fgs, proportion=1, flag=wx.ALL | wx.EXPAND, border=4)
        self.panel.SetSizer(hbox)

    def save_file(self, e):
        if self.path_tem:
            file = open(self.path_tem, 'w', encoding='UTF-8')  # 打开选中文件，可编辑
            file.write(self.code.GetValue())  # 将textEdit中的文本写入文件
            file.close()  # 关闭文件
        else:
            # wildcard = 'All files(*.*)|*.*'
            fd = wx.FileDialog(self, '把文件保存到何处', '', '.c', 'C Source file(*.c)|*.c', wx.FD_SAVE)
            if fd.ShowModal() == wx.ID_OK:
                file_name = fd.GetFilename()
                dir_name = fd.GetDirectory()
                with open(dir_name + '\\' + file_name, 'w') as new_file:
                    new_file.writelines(self.code.GetValue())

    def new_file(self, e):
        if self.code.GetValue() != '':
            self.save_file(e)
        self.path_tem = ''
        self.SetTitle('new.c')
        self.code.SetValue('')

    def run(self, e):
        pass

    def comp(self, e):
        pass


if __name__ == '__main__':
    app = wx.App(False)
    frame = CompilerMain()
    app.MainLoop()
