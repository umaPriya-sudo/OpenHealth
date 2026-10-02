# =========================================================
# OpenHealth - Medicine Service
# =========================================================

import os
import json
import requests
from rapidfuzz import process, fuzz

import re
import cv2
import numpy as np

try:
    import pytesseract
    from PIL import Image

    HAS_OCR = True

    # Windows Tesseract path
    pytesseract.pytesseract.tesseract_cmd = (
        r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    )

    print("✅ Tesseract OCR loaded successfully")

except ImportError:
    HAS_OCR = False
    print(
        "⚠️ OCR packages not installed. "
        "Run: pip install pytesseract pillow opencv-python"
    )

except Exception as e:
    HAS_OCR = False
    print(f"⚠️ OCR setup error: {e}")

# =========================================================
# MEDICINE DATABASE
# =========================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

MEDICINE_DATABASE_PATH = os.path.join(
    BASE_DIR,
    'data',
    'medicines.json'
)


def load_medicine_database():
    """Load medicine information from medicines.json"""

    try:
        with open(
            MEDICINE_DATABASE_PATH,
            'r',
            encoding='utf-8'
        ) as file:

            database = json.load(file)

        print(
            f"✅ Medicine database loaded: "
            f"{len(database)} medicines"
        )

        return database

    except FileNotFoundError:

        print(
            "❌ medicines.json not found at: "
            f"{MEDICINE_DATABASE_PATH}"
        )

        return {}

    except json.JSONDecodeError as e:

        print(
            f"❌ Invalid medicines.json format: {e}"
        )

        return {}

    except Exception as e:

        print(
            f"❌ Error loading medicine database: {e}"
        )

        return {}


# Load database once when application starts
medicine_database = load_medicine_database()

# =========================================================
# MEDICINE TEXT NORMALIZATION
# =========================================================

import re


def normalize_medicine_text(text):
    """
    Normalize medicine names/text before matching.
    """

    if not text:
        return ""

    text = str(text).lower().strip()

    # Replace common separators with spaces
    text = re.sub(r'[_\-]+', ' ', text)

    # Remove punctuation but keep letters and numbers
    text = re.sub(r'[^a-z0-9\s]', ' ', text)

    # Normalize multiple spaces
    text = re.sub(r'\s+', ' ', text)

    return text.strip()



# =========================================================
# SMART MEDICINE SEARCH
# =========================================================

