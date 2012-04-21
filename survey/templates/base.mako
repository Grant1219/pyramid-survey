<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
    <head>
        <%block name="title">
        <title>Survey application</title>
        </%block>
        <meta http-equiv="Content-Type" content="text/html;charset=utf-8" />
        <meta name="keywords" content="survey" />
        <meta name="description" content="survey" />
        <link rel="shortcut icon" href="${request.static_url('survey:static/favicon.ico')}" />
        <link rel="stylesheet" href="${request.static_url('survey:static/blueprint/screen.css')}" type="text/css" media="screen, projection" />
        <link rel="stylesheet" href="${request.static_url('survey:static/blueprint/plugins/buttons/screen.css')}" type="text/css" media="screen, projection" />
        <link rel="stylesheet" href="${request.static_url('survey:static/blueprint/print.css')}" type="text/css" media="print" />
        <link rel="stylesheet" href="${request.static_url('survey:static/survey.css')}" type="text/css" media="screen, projection" />
        <!--[if lt IE 8]>
        <link rel="stylesheet" href="${request.static_url('survey:static/blueprint/ie.css')}" type="text/css" media="screen, projection" />
        <![endif]-->
        <script type="text/javascript" src="${request.static_url('survey:static/js/jquery-1.7.2.min.js')}"></script>
        <%block name="head">
        </%block>
    </head>
    <body>
    ${next.body ()}
    </body>
</html>
