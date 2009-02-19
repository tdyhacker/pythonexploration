from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 5
_modified_time = 1234995794.5469649
_template_filename='/home/adorrycott/PylonsApps/pyexp/kusinwolf/PylonsApps/YinYang/yinyang/templates/base.mako'
_template_uri='/base.mako'
_template_cache=cache.Cache(__name__, _modified_time)
_source_encoding='utf-8'
from webhelpers.html import escape
_exports = ['footer', 'head_tags']


def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        self = context.get('self', UNDEFINED)
        next = context.get('next', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'<html>\n  <head>\n    ')
        # SOURCE LINE 3
        __M_writer(escape(self.head_tags()))
        __M_writer(u' <!-- Build out header either by default or overwrite it -->\n    <link href="/css/base.css" rel="stylesheet" type="text/css">\n  </head>\n  <body>\n    ')
        # SOURCE LINE 7
        __M_writer(escape(next.body()))
        __M_writer(u"\n    <BR />\n    <div id='footer'>\n        ")
        # SOURCE LINE 10
        __M_writer(escape(self.footer()))
        __M_writer(u' <!-- Build out footer either by default or overwrite it -->\n    </div>\n  </body>\n</html>\n\n<!-- Default assigned tags that if not defined throw an error -->\n\n')
        # SOURCE LINE 19
        __M_writer(u'\n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_footer(context):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 21
        __M_writer(u'\n    Site Map\n    <BR />\n    :D\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_head_tags(context):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 17
        __M_writer(u'\n    <title>Default Name</title>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


