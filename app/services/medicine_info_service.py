import requests
import xml.etree.ElementTree as ET


RXNORM_URL = "https://rxnav.nlm.nih.gov/REST/rxcui.json"
DAILYMED_URL = "https://dailymed.nlm.nih.gov/dailymed/services/v2/spls"


def find_rxcui(medicine_name):
    """
    Find the standardized RxNorm ingredient concept
    for a medicine name.
    """

    medicine_name = medicine_name.strip()

    if not medicine_name:
        return None

    params = {
        "name": medicine_name,
        "search": "2"
    }

    try:

        response = requests.get(
            RXNORM_URL,
            params=params,
            timeout=15
        )

        if response.status_code != 200:
            return None

        data = response.json()

        rxnorm_ids = (
            data
            .get("idGroup", {})
            .get("rxnormId", [])
        )

        if not rxnorm_ids:
            return None

        return rxnorm_ids[0]

    except (
        requests.exceptions.RequestException,
        ValueError
    ):

        return None


def get_dailymed_spls(rxcui):
    """
    Find DailyMed SPL records associated with an RxCUI.
    """

    if not rxcui:
        return []

    params = {
        "rxcui": rxcui,
        "pagesize": 20
    }

    try:

        response = requests.get(
            DAILYMED_URL + ".json",
            params=params,
            timeout=15
        )

        if response.status_code != 200:
            return []

        data = response.json()

        return data.get(
            "data",
            []
        )

    except (
        requests.exceptions.RequestException,
        ValueError
    ):

        return []


def get_dailymed_xml(set_id):
    """
    Retrieve the complete DailyMed SPL XML
    using a specific SET ID.
    """

    if not set_id:
        return None

    url = (
        f"{DAILYMED_URL}/"
        f"{set_id}.xml"
    )

    try:

        response = requests.get(
            url,
            timeout=20
        )

        if response.status_code != 200:
            return None

        return response.text

    except requests.exceptions.RequestException:

        return None


def clean_text(element):
    """
    Convert an XML element and its children
    into clean readable text.
    """

    if element is None:
        return ""

    text = " ".join(
        part.strip()
        for part in element.itertext()
        if part.strip()
    )

    return " ".join(
        text.split()
    )


def extract_section_text(root, section_patterns):
    namespace = {"hl7": "urn:hl7-org:v3"}
    section_patterns = [pattern.lower() for pattern in section_patterns]
    matched_sections = []

    for section in root.findall(".//hl7:section", namespace):
        title_element = section.find("hl7:title", namespace)

        if title_element is None:
            continue

        title = clean_text(title_element)
        title_lower = title.lower()

        if not any(pattern in title_lower for pattern in section_patterns):
            continue

        # Get all text inside this section, including nested subsections
        section_text = clean_text(section)

        if section_text:
            matched_sections.append(section_text)

    return "\n\n".join(matched_sections)


def extract_medicine_name(root):
    """
    Extract the main medicine/product name
    from the SPL XML.
    """

    namespace = {
        "hl7": "urn:hl7-org:v3"
    }

    title_element = root.find(
        "hl7:title",
        namespace
    )

    if title_element is None:
        return ""

    title = clean_text(
        title_element
    )

    return title


def extract_active_ingredient(root):
    namespace = {"hl7": "urn:hl7-org:v3"}
    ingredients = []

    for ingredient in root.findall(".//hl7:ingredient", namespace):
        class_code = ingredient.get("classCode")

        # ACTIM = active ingredient
        if class_code != "ACTIM":
            continue

        name_element = ingredient.find(
            ".//hl7:ingredientSubstance/hl7:name",
            namespace
        )

        if name_element is None:
            continue

        name = clean_text(name_element)

        if name and name not in ingredients:
            ingredients.append(name)

    return ingredients


