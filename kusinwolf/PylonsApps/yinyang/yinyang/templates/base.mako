<html>
  <head>
    ${self.head_tags()} <!-- Build out header either by default or overwrite it -->
    ${h.javascript_include_tag(builtins=True)}
    <link href="/css/base.css" rel="stylesheet" type="text/css">
  </head>
  <body>
    ${next.body()}
    <BR />
    <div id='footer'>
        ${self.footer()} <!-- Build out footer either by default or overwrite it -->
    </div>
  </body>
</html>

<!-- Default assigned tags that if not defined throw an error -->

<%def name="head_tags()">
    <title>Default Name</title>
</%def>

<%def name="footer()">
    Site Map
    <BR />
    :D
</%def>
