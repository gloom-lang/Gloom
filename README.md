# Gloom

Gloom is a hardcore language for building extreme systems, designed from the ground up for getting real work done. Unlike other languages that supposedly provide safety and reliability (aka bureaucratic paperwork), Gloom embraces the idea that there's an element of danger in most things worth doing. Hence all computations in Gloom have side effects. So little as printing an object changes its state. In blending operations and consequences, the Gloom language forces developers to become acutely mindful of their actions and the immediate repercussions those actions have on their systems.

Gloom's philosophy hinges on the belief that programming, much like life itself, is messy, unpredictable, and filled with risks. Rather than hiding from these realities, Gloom programmers are encouraged to master them. This brutal approach may not be for the faint of heart, but for those who crave raw, unfiltered interaction with their code, Gloom offers an unparalleled experience.

# Status

This is in early stages. Currently this repository is more of a playground to work out the language's semantics, so nothing here really works at the moment.

# Grammar (tentative)

```ebnf
    program = { statement }
    statement = message_send "."
    message_send = receiver { argument } 
    receiver = "(" message_send ")" | value
    argument = named_parameter | binary_parameter | unary_parameter
    unary_parameter = ":" name
    named_parameter = ":" parameter_name value
    binary_parameter = operator value
    operator = "+" | "-" | "," | "*" | "/" | "%"
    value = literal | name | "(" message_send ")"
    literal = number | string | boolean | array
    array = "(" { literal }")"
    name = letter { letter | digit }
```

# Disclaimer

This is all intended to be silly -- Gloom is an artlang and learning project. Please use whatever guardrails make sense for your use-case. Guardrails like types and memory safety are nice because people make mistakes. Please be nice to each other 