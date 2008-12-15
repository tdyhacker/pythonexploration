from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
_magic_number = 2
_modified_time = 1223666728.768846
_template_filename='/home/adorrycott/PylonsApps/helloworld/helloworld/templates/alllinks.mako'
_template_uri='/alllinks.mako'
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
        context.write(unicode(h.form(h.url(controller='hello', action='allLinks'), method='GET')))
        context.write(u"\n\n<span class='controls-top'>\n# Per Page\n</span\n<select name='limit'>\n")
        # SOURCE LINE 17
        for length in c.pagelimits:
            # SOURCE LINE 18
            if c.pagesize == length:
                # SOURCE LINE 19
                context.write(u'        <option value=')
                context.write(unicode(length))
                context.write(u" selected='selected'>")
                context.write(unicode(length))
                context.write(u'</option>\n')
                # SOURCE LINE 20
            else:
                # SOURCE LINE 21
                context.write(u'        <option value=')
                context.write(unicode(length))
                context.write(u'>')
                context.write(unicode(length))
                context.write(u'</option>\n')
        # SOURCE LINE 24
        context.write(u"</select>\n\n<span class='controls-top'>\nPage #\n</span>\n<select name='offset'>\n")
        # SOURCE LINE 30
        for length in range(1, c.pageoffset + 1):
            # SOURCE LINE 31
            if c.pagenumber == length:
                # SOURCE LINE 32
                context.write(u'            <option value=')
                context.write(unicode(length))
                context.write(u" selected='selected'>")
                context.write(unicode(length))
                context.write(u'</option>\n')
                # SOURCE LINE 33
            else:
                # SOURCE LINE 34
                context.write(u'            <option value=')
                context.write(unicode(length))
                context.write(u'>')
                context.write(unicode(length))
                context.write(u'</option>\n')
        # SOURCE LINE 37
        context.write(u'</select>\n\n')
        # SOURCE LINE 39
        context.write(unicode(h.submit('Go')))
        context.write(u'\n')
        # SOURCE LINE 40
        context.write(unicode(h.end_form()))
        context.write(u'\n\n<span class="controls-bottom">\n')
        # SOURCE LINE 43
        if c.pagenumber <= 1:
            # SOURCE LINE 44
            context.write(u'        [ Previous ] -\n')
            # SOURCE LINE 45
        else:
            # SOURCE LINE 46
            context.write(u'        [ ')
            context.write(unicode(h.link_to("Previous", h.url(controller='hello', action='allLinks', limit=c.pagesize, offset=c.pagenumber-1), method='GET')))
            context.write(u' ] -\n')
        # SOURCE LINE 48
        context.write(u'    \n')
        # SOURCE LINE 49
        if c.pagenumber >= c.pageoffset:
            # SOURCE LINE 50
            context.write(u'        [ Next ]\n')
            # SOURCE LINE 51
        else:
            # SOURCE LINE 52
            context.write(u'        [ ')
            context.write(unicode(h.link_to("Next",h.url(controller='hello', action='allLinks', limit=c.pagesize, offset=c.pagenumber+1), method='GET')))
            context.write(u' ]\n')
        # SOURCE LINE 54
        context.write(u'</span>\n\n<BR><BR>\n\n')
        # SOURCE LINE 58
        context.write(unicode(h.form(h.url(controller='hello', action='inactivateObject'), method='post')))
        context.write(u'\n')
        # SOURCE LINE 59
        context.write(unicode(h.hidden_field(name='Redirect', value='alllinks', checked='checked')))
        context.write(u'\n<TABLE border=\'3\' width=\'100%\'>\n    <TR>\n        <TD width=\'10%\' colspan=2>\n            <div class="tableheader">\n                Options\n            </div>\n        </TD>\n        <TD>\n            <div class="tableheader">\n                Link\n            </div>\n        </TD>\n        <TD width=\'7%\'>\n            <div class="tableheader">\n                Added\n            </div>\n        </TD>\n        <TD width=\'10%\'>\n            <div class="tableheader">\n                Modified\n            </div>\n        </TD>\n    </TR>\n    <TR></<TR>\n    ')
        # SOURCE LINE 84
        context.write(unicode(h.form(h.url(id="ZOMG BORKED!"))))
        context.write(u'\n    ')
        # SOURCE LINE 85
        context.write(unicode(h.end_form()))
        context.write(u'\n')
        # SOURCE LINE 86
        for l in c.link_data:
            # SOURCE LINE 87
            context.write(u"    <TR>\n        <TD align='center' width='5%'>\n            ")
            # SOURCE LINE 89
            context.write(unicode(h.check_box(name='Delete', value=l.getID(), checked='')))
            context.write(u"\n        </TD>\n        <TD align='center' width='5%'>\n            ")
            # SOURCE LINE 92
            context.write(unicode(h.form(h.url(controller='hello', action='edit', method='POST'))))
            context.write(u'\n            ')
            # SOURCE LINE 93
            context.write(unicode(h.hidden_field(name='id', value=l.getID(), checked='checked')))
            context.write(u'\n            ')
            # SOURCE LINE 94
            context.write(unicode(h.submit('Edit')))
            context.write(u'\n            ')
            # SOURCE LINE 95
            context.write(unicode(h.end_form()))
            context.write(u'\n        </TD>\n        <TD>\n            ID:\n            ')
            # SOURCE LINE 99
            context.write(unicode(l.getID()))
            context.write(u':\n            ')
            # SOURCE LINE 100
            context.write(unicode(h.link_to(l.getLink(), l.getLink())))
            context.write(u'\n            <div class="tab">\n                <div class="namespace">\n                    <span class="namespacetitles">\n                        Notes:\n                    </span>\n                    ')
            # SOURCE LINE 106
            context.write(unicode(l.getNotes()))
            context.write(u'\n                    <BR>\n                    <span class="namespacetitles">\n                        Tags:\n                    </span>\n')
            # SOURCE LINE 111
            for t in l.parseTags():
                # SOURCE LINE 112
                context.write(u'                        ')
                context.write(unicode(h.link_to(t, h.url(controller='hello', action='search', method='GET', tags=t))))
                context.write(u'\n')
            # SOURCE LINE 114
            context.write(u'                </div>\n            </div>\n        </TD>\n        <TD align=\'center\' width=\'10%\'>\n            <div class="datedisplay">\n                ')
            # SOURCE LINE 119
            context.write(unicode(l.getAddTime()))
            context.write(u'\n            </div>\n        </TD>\n        <TD align=\'center\' width=\'10%\'>\n            <div class="datedisplay">\n                ')
            # SOURCE LINE 124
            context.write(unicode(l.getModTime()))
            context.write(u'\n            </div>\n        </TD>\n    </TR>\n    <TR></<TR>\n')
        # SOURCE LINE 130
        context.write(u"    <TR>\n        <TD align='center' width='5%'>\n            ")
        # SOURCE LINE 132
        context.write(unicode(h.submit('Delete', confirm="Delete?")))
        context.write(u'\n            ')
        # SOURCE LINE 133
        context.write(unicode(h.end_form()))
        context.write(u'\n        </TD>\n        <TD align=\'center\' width=\'5%\'>\n        </TD>\n        <TD>\n        </TD>\n        <TD align=\'center\' width=\'10%\'>\n        </TD>\n        <TD align=\'center\' width=\'10%\'>\n        </TD>\n    </TR>\n</TABLE>\n\n<BR>\n<div class="datalink">\n')
        # SOURCE LINE 148
        context.write(unicode(h.link_to("Main Menu", h.url(controller="hello", action="index"))))
        context.write(u'\n</div>\n\n')
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


