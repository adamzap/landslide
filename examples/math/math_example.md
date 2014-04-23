# MathJax Support

---

## Math

To get MathJax rendering, you must:

1. Compile your presentation with the `-m` flag
2. Escape all backslashes in your MathJax markup

So this MathJax markup: `\[ \left( \sum_{k=1}^n a_k b_k \right)^2 \]`

When escaped as this: `\\[ \\left( \\sum_{k=1}^n a_k b_k \\right)^2 \\]`

Renders to this:

\\[ \\left( \\sum_{k=1}^n a_k b_k \\right)^2 \\]
