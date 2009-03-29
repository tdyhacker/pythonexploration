<%inherit file="base.mako"/>
<%def name="head_tags()">
    <title>Tons of tests all at once</title>
    ${h.javascript_include_tag(builtins=True)}
</%def>
What?
${c.helloobj.serverinfo()}


${from helloworld.model import meta}

Is this?
<BR>

<%
    context.write("some programmatic text")
    some = "Thing"
    id = "Quake"
    one = ['two', 'three', 'four']
    context.write("<BR>")
    context.write(some)
    g.params = request.params
    "What?"
%>

<%
    context.write("there is some%s missing here" % some)
%>

<FORM action="/" method="POST" name="Selection">
${
"""<input type="text" value="%s" id="SSO Name" name="SSO Name" size='30'>""" % c.name
}
<BR><BR>

%try:
    ${"""<input type="text" value="%s" id="link" name="link" size='128'>""" % g.params['link']}
%except:
    ${"""<input type="text" value="" id="link" name="link" size='128'>"""}
%endtry
<BR><BR>

%try:

${c.helloobj.strip()}
${"""<a href="%s">%s</a>""" % (c.link, c.link)}
${meta.Session.save(Links(g.params['link'], c.link, c.songname))}
${meta.Session.commit()}

%except:

<!-- Did Nothing with strip()-->

%endtry

<BR><BR>

<select NAME="Catch Phrase">
% for name in g.message:
    %try:
        %if request.params['Catch Phrase']:
            %if request.params['Catch Phrase'] == name:
                ${"""<option selected="selected">%s</option>""" % name}
            %else:
                ${"""<option>%s</option>""" % name}
            %endif
        %endif
    %except:
        ${"""<option>%s</option>""" % name}
    %endtry
% endfor
</select>
<BR><BR>
${request.params}
<BR><BR>
<input type="submit" value="Select">
</FORM>
${c.helloobj.paramParse()}
${h.link_to('alan', h.url(controller='whatever', action='show', id=1))}
${h.link_to_remote("Info!", dict(update="responsebox", url=h.url_for(action='paramParse')))}
${h.link_to_remote("ping!", dict(update="pongbox", url=h.url_for(action='pong'), complete=h.visual_effect('Highlight', "pongbox", duration=1)))} 
<div id="pongbox"></div>
<div id="responsebox"></div>
<BR>
${c.helloobj.counter()}
<BR>
<FONT size='10'>
%try:
    %if request.params['Font']:
        ${"<FONT size='%s'>" % request.params['Font']}
    %endif
%except:
    <FONT size='3'>
%endtry
%try:
    %if request.params['Catch Phrase']:
        ${"<p>%s, " % request.params['Catch Phrase']}
    %endif
    %try:
        %if request.params['SSO Name']:
            ${"%s?</p>" % request.params['SSO Name']}
        %endif
    %except:
        </p>
    %endtry
%except:
    <!-- Do nothing -->
%endtry
</FONT>

<!--
<BR><BR>
${session}
<BR>
<BR>
${request.cookies}
<BR>
<BR>
${h.url_for('SSO Name', id = 'SSO Name')}
<BR>
<BR>
${request.params}
<BR>
<BR>
<BR>
% for a in request.headers:
    ${a}:
    ${request.headers[a]}
    <BR>
    <BR>
% endfor
<BR>

<p>The WSGI environ:<br />
<pre>${c.envy}</pre>
</p>

<h2>
Server info for ${request.host}
</h2>

<p>
The URL you called: ${h.url_for()}
</p>

<p>Hi there ${c.name or c.full_name or "Joe Smith"}</p>

<p>
The name you set: ${c.name or g.name}
</p>
-->

<BR>
<FONT size='3'>
% try:
    % for link in Session.query(Links):
${link}
<BR>
    % endfor
% except:
No Links
% endtry
</FONT>