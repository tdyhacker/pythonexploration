from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
_magic_number = 2
_modified_time = 1223506474.2395051
_template_filename='/home/adorrycott/PylonsApps/helloworld/helloworld/templates/edit.mako'
_template_uri='/edit.mako'
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
        context.write(u'\n\n<BR>\n    ')
        # SOURCE LINE 7
        context.write(unicode(h.form(h.url(controller='hello', action='edit', method='post'))))
        context.write(u"\n<div class='editpage'>\n    Link:\n")
        # SOURCE LINE 10
        if c.link_data.getLink():
            # SOURCE LINE 11
            context.write(u'            ')
            context.write(unicode(h.text_field(name='link', value=c.link_data.getLink(), size='128')))
            context.write(u'\n')
            # SOURCE LINE 12
        else:
            # SOURCE LINE 13
            context.write(u'            ')
            context.write(unicode(h.text_field(name='link', value='', size='128')))
            context.write(u'\n')
        # SOURCE LINE 15
        context.write(u"    <BR>\n    Notes:\n    <div class='editpagefields'>\n")
        # SOURCE LINE 18
        if c.link_data.getNotes():
            # SOURCE LINE 19
            context.write(u'            ')
            context.write(unicode(h.text_field(name='notes', value=c.link_data.getNotes(), size='128')))
            context.write(u'\n')
            # SOURCE LINE 20
        else:
            # SOURCE LINE 21
            context.write(u'            ')
            context.write(unicode(h.text_field(name='notes', value='', size='128')))
            context.write(u'\n')
        # SOURCE LINE 23
        context.write(u"    </div>\n    <BR>\n\n    Tags:\n    <div class='editpagefields'>\n")
        # SOURCE LINE 28
        if c.link_data.getTags():
            # SOURCE LINE 29
            context.write(u'            ')
            context.write(unicode(h.text_field(name='tags', value=c.link_data.getTags(), size='128')))
            context.write(u'\n')
            # SOURCE LINE 30
        else:
            # SOURCE LINE 31
            context.write(u'            ')
            context.write(unicode(h.text_field(name='tags', value='', size='128')))
            context.write(u'\n')
        # SOURCE LINE 33
        context.write(u"    </div>\n    <BR>\n\n    Activity:\n        <select name='active'>\n")
        # SOURCE LINE 38
        if c.link_data.getActivity():
            # SOURCE LINE 39
            context.write(u'            <option value="True" selected=\'selected\'>Active</option>\n            <option value="False">Inactive</option>\n')
            # SOURCE LINE 41
        else:
            # SOURCE LINE 42
            context.write(u'            <option value="True">Active</option>\n            <option value="False" selected=\'selected\'>Inactive</option>\n')
        # SOURCE LINE 45
        context.write(u'        </select>\n\n    <BR>\n    <BR>\n    ')
        # SOURCE LINE 49
        context.write(unicode(h.hidden_field(name='id', value=c.link_data.getID(), checked='checked', method='GET')))
        context.write(u'\n    ')
        # SOURCE LINE 50
        context.write(unicode(h.submit('Edit', confirm="Is this correct?")))
        context.write(u'\n</div>\n    ')
        # SOURCE LINE 52
        context.write(unicode(h.end_form()))
        context.write(u"\n\n<BR><BR>\n    \n<div class='editpage'>\n")
        # SOURCE LINE 57
        if c.success:
            # SOURCE LINE 58
            context.write(u'        ')
            context.write(unicode(c.success))
            context.write(u'\n')
        # SOURCE LINE 60
        context.write(u'</div>\n\n<div class="datalink">\n')
        # SOURCE LINE 63
        context.write(unicode(h.link_to("Main Menu", h.url(controller="hello", action="index"))))
        context.write(u'\n</div>\n<BR>\n')
        return ''
    finally:
        context.caller_stack.pop_frame()


def render_head_tags(context):
    context.caller_stack.push_frame()
    try:
        # SOURCE LINE 2
        context.write(u'\n    <title>Edit Link</title>\n')
        return ''
    finally:
        context.caller_stack.pop_frame()


