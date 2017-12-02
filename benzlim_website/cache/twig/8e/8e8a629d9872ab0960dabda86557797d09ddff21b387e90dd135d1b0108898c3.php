<?php

/* error.html.twig */
class __TwigTemplate_bfa3b999c63ef349bab9f6d3b5eda7036275327eeb5069f81317e14925168939 extends Twig_Template
{
    public function __construct(Twig_Environment $env)
    {
        parent::__construct($env);

        // line 1
        $this->parent = $this->loadTemplate("partials/base.html.twig", "error.html.twig", 1);
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
        <h1 class=\"arrow\">Error ";
        // line 8
        echo $this->getAttribute($this->getAttribute(($context["page"] ?? null), "header", array()), "http_response_code", array());
        echo "</h1>
        ";
        // line 9
        echo $this->getAttribute(($context["page"] ?? null), "content", array());
        echo "
      </div>
    </div>
  </div>
</section>
";
    }

    // line 15
    public function block_footer($context, array $blocks = array())
    {
    }

    public function getTemplateName()
    {
        return "error.html.twig";
    }

    public function isTraitable()
    {
        return false;
    }

    public function getDebugInfo()
    {
        return array (  58 => 15,  48 => 9,  44 => 8,  38 => 4,  35 => 3,  30 => 2,  11 => 1,);
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
        <h1 class=\"arrow\">Error {{ page.header.http_response_code }}</h1>
        {{ page.content }}
      </div>
    </div>
  </div>
</section>
{% endblock %}
{% block footer %}{% endblock %}
", "error.html.twig", "/Users/aminakbariazirani/Sites/benzlim/user/themes/landio/templates/error.html.twig");
    }
}
