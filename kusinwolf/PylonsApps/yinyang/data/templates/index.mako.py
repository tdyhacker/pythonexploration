from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
_magic_number = 2
_modified_time = 1234906781.4149089
_template_filename='/home/adorrycott/PylonsApps/pyexp/kusinwolf/PylonsApps/yinyang/yinyang/templates/index.mako'
_template_uri='/index.mako'
_template_cache=cache.Cache(__name__, _modified_time)
_source_encoding=None
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
    return runtime._inherit_from(context, u'base.mako', _template_uri)
def render_body(context,**pageargs):
    context.caller_stack.push_frame()
    try:
        __M_locals = dict(pageargs=pageargs)
        # SOURCE LINE 1
        context.write(u'\n')
        # SOURCE LINE 4
        context.write(u'\n\n<BR />\n<BR />\n<BR />\n<div id="addevent">\n<FORM id="event" name="event">\n    <TABLE width=100%>\n        <TR>\n            <TD width=70%>\n                <div id="addevent-title">\n                    <input type="text" name="event-title" value="Title" size=70%>\n                </div>\n            </TD>\n            <TD width=30% valign=top>\n                <div id="addevent-type">\n                    <SELECT>\n                    <OPTION value="yang">Yang (Good)</OPTION>\n                    <OPTION value="neutral">Neutral</OPTION>\n                    <OPTION value="yin">Yin (Bad)</OPTION>\n                    </SELECT>\n                </div>\n            </TD>\n        </TR>\n    </TABLE>\n    <div id="addevent-text">\n        <BR />\n        <CENTER>\n            <textarea id="event-text" rows="8" cols="100">Event</textarea> <!-- Prevents extra newlines being placed in the field -->\n        </CENTER>\n        <BR />\n    </div>\n</FORM>\n</div>\n<BR />\n<BR />\n<BR />\n')
        return ''
    finally:
        context.caller_stack.pop_frame()


def render_head_tags(context):
    context.caller_stack.push_frame()
    try:
        # SOURCE LINE 2
        context.write(u'\n    <title>YiYa Blog</title>\n')
        return ''
    finally:
        context.caller_stack.pop_frame()


