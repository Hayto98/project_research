"""
Sinh code PlantUML đa dạng cho 6 loại diagram, nhiều domain khác nhau.
Mỗi lần gọi hàm generate_xxx() sẽ random ra 1 cấu trúc + nội dung khác nhau.
"""
import random

random.seed()  # non-deterministic mỗi lần chạy script; ta sẽ seed theo index ở caller

# ---------------------------------------------------------------------------
# Domain vocab pools - mỗi domain có 1 bộ danh từ riêng để tạo class/actor/...
# ---------------------------------------------------------------------------
DOMAINS = {
    "ecommerce": {
        "nouns": ["Product", "Order", "Customer", "Cart", "Payment", "Invoice", "Shipment",
                  "Review", "Coupon", "Category", "Warehouse", "Supplier", "Return", "Wishlist"],
        "actors": ["Customer", "Admin", "Seller", "Payment Gateway", "Delivery Service"],
        "actions": ["Browse Products", "Add To Cart", "Checkout", "Make Payment", "Track Order",
                    "Cancel Order", "Write Review", "Apply Coupon", "Manage Inventory"],
    },
    "banking": {
        "nouns": ["Account", "Transaction", "Customer", "Card", "Loan", "Branch", "Teller",
                  "Statement", "Deposit", "Withdrawal", "Transfer", "Interest", "Beneficiary"],
        "actors": ["Account Holder", "Bank Teller", "ATM", "Branch Manager", "Auditor"],
        "actions": ["Open Account", "Deposit Money", "Withdraw Cash", "Transfer Funds",
                    "Apply For Loan", "View Statement", "Block Card", "Pay Bill"],
    },
    "healthcare": {
        "nouns": ["Patient", "Doctor", "Appointment", "Prescription", "MedicalRecord", "Nurse",
                  "Diagnosis", "Treatment", "Insurance", "Hospital", "Ward", "LabTest", "Billing"],
        "actors": ["Patient", "Doctor", "Nurse", "Receptionist", "Insurance Provider", "Lab Technician"],
        "actions": ["Book Appointment", "Examine Patient", "Issue Prescription", "Run Lab Test",
                    "Update Medical Record", "Process Insurance Claim", "Admit Patient", "Discharge Patient"],
    },
    "education": {
        "nouns": ["Student", "Teacher", "Course", "Enrollment", "Assignment", "Grade", "Classroom",
                  "Exam", "Schedule", "Department", "Library", "Book", "Attendance"],
        "actors": ["Student", "Teacher", "Registrar", "Librarian", "Parent", "Admin"],
        "actions": ["Enroll Course", "Submit Assignment", "Grade Exam", "Borrow Book",
                    "Take Attendance", "View Schedule", "Register Student", "Issue Certificate"],
    },
    "logistics": {
        "nouns": ["Shipment", "Vehicle", "Driver", "Route", "Warehouse", "Package", "Tracking",
                  "Depot", "FuelLog", "Manifest", "Customer", "DeliveryNote", "Inventory"],
        "actors": ["Driver", "Dispatcher", "Warehouse Staff", "Customer", "Fleet Manager"],
        "actions": ["Assign Route", "Load Package", "Deliver Package", "Track Shipment",
                    "Update Inventory", "Schedule Pickup", "Report Issue", "Fuel Vehicle"],
    },
    "hotel": {
        "nouns": ["Room", "Reservation", "Guest", "Booking", "Invoice", "Housekeeping", "Amenity",
                  "Staff", "CheckIn", "CheckOut", "Restaurant", "Service", "Payment"],
        "actors": ["Guest", "Receptionist", "Manager", "Housekeeper", "Chef"],
        "actions": ["Book Room", "Check In", "Check Out", "Request Service", "Order Room Service",
                    "Clean Room", "Process Payment", "Cancel Reservation"],
    },
    "social_media": {
        "nouns": ["User", "Post", "Comment", "Like", "Follower", "Message", "Notification",
                  "Profile", "Group", "Story", "Hashtag", "Album", "Report"],
        "actors": ["User", "Admin", "Moderator", "Advertiser"],
        "actions": ["Create Post", "Like Post", "Comment", "Follow User", "Send Message",
                    "Report Content", "Share Post", "Edit Profile"],
    },
    "library": {
        "nouns": ["Book", "Member", "Loan", "Reservation", "Author", "Publisher", "Fine",
                  "Catalog", "Shelf", "Librarian", "Branch", "Renewal"],
        "actors": ["Member", "Librarian", "Admin"],
        "actions": ["Search Catalog", "Borrow Book", "Return Book", "Reserve Book",
                    "Pay Fine", "Renew Loan", "Add New Book", "Register Member"],
    },
}

