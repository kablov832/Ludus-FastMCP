"""Randomization logic for generating varied scenario configurations."""

import random
from typing import Any
from ..schemas.scenario_customization import (
    ScenarioCustomization,
    ADUserCustomization,
    VulnerabilityConfig,
    NetworkCustomization,
    VMCustomization,
    RandomizationConfig,
)


# Realistic name components for generating random users
FIRST_NAMES = [
    "James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda",
    "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica",
    "Thomas", "Sarah", "Charles", "Karen", "Christopher", "Nancy", "Daniel", "Lisa",
    "Matthew", "Betty", "Anthony", "Margaret", "Mark", "Sandra", "Donald", "Ashley",
    "Steven", "Kimberly", "Paul", "Emily", "Andrew", "Donna", "Joshua", "Michelle",
    "Kenneth", "Carol", "Kevin", "Amanda", "Brian", "Dorothy", "George", "Melissa",
    "Timothy", "Deborah", "Ronald", "Stephanie", "Jason", "Rebecca", "Edward", "Sharon",
    "Jeffrey", "Laura", "Ryan", "Cynthia", "Jacob", "Kathleen", "Gary", "Amy",
    "Nicholas", "Angela", "Eric", "Shirley", "Jonathan", "Anna", "Stephen", "Brenda",
    "Larry", "Pamela", "Justin", "Emma", "Scott", "Nicole", "Brandon", "Helen",
    "Benjamin", "Samantha", "Samuel", "Katherine", "Frank", "Christine", "Gregory", "Debra",
    "Raymond", "Rachel", "Alexander", "Carolyn", "Patrick", "Janet", "Jack", "Virginia",
    "Dennis", "Maria", "Jerry", "Heather", "Tyler", "Diane", "Aaron", "Julie",
    "Jose", "Joyce", "Adam", "Victoria", "Nathan", "Kelly", "Henry", "Christina",
    "Zachary", "Joan", "Douglas", "Evelyn", "Kyle", "Judith", "Noah", "Megan",
    "Ethan", "Cheryl", "Jeremy", "Andrea", "Walter", "Hannah", "Christian", "Jacqueline",
    "Keith", "Martha", "Roger", "Gloria", "Terry", "Teresa", "Gerald", "Sara",
    "Harold", "Janice", "Sean", "Marie", "Austin", "Julia", "Carl", "Grace",
    "Arthur", "Judy", "Lawrence", "Theresa", "Dylan", "Madison", "Jesse", "Beverly",
    "Jordan", "Denise", "Bryan", "Marilyn", "Billy", "Amber", "Joe", "Danielle",
    "Bruce", "Rose", "Gabriel", "Brittany", "Logan", "Diana", "Alan", "Abigail",
    "Juan", "Jane", "Wayne", "Lori", "Roy", "Alexis", "Ralph", "Marie",
    "Randy", "Olivia", "Eugene", "Tiffany", "Vincent", "Kimberly", "Russell", "Kayla",
    "Louis", "Nancy", "Philip", "Kathy", "Johnny", "Deborah", "Bobby", "Rachel",
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
    "Rodriguez", "Martinez", "Hernandez", "Lopez", "Wilson", "Anderson", "Thomas", "Taylor",
    "Moore", "Jackson", "Martin", "Lee", "Thompson", "White", "Harris", "Sanchez",
    "Clark", "Ramirez", "Lewis", "Robinson", "Walker", "Young", "Allen", "King",
    "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores", "Green", "Adams",
    "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell", "Carter", "Roberts",
    "Gomez", "Phillips", "Evans", "Turner", "Diaz", "Parker", "Cruz", "Edwards",
    "Collins", "Stewart", "Morris", "Morales", "Murphy", "Cook", "Rogers", "Gutierrez",
    "Ortiz", "Morgan", "Cooper", "Peterson", "Bailey", "Reed", "Kelly", "Howard",
    "Ramos", "Kim", "Cox", "Ward", "Richardson", "Watson", "Brooks", "Chavez",
    "Wood", "James", "Bennett", "Gray", "Mendoza", "Ruiz", "Hughes", "Price",
    "Alvarez", "Castillo", "Sanders", "Patel", "Myers", "Long", "Ross", "Foster",
    "Jimenez", "Powell", "Jenkins", "Perry", "Russell", "Sullivan", "Bell", "Coleman",
    "Butler", "Henderson", "Barnes", "Gonzales", "Fisher", "Vasquez", "Simmons", "Romero",
    "Jordan", "Patterson", "Alexander", "Hamilton", "Graham", "Reynolds", "Griffin", "Wallace",
    "Moreno", "West", "Cole", "Hayes", "Bryant", "Herrera", "Gibson", "Ellis",
    "Tran", "Medina", "Aguilar", "Stevens", "Murray", "Ford", "Castro", "Marshall",
    "Owens", "Harrison", "Fernandez", "Mcdonald", "Woods", "Washington", "Kennedy", "Wells",
    "Vargas", "Henry", "Chen", "Freeman", "Webb", "Tucker", "Guzman", "Burns",
    "Crawford", "Olson", "Simpson", "Porter", "Hunter", "Gordon", "Mendez", "Silva",
    "Shaw", "Snyder", "Mason", "Dixon", "Munoz", "Hunt", "Hicks", "Holmes",
    "Palmer", "Wagner", "Black", "Robertson", "Boyd", "Rose", "Stone", "Salazar",
    "Fox", "Warren", "Mills", "Meyer", "Rice", "Schmidt", "Garza", "Daniels",
    "Ferguson", "Nichols", "Stephens", "Soto", "Weaver", "Ryan", "Gardner", "Payne",
    "Grant", "Dunn", "Kelley", "Spencer", "Hawkins", "Arnold", "Pierce", "Vazquez",
    "Hansen", "Peters", "Santos", "Hart", "Bradley", "Knight", "Elliott", "Cunningham",
    "Duncan", "Armstrong", "Hudson", "Carroll", "Lane", "Riley", "Andrews", "Alvarado",
    "Ray", "Delgado", "Berry", "Perkins", "Hoffman", "Johnston", "Matthews", "Pena",
    "Richards", "Contreras", "Willis", "Carpenter", "Lawrence", "Sandoval", "Guerrero", "George",
    "Chapman", "Rios", "Estrada", "Ortega", "Watkins", "Greene", "Nunez", "Wheeler",
    "Valdez", "Harper", "Lynch", "Barker", "Malone", "Saunders", "Hammond", "Carr",
    "Townsend", "Wise", "Ingram", "Barton", "Mejia", "Ayala", "Schroeder", "Hampton",
    "Rowe", "Parsons", "Frank", "Waters", "Strickland", "Osborne", "Maxwell", "Chan",
    "Deleon", "Norman", "Harrington", "Casey", "Patton", "Logan", "Bowers", "Mueller",
    "Glover", "Floyd", "Hartman", "Buchanan", "Cobb", "French", "Kramer", "Mccormick",
    "Clarke", "Tyler", "Gibbs", "Moody", "Conner", "Sparks", "Mcguire", "Leon",
    "Wade", "Bauer", "Rivers", "Ball", "Figueroa", "Hodge", "Cherry", "Walters",
    "Mckinney", "Mann", "Poole", "Klein", "Espinoza", "Baldwin", "Moran", "Love",
    "Robbins", "Higgins", "Ballard", "Cortez", "Le", "Griffith", "Bowen", "Sharp",
    "Cummings", "Ramsey", "Hardy", "Swanson", "Barber", "Acosta", "Luna", "Chandler",
    "Blair", "Daniel", "Cross", "Simon", "Dennis", "Oconnor", "Quinn", "Gross",
    "Navarro", "Moss", "Fitzgerald", "Doyle", "Mclaughlin", "Rojas", "Rodgers", "Stevenson",
    "Singh", "Yang", "Figueroa", "Harmon", "Newton", "Paul", "Manning", "Garner",
    "Mcgee", "Reese", "Francis", "Burgess", "Adkins", "Goodman", "Curry", "Brady",
    "Christensen", "Potter", "Walton", "Goodwin", "Mullins", "Molina", "Webster", "Fischer",
    "Campos", "Avila", "Sherman", "Todd", "Chang", "Blake", "Malone", "Wolf",
    "Hodges", "Juarez", "Gill", "Hobbs", "Ibarra", "Keith", "Macias", "Khan",
    "Andrade", "Ware", "Stephenson", "Henson", "Wilkerson", "Dyer", "Mcclure", "Blackwell",
    "Mercado", "Tanner", "Eaton", "Clay", "Barron", "Beasley", "Oneal", "Preston",
    "Small", "Wu", "Zamora", "Macdonald", "Vance", "Snow", "Mcclain", "Stafford",
    "Orozco", "Barry", "English", "Shannon", "Kline", "Jacobson", "Woodard", "Huang",
    "Kemp", "Mosley", "Prince", "Merritt", "Hurst", "Villanueva", "Roach", "Nolan",
    "Lam", "Yoder", "Mccullough", "Lester", "Santana", "Valenzuela", "Winters", "Barrera",
    "Leach", "Orr", "Berger", "Mckee", "Strong", "Conway", "Stein", "Whitehead",
    "Bullock", "Escobar", "Knox", "Meadows", "Solomon", "Velez", "Odonnell", "Kerr",
    "Stout", "Blankenship", "Browning", "Kent", "Lozano", "Bartlett", "Pruitt", "Buck",
    "Barr", "Gaines", "Durham", "Gentry", "Mcintyre", "Sloan", "Melendez", "Rocha",
    "Herman", "Sexton", "Moon", "Hendricks", "Rangel", "Stark", "Lowery", "Hardin",
    "Hull", "Sellers", "Ellison", "Calhoun", "Gillespie", "Mora", "Knapp", "Mccall",
    "Morse", "Dorsey", "Weeks", "Nielsen", "Livingston", "Leblanc", "Mclean", "Bradshaw",
    "Glass", "Middleton", "Buckley", "Schaefer", "Frost", "Howe", "House", "Mcintosh",
    "Hoover", "Patton", "Brewer", "Cardenas", "Copeland", "Cain", "Dickson", "Bond",
    "Sheppard", "Barrera", "Mccall", "Hess", "Melton", "Monroe", "Mcconnell", "Hays",
    "Dudley", "Marks", "Cantrell", "Mccormick", "Waller", "Boyle", "Mayer", "Zuniga",
    "Giles", "Pineda", "Pace", "Hurley", "Mays", "Mcmillan", "Crosby", "Ayers",
    "Case", "Bentley", "Shepard", "Everett", "Pugh", "David", "Mcmahon", "Dunlap",
    "Bender", "Hahn", "Harding", "Acevedo", "Raymond", "Blackburn", "Duffy", "Landry",
    "Dougherty", "Bautista", "Shah", "Potts", "Arroyo", "Valentine", "Meza", "Gould",
    "Vaughan", "Fry", "Rush", "Avery", "Herring", "Dodson", "Clements", "Sampson",
    "Tapia", "Bean", "Lynn", "Crane", "Farley", "Cisneros", "Benton", "Ashley",
    "Mckay", "Finley", "Best", "Blevins", "Friedman", "Moses", "Sosa", "Blanchard",
    "Huber", "Frye", "Krueger", "Bernard", "Rosa", "Santos", "Weiss", "Mullen",
    "Acosta", "Lucero", "Brennan", "Kramer", "Heath", "Hancock", "Gallagher", "Gay",
    "Short", "Baird", "Phelps", "Marks", "Hanna", "Booth", "Casey", "Herrera",
    "Hess", "Marsh", "Hull", "Frye", "Hobbs", "Kemp", "Mccall", "England",
    "Mccarthy", "Sheppard", "Garza", "Mcconnell", "Cunningham", "Hendricks", "Schmidt", "Carr",
    "Bowen", "Dominguez", "Schneider", "Fitzgerald", "Norris", "Sellers", "Espinoza", "Colon",
    "Mccarthy", "Avila", "Booker", "Waller", "Parks", "Mcdonald", "Mccall", "Mccarthy",
    "Mccarthy", "Mccarthy", "Mccarthy", "Mccarthy", "Mccarthy", "Mccarthy", "Mccarthy", "Mccarthy",
]

