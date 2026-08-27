# Build PentUI — Nmap TUI MVP

You are building the first working version of a terminal-based security tool launcher called **PentUI**.

For this stage, implement **ONLY the Nmap section** and the generic architecture required to support it later.

Do not implement SQLMap, Metasploit, FFUF, Gobuster, Nikto, Hydra, or any other tool yet.

The application must be written in **Python** and use **Textual** for the TUI.

The goal is to create a clean, modular foundation where additional tools can later be added without rewriting the UI architecture.

---

## 1. Core UI concept

The application has separate screens.

### Screen 1 — Tool Selection

When PentUI starts, show a tool-selection screen:

```text
╭──────────────────────────────────────────────────────────────╮
│                         PENTUI                                │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│   SELECT TOOL                                                │
│                                                              │
│   > Nmap                                                     │
│     SQLMap              Coming soon                          │
│     FFUF                Coming soon                          │
│     Metasploit          Coming soon                          │
│                                                              │
├──────────────────────────────────────────────────────────────┤
│ ↑↓ Navigate    ENTER Select    Q Quit                        │
╰──────────────────────────────────────────────────────────────╯
```

For now, only Nmap needs to actually work.

The other tools can appear as disabled/coming-soon entries, but do not implement their functionality.

---

# 2. IMPORTANT SCREEN BEHAVIOR

When the user selects Nmap, **do not keep the tool list visible**.

The entire screen must transition into the Nmap configuration screen.

Do NOT use a permanent split layout such as:

```text
TOOLS             OPTIONS
Nmap              [ ] -sV
SQLMap             [ ] -Pn
FFUF               ...
```

That is NOT what I want.

Instead:

```text
Tool Selection
      ↓
select Nmap
      ↓
Nmap Configuration Screen
```

The Nmap screen should occupy the full TUI.

The user can return to the tool-selection screen with `Esc`.

---

# 3. Nmap configuration screen

The screen should look approximately like this:

```text
╭──────────────────────────────────────────────────────────────╮
│ NMAP CONFIGURATION                                           │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│ COMMAND                                                      │
│ ──────────────────────────────────────────────────────────── │
│ nmap                                                         │
│                                                              │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│ SCAN TECHNIQUES                                              │
│                                                              │
│ [ ] -sS    TCP SYN scan                                      │
│ [ ] -sT    TCP connect scan                                  │
│ [ ] -sU    UDP scan                                          │
│ [ ] -sA    TCP ACK scan                                      │
│                                                              │
│ HOST DISCOVERY                                               │
│                                                              │
│ [ ] -Pn    Treat hosts as online; skip host discovery       │
│ [ ] -sn    Host discovery only                               │
│                                                              │
│ SERVICE / VERSION                                            │
│                                                              │
│ [ ] -sV    Detect service and version information             │
│                                                              │
│ OS DETECTION                                                 │
│                                                              │
│ [ ] -O     Enable operating-system detection                 │
│                                                              │
│ PORTS                                                         │
│                                                              │
│ [ ] -p     Specify ports                                     │
│                                                              │
├──────────────────────────────────────────────────────────────┤
│ TARGET                                                       │
│ >                                                               │
├──────────────────────────────────────────────────────────────┤
│ SPACE Select   ENTER Edit   R Run   ESC Back   Q Quit        │
╰──────────────────────────────────────────────────────────────╯
```

The exact visual styling can be improved, but preserve the basic UX.

---

# 4. Command preview

The command preview at the top is a core feature.

Initially:

```text
COMMAND
nmap
```

If the user selects:

```text
[✓] -Pn
```

the command preview immediately becomes:

```text
nmap -Pn
```

If they then select:

```text
[✓] -sV
```

it becomes:

```text
nmap -Pn -sV
```

If they add ports:

```text
-p 80,443
```

it becomes:

```text
nmap -Pn -sV -p 80,443
```

If they finally enter:

```text
192.168.1.10
```

it becomes:

