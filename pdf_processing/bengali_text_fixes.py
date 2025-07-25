"""
Bengali Text Fixes Module
Contains comprehensive fixes for Bengali OCR spacing errors and text normalization.
"""

# Comprehensive Bengali OCR fixes dictionary
BENGALI_FIXES = {
    # ============= VOWEL SIGNS WITH NUKTA (়) =============
    'া ়': 'া়', 'ি ়': 'ি়', 'ী ়': 'ী়', 'ু ়': 'ু়', 'ূ ়': 'ূ়',
    'ৃ ়': 'ৃ়', 'ৄ ়': 'ৄ়', 'ে ়': 'ে়', 'ৈ ়': 'ৈ়', 'ো ়': 'ো়', 'ৌ ়': 'ৌ়',
    
    # ============= OTHER DIACRITICAL MARKS WITH NUKTA =============
    'ং ়': 'ং়', 'ঃ ়': 'ঃ়', 'ঁ ়': 'ঁ়', 'ঀ ়': 'ঀ়',
    
    # ============= ALL CONSONANTS WITH HASANTA (্) =============
    'ক ্': 'ক্', 'খ ্': 'খ্', 'গ ্': 'গ্', 'ঘ ্': 'ঘ্', 'ঙ ্': 'ঙ্',
    'চ ্': 'চ্', 'ছ ্': 'ছ্', 'জ ্': 'জ্', 'ঝ ্': 'ঝ্', 'ঞ ্': 'ঞ্',
    'ট ্': 'ট্', 'ঠ ্': 'ঠ্', 'ড ্': 'ড্', 'ঢ ্': 'ঢ্', 'ণ ্': 'ণ্',
    'ত ্': 'ত্', 'থ ্': 'থ্', 'দ ্': 'দ্', 'ধ ্': 'ধ্', 'ন ্': 'ন্',
    'প ্': 'প্', 'ফ ্': 'ফ্', 'ব ্': 'ব্', 'ভ ্': 'ভ্', 'ম ্': 'ম্',
    'য ্': 'য্', 'র ্': 'র্', 'ল ্': 'ল্', 'শ ্': 'শ্', 'ষ ্': 'ষ্',
    'স ্': 'স্', 'হ ্': 'হ্',
    
    # ============= ADDITIONAL CONSONANTS =============
    'ড় ্': 'ড়্', 'ঢ় ্': 'ঢ়্', 'য় ্': 'য়্',
    
    # ============= VOWEL SIGN SPACING FIXES =============
    ' া': 'া', ' ি': 'ি', ' ী': 'ী', ' ু': 'ু', ' ূ': 'ূ',
    ' ৃ': 'ৃ', ' ৄ': 'ৄ', ' ে': 'ে', ' ৈ': 'ৈ', ' ো': 'ো', ' ৌ': 'ৌ',
    
    # ============= DIACRITIC MARKS SPACING FIXES =============
    ' ং': 'ং', ' ঃ': 'ঃ', ' ঁ': 'ঁ', ' ়': '়', ' ্': '্',
    
    # ============= CONSONANTS WITH NUKTA SPACING =============
    'ক ়': 'ক়', 'খ ়': 'খ়', 'গ ়': 'গ়', 'ঘ ়': 'ঘ়', 'জ ়': 'জ়',
    'ড ়': 'ড়', 'ঢ ়': 'ঢ়', 'ত ়': 'ত়', 'থ ়': 'থ়', 'দ ়': 'দ়',
    'ধ ়': 'ধ়', 'ন ়': 'ন়', 'প ়': 'প়', 'ফ ়': 'ফ়', 'ব ়': 'ব়',
    'ভ ়': 'ভ়', 'ম ়': 'ম়', 'য ়': 'য়', 'র ়': 'র়', 'ল ়': 'ল়',
    'শ ়': 'শ়', 'ষ ়': 'ষ়', 'স ়': 'স়', 'হ ়': 'হ়',
    
    # ============= COMMON CONJUNCT CONSONANTS =============
    'ক ্ক': 'ক্ক', 'ক ্ত': 'ক্ত', 'ক ্র': 'ক্র', 'ক ্ল': 'ক্ল', 'ক ্ষ': 'ক্ষ',
    'গ ্ধ': 'গ্ধ', 'গ ্ন': 'গ্ন', 'গ ্ম': 'গ্ম', 'গ ্র': 'গ্র', 'গ ্ল': 'গ্ল',
    'ঙ ্ক': 'ঙ্ক', 'ঙ ্গ': 'ঙ্গ', 'চ ্চ': 'চ্চ', 'চ ্ছ': 'চ্ছ', 'জ ্জ': 'জ্জ',
    'জ ্ঞ': 'জ্ঞ', 'ঞ ্চ': 'ঞ্চ', 'ঞ ্জ': 'ঞ্জ', 'ট ্ট': 'ট্ট', 'ণ ্ট': 'ণ্ট',
    'ণ ্ঠ': 'ণ্ঠ', 'ণ ্ড': 'ণ্ড', 'ণ ্ণ': 'ণ্ণ', 'ত ্ত': 'ত্ত', 'ত ্থ': 'ত্থ',
    'ত ্ন': 'ত্ন', 'ত ্ম': 'ত্ম', 'ত ্র': 'ত্র', 'দ ্দ': 'দ্দ', 'দ ্ধ': 'দ্ধ',
    'দ ্ব': 'দ্ব', 'দ ্ম': 'দ্ম', 'দ ্র': 'দ্র', 'ধ ্ন': 'ধ্ন', 'ধ ্ম': 'ধ্ম',
    'ধ ্র': 'ধ্র', 'ন ্ত': 'ন্ত', 'ন ্থ': 'ন্থ', 'ন ্দ': 'ন্দ', 'ন ্ধ': 'ন্ধ',
    'ন ্ন': 'ন্ন', 'ন ্ম': 'ন্ম', 'ন ্র': 'ন্র', 'প ্ত': 'প্ত', 'প ্প': 'প্প',
    'প ্র': 'প্র', 'প ্ল': 'প্ল', 'প ্স': 'প্স', 'ব ্দ': 'ব্দ', 'ব ্ধ': 'ব্ধ',
    'ব ্ব': 'ব্ব', 'ব ্র': 'ব্র', 'ব ্ল': 'ব্ল', 'ভ ্র': 'ভ্র', 'ম ্ন': 'ম্ন',
    'ম ্প': 'ম্প', 'ম ্ফ': 'ম্ফ', 'ম ্ব': 'ম্ব', 'ম ্ভ': 'ম্ভ', 'ম ্ম': 'ম্ম',
    'ম ্র': 'ম্র', 'ম ্ল': 'ম্ল', 'র ্ক': 'র্ক', 'র ্গ': 'র্গ', 'র ্ঘ': 'র্ঘ',
    'র ্চ': 'র্চ', 'র ্জ': 'র্জ', 'র ্ট': 'র্ট', 'র ্ড': 'র্ড', 'র ্ণ': 'র্ণ',
    'র ্ত': 'র্ত', 'র ্থ': 'র্থ', 'র ্দ': 'র্দ', 'র ্ধ': 'র্ধ', 'র ্ন': 'র্ন',
    'র ্প': 'র্প', 'র ্ফ': 'র্ফ', 'র ্ব': 'র্ব', 'র ্ভ': 'র্ভ', 'র ্ম': 'র্ম',
    'র ্য': 'র্য', 'র ্র': 'র্র', 'র ্ল': 'র্ল', 'র ্শ': 'র্শ', 'র ্ষ': 'র্ষ',
    'র ্স': 'র্স', 'র ্হ': 'র্হ', 'ল ্ক': 'ল্ক', 'ল ্গ': 'ল্গ', 'ল ্ট': 'ল্ট',
    'ল ্ড': 'ল্ড', 'ল ্ত': 'ল্ত', 'ল ্দ': 'ল্দ', 'ল ্ধ': 'ল্ধ', 'ল ্ন': 'ল্ন',
    'ল ্প': 'ল্প', 'ল ্ফ': 'ল্ফ', 'ল ্ব': 'ল্ব', 'ল ্ভ': 'ল্ভ', 'ল ্ম': 'ল্ম',
    'ল ্য': 'ল্য', 'ল ্ল': 'ল্ল', 'শ ্চ': 'শ্চ', 'শ ্ছ': 'শ্ছ', 'শ ্ত': 'শ্ত',
    'শ ্ন': 'শ্ন', 'শ ্ম': 'শ্ম', 'শ ্র': 'শ্র', 'শ ্ল': 'শ্ল', 'ষ ্ক': 'ষ্ক',
    'ষ ্ট': 'ষ্ট', 'ষ ্ঠ': 'ষ্ঠ', 'ষ ্ণ': 'ষ্ণ', 'ষ ্প': 'ষ্প', 'ষ ্ফ': 'ষ্ফ',
    'ষ ্ম': 'ষ্ম', 'স ্ক': 'স্ক', 'স ্খ': 'স্খ', 'স ্ত': 'স্ত', 'স ্থ': 'স্থ',
    'স ্ন': 'স্ন', 'স ্প': 'স্প', 'স ্ফ': 'স্ফ', 'স ্ব': 'স্ব', 'স ্ম': 'স্ম',
    'স ্র': 'স্র', 'স ্ল': 'স্ল', 'হ ্ণ': 'হ্ণ', 'হ ্ন': 'হ্ন', 'হ ্ম': 'হ্ম',
    'হ ্য': 'হ্য', 'হ ্র': 'হ্র', 'হ ্ল': 'হ্ল',
    
    # ============= NUMBERS AND PUNCTUATION =============
    '০ ়': '০়', '১ ়': '১়', '২ ়': '২়', '৩ ়': '৩়', '৪ ়': '৪়',
    '৫ ়': '৫়', '৬ ়': '৬়', '৭ ়': '৭়', '৮ ়': '৮়', '৯ ়': '৯়',
    ' ।': '।', ' ॥': '॥', '। ': '।', '॥ ': '॥',
    
    # ============= MULTIPLE SPACES =============
    '  ': ' ', '   ': ' ', '    ': ' ',
    
    # ============= TRAILING/LEADING SPACES WITH DIACRITICS =============
    ' ্': '্', '্ ': '্', ' ়': '়', '় ': '়',
}