DEPARTMENTS = ["IT", "HR", "Finance", "Sales", "Marketing", "Operations", "Legal", "Executive"]
TITLES = [
    "Administrator", "Manager", "Director", "Specialist", "Analyst", "Coordinator",
    "Assistant", "Technician", "Engineer", "Consultant", "Representative", "Supervisor",
]

PASSWORD_PATTERNS = [
    "{name}123!", "{name}2024!", "Welcome{year}!", "Password{num}!", "{dept}{year}!",
    "{title}{num}!", "Company{year}!", "{name}@123", "{dept}Pass{num}!", "Secure{year}!",
]


def generate_random_users(
    count: int | None = None,
    min_count: int = 5,
    max_count: int = 15,
    seed: int | None = None,
) -> list[ADUserCustomization]:
    """Generate random but realistic AD users.
    
    Args:
        count: Exact number of users to generate (overrides min/max)
        min_count: Minimum number of users
        max_count: Maximum number of users
        seed: Random seed for reproducibility
        
    Returns:
        List of random AD user customizations
    """
    if seed is not None:
        random.seed(seed)
    
    if count is None:
        count = random.randint(min_count, max_count)
    
    users = []
    used_usernames = set()
    
    for _ in range(count):
        # Generate unique username
        attempts = 0
        while attempts < 100:
            first_name = random.choice(FIRST_NAMES)
            last_name = random.choice(LAST_NAMES)
            username = f"{first_name.lower()}.{last_name.lower()}"
            
            if username not in used_usernames:
                used_usernames.add(username)
                break
            attempts += 1
        else:
            # Fallback if we can't generate unique username
            username = f"user{random.randint(1000, 9999)}"
        
        display_name = f"{first_name} {last_name}"
        department = random.choice(DEPARTMENTS)
        title = random.choice(TITLES)
        
        # Generate password using pattern
        pattern = random.choice(PASSWORD_PATTERNS)
        password = pattern.format(
            name=first_name,
            year=random.choice(["2023", "2024", "2025"]),
            num=random.randint(1, 999),
            dept=department,
            title=title,
        )
        
        # Generate groups
        groups = ["Domain Users"]
        if department:
            groups.append(f"{department} Department")
        if random.random() < 0.3:  # 30% chance of additional groups
            groups.append(random.choice(["Remote Desktop Users", "Power Users", "Backup Operators"]))
        
        user = ADUserCustomization(
            username=username,
            display_name=display_name,
            password=password,
            department=department,
            title=title,
            groups=groups,
            password_never_expires=random.random() < 0.2,  # 20% chance
            account_disabled=random.random() < 0.1,  # 10% chance
            description=f"{title} - {department} Department",
        )
        users.append(user)
    
    return users