def get_medicine_info(search_term):
    """
    Search medicine database using:
    1. Exact medicine name
    2. Exact brand name
    3. Partial matching
    4. Fuzzy matching
    """

    if not search_term:
        return (
            "🔍 **No medicine name detected.**\n\n"
            "Please enter a medicine name or upload a clearer image."
        )

    # --------------------------------------------------------
    # Normalize input
    # --------------------------------------------------------

    original_search = str(search_term).strip()

    normalized_search = normalize_medicine_text(
        original_search
    )

    if not normalized_search:
        return (
            "🔍 **No valid medicine name detected.**\n\n"
            "Please try again with a medicine name."
        )

    # --------------------------------------------------------
    # 1. EXACT MEDICINE NAME MATCH
    # --------------------------------------------------------

    if normalized_search in medicine_database:

        info = medicine_database[
            normalized_search
        ]

        return format_medicine_info(
            normalized_search,
            info
        )

    # --------------------------------------------------------
    # 2. EXACT BRAND NAME MATCH
    # --------------------------------------------------------

    if normalized_search in medicine_search_index:

        matched_key = medicine_search_index[
            normalized_search
        ]

        info = medicine_database[
            matched_key
        ]

        return format_medicine_info(
            matched_key,
            info
        )

    # --------------------------------------------------------
    # 3. PARTIAL MATCH
    # --------------------------------------------------------

    partial_matches = []

    for medicine_key, info in medicine_database.items():

        medicine_name = normalize_medicine_text(
            medicine_key
        )

        # Medicine name appears inside search text
        if medicine_name in normalized_search:

            partial_matches.append(
                medicine_key
            )

            continue

        # Brand name appears inside search text
        for brand in info.get("brand_names", []):

            normalized_brand = normalize_medicine_text(
                brand
            )

            if (
                normalized_brand
                and normalized_brand in normalized_search
            ):

                partial_matches.append(
                    medicine_key
                )

                break

    if partial_matches:

        matched_key = partial_matches[0]

        return format_medicine_info(
            matched_key,
            medicine_database[matched_key]
        )

    # --------------------------------------------------------
    # 4. FUZZY MATCHING
    # --------------------------------------------------------

    search_choices = list(
        medicine_search_index.keys()
    )

    fuzzy_results = process.extract(
        normalized_search,
        search_choices,
        scorer=fuzz.WRatio,
        limit=5
    )

    # --------------------------------------------------------
    # Select best candidate
    # --------------------------------------------------------

    if fuzzy_results:

        best_match = fuzzy_results[0]

        matched_text = best_match[0]
        match_score = float(best_match[1])

        matched_key = medicine_search_index[
            matched_text
        ]

        # ----------------------------------------------------
        # HIGH CONFIDENCE
        # ----------------------------------------------------

        if match_score >= 85:

            info = medicine_database[
                matched_key
            ]

            return format_medicine_info(
                matched_key,
                info
            )

        # ----------------------------------------------------
        # MEDIUM CONFIDENCE
        # ----------------------------------------------------

        elif match_score >= 65:

            suggestions = []

            for result in fuzzy_results:

                candidate_text = result[0]
                candidate_score = float(result[1])

                candidate_key = medicine_search_index[
                    candidate_text
                ]

                candidate_info = medicine_database[
                    candidate_key
                ]

                candidate_name = candidate_info[
                    "name"
                ]

                suggestions.append(
                    f"• {candidate_name} "
                    f"({candidate_score:.1f}% match)"
                )

            suggestion_text = "\n".join(
                suggestions
            )

            return f"""🔍 **Possible Medicine Matches**

The uploaded/search text could not be matched with high confidence.

**Possible matches:**

{suggestion_text}

Please check the medicine name or upload a clearer image.

⚠️ **Important:** A fuzzy match is only a text-recognition result and does not confirm the medicine identity."""

    # --------------------------------------------------------
    # NO MATCH
    # --------------------------------------------------------

    common_medicines = [
        "Paracetamol",
        "Ibuprofen",
        "Amoxicillin",
        "Metformin",
        "Omeprazole",
        "Losartan",
        "Atorvastatin",
        "Levothyroxine"
    ]

    common_text = "\n".join(
        f"• {medicine}"
        for medicine in common_medicines
    )

    return f"""🔍 **No confident medicine match found** Search text: **{original_search}**
            **💊 Medicines currently available in the database:** {common_text}
            Please enter the medicine name more clearly or upload a clearer medicine image.
            ⚠️ **Disclaimer:** This system provides informational assistance only and does not confirm the identity, safety, or suitability of a medicine."""


# =========================================================
# MEDICINE SEARCH INDEX
# =========================================================

def build_medicine_search_index(database):
    """
    Create searchable medicine-name and brand-name entries.
    """

    search_index = {}

    for key, info in database.items():

        # Generic medicine name
        search_index[key.lower()] = key

        # Brand names
        for brand in info.get("brand_names", []):

            brand_key = normalize_medicine_text(brand)

            if brand_key:
                search_index[brand_key] = key

    return search_index


medicine_search_index = build_medicine_search_index(
    medicine_database
)

# =========================================================
# FORMAT MEDICINE INFORMATION
# =========================================================

def format_medicine_info(key, info):

    response = f"🔬 **Medicine Information:**\n\n"

    response += f"**💊 {info['name']}**\n"

    response += (
        f"• **Category:** "
        f"{info.get('category', 'Not specified')}\n"
    )

    response += (
        f"• **Uses:** "
        f"{info['uses']}\n"
    )

    response += (
        f"• **Dosage:** "
        f"{info['dosage']}\n"
    )

    response += (
        f"• **Side Effects:** "
        f"{info['side_effects']}\n"
    )

    response += (
        f"• **Warning:** "
        f"{info['warning']}\n"
    )

    if info.get('brand_names'):

        response += (
            f"• **Brand Names:** "
            f"{', '.join(info['brand_names'])}\n"
        )

    response += (
        "\n⚠️ **Disclaimer:** "
        "This is for informational purposes only. "
        "Always consult a doctor or pharmacist "
        "for medical advice."
    )

    return response


