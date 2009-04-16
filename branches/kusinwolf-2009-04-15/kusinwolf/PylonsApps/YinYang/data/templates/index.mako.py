from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 5
_modified_time = 1235001006.2686141
_template_filename='/home/adorrycott/PylonsApps/pyexp/kusinwolf/PylonsApps/YinYang/yinyang/templates/index.mako'
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
        url = context.get('url', UNDEFINED)
        end_form = context.get('end_form', UNDEFINED)
        submit = context.get('submit', UNDEFINED)
        text_field = context.get('text_field', UNDEFINED)
        form = context.get('form', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'\n')
        # SOURCE LINE 4
        __M_writer(u'\n\n<BR />\n<BR />\n<BR />\n')
        # SOURCE LINE 9
        __M_writer(escape(form(url(controller='controller', action='login', method='post'), name="login", id="login")))
        __M_writer(u'\n<div id="addevent">\nUsername: ')
        # SOURCE LINE 11
        __M_writer(escape(text_field(name='login-username', id='login-username', value='', size='128')))
        __M_writer(u'<BR />\nPassword: ')
        # SOURCE LINE 12
        __M_writer(escape(text_field(name='login-password', id='login-password', value='', size='128')))
        __M_writer(u'<BR />\n')
        # SOURCE LINE 13
        __M_writer(escape(submit('Login')))
        __M_writer(u'\n')
        # SOURCE LINE 14
        __M_writer(escape(end_form()))
        __M_writer(u'\n</div>\n\n</FORM>\n<BR />\n<BR />\n<BR />')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_head_tags(context):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 2
        __M_writer(u'\n    <title>Yin & Yang Blog</title>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