def parse_dailymed_xml(xml_text):
    """
    Parse DailyMed SPL XML and extract
    the major medicine-information sections.
    """

    if not xml_text:

        return {
            "success": False,
            "error": "No DailyMed XML received."
        }

    try:

        root = ET.fromstring(
            xml_text
        )

        medicine_name = extract_medicine_name(
            root
        )

        active_ingredients = extract_active_ingredient(
            root
        )

        indications = extract_section_text(
            root,
            [
                "1 indications and usage",
                "indications and usage",
                "indications & usage"
            ]
        )

        dosage = extract_section_text(
            root,
            [
                "2 dosage and administration",
                "dosage and administration",
                "dosage & administration"
            ]
        )

        warnings = extract_section_text(
            root,
            [
                "5 warnings and precautions",
                "5.1 ",
                "5.2 ",
                "5.3 ",
                "5.4 ",
                "5.5 ",
                "5.6 "
            ]
)

        contraindications = extract_section_text(
            root,
            [
                "contraindications"
            ]
        )

        adverse_reactions = extract_section_text(
            root,
            [
                "6 adverse reactions",
                "6.1 ",
                "6.2 "
            ]
        )

        storage = extract_section_text(
            root,
            [
                "storage and handling",
                "storage"
            ]
        )

        return {

            "success": True,

            "medicine_name": medicine_name,

            "active_ingredients": active_ingredients,

            "uses": indications,

            "dosage": dosage,

            "warnings": warnings,

            "contraindications": contraindications,

            "side_effects": adverse_reactions,

            "storage": storage
        }

    except ET.ParseError:

        return {
            "success": False,
            "error": "Unable to parse DailyMed XML."
        }


def get_medicine_information(medicine_name):
    """
    Complete medicine-information lookup.

    Flow:

    Medicine name
        ↓
    RxNorm
        ↓
    RxCUI
        ↓
    DailyMed
        ↓
    Prefer medicine-specific labels
        ↓
    Parse useful information
    """

    rxcui = find_rxcui(
        medicine_name
    )

    if not rxcui:

        return {
            "success": False,
            "error": "Medicine not found in RxNorm."
        }

    spls = get_dailymed_spls(
        rxcui
    )

    if not spls:

        return {
            "success": False,
            "rxcui": rxcui,
            "error": "No DailyMed label found."
        }

    medicine_lower = str(
        medicine_name
    ).strip().lower()

    best_parsed = None
    best_set_id = None
    best_score = -1

    for spl in spls:

        set_id = spl.get(
            "setid"
        )

        title = str(
            spl.get(
                "title",
                ""
            )
        )

        if not set_id:
            continue

        title_lower = title.lower()

        # ----------------------------------------------------
        # SCORE THE LABEL
        # ----------------------------------------------------

        score = 0

        # Medicine name should appear in the label title.
        if medicine_lower in title_lower:
            score += 10

        # Prefer labels that look like the requested
        # medicine alone rather than combination products.
        combination_terms = [
            " and ",
            " with ",
            "/",
            "combination"
        ]

        is_combination = any(
            term in title_lower
            for term in combination_terms
        )

        if is_combination:
            score -= 15

        # Prefer simple dosage forms containing the
        # requested medicine name.
        if medicine_lower in title_lower:
            score += 5

        # ----------------------------------------------------
        # DOWNLOAD AND PARSE
        # ----------------------------------------------------

        xml_text = get_dailymed_xml(
            set_id
        )

        if not xml_text:
            continue

        parsed = parse_dailymed_xml(
            xml_text
        )

        if not parsed:
            continue

        # ----------------------------------------------------
        # CONTENT SCORE
        # ----------------------------------------------------

        if parsed.get("active_ingredients"):
            score += 5

        if parsed.get("uses"):
            score += 3

        if parsed.get("dosage"):
            score += 3

        if parsed.get("warnings"):
            score += 3

        if parsed.get("contraindications"):
            score += 2

        if parsed.get("side_effects"):
            score += 3

        if parsed.get("storage"):
            score += 2

        # ----------------------------------------------------
        # KEEP THE BEST LABEL
        # ----------------------------------------------------

        if score > best_score:

            best_score = score
            best_parsed = parsed
            best_set_id = set_id

    # --------------------------------------------------------
    # NO USABLE LABEL
    # --------------------------------------------------------

    if not best_parsed:

        return {
            "success": False,
            "rxcui": rxcui,
            "error": "Unable to retrieve usable DailyMed medicine information."
        }

    return {

        "success": best_parsed.get(
            "success",
            False
        ),

        "medicine_name": medicine_name,

        "rxcui": rxcui,

        "set_id": best_set_id,

        "label_title": best_parsed.get(
            "medicine_name",
            ""
        ),

        "active_ingredients": best_parsed.get(
            "active_ingredients",
            []
        ),

        "uses": best_parsed.get(
            "uses",
            ""
        ),

        "dosage": best_parsed.get(
            "dosage",
            ""
        ),

        "warnings": best_parsed.get(
            "warnings",
            ""
        ),

        "contraindications": best_parsed.get(
            "contraindications",
            ""
        ),

        "side_effects": best_parsed.get(
            "side_effects",
            ""
        ),

        "storage": best_parsed.get(
            "storage",
            ""
        ),

        "dailymed_results": spls
    }