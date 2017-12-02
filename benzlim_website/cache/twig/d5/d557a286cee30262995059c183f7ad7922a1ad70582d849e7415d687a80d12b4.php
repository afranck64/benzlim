<?php

/* formdata.html.twig */
class __TwigTemplate_2840575fbc429c70d9a5e2f530832a9b50466dbcb44cb78b19842db9659c2557 extends Twig_Template
{
    public function __construct(Twig_Environment $env)
    {
        parent::__construct($env);

        // line 1
        $this->parent = $this->loadTemplate("partials/base.html.twig", "formdata.html.twig", 1);
        $this->blocks = array(
            'header' => array($this, 'block_header'),
            'content' => array($this, 'block_content'),
            'footer' => array($this, 'block_footer'),
        );
    }

    protected function doGetParent(array $context)
    {
        return "partials/base.html.twig";
    }

    protected function doDisplay(array $context, array $blocks = array())
    {
        $this->parent->display($context, array_merge($this->blocks, $blocks));
    }

    // line 2
    public function block_header($context, array $blocks = array())
    {
    }

    // line 3
    public function block_content($context, array $blocks = array())
    {
        // line 4
        echo "<section class=\"section-text\">
    <div class=\"container\">
        <div class=\"row text-center\">
            <div class=\"col-md-8 col-xl-4 col-xl-offset-4\">
              <h2>";
        // line 8
        echo $this->getAttribute(($context["form"] ?? null), "message", array());
        echo "</h2>
              ";
        // line 9
        echo ($context["content"] ?? null);
        echo "

              ";
        // line 11
        $this->loadTemplate("forms/data.html.twig", "formdata.html.twig", 11)->display($context);
        // line 12
        echo "            </div>
        </div>
    </div>
</div>
</section>
";
    }

    // line 18
    public function block_footer($context, array $blocks = array())
    {
    }

    public function getTemplateName()
    {
        return "formdata.html.twig";
    }

    public function isTraitable()
    {
        return false;
    }

    public function getDebugInfo()
    {
        return array (  64 => 18,  55 => 12,  53 => 11,  48 => 9,  44 => 8,  38 => 4,  35 => 3,  30 => 2,  11 => 1,);
    }

    /** @deprecated since 1.27 (to be removed in 2.0). Use getSourceContext() instead */
    public function getSource()
    {
        @trigger_error('The '.__METHOD__.' method is deprecated since version 1.27 and will be removed in 2.0. Use getSourceContext() instead.', E_USER_DEPRECATED);

        return $this->getSourceContext()->getCode();
    }

    public function getSourceContext()
    {
        return new Twig_Source("{% extends 'partials/base.html.twig' %}
{% block header %}{% endblock %}
{% block content %}
<section class=\"section-text\">
    <div class=\"container\">
        <div class=\"row text-center\">
            <div class=\"col-md-8 col-xl-4 col-xl-offset-4\">
              <h2>{{ form.message }}</h2>
              {{ content }}

              {% include \"forms/data.html.twig\" %}
            </div>
        </div>
    </div>
</div>
</section>
{% endblock %}
{% block footer %}{% endblock %}
", "formdata.html.twig", "/Users/aminakbariazirani/Sites/benzlim/user/themes/landio/templates/formdata.html.twig");
    }
}
