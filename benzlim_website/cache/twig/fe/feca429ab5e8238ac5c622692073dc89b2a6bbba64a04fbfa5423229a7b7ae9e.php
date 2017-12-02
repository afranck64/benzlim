<?php

/* modular/features.html.twig */
class __TwigTemplate_46171b01753586c66d1e917eda748f7cfa7ffd0e6f20ef3d8e0dbd01fa5e47b2 extends Twig_Template
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
        echo "<section id=\"features\" class=\"section-features text-center\">
    <div class=\"container\">
        <div class=\"row\">
            ";
        // line 4
        echo $this->getAttribute(($context["page"] ?? null), "content", array());
        echo "
            <div class=\"features-wrapper\">
                ";
        // line 6
        $context['_parent'] = $context;
        $context['_seq'] = twig_ensure_traversable($this->getAttribute($this->getAttribute(($context["page"] ?? null), "header", array()), "features", array()));
        foreach ($context['_seq'] as $context["_key"] => $context["item"]) {
            // line 7
            echo "                <div class=\"col-md-4\">
                    <div class=\"card\">
                        <div class=\"card-block\">
                            ";
            // line 10
            if ($this->getAttribute($context["item"], "icon", array())) {
                // line 11
                echo "                                <span class=\"icon-";
                echo $this->getAttribute($context["item"], "icon", array());
                echo "\"></span>
                            ";
            }
            // line 13
            echo "                            ";
            if ($this->getAttribute($context["item"], "title", array())) {
                // line 14
                echo "                                <h4 class=\"card-title\">";
                echo $this->getAttribute($context["item"], "title", array());
                echo "</h4>
                            ";
            }
            // line 16
            echo "                            ";
            if ($this->getAttribute($context["item"], "subtitle", array())) {
                // line 17
                echo "                                <h6 class=\"card-subtitle text-muted\">";
                echo $this->getAttribute($context["item"], "subtitle", array());
                echo "</h6>
                            ";
            }
            // line 19
            echo "                            ";
            if ($this->getAttribute($context["item"], "text", array())) {
                // line 20
                echo "                                <p class=\"card-text\">";
                echo $this->getAttribute($context["item"], "text", array());
                echo "</p>
                            ";
            }
            // line 22
            echo "                        </div>
                    </div>
                </div>
                ";
        }
        $_parent = $context['_parent'];
        unset($context['_seq'], $context['_iterated'], $context['_key'], $context['item'], $context['_parent'], $context['loop']);
        $context = array_intersect_key($context, $_parent) + $_parent;
        // line 26
        echo "            </div>
        </div>
    </div>
</section>
";
    }

    public function getTemplateName()
    {
        return "modular/features.html.twig";
    }

    public function isTraitable()
    {
        return false;
    }

    public function getDebugInfo()
    {
        return array (  82 => 26,  73 => 22,  67 => 20,  64 => 19,  58 => 17,  55 => 16,  49 => 14,  46 => 13,  40 => 11,  38 => 10,  33 => 7,  29 => 6,  24 => 4,  19 => 1,);
    }

    /** @deprecated since 1.27 (to be removed in 2.0). Use getSourceContext() instead */
    public function getSource()
    {
        @trigger_error('The '.__METHOD__.' method is deprecated since version 1.27 and will be removed in 2.0. Use getSourceContext() instead.', E_USER_DEPRECATED);

        return $this->getSourceContext()->getCode();
    }

    public function getSourceContext()
    {
        return new Twig_Source("<section id=\"features\" class=\"section-features text-center\">
    <div class=\"container\">
        <div class=\"row\">
            {{ page.content }}
            <div class=\"features-wrapper\">
                {% for item in page.header.features %}
                <div class=\"col-md-4\">
                    <div class=\"card\">
                        <div class=\"card-block\">
                            {% if item.icon %}
                                <span class=\"icon-{{ item.icon }}\"></span>
                            {% endif %}
                            {% if item.title %}
                                <h4 class=\"card-title\">{{ item.title }}</h4>
                            {% endif %}
                            {% if item.subtitle %}
                                <h6 class=\"card-subtitle text-muted\">{{ item.subtitle }}</h6>
                            {% endif %}
                            {% if item.text %}
                                <p class=\"card-text\">{{ item.text }}</p>
                            {% endif %}
                        </div>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>
    </div>
</section>
", "modular/features.html.twig", "/Users/aminakbariazirani/Sites/benzlim/user/themes/landio/templates/modular/features.html.twig");
    }
}