FIELD_TYPES = ["String", "int", "long", "double", "boolean", "Date", "float"]
FIELD_NAMES = ["id", "name", "code", "status", "createdAt", "updatedAt", "description",
               "amount", "quantity", "email", "phone", "address", "price", "total",
               "type", "note", "active", "score", "level", "duration"]
VISIBILITY = ["+", "-", "#"]

# skinparam-based "style packs" (compatible with old PlantUML, unlike !theme which
# is not supported in this jar version and silently breaks rendering)
COLOR_PACKS = [
    "",  # default style
    "skinparam backgroundColor #FFFFFF\nskinparam classBackgroundColor #E8F4FA\nskinparam classBorderColor #2C7DA0",
    "skinparam backgroundColor #FAFAFA\nskinparam classBackgroundColor #FFF3E0\nskinparam classBorderColor #E65100",
    "skinparam backgroundColor #FFFFFF\nskinparam classBackgroundColor #F1F8E9\nskinparam classBorderColor #33691E",
    "skinparam backgroundColor #FFFFFF\nskinparam classBackgroundColor #F3E5F5\nskinparam classBorderColor #6A1B9A",
    "skinparam backgroundColor #FFFDE7\nskinparam classBackgroundColor #FFF9C4\nskinparam classBorderColor #F57F17",
    "skinparam monochrome true",
    "skinparam shadowing false\nskinparam backgroundColor #F5F5F5",
    "skinparam backgroundColor #FFFFFF\nskinparam roundCorner 15",
    "skinparam backgroundColor #ECEFF1\nskinparam classBackgroundColor #FFFFFF\nskinparam classBorderColor #455A64",
]

FONT_PACK_EXTRA = [
    "", "skinparam defaultFontSize 11", "skinparam defaultFontSize 13",
    "skinparam ArrowColor #555555", "skinparam shadowing true",
]


def rand_fields(n_min=2, n_max=5):
    chosen = random.sample(FIELD_NAMES, k=random.randint(n_min, n_max))
    lines = []
    for f in chosen:
        vis = random.choice(VISIBILITY)
        typ = random.choice(FIELD_TYPES)
        lines.append(f"  {vis}{typ} {f}")
    return lines


def rand_methods(n_min=1, n_max=4, verbs=None):
    verbs = verbs or ["get", "set", "update", "delete", "create", "validate", "calculate",
                       "process", "send", "cancel", "save", "find"]
    n = random.randint(n_min, n_max)
    # Build unique (verb, field) combos to avoid duplicate method signatures
    combos = list({(v, f) for v in verbs for f in FIELD_NAMES})
    chosen = random.sample(combos, k=min(n, len(combos)))
    return [f"  +{v}{f.capitalize()}()" for v, f in chosen]


def pick_domain():
    name = random.choice(list(DOMAINS.keys()))
    return name, DOMAINS[name]


