<?php

/* forms/field.html.twig */
class __TwigTemplate_9842e49996bf50d23cfe73854a7b47f759dceae7fbbe68f32f7c72d92c5533aa extends Twig_Template
{
    public function __construct(Twig_Environment $env)
    {
        parent::__construct($env);

        $this->parent = false;

        $this->blocks = array(
            'field' => array($this, 'block_field'),
            'contents' => array($this, 'block_contents'),
            'label' => array($this, 'block_label'),
            'global_attributes' => array($this, 'block_global_attributes'),
            'group' => array($this, 'block_group'),
            'input' => array($this, 'block_input'),
            'input_attributes' => array($this, 'block_input_attributes'),
        );
    }

    protected function doDisplay(array $context, array $blocks = array())
    {
        // line 1
        $context["originalValue"] = ((array_key_exists("originalValue", $context)) ? (($context["originalValue"] ?? null)) : (($context["value"] ?? null)));
        // line 2
        $context["value"] = (((null === ($context["value"] ?? null))) ? ($this->getAttribute(($context["field"] ?? null), "default", array())) : (($context["value"] ?? null)));
        // line 4
        $context["vertical"] = true;
        // line 5
        echo "
";
        // line 6
        $this->displayBlock('field', $context, $blocks);
    }

    public function block_field($context, array $blocks = array())
    {
        // line 7
        echo "    <div class=\"form-field ";
        if (($context["vertical"] ?? null)) {
            echo " vertical";
        }
        echo "\">
        ";
        // line 8
        $this->displayBlock('contents', $context, $blocks);
        // line 57
        echo "    </div>
";
    }

    // line 8
    public function block_contents($context, array $blocks = array())
    {
        // line 9
        echo "            <div class=\"form-label";
        if ( !($context["vertical"] ?? null)) {
            echo " block size-1-3";
        }
        echo "\">
                <label class=\"sr-only\">
                ";
        // line 11
        $this->displayBlock('label', $context, $blocks);
        // line 19
        echo "                </label>
            </div>
            <div class=\"form-data";
        // line 21
        if ( !($context["vertical"] ?? null)) {
            echo " block size-2-3";
        }
        echo "\"
                ";
        // line 22
        $this->displayBlock('global_attributes', $context, $blocks);
        // line 27
        echo "            >
                ";
        // line 28
        $this->displayBlock('group', $context, $blocks);
        // line 55
        echo "            </div>
        ";
    }

    // line 11
    public function block_label($context, array $blocks = array())
    {
        // line 12
        echo "                    ";
        if ($this->getAttribute(($context["field"] ?? null), "help", array())) {
            // line 13
            echo "                    <span class=\"tooltip\" data-asTooltip-position=\"w\" title=\"";
            echo twig_escape_filter($this->env, $this->getAttribute(($context["field"] ?? null), "help", array()));
            echo "\">";
            echo $this->getAttribute(($context["field"] ?? null), "label", array());
            echo "</span>
                    ";
        } else {
            // line 15
            echo "                    ";
            echo $this->getAttribute(($context["field"] ?? null), "label", array());
            echo "
                    ";
        }
        // line 17
        echo "                    ";
        echo ((twig_in_filter($this->getAttribute($this->getAttribute(($context["field"] ?? null), "validate", array()), "required", array()), array(0 => "on", 1 => "true", 2 => 1))) ? ("<span class=\"required\">*</span>") : (""));
        echo "
                ";
    }

    // line 22
    public function block_global_attributes($context, array $blocks = array())
    {
        // line 23
        echo "                data-grav-field=\"";
        echo $this->getAttribute(($context["field"] ?? null), "type", array());
        echo "\"
                data-grav-disabled=\"";
        // line 24
        echo (((null === ($context["originalValue"] ?? null))) ? ("true") : ("false"));
        echo "\"
                data-grav-default=\"";
        // line 25
        echo twig_escape_filter($this->env, twig_jsonencode_filter($this->getAttribute(($context["field"] ?? null), "default", array())), "html_attr");
        echo "\"
                ";
    }

    // line 28
    public function block_group($context, array $blocks = array())
    {
        // line 29
        echo "                    ";
        $this->displayBlock('input', $context, $blocks);
        // line 54
        echo "                ";
    }

