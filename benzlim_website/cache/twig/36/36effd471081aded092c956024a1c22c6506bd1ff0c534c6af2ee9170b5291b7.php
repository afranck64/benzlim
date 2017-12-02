<?php

/* partials/simplesearch_searchbox.html.twig */
class __TwigTemplate_c58e14c981f1f2262f5a98a9a4b186c3cad91aceb2d6bb30d0883fd653a12ac4 extends Twig_Template
{
    public function __construct(Twig_Environment $env)
    {
        parent::__construct($env);

        $this->parent = false;

        $this->blocks = array(
        );
    }

    protected function doDisplay(array $context, array $blocks = array())
    {
        // line 1
        echo "<input class=\"form-control navbar-search-input\" type=\"text\" placeholder=\"Type your search &amp; hit Enter&hellip;\" value=\"";
        echo ($context["query"] ?? null);
        echo "\" data-search-input";
        if (($context["form2"] ?? null)) {
            echo "2";
        }
        echo "=\"";
        echo ($context["base_url"] ?? null);
        echo $this->getAttribute($this->getAttribute($this->getAttribute(($context["config"] ?? null), "plugins", array()), "simplesearch", array()), "route", array());
        echo "/query\" />
<script>
jQuery(document).ready(function(\$){
    var input = \$('[data-search-input";
        // line 4
        if (($context["form2"] ?? null)) {
            echo "2";
        }
        echo "]');

    input.on('keypress', function(event) {
        if (event.which == 13 && input.val().length > 3) {
            event.preventDefault();
            window.location.href = input.data('search-input";
        // line 9
        if (($context["form2"] ?? null)) {
            echo "2";
        }
        echo "') + '";
        echo $this->getAttribute($this->getAttribute(($context["config"] ?? null), "system", array()), "param_sep", array());
        echo "' + input.val();
        }
    });
});
</script>
";
    }

    public function getTemplateName()
    {
        return "partials/simplesearch_searchbox.html.twig";
    }

    public function isTraitable()
    {
        return false;
    }

    public function getDebugInfo()
    {
        return array (  43 => 9,  33 => 4,  19 => 1,);
    }

    /** @deprecated since 1.27 (to be removed in 2.0). Use getSourceContext() instead */
    public function getSource()
    {
        @trigger_error('The '.__METHOD__.' method is deprecated since version 1.27 and will be removed in 2.0. Use getSourceContext() instead.', E_USER_DEPRECATED);

        return $this->getSourceContext()->getCode();
    }

    public function getSourceContext()
    {
        return new Twig_Source("<input class=\"form-control navbar-search-input\" type=\"text\" placeholder=\"Type your search &amp; hit Enter&hellip;\" value=\"{{ query }}\" data-search-input{% if form2 %}2{% endif %}=\"{{ base_url }}{{ config.plugins.simplesearch.route}}/query\" />
<script>
jQuery(document).ready(function(\$){
    var input = \$('[data-search-input{% if form2 %}2{% endif %}]');

    input.on('keypress', function(event) {
        if (event.which == 13 && input.val().length > 3) {
            event.preventDefault();
            window.location.href = input.data('search-input{% if form2 %}2{% endif %}') + '{{ config.system.param_sep }}' + input.val();
        }
    });
});
</script>
", "partials/simplesearch_searchbox.html.twig", "/Users/aminakbariazirani/Sites/benzlim/user/themes/landio/templates/partials/simplesearch_searchbox.html.twig");
    }
}