# =========================================================
# MEDICINE STRENGTH EXTRACTION
# =========================================================

def extract_medicine_strength(ocr_text):
    """
    Extract medicine strength such as:
    500 mg
    650 mg
    20 mg
    5 ml
    100 mcg
    """

    if not ocr_text:
        return None

    text = str(ocr_text)

    # Normalize spacing between number and unit
    text = re.sub(
        r'(\d+(?:\.\d+)?)\s*(mg|mcg|g|ml|kg|%)',
        r'\1 \2',
        text,
        flags=re.IGNORECASE
    )

    # Find strength values
    pattern = (
        r'\b\d+(?:\.\d+)?\s*'
        r'(?:mg|mcg|g|ml|kg|%)\b'
    )

    matches = re.findall(
        pattern,
        text,
        flags=re.IGNORECASE
    )

    if not matches:
        return None

    # Return the first detected strength
    return matches[0].strip()

# ============================================================
# BUILD STRUCTURED MEDICINE RESULT
# ============================================================

def build_medicine_result(
    medicine_key,
    match_score=0.0,
    match_type="unknown",
    matched_text=None,
    ocr_text="",
    ocr_confidence=None,
):
    """
    Build structured medicine information for the frontend.
    """

    info = medicine_database.get(
        medicine_key
    )

    if not info:
        return {
            "success": False,
            "medicine": None,
            "error": "Medicine information not found."
        }

    # Extract strength from OCR text
    strength = extract_medicine_strength(
        ocr_text
    )


    result = {
        "success": True,

        "medicine": {
            "key": medicine_key,

            "name": info.get(
                "name",
                medicine_key.title()
            ),

            "category": info.get(
                "category",
                "Not specified"
            ),

            "uses": info.get(
                "uses",
                "Not specified"
            ),

            "dosage": info.get(
                "dosage",
                "See package/medical advice"
            ),

            "side_effects": info.get(
                "side_effects",
                "Not specified"
            ),

            "warning": info.get(
                "warning",
                "Consult a doctor or pharmacist."
            ),

            "brand_names": info.get(
                "brand_names",
                []
            ),

            "strength": strength,
        },

        "recognition": {
            "matched_text": matched_text,
            "match_type": match_type,
            "match_score": round(
                float(match_score),
                2
            ),
            "ocr_confidence": (
                round(
                    float(ocr_confidence),
                    2
                )
                if ocr_confidence is not None
                else None
            )
        },

        "ocr": {
            "extracted_text": ocr_text
        }
    }

    return result

def extract_medicine_candidates(ocr_text):
    """
    Extract likely medicine names from OCR text.

    The function checks the OCR text against known
    medicine names and brand names.
    """

    if not ocr_text:
        return []

    normalized_text = normalize_medicine_text(
        ocr_text
    )

    candidates = []

    # --------------------------------------------------------
    # 1. Check medicine names
    # --------------------------------------------------------

    for medicine_key, info in medicine_database.items():

        medicine_name = normalize_medicine_text(
            medicine_key
        )

        if medicine_name in normalized_text:

            candidates.append({
                "medicine_key": medicine_key,
                "matched_text": medicine_name,
                "match_type": "medicine_name",
                "score": 100.0
            })

            continue

        # ----------------------------------------------------
        # 2. Check brand names
        # ----------------------------------------------------

        for brand in info.get(
            "brand_names",
            []
        ):

            normalized_brand = normalize_medicine_text(
                brand
            )

            if (
                normalized_brand
                and normalized_brand in normalized_text
            ):

                candidates.append({
                    "medicine_key": medicine_key,
                    "matched_text": normalized_brand,
                    "match_type": "brand_name",
                    "score": 100.0
                })

                break

    return candidates


