<%inherit file="base.mako"/>
<%def name="head_tags()">
    <title>Yin & Yang Blog</title>
</%def>

<BR />
<BR />
<BR />
${form(url(controller='controller', action='login', method='post'), name="login", id="login")}
<div id="addevent">
Username: ${text_field(name='login-username', id='login-username', value='', size='128')}<BR />
Password: ${text_field(name='login-password', id='login-password', value='', size='128')}<BR />
${submit('Login')}
${end_form()}
</div>

</FORM>
<BR />
<BR />
<BR />