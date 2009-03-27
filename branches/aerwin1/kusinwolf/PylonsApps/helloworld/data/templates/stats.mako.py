from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
_magic_number = 2
_modified_time = 1223592894.383559
_template_filename='/home/adorrycott/PylonsApps/helloworld/helloworld/templates/stats.mako'
_template_uri='/stats.mako'
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
        context.write(u"\n\n<div id='statsbox'>\n")
        # SOURCE LINE 7
        for s in c.stats:
            # SOURCE LINE 8
            context.write(u'        ')
            context.write(unicode("<FONT style=\"font-size: %spt\">" % c.stats[s][1]))
            context.write(unicode(h.link_to(s, h.url(controller='hello', action='search', method='GET', tags=s))))
            context.write(u'</FONT>\n        -\n')
        # SOURCE LINE 11
        context.write(u"</div>\n\n<div id='statsright'>\n    Amount - Tag\n")
        # SOURCE LINE 15
        for s in c.sorted:
            # SOURCE LINE 16
            context.write(u'        <BR>')
            context.write(unicode(s[0][0]))
            context.write(u' - ')
            context.write(unicode(h.link_to(s[1], h.url(controller='hello', action='search', method='GET', tags=s[1]))))
            context.write(u'\n')
        # SOURCE LINE 18
        context.write(u'</div>\n\n\n')
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


