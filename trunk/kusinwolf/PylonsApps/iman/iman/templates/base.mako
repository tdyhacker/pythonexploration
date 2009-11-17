<html>
  <head>
    ${self.head_tags()} <!-- Build out header either by default or overwrite it -->
    <link rel="stylesheet" type="text/css" href="../css/base.css">
    <link rel="stylesheet" type="text/css" href="../../css/base.css">
  </head>
  <body bgcolor="EEEEEE">
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
  <center>
    Local Site Map
    <BR />
    % for page in g.sitemap:
      ${h.link_to(page[0], h.url_for(action=page[1], id=None))} |
    % endfor
    <BR />
    Global Site Map
    <BR />
    % for page in g.externallinks:
      ${h.link_to(page[0], h.url_for(controller=page[1].get("controller", None), action=page[1].get("action", None), id=page[1].get("id", None)))} |
    % endfor
  </center>
</%def>