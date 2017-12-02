<?php

/* modular/text.html.twig */
class __TwigTemplate_43aabf322be70e99566b1cc5097bf55eef496daceef4d8d3330951d121edfaba extends Twig_Template
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
        echo "<section class=\"section-text\">
  <div class=\"container\">
    ";
        // line 3
        echo $this->getAttribute(($context["page"] ?? null), "content", array());
        echo "
    ";
        // line 4
        $context['_parent'] = $context;
        $context['_seq'] = twig_ensure_traversable(twig_array_batch($this->getAttribute($this->getAttribute(($context["page"] ?? null), "header", array()), "text", array()), 2));
        foreach ($context['_seq'] as $context["_key"] => $context["row"]) {
            // line 5
            echo "    <div class=\"row p-y-lg\">
      ";
            // line 6
            $context['_parent'] = $context;
            $context['_seq'] = twig_ensure_traversable($context["row"]);
            $context['loop'] = array(
              'parent' => $context['_parent'],
              'index0' => 0,
              'index'  => 1,
              'first'  => true,
            );
            if (is_array($context['_seq']) || (is_object($context['_seq']) && $context['_seq'] instanceof Countable)) {
                $length = count($context['_seq']);
                $context['loop']['revindex0'] = $length - 1;
                $context['loop']['revindex'] = $length;
                $context['loop']['length'] = $length;
                $context['loop']['last'] = 1 === $length;
            }
            foreach ($context['_seq'] as $context["_key"] => $context["text"]) {
                // line 7
                echo "      <div class=\"col-md-5 ";
                if ( !$this->getAttribute($context["loop"], "first", array())) {
                    echo "col-md-offset-2 separator-x";
                }
                echo "\">
        <p class=\"wp ";
                // line 8
                if ($this->getAttribute($context["text"], "css_suffix", array())) {
                    echo $this->getAttribute($context["text"], "css_suffix", array());
                }
                echo "\">
          ";
                // line 9
                echo $this->getAttribute($context["text"], "content", array());
                echo "
        </p>
      </div>
      ";
                ++$context['loop']['index0'];
                ++$context['loop']['index'];
                $context['loop']['first'] = false;
                if (isset($context['loop']['length'])) {
                    --$context['loop']['revindex0'];
                    --$context['loop']['revindex'];
                    $context['loop']['last'] = 0 === $context['loop']['revindex0'];
                }
            }
            $_parent = $context['_parent'];
            unset($context['_seq'], $context['_iterated'], $context['_key'], $context['text'], $context['_parent'], $context['loop']);
            $context = array_intersect_key($context, $_parent) + $_parent;
            // line 13
            echo "    </div>
    ";
        }
        $_parent = $context['_parent'];
        unset($context['_seq'], $context['_iterated'], $context['_key'], $context['row'], $context['_parent'], $context['loop']);
        $context = array_intersect_key($context, $_parent) + $_parent;
        // line 15
        echo "  </div>
</div>
</section>
";
    }

    public function getTemplateName()
    {
        return "modular/text.html.twig";
    }

    public function isTraitable()
    {
        return false;
    }

    public function getDebugInfo()
    {
        return array (  89 => 15,  82 => 13,  64 => 9,  58 => 8,  51 => 7,  34 => 6,  31 => 5,  27 => 4,  23 => 3,  19 => 1,);
    }

    /** @deprecated since 1.27 (to be removed in 2.0). Use getSourceContext() instead */
    public function getSource()
    {
        @trigger_error('The '.__METHOD__.' method is deprecated since version 1.27 and will be removed in 2.0. Use getSourceContext() instead.', E_USER_DEPRECATED);

        return $this->getSourceContext()->getCode();
    }

    public function getSourceContext()
    {
        return new Twig_Source("<section class=\"section-text\">
  <div class=\"container\">
    {{ page.content }}
    {% for row in page.header.text|batch(2) %}
    <div class=\"row p-y-lg\">
      {% for text in row %}
      <div class=\"col-md-5 {% if not loop.first %}col-md-offset-2 separator-x{% endif %}\">
        <p class=\"wp {% if text.css_suffix %}{{ text.css_suffix }}{% endif %}\">
          {{ text.content }}
        </p>
      </div>
      {% endfor %}
    </div>
    {% endfor %}
  </div>
</div>
</section>
", "modular/text.html.twig", "/Users/aminakbariazirani/Sites/benzlim/user/themes/landio/templates/modular/text.html.twig");
    }
}
