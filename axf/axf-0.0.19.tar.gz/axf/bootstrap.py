from tw2.forms.widgets import BaseLayout


class BootstrapFormLayout(BaseLayout):
    inline_engine_name = 'genshi'
    template = '''
<div xmlns:py="http://genshi.edgewall.org/" py:strip="True">
    <py:for each="c in w.children_hidden">
        ${c.display()}
    </py:for>
    <div>
        <span id="${w.compound_id}:error" class="error" >
            <p py:for="error in w.rollup_errors" class="alert alert-danger">
               <span class="glyphicon glyphicon-exclamation-sign"></span>
               ${error}
           </p>
        </span>
    </div>
    <div class="form-horizontal">
        <div py:for="c in w.children_non_hidden"
             class="form-group ${((c.validator and getattr(c.validator, 'required', getattr(c.validator, 'not_empty', False))) and ' required' or '') + (c.error_msg and ' has-error' or '')}">
            <label py:if="c.label != None" class="col-sm-3 control-label" for="${c.compound_id}">
               $c.label
            </label>
            <div class="col-sm-9">
                ${c.display()}
                <span id="${c.compound_id}:error" class="error help-block" py:content="c.error_msg"/>
            </div>
        </div>
    </div>
</div>
'''

    @classmethod
    def post_define(cls):
        for c in getattr(cls, 'children', []):
            if not c.css_class:
                c.css_class = 'form-control'

            if 'form-control' not in c.css_class:
                c.css_class += ' form-control'
