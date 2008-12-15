from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
_magic_number = 2
_modified_time = 1223667025.432497
_template_filename='/home/adorrycott/PylonsApps/helloworld/helloworld/templates/serverinfo.mako'
_template_uri='/serverinfo.mako'
_template_cache=cache.Cache(__name__, _modified_time)
_source_encoding=None
_exports = ['column_two', 'column_one', 'head_tags']


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
        context.write(u'\n\n<div id=\'processbox\'>\n    <div class=\'innerprocessbox\'>\n        <!--Ex: "http://Gibberish.com/here.html?originallink=http://What_we_are_looking_for.com/the_name.mp3"<BR>-->\n        Ex: "http://www.google.com/"\n    </div>\n    ')
        # SOURCE LINE 11
        context.write(unicode(h.form(h.url(controller='hello', action='', method='post'))))
        context.write(u'\n    Link - \n    ')
        # SOURCE LINE 13
        context.write(unicode(h.text_field(name='link', id='link', value='', size='128')))
        context.write(u'\n    <BR>\n    <BR>\n    <div class=\'innerprocessbox\'>\n        Ex: "This information is useful!"\n    </div>\n    Notes - \n    ')
        # SOURCE LINE 20
        context.write(unicode(h.text_field(name='notes', id='notes', value='', size='128')))
        context.write(u'\n    <BR>\n    <BR>\n    <div class=\'innerprocessbox\'>\n        Ex: "searchengine google homepage"\n        <BR>\n        Info: Tags are broken apart by spaces and non-alphabet characters\n    </div>\n    Tags - \n    ')
        # SOURCE LINE 29
        context.write(unicode(h.text_field(name='tags', id='tags', value='', size='128')))
        context.write(u"\n    <BR>\n    <BR>\n    <div class='innerprocessbox'>\n    ")
        # SOURCE LINE 33
        context.write(unicode(h.submit('Process')))
        context.write(u'\n    </div>\n    ')
        # SOURCE LINE 35
        context.write(unicode(h.end_form()))
        context.write(u"\n</div>\n\n<div class='editpage'>\n")
        # SOURCE LINE 39
        if c.success:
            # SOURCE LINE 40
            context.write(u'        ')
            context.write(unicode(c.success))
            context.write(u'\n')
        # SOURCE LINE 42
        context.write(u'</div>\n\n<div class="datalink">\n    ')
        # SOURCE LINE 45
        context.write(unicode(h.link_to("Whole List", h.url(controller="hello", action="allLinks"))))
        context.write(u'\n</div>\n\n<BR>\n')
        # SOURCE LINE 49
        context.write(unicode(h.form(h.url(controller='hello', action='inactivateObject', method='post'))))
        context.write(u'\n')
        # SOURCE LINE 50
        context.write(unicode(h.hidden_field(name='Redirect', value='serverinfo', checked='checked')))
        context.write(u'\n<center>\n<TABLE border=\'3\' width=\'100%\'>\n    <TR>\n        <TD width=\'10%\' colspan=2>\n            <div class="tableheader">\n                Options\n            </div>\n        </TD>\n        <TD>\n            <div class="tableheader">\n                Link\n            </div>\n        </TD>\n        <TD width=\'7%\'>\n            <div class="tableheader">\n                Added\n            </div>\n        </TD>\n        <TD width=\'10%\'>\n            <div class="tableheader">\n                Modified\n            </div>\n        </TD>\n    </TR>\n    <TR></<TR>\n    ')
        # SOURCE LINE 76
        context.write(unicode(h.form(h.url(id="ZOMG BORKED!"))))
        context.write(u'\n    ')
        # SOURCE LINE 77
        context.write(unicode(h.end_form()))
        context.write(u'\n')
        # SOURCE LINE 78
        for l in c.link_data:
            # SOURCE LINE 79
            context.write(u"    <TR>\n        <TD align='center' width='5%'>\n            ")
            # SOURCE LINE 81
            context.write(unicode(h.check_box(name='Delete', value=l.getID(), checked='')))
            context.write(u"\n        </TD>\n        <TD align='center' width='5%'>\n            ")
            # SOURCE LINE 84
            context.write(unicode(h.form(h.url(controller='hello', action='edit'), method='GET')))
            context.write(u'\n            ')
            # SOURCE LINE 85
            context.write(unicode(h.hidden_field(name='id', value=l.getID(), checked='checked')))
            context.write(u'\n            ')
            # SOURCE LINE 86
            context.write(unicode(h.submit('Edit')))
            context.write(u'\n            ')
            # SOURCE LINE 87
            context.write(unicode(h.end_form()))
            context.write(u'\n        </TD>\n        <TD>\n            ID:\n            ')
            # SOURCE LINE 91
            context.write(unicode(l.getID()))
            context.write(u':\n            ')
            # SOURCE LINE 92
            context.write(unicode(h.link_to(l.getLink(), l.getLink())))
            context.write(u'\n            <div class="tab">\n                <div class="namespace">\n                    <span class="namespacetitles">\n                        Notes:\n                    </span>\n                    ')
            # SOURCE LINE 98
            context.write(unicode(l.getNotes()))
            context.write(u'\n                    <BR>\n                    <span class="namespacetitles">\n                        Tags:\n                    </span>\n')
            # SOURCE LINE 103
            for t in l.parseTags():
                # SOURCE LINE 104
                context.write(u'                        ')
                context.write(unicode(h.link_to(t, h.url(controller='hello', action='search', tags=t), method='GET')))
                context.write(u'\n')
            # SOURCE LINE 106
            context.write(u'                </div>\n            </div>\n        </TD>\n        <TD align=\'center\' width=\'10%\'>\n            <div class="datedisplay">\n                ')
            # SOURCE LINE 111
            context.write(unicode(l.getAddTime()))
            context.write(u'\n            </div>\n        </TD>\n        <TD align=\'center\' width=\'10%\'>\n            <div class="datedisplay">\n                ')
            # SOURCE LINE 116
            context.write(unicode(l.getModTime()))
            context.write(u'\n            </div>\n        </TD>\n    </TR>\n    <TR></<TR>\n')
        # SOURCE LINE 122
        context.write(u"    <TR>\n        <TD align='center' width='5%'>\n            ")
        # SOURCE LINE 124
        context.write(unicode(h.submit('Delete', confirm="Delete?")))
        context.write(u'\n            ')
        # SOURCE LINE 125
        context.write(unicode(h.end_form()))
        context.write(u'\n        </TD>\n        <TD align=\'center\' width=\'5%\'>\n        </TD>\n        <TD>\n        </TD>\n        <TD align=\'center\' width=\'10%\'>\n        </TD>\n        <TD align=\'center\' width=\'10%\'>\n        </TD>\n    </TR>\n</TABLE>\n</center>\n\n<BR>\n\n<div class="datalink">\n    ')
        # SOURCE LINE 142
        context.write(unicode(h.link_to("Whole List", h.url(controller="hello", action="allLinks"))))
        context.write(u'\n</div>\n\n\n')
        # SOURCE LINE 148
        context.write(u'\n\n')
        return ''
    finally:
        context.caller_stack.pop_frame()


def render_column_two(context):
    context.caller_stack.push_frame()
    try:
        # SOURCE LINE 150
        context.write(u'\n    Nubbles\n')
        return ''
    finally:
        context.caller_stack.pop_frame()


def render_column_one(context):
    context.caller_stack.push_frame()
    try:
        # SOURCE LINE 146
        context.write(u'\n    Hello World!\n')
        return ''
    finally:
        context.caller_stack.pop_frame()


def render_head_tags(context):
    context.caller_stack.push_frame()
    try:
        # SOURCE LINE 2
        context.write(u'\n    <title>Link Saver</title>\n')
        return ''
    finally:
        context.caller_stack.pop_frame()


