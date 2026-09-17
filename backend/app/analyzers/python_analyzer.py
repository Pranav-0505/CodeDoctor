import ast
import re

from typing import List, Dict, Any, Set

from app.analyzers.base import BaseAnalyzer
from app.schemas.error_model import (
    DiagnosticItem,
    SeverityLevel,
    ErrorCategory,
)


class PythonAnalyzer(BaseAnalyzer):

    @property
    def language(self) -> str:
        return "python"

    def analyze(
        self,
        code: str,
        file_path: str = "snippet.py"
    ) -> List[DiagnosticItem]:

        diagnostics: List[DiagnosticItem] = []

        # ---------------------------------------------------------
        # 1. Syntax Check via AST
        # ---------------------------------------------------------
        parsed_ast = None

        try:
            parsed_ast = ast.parse(code, filename=file_path)

        except SyntaxError as se:
            diagnostics.append(
                DiagnosticItem(
                    id=f"PY-SYNTAX-{se.lineno or 1}-{se.offset or 1}",
                    rule_id="PY-E901",
                    language="python",
                    file=file_path,
                    line=se.lineno or 1,
                    column=se.offset or 1,
                    severity=SeverityLevel.CRITICAL,
                    category=ErrorCategory.SYNTAX,
                    title="Python Syntax Error",
                    message=str(
                        se.msg or "Invalid python syntax"
                    ),
                    root_cause=(
                        f"Syntax Error on line {se.lineno}: "
                        f"'{se.text.strip() if se.text else ''}'"
                    ),
                    explanation=(
                        "Python could not parse this statement because "
                        "of invalid syntax structure, missing punctuation, "
                        "or unbalanced brackets."
                    ),
                    impact="Code cannot compile or execute.",
                    confidence=1.0,
                    suggested_fix=(
                        "Fix the syntax error on line "
                        + str(se.lineno)
                    ),
                    corrected_code=None,
                    verification_status="UNVERIFIED",
                    is_root_cause=True,
                )
            )

            return diagnostics

        # ---------------------------------------------------------
        # 2. AST Visitor Checks
        # ---------------------------------------------------------
        if parsed_ast:
            visitor = PythonAstVisitor(code, file_path)
            visitor.visit(parsed_ast)
            diagnostics.extend(visitor.diagnostics)

        # ---------------------------------------------------------
        # 3. Regex / Pattern Checks
        # ---------------------------------------------------------
        pattern_diagnostics = self._run_pattern_checks(
            code,
            file_path
        )

        diagnostics.extend(pattern_diagnostics)

        return diagnostics

    def _run_pattern_checks(
        self,
        code: str,
        file_path: str
    ) -> List[DiagnosticItem]:

        items: List[DiagnosticItem] = []

        lines = code.splitlines()

        for idx, line in enumerate(lines, 1):

            stripped = line.strip()

            # -----------------------------------------------------
            # Security: Hardcoded API Key or Secret
            # -----------------------------------------------------
            if re.search(
                r'(api_key|secret|password|passwd|auth_token)\s*=\s*["\'][A-Za-z0-9_\-]{8,}["\']',
                stripped,
                re.IGNORECASE
            ):
                variable_name = (
                    line.split("=")[0].strip()
                    if "=" in line
                    else "SECRET"
                )

                items.append(
                    DiagnosticItem(
                        id=f"SEC-SECRET-{idx}",
                        rule_id="SEC-001",
                        language="python",
                        file=file_path,
                        line=idx,
                        column=1,
                        severity=SeverityLevel.HIGH,
                        category=ErrorCategory.SECURITY,
                        title="Exposed Hardcoded Secret / API Key",
                        message=(
                            "Hardcoded password, API key, or "
                            "authentication token detected."
                        ),
                        root_cause=(
                            "Sensitive secrets are hardcoded "
                            "in source code."
                        ),
                        explanation=(
                            "Storing secrets directly in code leads "
                            "to dangerous data leaks if committed "
                            "to source control."
                        ),
                        impact=(
                            "Potential unauthorized access or "
                            "privilege escalation."
                        ),
                        confidence=0.9,
                        suggested_fix=(
                            "Load secret from environment variable "
                            "using os.getenv('SECRET_KEY')"
                        ),
                        corrected_code=(
                            "import os\n"
                            f'{variable_name} = '
                            f'os.getenv("{variable_name.upper()}", "")'
                        ),
                        verification_status="UNVERIFIED",
                        is_root_cause=True,
                    )
                )

            # -----------------------------------------------------
            # Security: SQL Injection
            # -----------------------------------------------------
            if re.search(
                r'(SELECT|INSERT|UPDATE|DELETE|FROM|WHERE)\b.*\b(f["\']|\.format\(|%\s*)',
                stripped,
                re.IGNORECASE
            ):
                items.append(
                    DiagnosticItem(
                        id=f"SEC-SQLI-{idx}",
                        rule_id="SEC-002",
                        language="python",
                        file=file_path,
                        line=idx,
                        column=1,
                        severity=SeverityLevel.CRITICAL,
                        category=ErrorCategory.SECURITY,
                        title="Potential SQL Injection Vulnerability",
                        message=(
                            "Dynamic SQL query construction using "
                            "string interpolation."
                        ),
                        root_cause=(
                            "User input formatted directly into "
                            "raw SQL query string."
                        ),
                        explanation=(
                            "Directly interpolating variables into SQL "
                            "strings allows attacker-controlled input "
                            "to modify SQL query logic."
                        ),
                        impact=(
                            "Database corruption, unauthorized data "
                            "exfiltration, authentication bypass."
                        ),
                        confidence=0.95,
                        suggested_fix=(
                            "Use parameterized SQL queries with "
                            "placeholders like (?) or (:param)"
                        ),
                        corrected_code=(
                            '# Use parameterized query:\n'
                            'cursor.execute('
                            '"SELECT * FROM users WHERE name = ?", '
                            '(username,))'
                        ),
                        verification_status="UNVERIFIED",
                        is_root_cause=True,
                    )
                )

            # -----------------------------------------------------
            # Security: Debug mode exposed
            # -----------------------------------------------------
            if (
                "debug=True" in stripped
                and "app.run" in stripped
            ):
                items.append(
                    DiagnosticItem(
                        id=f"SEC-DEBUG-{idx}",
                        rule_id="SEC-003",
                        language="python",
                        file=file_path,
                        line=idx,
                        column=1,
                        severity=SeverityLevel.MEDIUM,
                        category=ErrorCategory.SECURITY,
                        title="Flask / Web App Debug Mode Exposed",
                        message=(
                            "Application server started with "
                            "debug=True enabled."
                        ),
                        root_cause=(
                            "Debug flag explicitly enabled in "
                            "application launch code."
                        ),
                        explanation=(
                            "Debug mode in production exposes "
                            "interactive code execution endpoints "
                            "and full stack traces to external users."
                        ),
                        impact=(
                            "Remote code execution risks in "
                            "production environments."
                        ),
                        confidence=1.0,
                        suggested_fix=(
                            "Set debug=False or retrieve debug mode "
                            "from environment variable."
                        ),
                        corrected_code=line.replace(
                            "debug=True",
                            "debug=os.getenv("
                            "'FLASK_DEBUG', 'False') == 'True'"
                        ),
                        verification_status="UNVERIFIED",
                        is_root_cause=True,
                    )
                )

        return items


