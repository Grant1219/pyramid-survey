<%!
from itertools import izip
%>
<%inherit file="base.mako" />
<%block name="title">
%if survey:
<title>${survey.title}</title>
%else:
<title>Survey application</title>
%endif
</%block>
<%block name="head">
<script type="text/javascript" src="${request.static_url('survey:static/js/jquery.validate.min.js')}"></script>
%if survey:
<script type="text/javascript">
$(document).ready (function () {
    $('#survey_${survey.id}').validate ({
        rules: {
        %for q in survey.questions:
            ${q.question_type}_question_${q.id}: 'required',
        %endfor
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
%endif
</%block>
<div class="survey_container">
    %for m in messages:
    <div class="${m['type']}">${m['message']}</div>
    %endfor
    %if survey:
    <h1>${survey.title}</h1>
    <form id="survey_${survey.id}" action="" method="post">
        <fieldset>
            %for q, q2 in izip (survey_form, survey.questions):
            <div class="question">
                <h3>${q.label.text}</h3>
                <label style="display: none;" for="${q.name}" class="error">This question is required</label>
                %if q.errors:
                %for e in q.errors:
                <label for="${q.name}" class="error">${e}</label>
                %endfor
                %endif
                <p>
                %if q2.question_type == 'choice':
                %for c in q:
                ${c} ${c.label}<br />
                %endfor
                %elif q2.question_type == 'text':
                ${q}
                %endif
                </p>
            </div>
            %endfor
            <button class="button" type="submit" name="submit">Submit response</button>
        </fieldset>
    </form>
    %endif
</div>