    // line 29
    public function block_input($context, array $blocks = array())
    {
        // line 30
        echo "                        <div class=\"form-group has-icon-left form-control-";
        echo $this->env->getExtension('Grav\Common\Twig\TwigExtension')->fieldNameFilter((($context["scope"] ?? null) . $this->getAttribute(($context["field"] ?? null), "name", array())));
        echo " ";
        echo $this->getAttribute(($context["field"] ?? null), "size", array());
        echo "\">
                            <input
                                ";
        // line 33
        echo "                                name=\"";
        echo $this->env->getExtension('Grav\Common\Twig\TwigExtension')->fieldNameFilter((($context["scope"] ?? null) . $this->getAttribute(($context["field"] ?? null), "name", array())));
        echo "\"
                                value=\"";
        // line 34
        echo twig_join_filter(($context["value"] ?? null), ", ");
        echo "\"
                                ";
        // line 36
        echo "                                ";
        $this->displayBlock('input_attributes', $context, $blocks);
        // line 51
        echo "                                />
                        </div>
                    ";
    }

    // line 36
    public function block_input_attributes($context, array $blocks = array())
    {
        // line 37
        echo "                                    ";
        if ($this->getAttribute(($context["field"] ?? null), "classes", array(), "any", true, true)) {
            echo "class=\"";
            echo $this->getAttribute(($context["field"] ?? null), "classes", array());
            echo "\" ";
        }
        // line 38
        echo "                                    ";
        if ($this->getAttribute(($context["field"] ?? null), "id", array(), "any", true, true)) {
            echo "id=\"";
            echo twig_escape_filter($this->env, $this->getAttribute(($context["field"] ?? null), "id", array()));
            echo "\" ";
        }
        // line 39
        echo "                                    ";
        if ($this->getAttribute(($context["field"] ?? null), "style", array(), "any", true, true)) {
            echo "style=\"";
            echo twig_escape_filter($this->env, $this->getAttribute(($context["field"] ?? null), "style", array()));
            echo "\" ";
        }
        // line 40
        echo "                                    ";
        if ($this->getAttribute(($context["field"] ?? null), "disabled", array())) {
            echo "disabled=\"disabled\"";
        }
        // line 41
        echo "                                    ";
        if ($this->getAttribute(($context["field"] ?? null), "placeholder", array())) {
            echo "placeholder=\"";
            echo $this->getAttribute(($context["field"] ?? null), "placeholder", array());
            echo "\"";
        }
        // line 42
        echo "                                    ";
        if (twig_in_filter($this->getAttribute(($context["field"] ?? null), "autofocus", array()), array(0 => "on", 1 => "true", 2 => 1))) {
            echo "autofocus=\"autofocus\"";
        }
        // line 43
        echo "                                    ";
        if (twig_in_filter($this->getAttribute(($context["field"] ?? null), "novalidate", array()), array(0 => "on", 1 => "true", 2 => 1))) {
            echo "novalidate=\"novalidate\"";
        }
        // line 44
        echo "                                    ";
        if (twig_in_filter($this->getAttribute(($context["field"] ?? null), "readonly", array()), array(0 => "on", 1 => "true", 2 => 1))) {
            echo "readonly=\"readonly\"";
        }
        // line 45
        echo "                                    ";
        if (twig_in_filter($this->getAttribute(($context["field"] ?? null), "autocomplete", array()), array(0 => "on", 1 => "off"))) {
            echo "autocomplete=\"";
            echo $this->getAttribute(($context["field"] ?? null), "autocomplete", array());
            echo "\"";
        }
        // line 46
        echo "                                    ";
        if (twig_in_filter($this->getAttribute($this->getAttribute(($context["field"] ?? null), "validate", array()), "required", array()), array(0 => "on", 1 => "true", 2 => 1))) {
            echo "required=\"required\"";
        }
        // line 47
        echo "                                    ";
        if ($this->getAttribute($this->getAttribute(($context["field"] ?? null), "validate", array()), "pattern", array())) {
            echo "pattern=\"";
            echo $this->getAttribute($this->getAttribute(($context["field"] ?? null), "validate", array()), "pattern", array());
            echo "\"";
        }
        // line 48
        echo "                                    ";
        if ($this->getAttribute($this->getAttribute(($context["field"] ?? null), "validate", array()), "message", array())) {
            echo "title=\"";
            echo call_user_func_array($this->env->getFilter('tu')->getCallable(), array(twig_escape_filter($this->env, $this->getAttribute($this->getAttribute(($context["field"] ?? null), "validate", array()), "message", array()))));
            echo "\"
                                    ";
        } elseif ($this->getAttribute(        // line 49
($context["field"] ?? null), "title", array(), "any", true, true)) {
            echo "title=\"";
            echo call_user_func_array($this->env->getFilter('tu')->getCallable(), array(twig_escape_filter($this->env, $this->getAttribute(($context["field"] ?? null), "title", array()))));
            echo "\" ";
        }
        // line 50
        echo "                                ";
    }

    public function getTemplateName()
    {
        return "forms/field.html.twig";
    }

    public function isTraitable()
    {
        return false;
    }

