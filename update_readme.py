import os
import re

# ─────────────────────────────────────────────
# CONFIGURAÇÃO — ajuste só aqui
# ─────────────────────────────────────────────
GITHUB_USER = "Leonardo0Arruda"
GITHUB_REPO = "hackerrank-solutions"
GITHUB_BRANCH = "main"
README_PATH = "README.md"

# Mapeamento: "Nome do problema no README" -> "caminho relativo do arquivo .py"
# Adicione novos problemas aqui conforme for resolvendo
SOLUTIONS_MAP = {
    # Python Language Proficiency
    'Say "Hello, World!" With Python': "python/string-formatting/Say Hello, World! With Python.py",
    "Python If-Else":                  "python/string-formatting/Python If-Else.py",
    "Arithmetic Operators":            "python/string-formatting/Arithmetic Operators.py",
    "Python Division":                 "python/string-formatting/Python Division.py",
    "Loops":                           "python/string-formatting/Loops.py",
    "Write a function":                "python/string-formatting/Write a function.py",
    "Print Function":                  "python/string-formatting/Print Function.py",
    "List Comprehensions":             "python/string-formatting/List Comprehensions.py",
    "Find the Runner-Up Score!":       "python/string-formatting/Find the Runner-Up Score!.py",
    "Nested Lists":                    "python/string-formatting/Nested Lists.py",
    "Finding the Percentage":          "python/string-formatting/Finding the Percentage.py",
    "Lists":                           "python/string-formatting/Lists.py",
    "Tuples":                          "python/string-formatting/Tuples.py",

    # String Formatting
    "sWAP cASE":                       "python/string-formatting/sWAP cASE.py",
    "String Split and Join":           "python/string-formatting/String Split and Join.py",
    "What's Your Name?":               "python/string-formatting/namelastname.py",
    "Mutations":                       "python/string-formatting/Mutations.py",
    "Find a string":                   "python/string-formatting/Find a string.py",
    "String Validators":               "python/string-formatting/String Validators.py",
    "Text Alignment":                  "python/string-formatting/Text Alignment.py",
    "Text Wrap":                       "python/string-formatting/Text Wrap.py",
    "Designer Door Mat":               "python/string-formatting/Designer Door Mat.py",
    "String Formatting":               "python/string-formatting/String Formatting.py",
    "Capitalize!":                     "python/string-formatting/Capitalize!.py",
    "The Minion Game":                 "python/string-formatting/The Minion Game.py",
    "Merge the Tools!":                "python/string-formatting/Merge the Tools!.py",
}

def github_link(filepath):
    """Gera o link direto pro arquivo no GitHub."""
    encoded = filepath.replace(" ", "%20")
    return f"https://github.com/{GITHUB_USER}/{GITHUB_REPO}/blob/{GITHUB_BRANCH}/{encoded}"

def file_exists(filepath):
    """Verifica se o arquivo existe localmente."""
    return os.path.isfile(filepath)

def make_check(filepath):
    """Retorna ✅ com link se existir, ou - se não existir."""
    if file_exists(filepath):
        link = github_link(filepath)
        return f"[✅ 1]({link})"
    return "-"

def update_readme():
    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    solved_count = {}  # domain -> count
    total_count = {}   # domain -> total

    current_domain = None
    new_lines = []

    for line in content.splitlines():
        # Detecta cabeçalho de domínio (## ou ###)
        domain_match = re.match(r'^##\s+(.+)', line)
        if domain_match:
            current_domain = domain_match.group(1).strip()
            if current_domain not in solved_count:
                solved_count[current_domain] = 0
                total_count[current_domain] = 0

        # Detecta linhas de tabela com problema
        if line.startswith("|") and current_domain:
            cells = [c.strip() for c in line.split("|")]
            # cells[0] vazio, cells[1]=No, cells[2]=Name, cells[3]=Diff, cells[4]=Score, cells[5]=Solutions, ...
            if len(cells) >= 6 and cells[1].isdigit():
                problem_name_raw = cells[2]
                # Remove links markdown se houver
                problem_name = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', problem_name_raw).strip()

                total_count[current_domain] = total_count.get(current_domain, 0) + 1

                if problem_name in SOLUTIONS_MAP:
                    filepath = SOLUTIONS_MAP[problem_name]
                    check = make_check(filepath)
                    cells[5] = check
                    if check != "-":
                        solved_count[current_domain] = solved_count.get(current_domain, 0) + 1
                    line = "| " + " | ".join(cells[1:]) + " |"
                    # Garante alinhamento mínimo
                    line = re.sub(r'\s*\|\s*', ' | ', line).strip()
                    line = "| " + line[2:] if not line.startswith("| ") else line

        new_lines.append(line)

    new_content = "\n".join(new_lines)

    # Atualiza Progress Summary
    def replace_progress(match):
        domain = match.group(1).strip()
        # Busca pelo domínio em solved_count
        for key in solved_count:
            if domain.lower() in key.lower() or key.lower() in domain.lower():
                s = solved_count[key]
                t = total_count[key]
                return f"| {domain} | {s} | {t} |"
        return match.group(0)

    new_content = re.sub(
        r'\|\s*([^|]+?)\s*\|\s*\d+\s*\|\s*\d+\s*\|',
        replace_progress,
        new_content
    )

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)

    print("✅ README.md atualizado com sucesso!\n")
    print("📊 Resumo:")
    for domain, total in total_count.items():
        solved = solved_count.get(domain, 0)
        bar = "█" * solved + "░" * (total - solved)
        print(f"  {domain[:30]:<30} {bar} {solved}/{total}")

if __name__ == "__main__":
    update_readme()