def randomize_vulnerabilities(seed: int | None = None) -> VulnerabilityConfig:
    """Generate random vulnerability configuration with comprehensive APT techniques.
    
    Args:
        seed: Random seed for reproducibility
        
    Returns:
        Random vulnerability configuration with realistic APT attack surfaces
    """
    if seed is not None:
        random.seed(seed)
    
    # AD CS vulnerabilities (common in enterprise)
    esc1 = random.random() < 0.7  # 70% chance
    esc2 = random.random() < 0.5  # 50% chance
    esc3 = random.random() < 0.3  # 30% chance
    esc4 = random.random() < 0.4  # 40% chance
    esc6 = random.random() < 0.6  # 60% chance
    esc7 = random.random() < 0.3  # 30% chance
    esc8 = random.random() < 0.5  # 50% chance
    
    # Kerberos attacks (very common)
    asrep_roasting = random.random() < 0.6  # 60% chance
    kerberoastable = random.random() < 0.7  # 70% chance
    
    # Delegation (common misconfiguration)
    unconstrained_delegation = random.random() < 0.2  # 20% chance
    constrained_delegation = random.random() < 0.4  # 40% chance
    rbcd = random.random() < 0.3  # 30% chance
    
    # Credential theft (very common)
    lsass_dumpable = random.random() < 0.8  # 80% chance (default Windows behavior)
    sam_dumpable = random.random() < 0.7  # 70% chance
    gpp_passwords = random.random() < 0.5  # 50% chance (legacy but still found)
    
    # ACL abuse (common in complex environments)
    dcsync_abuse = random.random() < 0.3  # 30% chance
    acl_backdoors = random.random() < 0.2  # 20% chance
    
    # Service misconfigurations (very common)
    service_weak_passwords = random.random() < 0.6  # 60% chance
    service_password_never_expires = random.random() < 0.7  # 70% chance
    local_admin_reuse = random.random() < 0.5  # 50% chance
    
    # Group-based attacks (common)
    dns_admins_abuse = random.random() < 0.3  # 30% chance
    backup_operators_abuse = random.random() < 0.4  # 40% chance
    
    # Network protocol vulnerabilities (very common)
    smb_signing_disabled = random.random() < 0.7  # 70% chance
    smb_relay_enabled = random.random() < 0.5  # 50% chance
    llmnr_enabled = random.random() < 0.8  # 80% chance (default)
    nbns_enabled = random.random() < 0.8  # 80% chance (default)
    
    # RPC/DCOM attacks (common)
    ms_efsrpc_abuse = random.random() < 0.4  # 40% chance
    print_spooler_enabled = random.random() < 0.9  # 90% chance (default)
    wmi_abuse = random.random() < 0.6  # 60% chance
    
    # Scheduled tasks and services (common)
    scheduled_tasks_weak_permissions = random.random() < 0.5  # 50% chance
    service_weak_permissions = random.random() < 0.4  # 40% chance
    unquoted_service_paths = random.random() < 0.3  # 30% chance
    
    # File shares (very common)
    open_shares = random.random() < 0.8  # 80% chance
    writable_shares = random.random() < 0.6  # 60% chance
    
    # GPO abuse (common in managed environments)
    gpo_weak_permissions = random.random() < 0.4  # 40% chance
    gpo_scheduled_tasks = random.random() < 0.3  # 30% chance
    
    # RDP (very common)
    rdp_enabled = random.random() < 0.9  # 90% chance
    rdp_weak_credentials = random.random() < 0.5  # 50% chance
    
    # Exchange (if present)
    exchange_privilege_escalation = random.random() < 0.3  # 30% chance (if Exchange exists)
    
    # SQL Server (if present)
    sql_server_weak_passwords = random.random() < 0.4  # 40% chance (if SQL exists)
    
    # Privilege abuse (common)
    seimpersonate_privilege_abuse = random.random() < 0.5  # 50% chance
    sebackup_privilege_abuse = random.random() < 0.3  # 30% chance
    
    return VulnerabilityConfig(
        # AD CS
        esc1_enabled=esc1,
        esc2_enabled=esc2,
        esc3_enabled=esc3,
        esc4_enabled=esc4,
        esc6_enabled=esc6,
        esc7_enabled=esc7,
        esc8_enabled=esc8,
        # Kerberos
        asrep_roasting_enabled=asrep_roasting,
        kerberoastable_accounts=kerberoastable,
        # Delegation
        unconstrained_delegation=unconstrained_delegation,
        constrained_delegation=constrained_delegation,
        resource_based_constrained_delegation=rbcd,
        # Credential theft
        lsass_dumpable=lsass_dumpable,
        sam_dumpable=sam_dumpable,
        gpp_passwords=gpp_passwords,
        # ACL abuse
        dcsync_abuse=dcsync_abuse,
        acl_backdoors=acl_backdoors,
        # Service misconfigurations
        service_account_weak_passwords=service_weak_passwords,
        service_account_password_never_expires=service_password_never_expires,
        local_admin_reuse=local_admin_reuse,
        # Group-based attacks
        dns_admins_abuse=dns_admins_abuse,
        backup_operators_abuse=backup_operators_abuse,
        # Network protocols
        smb_signing_disabled=smb_signing_disabled,
        smb_relay_enabled=smb_relay_enabled,
        llmnr_enabled=llmnr_enabled,
        nbns_enabled=nbns_enabled,
        # RPC/DCOM
        ms_efsrpc_abuse=ms_efsrpc_abuse,
        print_spooler_enabled=print_spooler_enabled,
        wmi_abuse=wmi_abuse,
        # Scheduled tasks/services
        scheduled_tasks_weak_permissions=scheduled_tasks_weak_permissions,
        service_weak_permissions=service_weak_permissions,
        unquoted_service_paths=unquoted_service_paths,
        # File shares
        open_shares=open_shares,
        writable_shares=writable_shares,
        # GPO
        gpo_weak_permissions=gpo_weak_permissions,
        gpo_scheduled_tasks=gpo_scheduled_tasks,
        # RDP
        rdp_enabled=rdp_enabled,
        rdp_weak_credentials=rdp_weak_credentials,
        # Exchange
        exchange_privilege_escalation=exchange_privilege_escalation,
        # SQL Server
        sql_server_weak_passwords=sql_server_weak_passwords,
        # Privileges
        seimpersonate_privilege_abuse=seimpersonate_privilege_abuse,
        sebackup_privilege_abuse=sebackup_privilege_abuse,
    )