```text
nmap -Pn -sV -p 80,443 192.168.1.10
```

The preview must update **reactively after every change**.

Do not require the user to press a separate "Build Command" button.

---

# 5. Do NOT represent the command internally as one string

Internally maintain structured state.

For example:

```python
CommandState(
    executable="nmap",
    arguments={
        "no_ping": True,
        "service_version": True,
        "ports": "80,443",
    },
    targets=["192.168.1.10"],
)
```

Then have a dedicated command builder convert that state into:

```python
[
    "nmap",
    "-Pn",
    "-sV",
    "-p",
    "80,443",
    "192.168.1.10",
]
```

The displayed command can then be rendered as:

```text
nmap -Pn -sV -p 80,443 192.168.1.10
```

The executor must use the argument list rather than passing an arbitrary shell command string to a shell.

---

# 6. Generic argument-definition system

Do not hard-code Nmap-specific UI logic into the widgets.

Create generic models such as:

```text
ToolDefinition
ArgumentDefinition
CommandState
```

An `ArgumentDefinition` should support at least:

```text
id
flag
type
description
required
default
choices
placeholder
group
```

Supported argument types should include:

```text
boolean
string
integer
enum
filepath
target
```

The UI should render the correct input widget based on the argument type.

---

# 7. Store Nmap options in a definition file

Do NOT put the complete list of Nmap arguments directly inside the UI code.

Create something such as:

```text
tools/
    nmap.yaml
```

The application loads this file at runtime.

The YAML should contain the Nmap metadata and arguments.

Example:

```yaml
name: nmap
display_name: Nmap
executable: nmap

arguments:

  - id: syn_scan
    flag: "-sS"
    type: boolean
    group: "Scan Techniques"
    description: "TCP SYN scan"

  - id: tcp_connect
    flag: "-sT"
    type: boolean
    group: "Scan Techniques"
    description: "TCP connect scan"

  - id: udp_scan
    flag: "-sU"
    type: boolean
    group: "Scan Techniques"
    description: "UDP scan"

  - id: no_ping
    flag: "-Pn"
    type: boolean
    group: "Host Discovery"
    description: "Treat hosts as online; skip host discovery"

  - id: service_version
    flag: "-sV"
    type: boolean
    group: "Service / Version"
    description: "Detect service and version information"

  - id: os_detection
    flag: "-O"
    type: boolean
    group: "OS Detection"
    description: "Enable operating-system detection"

  - id: ports
    flag: "-p"
    type: string
    group: "Ports"
    description: "Specify ports to scan"
    placeholder: "80,443"

  - id: target
    type: target
    group: "Target"
    description: "Host, IP, domain, or network range"
    required: true
```

The exact YAML schema can be improved if necessary, but keep it generic enough to support future tools.

---

# 8. Checkbox behavior

For boolean arguments:

```text
[ ] -sV    Detect service and version information
```

Pressing Space should change it to:

```text
[✓] -sV    Detect service and version information
```

and immediately update the command preview.

Pressing Space again should deselect it and remove the flag from the command.

Keyboard navigation must work naturally with arrow keys.

---

# 9. Arguments requiring input

This behavior is extremely important.

If an option requires a value, selecting it must immediately request the value.

For example:

```text
[ ] -p    Specify ports
```

When the user presses Space:

```text
┌─────────────────────────────────────────────┐
│ Specify ports                               │
├─────────────────────────────────────────────┤
│                                             │
│ Ports:                                      │
│ > 80,443,8080                               │
│                                             │
│             CANCEL          OK              │
└─────────────────────────────────────────────┘
```

After valid input:

```text
[✓] -p    Specify ports
```

and:

```text
nmap -p 80,443,8080
```

If the user cancels or enters invalid data, do not mark the checkbox as selected.

This means the application should conceptually perform:

```text
User selects option
        ↓
Determine whether option requires input
        ↓
No ────────────────→ Select option
        │
       Yes
        ↓
Open input modal
        ↓
Validate input
        ↓
Valid ─────────────→ Store value + select option
        │
      Invalid
        ↓
Show error
        ↓
Keep option unselected
```