def maybe_style():
    pack = random.choice(COLOR_PACKS)
    extra = random.choice(FONT_PACK_EXTRA)
    parts = [p for p in (pack, extra) if p]
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# 1. CLASS DIAGRAM
# ---------------------------------------------------------------------------
def generate_class_diagram():
    dname, d = pick_domain()
    nouns = random.sample(d["nouns"], k=min(len(d["nouns"]), random.randint(4, 7)))
    lines = ["@startuml", maybe_style()]

    classes = []
    for n in nouns:
        cls_type = random.choice(["class", "class", "class", "abstract class", "interface"])
        classes.append((n, cls_type))
        lines.append(f"{cls_type} {n} {{")
        lines.extend(rand_fields())
        lines.extend(rand_methods())
        lines.append("}")

    # random relations
    rel_symbols = ["--|>", "..|>", "--*", "--o", "-->", "..>"]
    n_rel = random.randint(2, len(classes) - 1) if len(classes) > 2 else 1
    used_pairs = set()
    for _ in range(n_rel):
        a, b = random.sample(classes, 2)
        pair = (a[0], b[0])
        if pair in used_pairs:
            continue
        used_pairs.add(pair)
        sym = random.choice(rel_symbols)
        label = ""
        if sym in ("-->", "..>"):
            card = random.choice(["1", "0..1", "1..*", "*"])
            label = f' : "{card}"'
        lines.append(f"{a[0]} {sym} {b[0]}{label}")

    lines.append("@enduml")
    return "\n".join(lines), dname


# ---------------------------------------------------------------------------
# 2. SEQUENCE DIAGRAM
# ---------------------------------------------------------------------------
def generate_sequence_diagram():
    dname, d = pick_domain()
    actors = random.sample(d["actors"], k=min(len(d["actors"]), random.randint(3, 5)))
    actions = random.sample(d["actions"], k=min(len(d["actions"]), random.randint(4, 7)))

    lines = ["@startuml", maybe_style()]
    safe_actors = []
    used_aliases = set()
    for a in actors:
        base_alias = "".join(w[0] for w in a.split()).upper()
        alias = base_alias
        suffix = 1
        while alias in used_aliases:
            suffix += 1
            alias = f"{base_alias}{suffix}"
        used_aliases.add(alias)
        safe_actors.append((a, alias))
        kind = random.choice(["participant", "actor", "boundary", "control", "entity"])
        lines.append(f'{kind} "{a}" as {alias}')

    for action in actions:
        a, b = random.sample(safe_actors, 2)
        arrow = random.choice(["->", "-->", "->>"])
        lines.append(f"{a[1]} {arrow} {b[1]} : {action}")
        if random.random() < 0.4:
            lines.append(f"activate {b[1]}")
            lines.append(f"{b[1]} --> {a[1]} : ACK")
            lines.append(f"deactivate {b[1]}")
        if random.random() < 0.25:
            lines.append(f"note over {b[1]} : processing {action.lower()}")

    lines.append("@enduml")
    return "\n".join(lines), dname


# ---------------------------------------------------------------------------
# 3. USE CASE DIAGRAM
# ---------------------------------------------------------------------------
def generate_usecase_diagram():
    dname, d = pick_domain()
    actors = random.sample(d["actors"], k=min(len(d["actors"]), random.randint(2, 4)))
    usecases = random.sample(d["actions"], k=min(len(d["actions"]), random.randint(5, 8)))

    lines = ["@startuml", maybe_style(), "left to right direction"]
    # Build unique aliases for actors (deduplicate by initials collision)
    used_actor_aliases = {}
    safe_actors_uc = []
    for a in actors:
        base = "".join(w[0] for w in a.split()).upper()
        if base in used_actor_aliases:
            used_actor_aliases[base] += 1
            alias = f"{base}{used_actor_aliases[base]}"
        else:
            used_actor_aliases[base] = 0
            alias = base
        safe_actors_uc.append((a, alias))
        lines.append(f'actor "{a}" as {alias}')

    lines.append(f'rectangle "{dname.replace("_"," ").title()} System" {{')
    uc_aliases = []
    for uc in usecases:
        alias = "UC_" + uc.replace(" ", "")
        uc_aliases.append((uc, alias))
        lines.append(f'  usecase "{uc}" as {alias}')
    lines.append("}")

    # Track actor→usecase links to avoid duplicates
    uc_links_used = set()
    for actor_name, actor_alias in safe_actors_uc:
        n_links = random.randint(1, min(3, len(uc_aliases)))
        for uc, uc_alias in random.sample(uc_aliases, n_links):
            link_key = (actor_alias, uc_alias)
            if link_key not in uc_links_used:
                uc_links_used.add(link_key)
                lines.append(f"{actor_alias} --> {uc_alias}")

    if len(uc_aliases) >= 2 and random.random() < 0.6:
        u1, u2 = random.sample(uc_aliases, 2)
        rel = random.choice(["..> ", "..|> "])
        keyword = random.choice(["<<include>>", "<<extend>>"])
        lines.append(f"{u1[1]} {rel.strip()} {u2[1]} : {keyword}")

    lines.append("@enduml")
    return "\n".join(lines), dname