def recognize_medicine_from_text(
    ocr_text,
    ocr_confidence=None
):
    """
    Recognize a medicine from OCR text.

    Priority:
    1. Exact medicine name
    2. Exact brand name
    3. Partial match
    4. Fuzzy match
    """

    if not ocr_text:

        return {
            "success": False,
            "medicine": None,
            "recognition": {
                "match_score": 0,
                "match_type": "none",
                "matched_text": None,
                "ocr_confidence": ocr_confidence
            },
            "ocr": {
                "extracted_text": ""
            }
        }

    normalized_text = normalize_medicine_text(
        ocr_text
    )

    # ========================================================
    # 1. EXACT MEDICINE NAME
    # ========================================================

    if normalized_text in medicine_database:

        return build_medicine_result(
            medicine_key=normalized_text,
            match_score=100,
            match_type="exact_medicine",
            matched_text=normalized_text,
            ocr_text=ocr_text,
            ocr_confidence=ocr_confidence
        )

    # ========================================================
    # 2. KNOWN MEDICINE / BRAND INSIDE OCR TEXT
    # ========================================================

    candidates = extract_medicine_candidates(
        ocr_text
    )

    if candidates:

        candidates.sort(
            key=lambda x: x.get("score", 0),
            reverse=True
        )

        best = candidates[0]

        return build_medicine_result(
            medicine_key=best["medicine_key"],
            match_score=best["score"],
            match_type=best["match_type"],
            matched_text=best["matched_text"],
            ocr_text=ocr_text,
            ocr_confidence=ocr_confidence
        )

    # ========================================================
    # 3. FUZZY MATCHING
    # ========================================================

    search_choices = list(
        medicine_search_index.keys()
    )

    fuzzy_results = process.extract(
        normalized_text,
        search_choices,
        scorer=fuzz.WRatio,
        limit=5
    )

    if fuzzy_results:

        best = fuzzy_results[0]

        matched_text = best[0]
        match_score = float(best[1])

        medicine_key = medicine_search_index[
            matched_text
        ]

        # ----------------------------------------------------
        # HIGH CONFIDENCE
        # ----------------------------------------------------

        if match_score >= 85:

            return build_medicine_result(
                medicine_key=medicine_key,
                match_score=match_score,
                match_type="fuzzy",
                matched_text=matched_text,
                ocr_text=ocr_text,
                ocr_confidence=ocr_confidence
            )

        # ----------------------------------------------------
        # LOW / UNCERTAIN
        # ----------------------------------------------------

        suggestions = []

        for item in fuzzy_results:

            candidate_text = item[0]
            candidate_score = float(item[1])

            candidate_key = (
                medicine_search_index[
                    candidate_text
                ]
            )

            candidate_info = (
                medicine_database[
                    candidate_key
                ]
            )

            suggestions.append({
                "medicine_key": candidate_key,
                "name": candidate_info.get(
                    "name",
                    candidate_key.title()
                ),
                "matched_text": candidate_text,
                "score": round(
                    candidate_score,
                    2
                )
            })

        return {
            "success": False,

            "medicine": None,

            "recognition": {
                "match_score": round(
                    match_score,
                    2
                ),

                "match_type": "uncertain",

                "matched_text": matched_text,

                "ocr_confidence": (
                    round(
                        float(ocr_confidence),
                        2
                    )
                    if ocr_confidence is not None
                    else None
                )
            },

            "ocr": {
                "extracted_text": ocr_text
            },

            "candidates": suggestions
        }

    # ========================================================
    # NO MATCH
    # ========================================================

    return {
        "success": False,

        "medicine": None,

        "recognition": {
            "match_score": 0,
            "match_type": "none",
            "matched_text": None,
            "ocr_confidence": ocr_confidence
        },

        "ocr": {
            "extracted_text": ocr_text
        },

        "candidates": []
    }

# ============================================================
# SMART OCR ENGINE
# ============================================================

