from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
_magic_number = 2
_modified_time = 1223666553.623426
_template_filename='/home/adorrycott/PylonsApps/helloworld/helloworld/templates/search.mako'
_template_uri='/search.mako'
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
        context.write(u"\n</div>\n<BR>\n\n<div id='processbox'>\n    ")
        # SOURCE LINE 12
        context.write(unicode(h.form(h.url(controller='hello', action='search'), method='GET')))
        context.write(u'\n    ')
        # SOURCE LINE 13
        context.write(unicode(h.hidden_field(name='limit', value=c.pagesize, checked='checked')))
        context.write(u'\n    ')
        # SOURCE LINE 14
        context.write(unicode(h.hidden_field(name='offset', value=c.pagenumber, checked='checked')))
        context.write(u'\n    <div class=\'innerprocessbox\'>\n        Search for Tag\n        <BR>\n        Ex: "google"\n    </div>\n    ')
        # SOURCE LINE 20
        context.write(unicode(h.text_field(name='tags', id='tags', value='%s', size='128') % c.tags))
        context.write(u"\n    <BR>\n    <BR>\n    <div class='innerprocessbox'>\n        ")
        # SOURCE LINE 24
        context.write(unicode(h.submit('Process')))
        context.write(u'\n    </div>\n    ')
        # SOURCE LINE 26
        context.write(unicode(h.end_form()))
        context.write(u'\n</div>\n\n<BR>\n')
        # SOURCE LINE 30
        context.write(unicode(h.form(h.url(controller='hello', action='search'), method='GET')))
        context.write(u'\n')
        # SOURCE LINE 31
        context.write(unicode(h.hidden_field(name='tags', value=c.tags, checked='checked')))
        context.write(u"\n\n<span class='controls-top'>\n# Per Page\n</span>\n<select name='limit'>\n")
        # SOURCE LINE 37
        for length in c.pagelimits:
            # SOURCE LINE 38
            if c.pagesize == length:
                # SOURCE LINE 39
                context.write(u'        <option value=')
                context.write(unicode(length))
                context.write(u" selected='selected'>")
                context.write(unicode(length))
                context.write(u'</option>\n')
                # SOURCE LINE 40
            else:
                # SOURCE LINE 41
                context.write(u'        <option value=')
                context.write(unicode(length))
                context.write(u'>')
                context.write(unicode(length))
                context.write(u'</option>\n')
        # SOURCE LINE 44
        context.write(u"</select>\n\n<span class='controls-top'>\nPage #\n</span>\n<select name='offset'>\n")
        # SOURCE LINE 50
        for length in range(1, c.pageoffset + 1):
            # SOURCE LINE 51
            if c.pagenumber == length:
                # SOURCE LINE 52
                context.write(u'            <option value=')
                context.write(unicode(length))
                context.write(u" selected='selected'>")
                context.write(unicode(length))
                context.write(u'</option>\n')
                # SOURCE LINE 53
            else:
                # SOURCE LINE 54
                context.write(u'            <option value=')
                context.write(unicode(length))
                context.write(u'>')
                context.write(unicode(length))
                context.write(u'</option>\n')
        # SOURCE LINE 57
        context.write(u'</select>\n\n')
        # SOURCE LINE 59
        context.write(unicode(h.submit('Go')))
        context.write(u'\n')
        # SOURCE LINE 60
        context.write(unicode(h.end_form()))
        context.write(u'\n\n<span class="controls-bottom">\n')
        # SOURCE LINE 63
        if c.pagenumber <= 1:
            # SOURCE LINE 64
            context.write(u'        [ Previous ] -\n')
            # SOURCE LINE 65
        else:
            # SOURCE LINE 66
            context.write(u'        [ ')
            context.write(unicode(h.link_to("Previous", h.url(controller='hello', action='search', limit=c.pagesize, offset=c.pagenumber-1, tags=c.tags), method='GET')))
            context.write(u' ] -\n')
        # SOURCE LINE 68
        context.write(u'    \n')
        # SOURCE LINE 69
        if c.pagenumber >= c.pageoffset:
            # SOURCE LINE 70
            context.write(u'        [ Next ]\n')
            # SOURCE LINE 71
        else:
            # SOURCE LINE 72
            context.write(u'        [ ')
            context.write(unicode(h.link_to("Next",h.url(controller='hello', action='search', limit=c.pagesize, offset=c.pagenumber+1, tags=c.tags), method='GET')))
            context.write(u' ]\n')
        # SOURCE LINE 74
        context.write(u'</span>\n\n<BR><BR>\n\n')
        # SOURCE LINE 78
        context.write(unicode(h.form(h.url(controller='hello', action='search', method='post'))))
        context.write(u'\n')
        # SOURCE LINE 79
        context.write(unicode(h.hidden_field(name='Redirect', value='serverinfo', checked='checked')))
        context.write(u'\n')
        # SOURCE LINE 80
        context.write(unicode(h.hidden_field(name='limit', value=c.pagesize, checked='checked')))
        context.write(u'\n')
        # SOURCE LINE 81
        context.write(unicode(h.hidden_field(name='offset', value=c.pagenumber, checked='checked')))
        context.write(u'\n<center>\n<TABLE border=\'3\' width=\'100%\'>\n    <TR>\n        <TD width=\'10%\' colspan=2>\n            <div class="tableheader">\n                Options\n            </div>\n        </TD>\n        <TD>\n            <div class="tableheader">\n                Link\n            </div>\n        </TD>\n        <TD width=\'7%\'>\n            <div class="tableheader">\n                Added\n            </div>\n        </TD>\n        <TD width=\'10%\'>\n            <div class="tableheader">\n                Modified\n            </div>\n        </TD>\n    </TR>\n    <TR></<TR>\n    ')
        # SOURCE LINE 107
        context.write(unicode(h.form(h.url(id="ZOMG BORKED!"))))
        context.write(u'\n    ')
        # SOURCE LINE 108
        context.write(unicode(h.end_form()))
        context.write(u'\n')
        # SOURCE LINE 109
        for l in c.link_data:
            # SOURCE LINE 110
            context.write(u"    <TR>\n        <TD align='center' width='5%'>\n            ")
            # SOURCE LINE 112
            context.write(unicode(h.check_box(name='Delete', value=l.getID(), checked='')))
            context.write(u"\n        </TD>\n        <TD align='center' width='5%'>\n            ")
            # SOURCE LINE 115
            context.write(unicode(h.form(h.url(controller='hello', action='edit', method='POST'))))
            context.write(u'\n            ')
            # SOURCE LINE 116
            context.write(unicode(h.hidden_field(name='id', value=l.getID(), checked='checked')))
            context.write(u'\n            ')
            # SOURCE LINE 117
            context.write(unicode(h.submit('Edit')))
            context.write(u'\n            ')
            # SOURCE LINE 118
            context.write(unicode(h.end_form()))
            context.write(u'\n        </TD>\n        <TD>\n            ID:\n            ')
            # SOURCE LINE 122
            context.write(unicode(l.getID()))
            context.write(u':\n            ')
            # SOURCE LINE 123
            context.write(unicode(h.link_to(l.getLink(), l.getLink())))
            context.write(u'\n            <div class="tab">\n                <div class="namespace">\n                    Notes:\n                    ')
            # SOURCE LINE 127
            context.write(unicode(l.getNotes()))
            context.write(u'\n                </div>\n                \n                Tags:\n')
            # SOURCE LINE 131
            for t in l.parseTags():
                # SOURCE LINE 132
                context.write(u'                    ')
                context.write(unicode(h.link_to(t, h.url(controller='hello', action='search', method='GET', tags=t))))
                context.write(u'\n')
            # SOURCE LINE 134
            context.write(u'            </div>\n        </TD>\n        <TD align=\'center\' width=\'10%\'>\n            <div class="datedisplay">\n                ')
            # SOURCE LINE 138
            context.write(unicode(l.getAddTime()))
            context.write(u'\n            </div>\n        </TD>\n        <TD align=\'center\' width=\'10%\'>\n            <div class="datedisplay">\n                ')
            # SOURCE LINE 143
            context.write(unicode(l.getModTime()))
            context.write(u'\n            </div>\n        </TD>\n    </TR>\n    <TR></<TR>\n')
        # SOURCE LINE 149
        context.write(u"    <TR>\n        <TD align='center' width='5%'>\n            ")
        # SOURCE LINE 151
        context.write(unicode(h.submit('Delete', confirm="Delete?")))
        context.write(u'\n            ')
        # SOURCE LINE 152
        context.write(unicode(h.end_form()))
        context.write(u'\n        </TD>\n        <TD align=\'center\' width=\'5%\'>\n        </TD>\n        <TD>\n        </TD>\n        <TD align=\'center\' width=\'10%\'>\n        </TD>\n        <TD align=\'center\' width=\'10%\'>\n        </TD>\n    </TR>\n</TABLE>\n</center>\n\n<BR>\n<div class="datalink">\n')
        # SOURCE LINE 168
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