# ---------------------------------------------------------------------------
# 4. ACTIVITY DIAGRAM
# ---------------------------------------------------------------------------
def generate_activity_diagram():
    dname, d = pick_domain()
    actions = random.sample(d["actions"], k=min(len(d["actions"]), random.randint(5, 8)))

    lines = ["@startuml", maybe_style(), "start"]
    for i, action in enumerate(actions):
        lines.append(f":{action};")
        if random.random() < 0.3 and i < len(actions) - 1:
            cond = random.choice(["valid?", "approved?", "available?", "success?"])
            lines.append(f"if ({cond}) then (yes)")
            lines.append(f":continue process;")
            lines.append("else (no)")
            lines.append(":handle error;")
            lines.append("stop")
            lines.append("endif")
        if random.random() < 0.15:
            lines.append("fork")
            lines.append(f":notify {random.choice(['user', 'admin', 'system'])};")
            lines.append("fork again")
            lines.append(f":log {random.choice(['event', 'action', 'change'])};")
            lines.append("end fork")
    lines.append("stop")
    lines.append("@enduml")
    return "\n".join(lines), dname


# ---------------------------------------------------------------------------
# 5. COMPONENT DIAGRAM
# ---------------------------------------------------------------------------
def generate_component_diagram():
    dname, d = pick_domain()
    comps = random.sample(d["nouns"], k=min(len(d["nouns"]), random.randint(4, 7)))
    comps = [f"{c} Service" for c in comps]

    lines = ["@startuml", maybe_style()]
    aliases = []
    for c in comps:
        alias = "C_" + c.replace(" ", "")
        aliases.append((c, alias))
        lines.append(f'component "{c}" as {alias}')

    db_alias = "DB_" + dname
    lines.append(f'database "{dname.replace("_"," ").title()} DB" as {db_alias}')

    for c, alias in aliases:
        if random.random() < 0.7:
            lines.append(f"{alias} --> {db_alias}")

    # Avoid duplicate directed links between components
    comp_links_used = set()
    n_links = random.randint(2, len(aliases) - 1) if len(aliases) > 2 else 1
    attempts = 0
    while len(comp_links_used) < n_links and attempts < n_links * 5:
        attempts += 1
        a, b = random.sample(aliases, 2)
        link_key = (a[1], b[1])
        if link_key in comp_links_used:
            continue
        comp_links_used.add(link_key)
        iface = random.choice(["REST", "gRPC", "MQ", "HTTP"])
        lines.append(f"{a[1]} ..> {b[1]} : {iface}")

    lines.append("@enduml")
    return "\n".join(lines), dname


# ---------------------------------------------------------------------------
# 6. STATE DIAGRAM
# ---------------------------------------------------------------------------
def generate_state_diagram():
    dname, d = pick_domain()
    # pick one "entity" to model lifecycle of
    entity = random.choice(d["nouns"])
    state_pool = ["Created", "Pending", "Active", "Processing", "Approved", "Rejected",
                  "Completed", "Cancelled", "OnHold", "Shipped", "Delivered", "Closed",
                  "Draft", "Reviewed", "Archived"]
    states = random.sample(state_pool, k=random.randint(4, 6))

    lines = ["@startuml", maybe_style(), "[*] --> " + states[0]]
    for i in range(len(states) - 1):
        trigger = random.choice(["submit", "approve", "reject", "process", "confirm",
                                  "cancel", "update", "review"])
        lines.append(f"{states[i]} --> {states[i+1]} : {trigger}")
        if random.random() < 0.3:
            lines.append(f"{states[i]} : entry / log {entity.lower()}")

    if random.random() < 0.5 and len(states) > 2:
        # Build existing transitions set to avoid creating a duplicate revert
        existing_transitions = {(states[i], states[i + 1]) for i in range(len(states) - 1)}
        candidates = [(a, b) for a in states for b in states
                      if a != b and (a, b) not in existing_transitions]
        if candidates:
            a, b = random.choice(candidates)
            lines.append(f"{a} --> {b} : revert")

    lines.append(f"{states[-1]} --> [*]")
    lines.append("@enduml")
    return "\n".join(lines), dname


