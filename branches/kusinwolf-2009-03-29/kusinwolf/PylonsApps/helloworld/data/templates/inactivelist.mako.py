from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
_magic_number = 2
_modified_time = 1223581567.8968799
_template_filename='/home/adorrycott/PylonsApps/helloworld/helloworld/templates/inactivelist.mako'
_template_uri='/inactivelist.mako'
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
        context.write(u'\n\n<div class="datalink">\n')
        # SOURCE LINE 7
        context.write(unicode(h.link_to("Main Menu", h.url(controller="hello", action="index"))))
        context.write(u'\n</div>\n<BR>\n\n')
        # SOURCE LINE 11
        context.write(unicode(h.form(h.url(controller='hello', action='caseDelete', method='post'))))
        context.write(u'\n')
        # SOURCE LINE 12
        context.write(unicode(h.hidden_field(name='Redirect', value='inactivelist', checked='checked')))
        context.write(u'\n<TABLE border=\'3\' width=\'100%\'>\n    <TR>\n        <TD width=\'10%\' colspan=2>\n            <div class="tableheader">\n                Options\n            </div>\n        </TD>\n        <TD>\n            <div class="tableheader">\n                Link - Inactive Links\n            </div>\n        </TD>        \n        <TD width=\'7%\'>\n            <div class="tableheader">\n                Reactivate\n            </div>\n        </TD>\n        <TD width=\'10%\'>\n            <div class="tableheader">\n                Inactivated\n            </div>\n        </TD>\n    </TR>\n    <TR></<TR>\n')
        # SOURCE LINE 37
        context.write(unicode(h.form(h.url(id="ZOMG BORKED!"))))
        context.write(u'\n')
        # SOURCE LINE 38
        context.write(unicode(h.end_form()))
        context.write(u'\n')
        # SOURCE LINE 39
        for l in c.link_data:
            # SOURCE LINE 40
            context.write(u"    <TR>\n        <TD align='center' width='5%'>\n            ")
            # SOURCE LINE 42
            context.write(unicode(h.check_box(name='Delete', value=l.getID(), checked='')))
            context.write(u"\n        </TD>\n        <TD align='center' width='5%'>            \n            ")
            # SOURCE LINE 45
            context.write(unicode(h.form(h.url(controller='hello', action='edit', method='post'))))
            context.write(u'\n            ')
            # SOURCE LINE 46
            context.write(unicode(h.hidden_field(name='id', value=l.getID(), checked='checked')))
            context.write(u'\n            ')
            # SOURCE LINE 47
            context.write(unicode(h.submit('Edit')))
            context.write(u'\n            ')
            # SOURCE LINE 48
            context.write(unicode(h.end_form()))
            context.write(u'\n        </TD>\n        <TD>\n            ID:\n            ')
            # SOURCE LINE 52
            context.write(unicode(l.getID()))
            context.write(u':\n            ')
            # SOURCE LINE 53
            context.write(unicode(h.link_to(l.getLink(), l.getLink())))
            context.write(u'\n            ')
            # SOURCE LINE 54
            context.write(unicode("""<input type='hidden' name='remove' value='%s' checked='checked'>""" % l.getLink()))
            context.write(u'\n            <div class="tab">\n                <div class="namespace">\n                    <span class="namespacetitles">\n                        Notes:\n                    </span>\n                    ')
            # SOURCE LINE 60
            context.write(unicode(l.getNotes()))
            context.write(u'\n                    <BR>\n                    <span class="namespacetitles">\n                        Tags:\n                    </span>\n')
            # SOURCE LINE 65
            for t in l.parseTags():
                # SOURCE LINE 66
                context.write(u'                        ')
                context.write(unicode(h.link_to(t, h.url(controller='hello', action='search', method='GET', tags=t))))
                context.write(u'\n')
            # SOURCE LINE 68
            context.write(u"                </div>\n            </div>\n        </TD>\n        <TD align='center' width='7%'>\n            ")
            # SOURCE LINE 72
            context.write(unicode(h.check_box(name='Activate', value=l.getID(), checked='')))
            context.write(u'\n            ')
            # SOURCE LINE 73
            context.write(unicode(h.hidden_field(name='Redirect', value='inactivelist', checked='checked')))
            context.write(u'\n        </TD>\n        <TD align=\'center\' width=\'10%\'>\n            <div class="datedisplay">\n                ')
            # SOURCE LINE 77
            context.write(unicode(l.getInaTime()))
            context.write(u'\n            </div>\n        </TD>\n    </TR>\n    <TR></<TR>\n')
        # SOURCE LINE 83
        context.write(u"    <TR>\n        <TD align='center' width='5%'>\n            ")
        # SOURCE LINE 85
        context.write(unicode(h.submit('Delete', confirm="Permanitly Delete?")))
        context.write(u"\n        </TD>\n        <TD align='center' width='5%'>\n        </TD>\n        <TD>\n        </TD>\n        <TD align='center' width='10%'>\n            ")
        # SOURCE LINE 92
        context.write(unicode(h.submit('Activate', confirm="Activate?")))
        context.write(u'\n            ')
        # SOURCE LINE 93
        context.write(unicode(h.end_form()))
        context.write(u'\n        </TD>\n        <TD align=\'center\' width=\'10%\'>\n        </TD>\n    </TR>\n</TABLE>\n\n<BR>\n<div class="datalink">\n')
        # SOURCE LINE 102
        context.write(unicode(h.link_to("Main Menu", h.url(controller="hello", action="index"))))
        context.write(u'\n</div>')
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


