from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
_magic_number = 2
_modified_time = 1223502121.132829
_template_filename='/home/adorrycott/PylonsApps/helloworld/helloworld/templates/status.mako'
_template_uri='/status.mako'
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
        h = context.get('h', UNDEFINED)
        c = context.get('c', UNDEFINED)
        # SOURCE LINE 1
        context.write(u'\n')
        # SOURCE LINE 4
        context.write(u"\n\n<div id='processbox'>\n")
        # SOURCE LINE 7
        for s in c.status:
            # SOURCE LINE 8
            context.write(u'        (')
            context.write(unicode(c.status[s][0]))
            context.write(u'):\n        ')
            # SOURCE LINE 9
            context.write(unicode("<FONT size=%s>" % c.status[s][1]))
            context.write(u'\n            ')
            # SOURCE LINE 10
            context.write(unicode(h.link_to(s, h.url(controller='hello', action='search', method='GET', tags=s))))
            context.write(u'\n        </FONT>\n')
        # SOURCE LINE 13
        context.write(u'</div>\n\n')
        return ''
    finally:
        context.caller_stack.pop_frame()


def render_head_tags(context):
    context.caller_stack.push_frame()
    try:
        # SOURCE LINE 2
        context.write(u'\n    <title>Link Database</title>\n')
        return ''
    finally:
        context.caller_stack.pop_frame()


