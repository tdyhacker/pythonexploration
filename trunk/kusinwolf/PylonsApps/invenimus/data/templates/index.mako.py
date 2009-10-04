from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 5
_modified_time = 1254613433.2747071
_template_filename='/home/kusinwolf/pyexp/kusinwolf/PylonsApps/invenimus/invenimus/templates/index.mako'
_template_uri='/index.mako'
_template_cache=cache.Cache(__name__, _modified_time)
_source_encoding='utf-8'
from webhelpers.html import escape
_exports = ['head_tags']


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
    return runtime._inherit_from(context, 'base.mako', _template_uri)
def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        range = context.get('range', UNDEFINED)
        c = context.get('c', UNDEFINED)
        len = context.get('len', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'\n')
        # SOURCE LINE 4
        __M_writer(u'\n\n')
        # SOURCE LINE 6
        for p in range(0, len(c.pictures), 3):
            # SOURCE LINE 7
            for q in range(0, 3):
                # SOURCE LINE 8
                __M_writer(u'            <img src="')
                __M_writer(escape(c.path + c.pictures[p + q]))
                __M_writer(u'">\n')
        # SOURCE LINE 11
        __M_writer(u'    \n    <br />\n    <img src="http://www.w3schools.com/images/pulpit.jpg">\n\n<br />\n<br />')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_head_tags(context):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 2
        __M_writer(u'\n    <title>Overview</title>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


