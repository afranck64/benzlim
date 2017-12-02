<?php

/* modular/form.html.twig */
class __TwigTemplate_c0f9ce366335a5b91ed3ece28e31cc054e39750817fd4b65035cfc4b371c9321 extends Twig_Template
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
        echo "<section class=\"section-signup bg-faded\">
  <div class=\"container\">
    ";
        // line 3
        echo $this->getAttribute(($context["page"] ?? null), "content", array());
        echo "

    <div class=\"col-md-8 col-md-offset-2 col-xl-6 col-xl-offset-3\">
    \t<div class=\"row\">
        \t";
        // line 7
        $this->loadTemplate("forms/form.html.twig", "modular/form.html.twig", 7)->display($context);
        // line 8
        echo "        </div>
    </div>
  </div>
</section>
";
    }

    public function getTemplateName()
    {
        return "modular/form.html.twig";
    }

    public function isTraitable()
    {
        return false;
    }

    public function getDebugInfo()
    {
        return array (  32 => 8,  30 => 7,  23 => 3,  19 => 1,);
    }

    /** @deprecated since 1.27 (to be removed in 2.0). Use getSourceContext() instead */
    public function getSource()
    {
        @trigger_error('The '.__METHOD__.' method is deprecated since version 1.27 and will be removed in 2.0. Use getSourceContext() instead.', E_USER_DEPRECATED);

        return $this->getSourceContext()->getCode();
    }

    public function getSourceContext()
    {
        return new Twig_Source("<section class=\"section-signup bg-faded\">
  <div class=\"container\">
    {{ page.content }}

    <div class=\"col-md-8 col-md-offset-2 col-xl-6 col-xl-offset-3\">
    \t<div class=\"row\">
        \t{% include \"forms/form.html.twig\" %}
        </div>
    </div>
  </div>
</section>
", "modular/form.html.twig", "/Users/aminakbariazirani/Sites/benzlim/user/themes/landio/templates/modular/form.html.twig");
    }
}