def randomize_network(seed: int | None = None) -> NetworkCustomization:
    """Generate random network customizations.
    
    Args:
        seed: Random seed for reproducibility
        
    Returns:
        Random network customization
    """
    if seed is not None:
        random.seed(seed)
    
    # Random VLAN changes (limited to avoid breaking scenarios)
    vlan_changes = {}
    # Only randomize if explicitly requested - network changes can break scenarios
    
    return NetworkCustomization(
        vlan_changes=vlan_changes,
        additional_rules=[],
        remove_rules=[],
        inter_vlan_default=None,
    )


def randomize_vm_config(
    scenario_type: str,
    seed: int | None = None,
    min_workstations: int = 2,
    max_workstations: int = 4,
) -> VMCustomization:
    """Generate random VM configuration customizations.
    
    Args:
        scenario_type: Type of scenario (affects what can be randomized)
        seed: Random seed for reproducibility
        min_workstations: Minimum workstation count
        max_workstations: Maximum workstation count
        
    Returns:
        Random VM customization
    """
    if seed is not None:
        random.seed(seed)
    
    vm_count_overrides = {}
    
    # Randomize workstation count for AD scenarios
    if "ad" in scenario_type.lower() or "redteam" in scenario_type.lower():
        workstation_count = random.randint(min_workstations, max_workstations)
        vm_count_overrides["workstation"] = workstation_count
    
    return VMCustomization(
        vm_count_overrides=vm_count_overrides,
        additional_vms=[],
        remove_vms=[],
        resource_overrides={},
    )


def randomize_scenario(
    scenario_key: str,
    config: RandomizationConfig,
) -> ScenarioCustomization:
    """Generate random customizations for a scenario.
    
    Args:
        scenario_key: Scenario identifier
        config: Randomization configuration
        
    Returns:
        Scenario customization with random values
    """
    seed = config.seed
    
    customization = ScenarioCustomization()
    
    if config.randomize_users:
        users = generate_random_users(
            min_count=config.min_users,
            max_count=config.max_users,
            seed=seed,
        )
        customization.custom_users = users
    
    if config.randomize_vulnerabilities:
        customization.vulnerability_config = randomize_vulnerabilities(seed=seed)
    
    if config.randomize_network:
        customization.network_customization = randomize_network(seed=seed)
    
    if config.randomize_vms:
        customization.vm_customization = randomize_vm_config(
            scenario_type=scenario_key,
            seed=seed,
            min_workstations=config.min_workstations,
            max_workstations=config.max_workstations,
        )
    
    customization.randomization_config = config
    
    return customization

