from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 5
_modified_time = 1254613064.8376479
_template_filename='/home/kusinwolf/pyexp/kusinwolf/PylonsApps/invenimus/invenimus/templates/base.mako'
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
        __M_writer(u' <!-- Build out header either by default or overwrite it -->\n    <link rel="stylesheet" type="text/css" href="../css/base.css">\n    <link rel="stylesheet" type="text/css" href="../../css/base.css">\n  </head>\n  <body>\n    ')
        # SOURCE LINE 8
        __M_writer(escape(next.body()))
        __M_writer(u"\n    <BR />\n    <div id='footer'>\n        ")
        # SOURCE LINE 11
        __M_writer(escape(self.footer()))
        __M_writer(u' <!-- Build out footer either by default or overwrite it -->\n    </div>\n  </body>\n</html>\n\n<!-- Default assigned tags that if not defined throw an error -->\n\n')
        # SOURCE LINE 20
        __M_writer(u'\n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_footer(context):
    context.caller_stack._push_frame()
    try:
        h = context.get('h', UNDEFINED)
        g = context.get('g', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 22
        __M_writer(u'\n    Local Site Map\n    <BR />\n')
        # SOURCE LINE 25
        for page in g.sitemap:
            # SOURCE LINE 26
            __M_writer(u'      ')
            __M_writer(escape(h.link_to(page[0], h.url_for(action=page[1], id=None))))
            __M_writer(u' |\n')
        # SOURCE LINE 28
        __M_writer(u'    <BR />\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_head_tags(context):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 18
        __M_writer(u'\n    <title>Default Name</title>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


