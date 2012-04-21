<%inherit file="base.mako" />
<%block name="title">
% if survey:
<title>${survey.title}</title>
% else:
<title>Survey application</title>
% endif
</%block>
<%block name="head">
<script type="text/javascript" src="${request.static_url('survey:static/js/jquery.validate.min.js')}"></script>
% if survey:
<script type="text/javascript">
$(document).ready (function () {
    $('#survey_${survey.id}').validate ({
        rules: {
        % for q in survey.questions:
            question_${q.id}: 'required',
        % endfor
        }
    });
    $('#survey_${survey.id}').submit (function () {
        if ($('#survey_${survey.id}').valid () ) {
            return confirm ('Are you sure?');
        }
        else {
            $('#survey_${survey.id}').validate ();
            $('input[type="radio"]').removeClass ('error');
            return false;
        }
    });
});
</script>
% endif
</%block>
<div class="survey_container">
    % for m in messages:
    <div class="${m['type']}">${m['message']}</div>
    % endfor
    % if survey:
    <h1>${survey.title}</h1>
    <form id="survey_${survey.id}" action="" method="post">
        <fieldset>
            % for q in survey_form:
            <div class="question">
                <h3>${q.label.text}</h3>
                <label style="display: none;" for="${q.name}" class="error">This question is required</label>
                % if q.errors:
                % for e in q.errors:
                <label for="${q.name}" class="error">${e}</label>
                % endfor
                % endif
                <p>
                % for c in q:
                ${c} ${c.label}<br />
                % endfor
                </p>
            </div>
            % endfor
            <button class="button" type="submit" name="submit">Submit response</button>
        </fieldset>
    </form>
    % endif
</div>