def apply_bengali_fixes(text: str) -> str:
    """
    Apply comprehensive Bengali OCR fixes to text.
    
    Args:
        text (str): Bengali text with potential OCR spacing errors
        
    Returns:
        str: Text with Bengali OCR errors fixed
    """
    if not text:
        return text
        
    fixed_text = text
    
    # Apply all fixes from the dictionary
    for incorrect, correct in BENGALI_FIXES.items():
        fixed_text = fixed_text.replace(incorrect, correct)
    
    return fixed_text


def clean_bengali_text(text: str) -> str:
    """
    Comprehensive Bengali text cleaning including fixes and normalization.
    
    Args:
        text (str): Raw Bengali text from OCR
        
    Returns:
        str: Cleaned and normalized Bengali text
    """
    import re
    
    if not text:
        return ""
    
    # Apply Bengali fixes first
    text = apply_bengali_fixes(text)
    
    # Remove excessive whitespace and newlines
    text = re.sub(r'\n\s*\n', '\n\n', text)
    text = re.sub(r' +', ' ', text)
    
    # Remove isolated single characters that are likely OCR errors
    text = re.sub(r'\b[।০-৯]\b', '', text)
    
    # Clean up multiple spaces (additional cleanup after fixes)
    text = re.sub(r'\s+', ' ', text)
    
    # Trim leading and trailing spaces
    text = text.strip()
    
    return text


# Utility function to get specific fix categories
def get_vowel_fixes():
    """Get only vowel-related fixes"""
    return {k: v for k, v in BENGALI_FIXES.items() if any(vowel in k for vowel in ['া', 'ি', 'ী', 'ু', 'ূ', 'ৃ', 'ৄ', 'ে', 'ৈ', 'ো', 'ৌ'])}


def get_conjunct_fixes():
    """Get only conjunct consonant fixes"""
    return {k: v for k, v in BENGALI_FIXES.items() if '্' in k and len(k) > 3}


def get_nukta_fixes():
    """Get only nukta-related fixes"""
    return {k: v for k, v in BENGALI_FIXES.items() if '়' in k}