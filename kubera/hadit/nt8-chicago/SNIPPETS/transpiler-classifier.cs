// Verbatim excerpt from NinjaScript.Transpiler/Program.cs (build-host copy).
// This is pure C#-source classification logic used to catalog NinjaScript files
// (Strategy / Indicator / AddOn) by their base type and enumerate their public
// methods. It contains no trading rules, parameters, or strategy logic — it is
// the tool that reads strategy source files, not one of the strategies itself.

static string DetectKind(List<string> baseTypes)
{
    if (baseTypes.Any(b => b.EndsWith("Strategy") || b == "Strategy"))
        return "Strategy";

    if (baseTypes.Any(b => b.EndsWith("Indicator") || b == "Indicator"))
        return "Indicator";

    if (baseTypes.Any(b => b.EndsWith("AddOnBase") || b == "AddOnBase"))
        return "AddOn";

    return "Unknown";
}

static List<string> ExtractMethods(ClassDeclarationSyntax cls)
{
    return cls.Members
        .OfType<MethodDeclarationSyntax>()
        .Select(m => m.Identifier.Text)
        .Distinct()
        .OrderBy(x => x)
        .ToList();
}