GENERATORS = {
    "class_diagram": generate_class_diagram,
    "sequence_diagram": generate_sequence_diagram,
    "usecase_diagram": generate_usecase_diagram,
    "activity_diagram": generate_activity_diagram,
    "component_diagram": generate_component_diagram,
    "state_diagram": generate_state_diagram,
}


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------
def validate_puml(code: str, diagram_type: str = "") -> list[str]:
    """
    Kiểm tra tính hợp lệ cơ bản của một đoạn PlantUML.
    Trả về list[str] chứa các lỗi tìm thấy (rỗng = hợp lệ).
    """
    errors = []
    lines = [ln.strip() for ln in code.splitlines() if ln.strip()]

    # --- Structural checks ---
    if not lines or lines[0] != "@startuml":
        errors.append("Missing or misplaced @startuml")
    if not lines or lines[-1] != "@enduml":
        errors.append("Missing or misplaced @enduml")

    body = [l for l in lines if l not in ("@startuml", "@enduml")]
    if not body:
        errors.append("Diagram body is empty")
        return errors

    # --- Duplicate line check ---
    # Activity diagrams intentionally repeat template lines (conditions, fork blocks);
    # exclude them to avoid false positives.
    ACTIVITY_TEMPLATES = {
        ":continue process;", ":handle error;",
        "else (no)", "else (yes)",
    }
    _is_activity_template = lambda l: (
        l.startswith(":log ") or l.startswith(":notify ") or
        l.startswith("if (") or l in ACTIVITY_TEMPLATES
    )
    non_trivial = [l for l in body if not l.startswith("skinparam") and l not in
                   ("start", "stop", "left to right direction", "}", "{",
                    "fork", "fork again", "end fork", "endif")
                   and not _is_activity_template(l)]
    seen = set()
    for line in non_trivial:
        if line in seen:
            errors.append(f"Duplicate line detected: {line!r}")
        seen.add(line)

    # --- Type-specific checks ---
    joined = "\n".join(body)
    if diagram_type == "class_diagram":
        if "class " not in joined and "interface " not in joined and "abstract " not in joined:
            errors.append("class_diagram: no class/interface/abstract found")
    elif diagram_type == "sequence_diagram":
        if "->" not in joined:
            errors.append("sequence_diagram: no message arrows found")
    elif diagram_type == "usecase_diagram":
        if "usecase" not in joined:
            errors.append("usecase_diagram: no usecase declarations found")
        if "actor" not in joined:
            errors.append("usecase_diagram: no actor declarations found")
    elif diagram_type == "activity_diagram":
        if "start" not in joined:
            errors.append("activity_diagram: missing 'start'")
        if "stop" not in joined:
            errors.append("activity_diagram: missing 'stop'")
    elif diagram_type == "component_diagram":
        if "component" not in joined:
            errors.append("component_diagram: no component declarations found")
    elif diagram_type == "state_diagram":
        if "[*]" not in joined:
            errors.append("state_diagram: missing initial/final [*] pseudostate")

    return errors

if __name__ == "__main__":
    random.seed(42)
    for label, fn in GENERATORS.items():
        code, domain = fn()
        errors = validate_puml(code, diagram_type=label)
        status = "✅ OK" if not errors else f"❌ {len(errors)} error(s)"
        print(f"=== {label} ({domain}) [{status}] ===")
        if errors:
            for e in errors:
                print(f"  [ERROR] {e}")
        print(code)
        print()