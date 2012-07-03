<%inherit file="base.mako" />
<%block name="head">
<link rel="stylesheet" href="${request.static_url ('survey:static/js/tablesorter_themes/blue/style.css')}" type="text/css" media="screen, projection" />
<script src="${request.static_url ('survey:static/js/jquery.tablesorter.min.js')}" type="text/javascript"></script>
<script type="text/javascript">
$(document).ready (function () {
    $('#result_list').tablesorter ( { headers: { 4: { sorter: false } } } );
});
</script>
</%block>
<div class="admin_container">
    %if results:
    <h1>Result list</h1>
    <table id="result_list" class="tablesorter">
        <thead>
            <tr>
            <th>First name</th>
            <th>Last name</th>
            <th>Email</th>
            <th>Date/time submitted</th>
            <th>Actions</th>
            </tr>
        </thead>
        <tbody>
        %for r in results:
            %if r.submit_datetime:
            <tr>
            <td>${r.user.first_name}</a></td>
            <td>${r.user.last_name}</td>
            <td>${r.user.email}</td>
            <td>${r.submit_datetime}</td>
            <td>
                <a class="button negative" href="/admin/result/delete/${r.id}" onclick="return confirm ('Are you sure you want to delete this user\'s response?');">Delete result</a>
            </td>
            </tr>
            %endif
        %endfor
        </tbody>
    </table>
    %else:
    <div class="error">The survey does not exist</div>
    %endif
</div>
