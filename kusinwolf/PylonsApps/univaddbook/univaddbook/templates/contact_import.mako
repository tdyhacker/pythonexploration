<%inherit file="base.mako"/>
<%def name="head_tags()">
    <title>Index</title>
</%def>

${h.form(h.url_for(action='csv_import', method='POST'), multipart=True)}
    Select File: ${h.file("contacts",)}
    ${h.submit("Import", "Import")}
${h.end_form()}