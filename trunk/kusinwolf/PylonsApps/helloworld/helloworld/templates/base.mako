<html>
  <head>
    ${self.head_tags()}
    ${h.javascript_include_tag(builtins=True)}
    <link href="/css/hello.css" rel="stylesheet" type="text/css">
  </head>
  <body>
    ${next.body()}
    <BR>
    <div id='footer'>
        ${self.footer()}
    </div>
  </body>
</html>

<!-- Default assigned tags that if not defined throw an error -->

<%def name="head_tags()">
    <title>Default Name</title>
</%def>

<%def name="footer()">
    Site Map
    <BR>
    [ ${h.link_to("Index", h.url(controller="hello", action=""))} ]
    - [ ${h.link_to("All Links", h.url(controller="hello", action="allLinks"))} ]
    - [ ${h.link_to("Search Tags", h.url(controller="hello", action="search"))} ]
    - [ ${h.link_to("Tags", h.url(controller="hello", action="stats"))} ]
</%def>
