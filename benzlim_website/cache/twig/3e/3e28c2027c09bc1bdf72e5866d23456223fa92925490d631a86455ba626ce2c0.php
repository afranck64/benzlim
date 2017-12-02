<?php

/* partials/form-messages.html.twig */
class __TwigTemplate_3739f8ddec7574e6b5181b472447ecdbf92344f2625f5d765861b2a3a147c071 extends Twig_Template
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
        if ($this->getAttribute(($context["form"] ?? null), "message", array())) {
            // line 2
            echo "    ";
            $context["message"] = ((($this->getAttribute(($context["form"] ?? null), "inline_errors", array()) && $this->getAttribute(($context["form"] ?? null), "messages", array()))) ? ($this->env->getExtension('Grav\Common\Twig\TwigExtension')->translate("FORM.VALIDATION_FAIL")) : ($this->getAttribute(($context["form"] ?? null), "message", array())));
            // line 3
            echo "
    <div class=\"alert notices ";
            // line 4
            echo (($this->getAttribute(($context["form"] ?? null), "message_color", array())) ? ($this->getAttribute(($context["form"] ?? null), "message_color", array())) : ("green"));
            echo "\"><p>";
            echo ($context["message"] ?? null);
            echo "</p></div>
";
        }
    }

    public function getTemplateName()
    {
        return "partials/form-messages.html.twig";
    }

    public function isTraitable()
    {
        return false;
    }

    public function getDebugInfo()
    {
        return array (  27 => 4,  24 => 3,  21 => 2,  19 => 1,);
    }

    /** @deprecated since 1.27 (to be removed in 2.0). Use getSourceContext() instead */
    public function getSource()
    {
        @trigger_error('The '.__METHOD__.' method is deprecated since version 1.27 and will be removed in 2.0. Use getSourceContext() instead.', E_USER_DEPRECATED);

        return $this->getSourceContext()->getCode();
    }

    public function getSourceContext()
    {
        return new Twig_Source("{% if form.message %}
    {% set message = form.inline_errors and form.messages ? \"FORM.VALIDATION_FAIL\"|t : form.message %}

    <div class=\"alert notices {{ form.message_color ?: 'green' }}\"><p>{{ message|raw }}</p></div>
{% endif %}", "partials/form-messages.html.twig", "/Users/aminakbariazirani/Sites/benzlim/user/plugins/form/templates/partials/form-messages.html.twig");
    }
}
