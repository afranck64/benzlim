<?php

/* modular/testimonials.html.twig */
class __TwigTemplate_5a7ed12895b7da29436af5aafd297fcc80546db2ab85e6022ba8e1aa9410c27c extends Twig_Template
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
        echo "<section class=\"section-testimonials text-center bg-inverse\">
  <div class=\"container\">
    ";
        // line 3
        echo $this->getAttribute(($context["page"] ?? null), "content", array());
        echo "
    <div id=\"carousel-testimonials\" class=\"carousel slide\" data-ride=\"carousel\" data-interval=\"0\">
      <div class=\"carousel-inner\" role=\"listbox\">
        ";
        // line 6
        $context['_parent'] = $context;
        $context['_seq'] = twig_ensure_traversable($this->getAttribute($this->getAttribute(($context["page"] ?? null), "header", array()), "testimonials", array()));
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
        foreach ($context['_seq'] as $context["_key"] => $context["testimonial"]) {
            // line 7
            echo "        <div class=\"carousel-item ";
            if ($this->getAttribute($context["loop"], "first", array())) {
                echo "active";
            }
            echo "\">
          <blockquote class=\"blockquote\">
            ";
            // line 9
            if ($this->getAttribute($context["testimonial"], "avatar", array())) {
                // line 10
                echo "            <img src=\"";
                echo $this->getAttribute($this->getAttribute($this->getAttribute($this->getAttribute(($context["page"] ?? null), "media", array()), "images", array()), $this->getAttribute($context["testimonial"], "avatar", array()), array(), "array"), "url", array());
                echo "\" alt=\"Avatar\" class=\"img\">
            ";
            }
            // line 12
            echo "            ";
            if ($this->getAttribute($context["testimonial"], "quote", array())) {
                // line 13
                echo "            <p class=\"h3\">";
                echo $this->getAttribute($context["testimonial"], "quote", array());
                echo "</p>
            ";
            }
            // line 15
            echo "            ";
            if ($this->getAttribute($context["testimonial"], "author", array())) {
                // line 16
                echo "            <footer>";
                echo $this->getAttribute($context["testimonial"], "author", array());
                echo "</footer>
            ";
            }
            // line 18
            echo "          </blockquote>
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
        unset($context['_seq'], $context['_iterated'], $context['_key'], $context['testimonial'], $context['_parent'], $context['loop']);
        $context = array_intersect_key($context, $_parent) + $_parent;
        // line 21
        echo "      </div>
      <ol class=\"carousel-indicators\">
        ";
        // line 23
        $context['_parent'] = $context;
        $context['_seq'] = twig_ensure_traversable($this->getAttribute($this->getAttribute(($context["page"] ?? null), "header", array()), "testimonials", array()));
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
        foreach ($context['_seq'] as $context["_key"] => $context["testimonial"]) {
            // line 24
            echo "        ";
            if ($this->getAttribute($context["testimonial"], "avatar", array())) {
                // line 25
                echo "        <li ";
                if ($this->getAttribute($context["loop"], "first", array())) {
                    echo "class=\"active\"";
                }
                echo "><img src=\"";
                echo $this->getAttribute($this->getAttribute($this->getAttribute($this->getAttribute(($context["page"] ?? null), "media", array()), "images", array()), $this->getAttribute($context["testimonial"], "avatar", array()), array(), "array"), "url", array());
                echo "\" alt=\"Navigation avatar\" data-target=\"#carousel-testimonials\" data-slide-to=\"";
                echo $this->getAttribute($context["loop"], "index0", array());
                echo "\" class=\"img-responsive img\"></li>
        ";
            }
            // line 27
            echo "        ";
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
        unset($context['_seq'], $context['_iterated'], $context['_key'], $context['testimonial'], $context['_parent'], $context['loop']);
        $context = array_intersect_key($context, $_parent) + $_parent;
        // line 28
        echo "      </ol>
    </div>
  </div>
</section>
";
    }

    public function getTemplateName()
    {
        return "modular/testimonials.html.twig";
    }

    public function isTraitable()
    {
        return false;
    }

    public function getDebugInfo()
    {
        return array (  146 => 28,  132 => 27,  120 => 25,  117 => 24,  100 => 23,  96 => 21,  80 => 18,  74 => 16,  71 => 15,  65 => 13,  62 => 12,  56 => 10,  54 => 9,  46 => 7,  29 => 6,  23 => 3,  19 => 1,);
    }

    /** @deprecated since 1.27 (to be removed in 2.0). Use getSourceContext() instead */
    public function getSource()
    {
        @trigger_error('The '.__METHOD__.' method is deprecated since version 1.27 and will be removed in 2.0. Use getSourceContext() instead.', E_USER_DEPRECATED);

        return $this->getSourceContext()->getCode();
    }

    public function getSourceContext()
    {
        return new Twig_Source("<section class=\"section-testimonials text-center bg-inverse\">
  <div class=\"container\">
    {{ page.content }}
    <div id=\"carousel-testimonials\" class=\"carousel slide\" data-ride=\"carousel\" data-interval=\"0\">
      <div class=\"carousel-inner\" role=\"listbox\">
        {% for testimonial in page.header.testimonials %}
        <div class=\"carousel-item {% if loop.first %}active{% endif %}\">
          <blockquote class=\"blockquote\">
            {% if testimonial.avatar %}
            <img src=\"{{ page.media.images[testimonial.avatar].url }}\" alt=\"Avatar\" class=\"img\">
            {% endif %}
            {% if testimonial.quote %}
            <p class=\"h3\">{{ testimonial.quote }}</p>
            {% endif %}
            {% if testimonial.author %}
            <footer>{{ testimonial.author }}</footer>
            {% endif %}
          </blockquote>
        </div>
        {% endfor %}
      </div>
      <ol class=\"carousel-indicators\">
        {% for testimonial in page.header.testimonials %}
        {% if testimonial.avatar %}
        <li {% if loop.first %}class=\"active\"{% endif %}><img src=\"{{ page.media.images[testimonial.avatar].url }}\" alt=\"Navigation avatar\" data-target=\"#carousel-testimonials\" data-slide-to=\"{{ loop.index0 }}\" class=\"img-responsive img\"></li>
        {% endif %}
        {% endfor %}
      </ol>
    </div>
  </div>
</section>
", "modular/testimonials.html.twig", "/Users/aminakbariazirani/Sites/benzlim/user/themes/landio/templates/modular/testimonials.html.twig");
    }
}
