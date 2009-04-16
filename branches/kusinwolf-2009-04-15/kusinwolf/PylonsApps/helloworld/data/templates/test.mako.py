from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
_magic_number = 2
_modified_time = 1229379575.0511451
_template_filename='/home/adorrycott/PylonsApps/helloworld/helloworld/templates/test.mako'
_template_uri='/test.mako'
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
        request = context.get('request', UNDEFINED)
        # SOURCE LINE 1
        context.write(u'\n')
        # SOURCE LINE 4
        context.write(u'\n\n')
        # SOURCE LINE 6
        context.write(unicode(h.form(h.url(controller='hello', action='test', method='post'))))
        context.write(u'\n')
        # SOURCE LINE 7
        context.write(unicode(h.select("Locations", c.drops)))
        context.write(u'\n')
        # SOURCE LINE 8
        context.write(unicode(h.submit("Press")))
        context.write(u'\n')
        # SOURCE LINE 9
        context.write(unicode(h.end_form()))
        context.write(u'\n\n')
        # SOURCE LINE 11
        try:
            # SOURCE LINE 12
            context.write(u'    ')
            context.write(unicode(request.params["Locations"]))
            context.write(u'\n')
            # SOURCE LINE 13
        except:
            # SOURCE LINE 14
            context.write(u'    ')
            context.write(unicode("Ooops"))
            context.write(u'\n')
        # SOURCE LINE 16
        context.write(u'\n<!--\n')
        # SOURCE LINE 18
        for a in range(50):
            # SOURCE LINE 19
            context.write(u'    ')
            context.write(unicode("<font style=\"font-size: %spt\">Testing</font>" % a))
            context.write(u'\n    <BR>\n')
        # SOURCE LINE 22
        context.write(u'-->\n')
        return ''
    finally:
        context.caller_stack.pop_frame()


def render_head_tags(context):
    context.caller_stack.push_frame()
    try:
        # SOURCE LINE 2
        context.write(u'\n    <title>Testing</title>\n')
        return ''
    finally:
        context.caller_stack.pop_frame()