---

# 10. Target input

The target should be a dedicated field rather than just another flag.

For example:

```text
TARGET
────────────────────────────────────────────

Target:
> 192.168.1.10
```

The command should not be considered ready to execute until a target is supplied.

Support basic targets such as:

```text
192.168.1.10
192.168.1.0/24
example.com
```

Do not attempt to build an overly complicated target parser for the MVP.

Basic validation is sufficient.

---

# 11. Nmap options for the MVP

Implement a useful but manageable initial set.

Organize them into groups.

### Scan Techniques

```text
-sS    TCP SYN scan
-sT    TCP connect scan
-sU    UDP scan
-sA    TCP ACK scan
```

### Host Discovery

```text
-Pn    Treat hosts as online; skip host discovery
-sn    Host discovery only
```

### Port Specification

```text
-p     Specify ports
-F     Fast scan
```

### Service / Version Detection

```text
-sV    Detect service/version information
```

### OS Detection

```text
-O     Enable OS detection
```

### Timing

Implement `-T` as an enum:

```text
0
1
2
3
4
5
```

Display descriptions for the choices if practical.

### Output

Implement at least:

```text
-oN    Normal output file
-oX    XML output file
```

These should request a filepath when selected.

Do not attempt to implement every Nmap flag in the first version.

The architecture must make it easy to add the rest later through `nmap.yaml`.

---

# 12. Argument dependencies

The architecture must support arguments that require values.

For example:

```text
-p
-T
-oN
-oX
```

must not simply append the flag.

They require:

```text
flag + value
```

The generic command builder should know how to construct these.

For example:

```text
-p
value="80,443"
```

becomes:

```text
-p 80,443
```

Do not hard-code this behavior specifically for `-p`.

---

# 13. Tool detection

When PentUI starts, detect whether Nmap exists.

Use Python functionality such as:

```python
shutil.which("nmap")
```

If installed:

```text
Nmap       ✓ installed
```

If not installed:

```text
Nmap       ✗ not installed
```

Do not automatically install Nmap.

If Nmap is unavailable and the user selects it, show a clear error.

---

# 14. Execution

Implement a basic execution engine.

When the user presses:

```text
R
```

the application should validate the configuration first.

If valid, execute the generated argument list.

For example:

```python
[
    "nmap",
    "-Pn",
    "-sV",
    "-p",
    "80,443",
    "192.168.1.10"
]
```

Do not use:

```python
subprocess.run(command_string, shell=True)
```

Use a safe argument-array approach.

The process should run asynchronously so that the TUI does not freeze.

---

# 15. Execution screen

When Nmap runs, switch to an execution/output screen.

Example:

```text
╭──────────────────────────────────────────────────────────────╮
│ NMAP — RUNNING                                               │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│ $ nmap -Pn -sV -p 80,443 192.168.1.10                       │
│                                                              │
│ Starting Nmap...                                             │
│ Nmap scan report for 192.168.1.10                            │
│ Host is up.                                                  │
│                                                              │
│ PORT    STATE    SERVICE                                     │
│ 80/tcp  open     http                                        │
│ 443/tcp open     https                                       │
│                                                              │
├──────────────────────────────────────────────────────────────┤
│ Q Stop    ESC Back                                           │
╰──────────────────────────────────────────────────────────────╯
```

Stream stdout and stderr into the output view.

The TUI must remain responsive while Nmap executes.

---

# 16. Validation

Before running:

```text
Command
↓
Validation
↓
Execution
```

The validator should check:

1. Nmap executable exists.
2. Required target exists.
3. Required option values exist.
4. Integer fields contain valid integers.
5. Enum values are valid.
6. Filepath fields are not empty.
7. No argument has an invalid state.

Display useful errors.

Example:

```text
Cannot run Nmap:

Target is required.
```

or:

```text
Invalid port specification.
```