class PythonAstVisitor(ast.NodeVisitor):

    def __init__(
        self,
        code: str,
        file_path: str
    ):
        self.code = code
        self.file_path = file_path
        self.lines = code.splitlines()

        self.diagnostics: List[DiagnosticItem] = []

        # ---------------------------------------------------------
        # Track defined variables
        # ---------------------------------------------------------
        self.known_variables: Set[str] = set()

        # ---------------------------------------------------------
        # Track imported modules
        # ---------------------------------------------------------
        self.imported_modules: Set[str] = set()

        # ---------------------------------------------------------
        # Track simple constant values
        #
        # Example:
        #     y = 0
        #     x / y
        # ---------------------------------------------------------
        self.constant_values: Dict[str, Any] = {}

        # ---------------------------------------------------------
        # Track variables known to be non-zero inside a guard.
        #
        # Example:
        #     if y != 0:
        #         x / y
        #
        # Inside the if body, y is known to be non-zero.
        # ---------------------------------------------------------
        self.nonzero_variables: Set[str] = set()

    # =============================================================
    # IMPORTS
    # =============================================================

    def visit_Import(self, node: ast.Import):

        for alias in node.names:
            self.imported_modules.add(
                alias.asname or alias.name
            )

        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom):

        for alias in node.names:
            self.imported_modules.add(
                alias.asname or alias.name
            )

        self.generic_visit(node)

    # =============================================================
    # ASSIGNMENTS
    # =============================================================

    def visit_Assign(self, node: ast.Assign):

        # Track defined variable names
        for target in node.targets:

            if isinstance(target, ast.Name):
                self.known_variables.add(target.id)

        # ---------------------------------------------------------
        # Track simple constant assignments.
        #
        # Example:
        #     y = 0
        #
        # This allows detection of:
        #     x / y
        # ---------------------------------------------------------
        if (
            len(node.targets) == 1
            and isinstance(node.targets[0], ast.Name)
        ):

            target_name = node.targets[0].id

            if (
                isinstance(node.value, ast.Constant)
                and isinstance(
                    node.value.value,
                    (int, float, complex)
                )
                and not isinstance(
                    node.value.value,
                    bool
                )
            ):

                self.constant_values[target_name] = (
                    node.value.value
                )

            elif target_name in self.constant_values:

                # Variable was reassigned to a non-constant
                # expression, so forget its previous value.
                del self.constant_values[target_name]

        # ---------------------------------------------------------
        # Static list assignment length.
        #
        # Example:
        #     numbers = [10, 20, 30]
        # ---------------------------------------------------------
        if (
            len(node.targets) == 1
            and isinstance(node.targets[0], ast.Name)
            and isinstance(node.value, ast.List)
        ):

            var_name = node.targets[0].id
            list_len = len(node.value.elts)

            setattr(
                self,
                f"_len_{var_name}",
                list_len
            )

        self.generic_visit(node)

    # =============================================================
    # IF / CONTROL FLOW
    # =============================================================

    def visit_If(self, node: ast.If):
        """
        Understand simple non-zero guards.

        Example:

            y = 0

            if y != 0:
                result = x / y

        The division is protected by the condition, so the
        analyzer must not report LOGIC-001 inside that block.
        """

        # ---------------------------------------------------------
        # Detect:
        #
        #     if variable != 0:
        # ---------------------------------------------------------
        if (
            isinstance(node.test, ast.Compare)
            and len(node.test.ops) == 1
            and isinstance(
                node.test.ops[0],
                ast.NotEq
            )
            and isinstance(
                node.test.left,
                ast.Name
            )
            and len(node.test.comparators) == 1
            and isinstance(
                node.test.comparators[0],
                ast.Constant
            )
            and node.test.comparators[0].value == 0
        ):

            variable_name = node.test.left.id

            was_already_protected = (
                variable_name
                in self.nonzero_variables
            )

            self.nonzero_variables.add(
                variable_name
            )

            # Visit the protected body.
            for statement in node.body:
                self.visit(statement)

            # Restore previous state.
            if not was_already_protected:
                self.nonzero_variables.discard(
                    variable_name
                )

            # The else branch does NOT have the
            # non-zero guarantee.
            for statement in node.orelse:
                self.visit(statement)

            return

        # ---------------------------------------------------------
        # All other if statements use normal AST traversal.
        # ---------------------------------------------------------
        self.generic_visit(node)

    # =============================================================
    # SUBSCRIPT / INDEX CHECK
    # =============================================================

    def visit_Subscript(self, node: ast.Subscript):

        # Predictive Index Error Detection
        #
        # Example:
        #
        #     numbers = [10, 20, 30]
        #     numbers[5]

        if (
            isinstance(node.value, ast.Name)
            and isinstance(node.slice, ast.Constant)
        ):

            var_name = node.value.id
            index_val = node.slice.value

            known_len = getattr(
                self,
                f"_len_{var_name}",
                None
            )

            if (
                known_len is not None
                and isinstance(index_val, int)
            ):

                if (
                    index_val >= known_len
                    or index_val < -known_len
                ):

                    self.diagnostics.append(
                        DiagnosticItem(
                            id=(
                                f"PRED-INDEX-"
                                f"{node.lineno}-"
                                f"{node.col_offset}"
                            ),
                            rule_id="PRED-001",
                            language="python",
                            file=self.file_path,
                            line=node.lineno,
                            column=node.col_offset + 1,
                            severity=SeverityLevel.HIGH,
                            category=ErrorCategory.RUNTIME,
                            title=(
                                "Predictive IndexError: "
                                "Out-of-bounds Array/List Access"
                            ),
                            message=(
                                f"Index {index_val} is accessed while "
                                f"statically known list '{var_name}' "
                                f"length is {known_len}."
                            ),
                            root_cause=(
                                f"List '{var_name}' has length "
                                f"{known_len}, valid indices are "
                                f"0 to {known_len - 1}."
                            ),
                            explanation=(
                                f"An index is the position of an item "
                                f"in a list. Your list has {known_len} "
                                f"items, so valid positions are "
                                f"0 to {known_len - 1}."
                            ),
                            impact=(
                                "Will raise IndexError at runtime "
                                "when executed."
                            ),
                            confidence=0.92,
                            suggested_fix=(
                                f"Use a valid index (< {known_len}) "
                                f"or check len({var_name}) "
                                f"before indexing."
                            ),
                            corrected_code=(
                                f"if len({var_name}) > {index_val}:\n"
                                f"    value = "
                                f"{var_name}[{index_val}]"
                            ),
                            verification_status="UNVERIFIED",
                            is_root_cause=True,
                        )
                    )

        self.generic_visit(node)

    # =============================================================
    # BINARY OPERATIONS
    # =============================================================

    def visit_BinOp(self, node: ast.BinOp):

        # ZeroDivisionError check
        #
        # Handles:
        #
        #     x / 0
        #     x // 0
        #     x % 0
        #
        # And:
        #
        #     y = 0
        #     x / y

        if isinstance(
            node.op,
            (
                ast.Div,
                ast.FloorDiv,
                ast.Mod,
            )
        ):

            # -----------------------------------------------------
            # Case 1: Direct constant zero
            # -----------------------------------------------------
            if (
                isinstance(
                    node.right,
                    ast.Constant
                )
                and node.right.value == 0
            ):

                self.diagnostics.append(
                    DiagnosticItem(
                        id=(
                            f"LOGIC-ZERODIV-"
                            f"{node.lineno}-"
                            f"{node.col_offset}"
                        ),
                        rule_id="LOGIC-001",
                        language="python",
                        file=self.file_path,
                        line=node.lineno,
                        column=node.col_offset + 1,
                        severity=SeverityLevel.CRITICAL,
                        category=ErrorCategory.LOGIC,
                        title="Division by Zero Error",
                        message=(
                            "Division or modulo operation with "
                            "constant divisor 0."
                        ),
                        root_cause=(
                            "Divisor expression evaluates "
                            "statically to zero."
                        ),
                        explanation=(
                            "Dividing any number by zero is "
                            "mathematically undefined and raises "
                            "ZeroDivisionError in Python."
                        ),
                        impact=(
                            "Crash with ZeroDivisionError exception."
                        ),
                        confidence=1.0,
                        suggested_fix=(
                            "Ensure divisor is non-zero before "
                            "performing division."
                        ),
                        corrected_code=None,
                        verification_status="UNVERIFIED",
                        is_root_cause=True,
                    )
                )

            # -----------------------------------------------------
            # Case 2: Variable whose value is known to be zero
            # -----------------------------------------------------
            elif isinstance(
                node.right,
                ast.Name
            ):

                divisor_name = node.right.id

                divisor_value = (
                    self.constant_values.get(
                        divisor_name
                    )
                )

                # IMPORTANT:
                #
                # If the variable is protected by:
                #
                #     if y != 0:
                #
                # then do not report LOGIC-001.
                #
                if (
                    divisor_value == 0
                    and divisor_name
                    not in self.nonzero_variables
                ):

                    self.diagnostics.append(
                        DiagnosticItem(
                            id=(
                                f"LOGIC-ZERODIV-"
                                f"{node.lineno}-"
                                f"{node.col_offset}"
                            ),
                            rule_id="LOGIC-001",
                            language="python",
                            file=self.file_path,
                            line=node.lineno,
                            column=node.col_offset + 1,
                            severity=SeverityLevel.CRITICAL,
                            category=ErrorCategory.LOGIC,
                            title="Division by Zero Error",
                            message=(
                                f"Division or modulo operation uses "
                                f"variable '{divisor_name}' whose "
                                f"value is 0."
                            ),
                            root_cause=(
                                f"Variable '{divisor_name}' is "
                                f"assigned the constant value 0."
                            ),
                            explanation=(
                                "The divisor is known to be zero, "
                                "so this operation will raise "
                                "ZeroDivisionError in Python."
                            ),
                            impact=(
                                "Crash with ZeroDivisionError "
                                "exception."
                            ),
                            confidence=1.0,
                            suggested_fix=(
                                f"Ensure '{divisor_name}' is "
                                f"non-zero before performing "
                                f"the operation."
                            ),
                            corrected_code=None,
                            verification_status="UNVERIFIED",
                            is_root_cause=True,
                        )
                    )

        self.generic_visit(node)

    # =============================================================
    # FUNCTION CALL SECURITY CHECK
    # =============================================================

    def visit_Call(self, node: ast.Call):

        # Unsafe Command Execution Security Check

        func_name = ""

        if isinstance(node.func, ast.Name):

            func_name = node.func.id

        elif isinstance(node.func, ast.Attribute):

            func_name = (
                f"{getattr(node.func.value, 'id', '')}."
                f"{node.func.attr}"
            )

        if func_name in (
            "eval",
            "exec",
            "os.system",
        ):

            self.diagnostics.append(
                DiagnosticItem(
                    id=(
                        f"SEC-EXEC-"
                        f"{node.lineno}-"
                        f"{node.col_offset}"
                    ),
                    rule_id="SEC-004",
                    language="python",
                    file=self.file_path,
                    line=node.lineno,
                    column=node.col_offset + 1,
                    severity=SeverityLevel.CRITICAL,
                    category=ErrorCategory.SECURITY,
                    title="Unsafe Command Execution",
                    message=(
                        f"Use of dangerous function "
                        f"'{func_name}' detected."
                    ),
                    root_cause=(
                        "Direct invocation of dynamic "
                        "code/command execution call "
                        f"'{func_name}'."
                    ),
                    explanation=(
                        "Executing arbitrary code via eval/exec "
                        "or OS commands can allow full remote "
                        "code execution."
                    ),
                    impact=(
                        "Complete system compromise if user "
                        "input is passed."
                    ),
                    confidence=0.98,
                    suggested_fix=(
                        "Replace with safe specific functions "
                        "or subprocess with shell=False."
                    ),
                    corrected_code=None,
                    verification_status="UNVERIFIED",
                    is_root_cause=True,
                )
            )

        self.generic_visit(node)

    # =============================================================
    # FOR LOOP / PERFORMANCE CHECK
    # =============================================================

    def visit_For(self, node: ast.For):

        # Performance Doctor:
        # Deeply Nested Loops Check

        depth = self._get_loop_depth(node)

        if depth >= 3:

            self.diagnostics.append(
                DiagnosticItem(
                    id=f"PERF-NESTEDLOOP-{node.lineno}",
                    rule_id="PERF-001",
                    language="python",
                    file=self.file_path,
                    line=node.lineno,
                    column=node.col_offset + 1,
                    severity=SeverityLevel.MEDIUM,
                    category=ErrorCategory.PERFORMANCE,
                    title=(
                        "Deeply Nested Loops "
                        "(O(N^3) Time Complexity)"
                    ),
                    message=(
                        f"Detected {depth}-level nested "
                        f"loop structure."
                    ),
                    root_cause=(
                        "Algorithm uses triple-nested loop "
                        "iterations over collections."
                    ),
                    explanation=(
                        f"Nested loops create exponential time "
                        f"complexity (O(N^{depth})). As list sizes "
                        f"grow, performance degrades drastically."
                    ),
                    impact=(
                        "High CPU utilization and severe "
                        "execution slowdowns."
                    ),
                    confidence=0.95,
                    suggested_fix=(
                        "Refactor using hashtables (dicts/sets), "
                        "list comprehensions, or vectorized operations."
                    ),
                    corrected_code=None,
                    verification_status="UNVERIFIED",
                    is_root_cause=True,
                )
            )

        self.generic_visit(node)

    # =============================================================
    # LOOP DEPTH
    # =============================================================

    def _get_loop_depth(
        self,
        node: ast.AST,
        current_depth: int = 1
    ) -> int:

        max_depth = current_depth

        for child in ast.iter_child_nodes(node):

            if isinstance(
                child,
                (
                    ast.For,
                    ast.While,
                )
            ):

                depth = self._get_loop_depth(
                    child,
                    current_depth + 1
                )

                if depth > max_depth:
                    max_depth = depth

        return max_depth