    public function getDebugInfo()
    {
        return array (  257 => 50,  251 => 49,  244 => 48,  237 => 47,  232 => 46,  225 => 45,  220 => 44,  215 => 43,  210 => 42,  203 => 41,  198 => 40,  191 => 39,  184 => 38,  177 => 37,  174 => 36,  168 => 51,  165 => 36,  161 => 34,  156 => 33,  148 => 30,  145 => 29,  141 => 54,  138 => 29,  135 => 28,  129 => 25,  125 => 24,  120 => 23,  117 => 22,  110 => 17,  104 => 15,  96 => 13,  93 => 12,  90 => 11,  85 => 55,  83 => 28,  80 => 27,  78 => 22,  72 => 21,  68 => 19,  66 => 11,  58 => 9,  55 => 8,  50 => 57,  48 => 8,  41 => 7,  35 => 6,  32 => 5,  30 => 4,  28 => 2,  26 => 1,);
    }

    /** @deprecated since 1.27 (to be removed in 2.0). Use getSourceContext() instead */
    public function getSource()
    {
        @trigger_error('The '.__METHOD__.' method is deprecated since version 1.27 and will be removed in 2.0. Use getSourceContext() instead.', E_USER_DEPRECATED);

        return $this->getSourceContext()->getCode();
    }

    public function getSourceContext()
    {
        return new Twig_Source("{% set originalValue = originalValue is defined ? originalValue : value %}
{% set value = (value is null ? field.default : value) %}
{# {% set vertical = field.style == 'vertical' %} #}
{% set vertical = true %}

{% block field %}
    <div class=\"form-field {% if vertical %} vertical{% endif %}\">
        {% block contents %}
            <div class=\"form-label{% if not vertical %} block size-1-3{% endif %}\">
                <label class=\"sr-only\">
                {% block label %}
                    {% if field.help %}
                    <span class=\"tooltip\" data-asTooltip-position=\"w\" title=\"{{ field.help|e }}\">{{ field.label }}</span>
                    {% else %}
                    {{ field.label }}
                    {% endif %}
                    {{ field.validate.required in ['on', 'true', 1] ? '<span class=\"required\">*</span>' }}
                {% endblock %}
                </label>
            </div>
            <div class=\"form-data{% if not vertical %} block size-2-3{% endif %}\"
                {% block global_attributes %}
                data-grav-field=\"{{ field.type }}\"
                data-grav-disabled=\"{{ originalValue is null ? 'true' : 'false' }}\"
                data-grav-default=\"{{ field.default|json_encode()|e('html_attr') }}\"
                {% endblock %}
            >
                {% block group %}
                    {% block input %}
                        <div class=\"form-group has-icon-left form-control-{{ (scope ~ field.name)|fieldName }} {{ field.size }}\">
                            <input
                                {# required attribute structures #}
                                name=\"{{ (scope ~ field.name)|fieldName }}\"
                                value=\"{{ value|join(', ') }}\"
                                {# input attribute structures #}
                                {% block input_attributes %}
                                    {% if field.classes is defined %}class=\"{{ field.classes }}\" {% endif %}
                                    {% if field.id is defined %}id=\"{{ field.id|e }}\" {% endif %}
                                    {% if field.style is defined %}style=\"{{ field.style|e }}\" {% endif %}
                                    {% if field.disabled %}disabled=\"disabled\"{% endif %}
                                    {% if field.placeholder %}placeholder=\"{{ field.placeholder }}\"{% endif %}
                                    {% if field.autofocus in ['on', 'true', 1] %}autofocus=\"autofocus\"{% endif %}
                                    {% if field.novalidate in ['on', 'true', 1] %}novalidate=\"novalidate\"{% endif %}
                                    {% if field.readonly in ['on', 'true', 1] %}readonly=\"readonly\"{% endif %}
                                    {% if field.autocomplete in ['on', 'off'] %}autocomplete=\"{{ field.autocomplete }}\"{% endif %}
                                    {% if field.validate.required in ['on', 'true', 1] %}required=\"required\"{% endif %}
                                    {% if field.validate.pattern %}pattern=\"{{ field.validate.pattern }}\"{% endif %}
                                    {% if field.validate.message %}title=\"{{ field.validate.message|e|tu }}\"
                                    {% elseif field.title is defined %}title=\"{{ field.title|e|tu }}\" {% endif %}
                                {% endblock %}
                                />
                        </div>
                    {% endblock %}
                {% endblock %}
            </div>
        {% endblock %}
    </div>
{% endblock %}
", "forms/field.html.twig", "/Users/aminakbariazirani/Sites/benzlim/user/themes/landio/templates/forms/field.html.twig");
    }
}
