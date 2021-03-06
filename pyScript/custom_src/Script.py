from PySide2.QtCore import QObject, Signal

# UI
from ui.w_ui_script import WUIScript

from custom_src.Flow import Flow
from custom_src.Log import Logger
from custom_src.script_variables.VariablesHandler import VariablesHandler
from custom_src.CodePreview_Widget import CodePreview_Widget


class Script(QObject):

    name_changed = Signal(str)

    def __init__(self, main_window, name, config=None):
        super(Script, self).__init__()

        self.main_window = main_window
        self.widget = WUIScript()

        # GENERAL ATTRIBUTES
        self.logger = Logger(self)
        self.variables = []
        self.variables_handler = None
        self.name = name
        self.flow = None
        self.thumbnail_source = ''  # URL to the Script's thumbnail picture
        self.code_preview_txt_edit = CodePreview_Widget()

        if config:
            self.name = config['name']
            self.variables_handler = VariablesHandler(self, config['variables'])
            self.flow = Flow(main_window, self, config['flow'])
            self.variables_handler.flow = self.flow
        else:
            self.flow = Flow(main_window, self)
            self.variables_handler = VariablesHandler(self)
            self.variables_handler.flow = self.flow

        # variables list widget
        self.widget.ui.variables_scrollArea.setWidget(self.variables_handler.list_widget)
        self.widget.ui.add_variable_push_button.clicked.connect(self.add_var_clicked)
        self.widget.ui.new_var_name_lineEdit.returnPressed.connect(self.new_var_line_edit_return_pressed)

        # flow
        self.widget.ui.splitter.insertWidget(0, self.flow)

        # code preview
        self.widget.ui.source_code_groupBox.layout().addWidget(self.code_preview_txt_edit)

        # logs
        self.widget.ui.logs_scrollArea.setWidget(self.logger)
        self.widget.ui.splitter.setSizes([700, 0])


    def show_NI_code(self, ni):
        """Called from Flow when the selection changed."""
        self.code_preview_txt_edit.update_code(ni)

    def add_var_clicked(self):
        self.variables_handler.create_new_var(self.widget.ui.new_var_name_lineEdit.text())

    def new_var_line_edit_return_pressed(self):
        self.variables_handler.create_new_var(self.widget.ui.new_var_name_lineEdit.text())


    def get_json_data(self):
        script_dict = {'name': self.name,
                       'variables': self.variables_handler.get_json_data(),
                       'flow': self.flow.get_json_data()}

        return script_dict