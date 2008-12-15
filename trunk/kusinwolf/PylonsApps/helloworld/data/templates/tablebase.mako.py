from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
_magic_number = 2
_modified_time = 1222198637.76476
_template_filename=u'/home/adorrycott/PylonsApps/helloworld/helloworld/templates/tablebase.mako'
_template_uri=u'/tablebase.mako'
_template_cache=cache.Cache(__name__, _modified_time)
_source_encoding=None
_exports = []


def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    pass
def _mako_inherit(template, context):
    _mako_generate_namespaces(context)
    return runtime._inherit_from(context, u'base.mako', _template_uri)
def render_body(context,**pageargs):
    context.caller_stack.push_frame()
    try:
        __M_locals = dict(pageargs=pageargs)
        self = context.get('self', UNDEFINED)
        # SOURCE LINE 1
        context.write(u'\n\n')
        # SOURCE LINE 3
        context.write(unicode(self.body_beforetable()))
        context.write(u'\n\n<TABLE border=\'3\' width=\'100%\'>\n    <TR>\n        <TD width=\'7%\'>\n            <div class="tableheader">\n                ')
        # SOURCE LINE 9
        context.write(unicode(self.table_header_left()))
        context.write(u'\n            </div>\n        </TD>\n        <TD>\n            <div class="tableheader">\n                ')
        # SOURCE LINE 14
        context.write(unicode(self.table_header_center()))
        context.write(u'\n            </div>\n        </TD>        \n        <TD width=\'7%\'>\n            <div class="tableheader">\n                ')
        # SOURCE LINE 19
        context.write(unicode(self.table_header_right()))
        context.write(u'\n            </div>\n        </TD>\n    </TR>\n    <TR></<TR>\n    ')
        # SOURCE LINE 24
        context.write(unicode(self.row_info()))
        context.write(u'\n</TABLE>\n\n')
        # SOURCE LINE 27
        context.write(unicode(self.body_aftertable()))
        return ''
    finally:
        context.caller_stack.pop_frame()


