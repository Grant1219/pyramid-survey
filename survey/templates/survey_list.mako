<%inherit file="base.mako" />
<%block name="head">
<link rel="stylesheet" href="${request.static_url ('survey:static/js/tablesorter_themes/blue/style.css')}" type="text/css" media="screen, projection" />
<script src="${request.static_url ('survey:static/js/jquery.tablesorter.min.js')}" type="text/javascript"></script>
<script type="text/javascript">
$(document).ready (function () {
    $('#survey_list').tablesorter ( { headers: { 5: { sorter: false } } } );
});
</script>
</%block>
<div class="admin_container">
    <h1>Survey list</h1>
    <table id="survey_list" class="tablesorter">
        <thead>
            <tr>
            <th>Title</th>
            <th>Date/time created</th>
            <th>Open date/time</th>
            <th>Close date/time</th>
            <th>Actions</th>
            </tr>
        </thead>
        <tbody>
        % for s in surveys:
            <tr>
            <td><a href="/admin/results/list/${s.id}">${s.title}</a></td>
            <td>${s.created_datetime}</td>
            <td>${s.open_datetime}</td>
            <td>${s.close_datetime}</td>
            <td>
                % if not s.open_datetime:
                <a class="button" href="/admin/survey/open/${s.id}">Open survey</a>
                % elif not s.close_datetime:
                <a class="button" href="/admin/survey/close/${s.id}">Close survey</a>
                % endif
                <a class="button" href="/admin/survey/export/users/${s.id}">Export users</a>
                <a class="button" href="/admin/survey/export/results/${s.id}">Export results</a>
                <a class="button negative" href="/admin/survey/delete/${s.id}" onclick="return confirm ('Are you sure you want to delete this survey and all results?');">Delete survey</a>
            </td>
            </tr>
        % endfor
        </tbody>
    </table>
</div>