def extract_text_from_image(image_path):
    """
    Extract medicine text using multiple preprocessing
    techniques and Tesseract OCR.

    Returns:
        {
            "text": str,
            "confidence": float,
            "quality_score": float,
            "method": str,
            "psm": int,
            "word_count": int,
            "alphabet_ratio": float,
            "digit_count": int
        }
    """

    # --------------------------------------------------------
    # OCR NOT AVAILABLE
    # --------------------------------------------------------

    if not HAS_OCR:
        return {
            "text": "",
            "confidence": 0.0,
            "quality_score": 0.0,
            "method": None,
            "psm": None,
            "word_count": 0,
            "alphabet_ratio": 0.0,
            "digit_count": 0,
            "error": "OCR not configured. Please install pytesseract."
        }

    try:

        # ====================================================
        # 1. READ IMAGE
        # ====================================================

        img = cv2.imread(image_path)

        if img is None:
            return {
                "text": "",
                "confidence": 0.0,
                "quality_score": 0.0,
                "method": None,
                "psm": None,
                "word_count": 0,
                "alphabet_ratio": 0.0,
                "digit_count": 0,
                "error": "Could not read image."
            }

        height, width = img.shape[:2]

        # ====================================================
        # 2. RESIZE SMALL IMAGES
        # ====================================================

        if width < 800:

            scale = 800 / width

            new_width = int(width * scale)
            new_height = int(height * scale)

            img = cv2.resize(
                img,
                (new_width, new_height),
                interpolation=cv2.INTER_CUBIC
            )

        # ====================================================
        # 3. GRAYSCALE
        # ====================================================

        gray = cv2.cvtColor(
            img,
            cv2.COLOR_BGR2GRAY
        )

        # ====================================================
        # 4. CONTRAST ENHANCEMENT
        # ====================================================

        clahe = cv2.createCLAHE(
            clipLimit=2.0,
            tileGridSize=(8, 8)
        )

        enhanced = clahe.apply(gray)

        # ====================================================
        # 5. DENOISING
        # ====================================================

        denoised = cv2.fastNlMeansDenoising(
            enhanced,
            None,
            10,
            7,
            21
        )

        # ====================================================
        # 6. SHARPENING
        # ====================================================

        sharpening_kernel = np.array([
            [-1, -1, -1],
            [-1,  9, -1],
            [-1, -1, -1]
        ])

        sharpened = cv2.filter2D(
            denoised,
            -1,
            sharpening_kernel
        )

        # ====================================================
        # 7. CREATE MULTIPLE OCR VERSIONS
        # ====================================================

        _, otsu = cv2.threshold(
            sharpened,
            0,
            255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )

        adaptive = cv2.adaptiveThreshold(
            sharpened,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            11,
            2
        )

        _, simple = cv2.threshold(
            gray,
            128,
            255,
            cv2.THRESH_BINARY
        )

        processed_images = [
            ("original", gray),
            ("enhanced", enhanced),
            ("otsu", otsu),
            ("adaptive", adaptive),
            ("simple", simple)
        ]

        # ====================================================
        # 8. OCR SETTINGS
        # ====================================================

        psm_modes = [6, 11, 12]

        results = []

        # ====================================================
        # 9. RUN OCR
        # ====================================================

        for method_name, processed_img in processed_images:

            pil_img = Image.fromarray(
                processed_img
            )

            for psm in psm_modes:

                try:

                    config = (
                        f'--oem 3 --psm {psm}'
                    )

                    data = pytesseract.image_to_data(
                        pil_img,
                        config=config,
                        output_type=pytesseract.Output.DICT
                    )

                    words = []
                    confidences = []

                    # ------------------------------------------------
                    # Extract words + confidence
                    # ------------------------------------------------

                    for i in range(
                        len(data["text"])
                    ):

                        word = data["text"][i].strip()

                        try:
                            confidence = float(
                                data["conf"][i]
                            )

                        except Exception:
                            confidence = -1

                        if (
                            word
                            and confidence >= 0
                        ):

                            words.append(word)

                            confidences.append(
                                confidence
                            )

                    # ------------------------------------------------
                    # Skip empty OCR results
                    # ------------------------------------------------

                    if not words:
                        continue

                    # ------------------------------------------------
                    # Build text
                    # ------------------------------------------------

                    text = " ".join(words)

                    text = re.sub(
                        r'\s+',
                        ' ',
                        text
                    ).strip()

                    # ------------------------------------------------
                    # Average OCR confidence
                    # ------------------------------------------------

                    if confidences:

                        avg_confidence = (
                            sum(confidences)
                            / len(confidences)
                        )

                    else:

                        avg_confidence = 0.0

                    # ------------------------------------------------
                    # Text quality
                    # ------------------------------------------------

                    alphabet_count = sum(
                        c.isalpha()
                        for c in text
                    )

                    digit_count = sum(
                        c.isdigit()
                        for c in text
                    )

                    total_chars = max(
                        len(text),
                        1
                    )

                    alphabet_ratio = (
                        alphabet_count
                        / total_chars
                    )

                    # ------------------------------------------------
                    # Combined quality score
                    # ------------------------------------------------

                    quality_score = (
                        avg_confidence * 0.7
                        +
                        alphabet_ratio * 100 * 0.3
                    )

                    results.append({

                        "text": text,

                        "confidence": (
                            float(avg_confidence)
                        ),

                        "quality_score": (
                            float(quality_score)
                        ),

                        "method": method_name,

                        "psm": psm,

                        "word_count": len(words),

                        "alphabet_ratio": (
                            float(alphabet_ratio)
                        ),

                        "digit_count": digit_count
                    })

                except Exception as ocr_error:

                    print(
                        f"⚠️ OCR attempt failed "
                        f"({method_name}, PSM {psm}): "
                        f"{ocr_error}"
                    )

                    continue

        # ====================================================
        # 10. NO OCR RESULT
        # ====================================================

        if not results:

            return {
                "text": "",
                "confidence": 0.0,
                "quality_score": 0.0,
                "method": None,
                "psm": None,
                "word_count": 0,
                "alphabet_ratio": 0.0,
                "digit_count": 0,
                "error": (
                    "No text detected. "
                    "Please try with a clearer image."
                )
            }

        # ====================================================
        # 11. SORT RESULTS BY QUALITY
        # ====================================================

        results.sort(
            key=lambda x: x["quality_score"],
            reverse=True
        )

        best_result = results[0]

        # ====================================================
        # 12. CLEAN FINAL TEXT
        # ====================================================

        final_text = best_result["text"]

        final_text = re.sub(
            r'[^\w\s.,;:!?()\-/%]',
            ' ',
            final_text
        )

        final_text = re.sub(
            r'\s+',
            ' ',
            final_text
        ).strip()

        # ====================================================
        # 13. LOG OCR INFORMATION
        # ====================================================

        print(
            "\n========== MEDICINE OCR =========="
        )

        print(
            f"Method: {best_result['method']}"
        )

        print(
            f"PSM: {best_result['psm']}"
        )

        print(
            f"OCR confidence: "
            f"{best_result['confidence']:.2f}%"
        )

        print(
            f"Quality score: "
            f"{best_result['quality_score']:.2f}"
        )

        print(
            f"Extracted text: {final_text}"
        )

        print(
            "==================================\n"
        )

        # ====================================================
        # 14. FINAL VALIDATION
        # ====================================================

        if (
            len(final_text) < 3
            or not any(
                c.isalpha()
                for c in final_text
            )
        ):

            return {
                "text": "",
                "confidence": round(
                    best_result["confidence"],
                    2
                ),
                "quality_score": round(
                    best_result["quality_score"],
                    2
                ),
                "method": best_result["method"],
                "psm": best_result["psm"],
                "word_count": best_result["word_count"],
                "alphabet_ratio": round(
                    best_result["alphabet_ratio"],
                    4
                ),
                "digit_count": best_result["digit_count"],
                "error": (
                    "No meaningful text detected. "
                    "Please upload a clearer medicine image."
                )
            }

        # ====================================================
        # 15. RETURN STRUCTURED OCR RESULT
        # ====================================================

        return {

            "text": final_text,

            "confidence": round(
                best_result["confidence"],
                2
            ),

            "quality_score": round(
                best_result["quality_score"],
                2
            ),

            "method": best_result["method"],

            "psm": best_result["psm"],

            "word_count": best_result["word_count"],

            "alphabet_ratio": round(
                best_result["alphabet_ratio"],
                4
            ),

            "digit_count": best_result["digit_count"]
        }

    except Exception as e:

        print(
            f"❌ OCR processing error: {e}"
        )

        return {
            "text": "",
            "confidence": 0.0,
            "quality_score": 0.0,
            "method": None,
            "psm": None,
            "word_count": 0,
            "alphabet_ratio": 0.0,
            "digit_count": 0,
            "error": (
                "Error processing image. "
                "Please try another image."
            )
        }
