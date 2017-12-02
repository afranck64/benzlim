<?php

/* @Var:Thank you for your feedback! */
class __TwigTemplate_248a302f11566253dcd3bb5dfea08733f9276c19d8f2acc90e48146dfe08c88c extends Twig_Template
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
        echo "Thank you for your feedback!";
    }

    public function getTemplateName()
    {
        return "@Var:Thank you for your feedback!";
    }

    public function getDebugInfo()
    {
        return array (  19 => 1,);
    }

    /** @deprecated since 1.27 (to be removed in 2.0). Use getSourceContext() instead */
    public function getSource()
    {
        @trigger_error('The '.__METHOD__.' method is deprecated since version 1.27 and will be removed in 2.0. Use getSourceContext() instead.', E_USER_DEPRECATED);

        return $this->getSourceContext()->getCode();
    }

    public function getSourceContext()
    {
        return new Twig_Source("Thank you for your feedback!", "@Var:Thank you for your feedback!", "");
    }
}
