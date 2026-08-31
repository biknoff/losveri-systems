# Snippets

Only one snippet is included: `transpiler-classifier.cs`, a verbatim excerpt from the
surviving NinjaScript transpiler's source classifier. It shows the mechanism (parse
NinjaScript C# source, detect Strategy/Indicator/AddOn by base type, enumerate methods)
with no trading logic in it.

A second snippet was deliberately not added. Everything else recoverable from this
project — strategy source, ATM templates, analyzer-log contents, the Chicago pipeline
description document — either encodes strategy identity/rules directly, or (in one case)
turned out to contain live credentials rather than clean pipeline description. Rather
than produce a second "safe-looking" excerpt by picking around those constraints, this
directory states plainly: one clean snippet exists, and it is here.