Do not silently fix malformed user input.

---

# 17. Back navigation

From Nmap:

```text
ESC
```

must return to the tool-selection screen.

The Nmap configuration should preferably remain in memory when returning, so if the user enters Nmap again during the same application session, their current configuration can be restored.

Do not persist it to disk yet.

---

# 18. Keyboard controls

Implement predictable keyboard controls:

```text
↑ / ↓       Navigate
SPACE       Select / deselect checkbox
ENTER       Edit/input selected option
R           Run
ESC         Back
Q           Quit
```

If Textual's normal widget behavior makes some of these mappings unnecessary, preserve the intended UX.

---

# 19. Code organization

Use a structure similar to:

```text
pentui/
│
├── main.py
│
├── core/
│   ├── models.py
│   ├── tool_loader.py
│   ├── command_builder.py
│   ├── validator.py
│   └── executor.py
│
├── tui/
│   ├── app.py
│   │
│   ├── screens/
│   │   ├── tool_selection.py
│   │   ├── nmap_config.py
│   │   └── execution.py
│   │
│   └── widgets/
│       ├── command_preview.py
│       ├── argument_item.py
│       ├── argument_list.py
│       ├── input_modal.py
│       └── target_input.py
│
├── tools/
│   └── nmap.yaml
│
├── tests/
│   ├── test_command_builder.py
│   ├── test_validator.py
│   └── test_tool_loader.py
│
├── requirements.txt
└── README.md
```

You may modify the structure if you have a better architecture, but maintain clear separation between:

```text
TUI
Core logic
Tool definitions
Execution
```

---

# 20. Testing requirements

Before considering the MVP complete, test at least:

### Command builder

Input:

```text
sV=True
Pn=True
ports="80,443"
target="192.168.1.10"
```

Expected:

```text
nmap -sV -Pn -p 80,443 192.168.1.10
```

### Empty target

Expected:

```text
validation failure
```

### Boolean deselection

Selecting and then deselecting `-Pn` must remove it from the generated command.

### Parameterized option

Selecting `-p` without providing a value must not result in:

```text
nmap -p
```

### Invalid enum

An invalid `-T` value must be rejected.

### Missing executable

If `nmap` cannot be found, execution must be blocked with a useful message.

---

# 21. Important implementation constraint

Do NOT over-engineer the first version.

I want a **working Nmap TUI MVP**, not a giant unfinished security framework.

Do NOT implement:

- SQLMap
- Metasploit
- plugin marketplaces
- automatic installation
- vulnerability databases
- exploit automation
- credential attacks
- report generation
- cloud integrations
- web dashboards
- complicated database systems

Those are future phases.

Build the foundation correctly.

---

# 22. Definition of done

The MVP is complete when I can run:

```text
python main.py
```

and:

1. See the PentUI tool-selection screen.
2. Select Nmap.
3. Have the entire screen transition to the Nmap options screen.
4. No tool list remains visible on the Nmap screen.
5. Navigate through Nmap options.
6. Select boolean flags with Space.
7. Immediately see the command preview update.
8. Select a parameterized option such as `-p`.
9. Receive an input modal.
10. Enter a value.
11. Have the option become selected only after valid input.
12. See the generated command update immediately.
13. Enter a target.
14. See the target appear in the command preview.
15. Press R.
16. Have the command validated.
17. Have Nmap execute asynchronously.
18. See live Nmap output.
19. Return with ESC.
20. Return to the tool-selection screen.
21. Have the architecture remain generic enough that another tool can later be added by creating another tool definition rather than rewriting the entire application.

Prioritize correctness, clean architecture, responsive TUI behavior, and maintainability over visual complexity.

When you finish, provide:

1. The complete project tree.
2. All source files.
3. `requirements.txt`.
4. `README.md` with installation and execution instructions.
5. Tests.
6. A brief explanation of the architecture.
7. Exact commands to install dependencies and run the application.

Do not merely provide pseudocode. Implement the working application.