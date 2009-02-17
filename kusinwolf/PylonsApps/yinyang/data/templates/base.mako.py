from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
_magic_number = 2
_modified_time = 1234903052.7952681
_template_filename=u'/home/adorrycott/PylonsApps/pyexp/kusinwolf/PylonsApps/yinyang/yinyang/templates/base.mako'
_template_uri=u'/base.mako'
_template_cache=cache.Cache(__name__, _modified_time)
_source_encoding=None
_exports = ['footer', 'head_tags']


def render_body(context,**pageargs):
    context.caller_stack.push_frame()
    try:
        __M_locals = dict(pageargs=pageargs)
        h = context.get('h', UNDEFINED)
        self = context.get('self', UNDEFINED)
        next = context.get('next', UNDEFINED)
        # SOURCE LINE 1
        context.write(u'<html>\n  <head>\n    ')
        # SOURCE LINE 3
        context.write(unicode(self.head_tags()))
        context.write(u' <!-- Build out header either by default or overwrite it -->\n    ')
        # SOURCE LINE 4
        context.write(unicode(h.javascript_include_tag(builtins=True)))
        context.write(u'\n    <link href="/css/hello.css" rel="stylesheet" type="text/css">\n  </head>\n  <body>\n    ')
        # SOURCE LINE 8
        context.write(unicode(next.body()))
        context.write(u"\n    <BR>\n    <div id='footer'>\n        ")
        # SOURCE LINE 11
        context.write(unicode(self.footer()))
        context.write(u' <!-- Build out footer either by default or overwrite it -->\n    </div>\n  </body>\n</html>\n\n<!-- Default assigned tags that if not defined throw an error -->\n\n')
        # SOURCE LINE 20
        context.write(u'\n\n')
        # SOURCE LINE 26
        context.write(u'\n')
        return ''
    finally:
        context.caller_stack.pop_frame()


def render_footer(context):
    context.caller_stack.push_frame()
    try:
        # SOURCE LINE 22
        context.write(u'\n    Site Map\n    <BR>\n    :D\n')
        return ''
    finally:
        context.caller_stack.pop_frame()


def render_head_tags(context):
    context.caller_stack.push_frame()
    try:
        # SOURCE LINE 18
        context.write(u'\n    <title>Default Name</title>\n')
        return ''
    finally:
        context.caller_stack.pop_frame()


