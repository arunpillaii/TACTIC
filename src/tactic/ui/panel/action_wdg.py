###########################################################
#
# Copyright (c) 2005, Southpaw Technology
#                     All Rights Reserved
#
# PROPRIETARY INFORMATION.  This software is proprietary to
# Southpaw Technology, and is not to be reproduced, transmitted,
# or disclosed in any way without written permission.
#
#
#
__all__ = ["TableActionWdg", "ViewActionWdg"]

from pyasm.common import Xml
from pyasm.web import Widget, DivWdg, HtmlElement, SpanWdg, WebContainer, Table
from pyasm.widget import SelectWdg, FilterSelectWdg, WidgetConfig, HiddenWdg, IconWdg


from tactic.ui.common import BaseRefreshWdg


class TableActionWdg(Widget):
    def __init__(self, **kwargs):
        # get the them from cgi
        self.handle_args(kwargs)
        self.target_id = kwargs.get("target_id")

        # FIXME: this is very tenous!!!
        self.table_id = "%s_table" % self.target_id

    #
    # Define a standard format for widgets
    #
    # Get it from web_form_values()
    def get_args_keys(self):
        '''external settings which populate the widget'''
        return {
        'target_id': 'Dom element target to replace the views',
        }

    def handle_args(self, kwargs):
        # verify the args
        args_keys = self.get_args_keys()
        for key in kwargs.keys():
            if key not in args_keys:
                raise WidgetException("Key [%s] not in accepted arguments" % key)

        web = WebContainer.get_web()
        args_keys = self.get_args_keys()
        for key in args_keys.keys():
            if key not in kwargs:
                value = web.get_form_value(key)
                kwargs[key] = value




    def get_display(self):

        # add a view action
        view_div = DivWdg()
        view_select = SelectWdg("action|table")
        view_select.add_style("text-align: right")
        view_select.add_empty_option("-- items --")
        view_select.set_option("values", "add|edit|retire|delete|export_all|export_selected")
        view_select.set_option("labels", "Add New Item|X Edit Selected|Retire Selected|Delete Selected|X CSV Export (all)|X CSV Export (selected)")
        view_div.add_style("float: right")
        view_div.add(view_select)

        #view_select.add_event("onchange", "spt.dg_table.retire_selected_cbk('%s')" % self.target_id)
        view_select.add_event("onchange", "spt.dg_table.table_action_cbk(this,'%s')" % self.table_id )

        return view_div


class ViewActionWdg(Widget):
    def __init__(self, **kwargs):
        # get the them from cgi
        self.handle_args(kwargs)
        self.target_id = kwargs.get("target_id")

        # FIXME: this is very tenous!!!
        self.table_id = "%s_table" % self.target_id

    #
    # Define a standard format for widgets
    #
    # Get it from web_form_values()
    def get_args_keys(self):
        '''external settings which populate the widget'''
        return {
        'target_id': 'Dom element target to replace the views',
        }

    def handle_args(self, kwargs):
        # verify the args
        args_keys = self.get_args_keys()
        for key in kwargs.keys():
            if key not in args_keys:
                raise WidgetException("Key [%s] not in accepted arguments" % key)

        web = WebContainer.get_web()
        args_keys = self.get_args_keys()
        for key in args_keys.keys():
            if key not in kwargs:
                value = web.get_form_value(key)
                kwargs[key] = value




    def get_display(self):
        # add a view action
        view_div = DivWdg()
        view_select = SelectWdg("action|view_action")
        view_select.add_style("text-align: right")
        view_select.add_empty_option("-- view --")
        view_select.set_option("values", "copy_url|add_my_view|edit|save|rename|delete|custom_property|custom_script")
        view_select.set_option("labels", "X Copy URL to this View|Add to My Views|Edit as Draft|Save Project View As|X Rename View|X Delete View|Add Custom Property|Add Custom Script")
        view_div.add_style("float: right")
        view_div.add(view_select)

        view_select.add_event("onchange", "spt.dg_table.view_action_cbk(this,'%s')" % self.table_id)

        return view_div




